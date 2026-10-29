#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
updater_cristale.py — Actualizează fișierele .mdx cu informații din Tavily API.
"""

import os
import re
import time
import requests
from pathlib import Path

TAVILY_API_KEY = "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"
TAVILY_SEARCH = "https://api.tavily.com/search"

CRYSTALS_DIR = Path(__file__).parent  # src/content/crystals

# Valid formula chars (no spaces, no Romanian letters, no digits-only)
FORMULA_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "0123456789₀₁₂₃₄₅₆₇₈₉"
    "()[]+-,.:"
)
# Words that start prose after a formula
PROSE_STARTERS = [
    'Durata', 'Duritate', 'Sistem', 'Culoare', 'Raritate', 'Origini',
    'Chakra', 'Chakre', 'Zodiac', 'Zodii', 'Element', 'Proprietăți',
    'Este', 'Nu', 'Acest', 'Aceasta', 'Se', 'Este un', 'Nu există',
    'compoziția', 'compoziţia', 'este un', 'este o', 'are forma',
    'cristalizează', 'cristalizeaza', 'apare în', 'apare in',
]


def search_tavily(crystal_name: str) -> str:
    query = (
        f"Informații despre cristalul {crystal_name} în limba română: "
        f"formulă chimică, duritate, sistem cristalin, culoare, raritate, origini, chakre, zodii, element, proprietăți."
    )
    resp = requests.post(TAVILY_SEARCH, json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": 3,
        "include_answer": True,
        "language": "romanian",
        "country": "romania",
    }, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    text = data.get("answer", "")
    for r in data.get("results", []):
        text += "\n\n" + r.get("content", "")
    return text.strip()


def extract_regex(text: str, pattern: str, group: int = 1, default: str = "") -> str:
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(group).strip()
    return default


def is_formula_like(s: str) -> bool:
    """Check if a string looks like a valid chemical formula."""
    if len(s) < 3 or len(s) > 80:
        return False
    if not s[0].isupper():
        return False
    # Must contain at least one lowercase letter or digit or subscript
    if not re.search(r'[a-z₀-₉]', s):
        return False
    # Must not contain common Romanian words
    bad_words = ['este', 'cristal', 'curent', 'acest', 'aceasta', 'forma']
    for w in bad_words:
        if w in s.lower():
            return False
    return True


def extract_formula(text: str) -> str:
    """Extract a clean chemical formula from the text."""
    # Strategy 1: Find "formula chimică este X" pattern
    m = re.search(r'formula\s*chimică\s+(?:este|:)\s+([A-Z][^\.\n]{2,150})', text, re.IGNORECASE)
    if m:
        candidate = m.group(1).strip()
        # Clean up common trailing patterns
        for sep in [' cu ', ' iar ', ' și ', ' , ', ' — ', ' Duritate', ' duritate', ' Sistem', ' sistem']:
            idx = candidate.find(sep)
            if idx > 0:
                candidate = candidate[:idx].strip()
        # Remove trailing punctuation
        candidate = re.sub(r'[.,;:]+$', '', candidate)
        # Filter to valid formula chars
        filtered = ''.join(c for c in candidate if c in FORMULA_CHARS)
        if filtered and is_formula_like(filtered):
            return filtered

    # Strategy 2: Find formula after marker with colon
    m = re.search(r'(?:formula\s*chimică|compozi[ție])[:\s]+([A-Z][^\n]{3,150})', text, re.IGNORECASE)
    if m:
        candidate = m.group(1).strip()
        # Stop at prose markers
        for sep in PROSE_STARTERS:
            idx = candidate.find(sep)
            if idx > 0:
                candidate = candidate[:idx].strip()
        # Stop at period and semicolon
        for sep in ['.', ';']:
            idx = candidate.find(sep)
            if idx > 0:
                candidate = candidate[:idx].strip()
        # Stop at whitespace followed by lowercase word
        prose_m = re.search(r'\s+[a-zăâîșț]', candidate)
        if prose_m:
            candidate = candidate[:prose_m.start()].strip()
        # If contains '+', take only the part before
        if '+' in candidate:
            candidate = candidate.split('+')[0].strip()
        # Remove trailing punctuation
        candidate = re.sub(r'[.,;:]+$', '', candidate)
        # Filter to valid formula chars
        filtered = ''.join(c for c in candidate if c in FORMULA_CHARS)
        if filtered and is_formula_like(filtered):
            return filtered

    # Strategy 3: Fallback - look for any formula-like token
    m = re.search(r'([A-Z][a-z]?(?:\([^)]+\))?[₀₁₂₃₄₅₆₇₈₉\d]+)', text)
    if m:
        candidate = m.group(1).strip()
        filtered = ''.join(c for c in candidate if c in FORMULA_CHARS)
        if filtered and is_formula_like(filtered):
            return filtered

    # Last resort: find simple SiO2/SiO₂
    m = re.search(r'\b(SiO[₂2])\b', text)
    return m.group(1) if m else ""


def extract_colors(text: str) -> list:
    """Extract crystal colors, excluding exception/negative mentions."""
    # Try to find color info after marker
    m = re.search(r'(?:culoare|culori)\s*[:\=]?\s*([^\.\n]{10,300})', text, re.IGNORECASE)
    if not m:
        return []

    color_text = m.group(1).strip()

    # Find exception colors (e.g., "în afara de albastru", "fără verde")
    exception_pattern = r'(?:în afara de|fără|except|exclusiv|nedefinit|nu\s+este)\s+(\w+)'
    exceptions = list(re.findall(exception_pattern, color_text, re.IGNORECASE))
    exceptions_lower = [e.lower() for e in exceptions]

    # Known color names
    known_colors = [
        'verde', 'albastru', 'roșu', 'rosu', 'galben', 'portocaliu',
        'mov', 'violet', 'roz', 'alb', 'negru', 'gri', 'maro',
        'transparent', 'smarald', 'închis', 'deschis', 'pal', 'intens',
        'bej', 'auriu', 'argintiu', 'rozaliu', 'lavandă', 'lavanda',
    ]

    # Find all color mentions
    all_colors = re.findall(r'\b(' + '|'.join(re.escape(c) for c in known_colors) + r')\b', color_text, re.IGNORECASE)
    # Filter out exceptions
    colors = [c.capitalize() for c in all_colors if c.lower() not in exceptions_lower]
    # Deduplicate while preserving order
    seen = set()
    result = []
    for c in colors:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return result


def is_real_description(desc: str) -> bool:
    """Check if a string looks like a real paragraph description vs a property list."""
    if not desc:
        return False
    # Reject table-like content
    if desc.startswith('|') or desc.startswith('---'):
        return False
    # Reject very short descriptions
    if len(desc) < 120:
        return False
    # A real description has proper sentences with verbs
    has_verb = bool(re.search(r'(?:este|are|cristalize|găse|variaz|include|este un|este o)', desc, re.IGNORECASE))
    is_list = re.search(r'^\s*(?:proprietăți|culoare|duritate|sistem|raritate|origini|chakre|zodii|element)[:\s]', desc, re.IGNORECASE)
    # Also reject if it's a Tavily-style property summary
    is_property_summary = bool(re.search(r'formula\s*chimică\s*:\s*[A-Z]', desc, re.IGNORECASE))
    # Reject if it's just a location list
    is_location_list = bool(re.search(r'^\s*(?:țările|unde\s+se|găsește|originile)', desc, re.IGNORECASE))
    return has_verb and not is_list and not is_property_summary and not is_location_list


def parse_crystal(text: str, slug: str) -> dict:
    name = slug.replace("-", " ").title()

    # --- chemicalFormula ---
    chem = extract_formula(text)

    # --- hardness ---
    dur = extract_regex(text, r"duritate[^\d]*([\d.,]+(?:\s*-\s*[\d.,]+)?)", default="")
    if "-" in dur:
        dur = dur.split("-")[0].strip()
    try:
        dur = float(dur.replace(",", "."))
        dur = round(dur, 1)
        # Validate hardness is on Mohs scale (1-10)
        if dur < 1 or dur > 10:
            dur = None
    except ValueError:
        dur = None

    # --- crystalSystem ---
    sys_m = extract_regex(text, r"(monoclinic|triclinic|cubic|hexagonal|trigonal|tetragonal|ortorombic)", default="")
    crystalSystem = sys_m.capitalize() if sys_m else ""

    # --- chakras ---
    known_chakras_map = {
        "Rădăcină": ["rădăcină"],
        "Sacrală": ["sacral", "sex"],
        "Plexului Solar": ["plex", "solar"],
        "Inimii": ["inim"],
        "Gâtului": ["gât", "garg"],
        "Frunții": ["frun", "ochi", "eyes", "third"],
        "Coroanei": ["coroa", "crown"],
    }
    chakras = []
    text_lower = text.lower()
    for chakra, keywords in known_chakras_map.items():
        if any(k in text_lower for k in keywords):
            full_name = f"Chakra {chakra}"
            if full_name not in chakras:
                chakras.append(full_name)

    # --- zodiac ---
    known_zodiacs = ["Berbec", "Taur", "Gemeni", "Rac", "Leu", "Fecioară", "Balanță", "Scorpion", "Săgetător", "Capricorn", "Vărsător", "Pești"]
    zodiac = [z for z in known_zodiacs if z.lower() in text_lower]

    # --- element ---
    known_elements = ["Foc", "Pământ", "Apă", "Aer"]
    element = [e for e in known_elements if e.lower() in text_lower]

    # --- planet ---
    planet_m = extract_regex(text, r"(?:planetă|planeta)\s*[:\=]?\s*([A-Z][a-zăâîșț]+)", default="")
    planet = planet_m if planet_m and planet_m.lower() not in ["proprietăți", "energie", "sistem"] else ""

    # --- origin ---
    origin_text = extract_regex(text, r"(?:origini|origine|provenien[țt][ăa]|din\s+[A-Z][a-z]+)\s*[:\=]?\s*([^\.\n]{10,150})", default="")
    if origin_text:
        countries = re.findall(r"\b(Brazilia|Madagascar|SUA|USA|Italia|Austria|Elveția|Canada|Australia|India|China|Japonia|Germania|Franța|Spania|Portugalia|Rusia|Africa|Asia|Europa|Mozambic|Namibia|Tanzania|Kenya|Maroc|Republica Cehă|Argentina|Patagonia|Suedia|Myanmar|Pakistan|Egipt|Polonia|Marea Britanie|Peru|Libia|Mexic|Norvegia)\b", origin_text, re.IGNORECASE)
        origin = list(dict.fromkeys([c.title() if c.lower() != "usa" else "SUA" for c in countries]))
    else:
        origin = []

    # --- rarity ---
    rarity = ""
    rarities = ["Foarte rar", "Unic", "Rar", "Comun"]
    for r in rarities:
        if r.lower() in text_lower:
            rarity = r
            break

    # --- color ---
    color = extract_colors(text)

    # --- description --- (only from Tavily if it's a real description)
    # Use the answer (first paragraph) or first substantial paragraph
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    description = ""
    for p in paragraphs:
        if is_real_description(p):
            description = p[:600] + "..." if len(p) > 600 else p
            break
    # If no real description found, leave empty
    if not description and paragraphs:
        # Check if first paragraph is at least 80 chars and not just a property list
        first = paragraphs[0]
        if len(first) > 80 and is_real_description(first):
            description = first[:600] + "..." if len(first) > 600 else first

    # --- properties (extracted from text, not default) ---
    # Look for property keywords in the text
    prop_keywords = {
        "Echilibru": ["echilibr", "echilibra"],
        "Protecție": ["protec", "apăra", "proteja"],
        "Vindecare": ["vindec", "terap", "restaura"],
        "Armonizare": ["harmoniz", "armon", "alini"],
        "Calmare": ["calm", "relax", " linișt", "calmează"],
        "Energizare": ["energiz", " vitalit", "stimule"],
        "Claritate": ["clar", "concentr", "focus"],
        "Intuiție": ["intui", "spiritual", "medita"],
    }
    properties = []
    for prop, keywords in prop_keywords.items():
        if any(k in text_lower for k in keywords):
            properties.append(prop)

    # --- history ---
    history = ""
    history_m = re.search(r'(?:istorie|utilizat|antich|tradiție|tradi\u0163ie)\s*[:\=]?\s*([^\n]{20,400})', text, re.IGNORECASE)
    if history_m:
        h = history_m.group(1).strip()
        # Clean it up
        h = re.sub(r'\s+', ' ', h)
        if len(h) > 20:
            history = h

    # --- healing ---
    healing = ""
    healing_m = re.search(r'(?:vindecare|efect.*terapeutic|proprietăți.*vindec|beneficii)\s*[:\=]?\s*([^\n]{20,400})', text, re.IGNORECASE)
    if healing_m:
        h = healing_m.group(1).strip()
        h = re.sub(r'\s+', ' ', h)
        if len(h) > 20:
            healing = h

    # --- affirmation ---
    affirmation = ""
    aff_m = re.search(r'(?:afirmație|afirma\u0163ie|mantra|gândire|afirmatie)\s*[:\=]?\s*["\"]?([^\n"\\]{10,200})["\"]?', text, re.IGNORECASE)
    if aff_m:
        a = aff_m.group(1).strip().strip('"').strip()
        if len(a) > 5:
            affirmation = a

    # --- care ---
    care = ""
    care_m = re.search(r'(?:îngrijire|întreținere|intre\u0163inere|curățare|cura|modalitatea* de\s*păstrare)\s*[:\=]?\s*([^\n]{20,300})', text, re.IGNORECASE)
    if care_m:
        c = care_m.group(1).strip()
        c = re.sub(r'\s+', ' ', c)
        if len(c) > 10:
            care = c

    # --- uses ---
    uses = []
    use_keywords = {
        "Meditație": ["medita", "mindfulness"],
        "Vindecare energetică": ["vindecare", "energetic"],
        "Colecționare": ["colecț", " colec"],
    }
    for use, keywords in use_keywords.items():
        if any(k in text_lower for k in keywords):
            uses.append(use)

    # --- combinations ---
    combinations = []
    comb_m = re.search(r'(?:combinație|combina\u0163ie|se\s*asociaz[ăa]\s+cu|potrivit\s+cu)\s*[:\=]?\s*([^\n]{10,200})', text, re.IGNORECASE)
    if comb_m:
        candidates = re.findall(r'\b([A-Z][a-zăâîșț]+(?:\s+(?:de\s+)?[a-zăâîșț]+)?)\b', comb_m.group(1))
        # Filter to likely crystal names
        for c in candidates:
            if len(c) > 3 and c.lower() not in ['cu', 'si', 'ce', 'sa', 'la', 'de']:
                combinations.append(c.title())
        combinations = list(dict.fromkeys(combinations))[:5]

    return {
        "name": name,
        "slug": slug,
        "chemicalFormula": chem,
        "hardness": dur,
        "crystalSystem": crystalSystem,
        "chakras": chakras,
        "zodiac": zodiac,
        "element": element,
        "planet": planet,
        "origin": origin,
        "rarity": rarity,
        "color": color,
        "properties": properties,
        "otherNames": [],
        "description": description,
        "history": history,
        "healing": healing,
        "uses": uses,
        "care": care,
        "combinations": combinations,
        "affirmation": affirmation,
        "image": "",
    }


def generate_yaml(data: dict) -> str:
    lines = ["---"]
    lines.append(f"name: {data['name']}")
    lines.append(f"slug: {data['slug']}")

    if data.get("chemicalFormula"):
        lines.append(f"chemicalFormula: \"{data['chemicalFormula']}\"")

    if data.get("hardness") is not None:
        lines.append(f"hardness: {data['hardness']}")

    if data.get("crystalSystem"):
        lines.append(f"crystalSystem: {data['crystalSystem']}")

    lines.append("chakras:")
    for c in data["chakras"]:
        lines.append(f"  - {c}")

    lines.append("zodiac:")
    for z in data["zodiac"]:
        lines.append(f"  - {z}")

    lines.append("element:")
    for e in data["element"]:
        lines.append(f"  - {e}")

    if data.get("planet"):
        lines.append(f"planet: {data['planet']}")

    lines.append("origin:")
    for o in data["origin"]:
        lines.append(f"  - {o}")

    if data.get("rarity"):
        lines.append(f"rarity: {data['rarity']}")
    else:
        lines.append("rarity: \"-\"")

    lines.append("color:")
    for c in data["color"]:
        lines.append(f"  - {c}")

    lines.append("properties:")
    for p in data["properties"]:
        lines.append(f"  - {p}")

    if data.get("otherNames"):
        lines.append("otherNames:")
        for n in data["otherNames"]:
            lines.append(f"  - {n}")

    # String fields - only include if non-empty
    for field in ["description", "history", "healing", "care", "affirmation"]:
        val = data.get(field, "").strip()
        if val:
            val_clean = val.replace('"', '\\"')
            lines.append(f'{field}: "{val_clean}"')
        else:
            lines.append(f'{field}: "-"')

    lines.append("uses:")
    for u in data["uses"]:
        lines.append(f"  - {u}")
    if not data["uses"]:
        lines.append("  - \"-\"")

    lines.append("combinations:")
    for c in data["combinations"]:
        lines.append(f"  - {c}")
    if not data["combinations"]:
        lines.append("  - \"-\"")

    lines.append("image: \"\"")
    lines.append("---")
    return "\n".join(lines) + "\n"


def main():
    mdx_files = sorted(CRYSTALS_DIR.glob("*.mdx"))
    if not mdx_files:
        print("Niciun fișier .mdx găsit.")
        return

    print(f"Găsit {len(mdx_files)} fișiere .mdx în {CRYSTALS_DIR}")

    dry_run = "--dry-run" in os.sys.argv
    if dry_run:
        print("🔍 MODE: dry-run (toate pentru test)")
        mdx_files = mdx_files[:20]  # Limit to first 20 for dry-run

    success = 0
    failed = 0

    for i, mdx_file in enumerate(mdx_files, 1):
        slug = mdx_file.stem
        crystal_name = slug.replace("-", " ").title()
        print(f"\n[{i}/{len(mdx_files)}] Procesez: {slug} ({crystal_name})...")

        try:
            text = search_tavily(crystal_name)
            if not text:
                print(f"  ⚠️  Niciun rezultat de la Tavily")
                failed += 1
                continue

            data = parse_crystal(text, slug)
            mdx = generate_yaml(data)

            if dry_run:
                print("  === Output preview ===")
                print(mdx)
                print("  === End preview ===")
            else:
                mdx_file.write_text(mdx, encoding="utf-8")
                print(f"  ✓ Scris {mdx_file.name} ({len(mdx)} bytes)")

            success += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"  ❌ Eroare: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Finalizat: {success} reușite, {failed} eșecuri din {len(mdx_files)}")


if __name__ == "__main__":
    main()
