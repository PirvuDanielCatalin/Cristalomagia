#!/usr/bin/env python3
"""
Generate MDX files for all 52 crystals in Cristalomagia
"""

crystals = [
    # Group 1: Cristale brut
    {
        "name": "Agat Muschi",
        "slug": "agat-muschi",
        "category": ["Cristale"],
        "chemicalFormula": "SiO₂",
        "hardness": 6.5,
        "crystalSystem": "Cristalin cubic",
        "chakras": ["Chakra Rădăcină", "Chakra Gâtului"],
        "zodiac": ["Capricorn", "Tacit"],
        "element": ["Pământ", "Apă"],
        "planet": "Mars",
        "origin": ["America de Nord"],
        "rarity": "Comun",
        "color": ["Verde", "Maro"],
        "properties": ["Protecție energetică", "Întărirea caracterului", "Gălcește înfrângerea", "Tăiere a blocurilor negative"],
        "description": "Agatul Muschi este unul dintre cele mai venerate cristale de protecție, cunoscut pentru capacitatea sa de a întări încrederea și a susține stabilitatea.",
        "history": "Agatul Muschi are o istorie milenară în tradițiile natalice și native americane. Cunoscut sub numele de Stone of Protection, a fost folosit de trecători și comercianți întregi lumea pentru a se proteja în călătorii și a întări succesul afacerilor. Legenda spune că agatul poate vorbi cu cerul rochilor și poate atrage vise bunele.",
        "healing": "Agatul Muschi este un cristal puternic de protecție, ideal pentru persoanele sensibile sau deschise energetic. Ajută la reglarea sistemului nervos, reduce anxietatea și îmbunătățește stabilitatea emoțională. În curățarea mineralogică, sprijină sistemul digestiv și substanțele de absorție a nutrienților.",
        "uses": ["Meditație și visualizare", "Protecție în medii stressante", "Întărirea încredere", "Gălcește problemele de sănătate"],
        "care": "Curățarea se face prin soare lunar noptean. Imaginați-l să fie albastru deschis, marcând curățenia. Programați-l lunar, în jur de luna Plină.",
        "combinations": ["Cu Aventurin pentru amplificare a curajului", "Cu Hematit pentru echilibru energetic", "Cu Lapis Lazuli pentru intuiție"],
        "affirmation": "Sunt sigur și puternic, protejat și protejați de toate energiile Negative.",
        "image": "/images/crystals/agat-muschi.jpg",
        "featured": True
    },
    {
        "name": "Agat Indian",
        "slug": "agat-indian",
        "category": ["Cristale"],
        "chemicalFormula": "SiO₂",
        "hardness": 6.5,
        "crystalSystem": "Cristalin cubic",
        "chakras": ["Chakra Rădăcină", "Chakra Inimii"],
        "zodiac": ["Gemini", "Socodor"],
        "element": ["Pământ", "Aer"],
        "planet": "Jupiter",
        "origin": ["America de Nord", "Mexic"],
        "rarity": "Rar",
        "color": ["Negru", "Verde", "Roșu"],
        "properties": ["Protecție adâncă", "Intuiție verde", "Stabilitate", "Conexiune cu natură"],
        "description": "Agatul Indian, de culoare negru-intunecată cu nuanțe verzi și cauri, este un cristal puternic de protecție adâncă.",
        "history": "Agatul Indian este folosit de mult timp de native americani pentru protecție și călătorii spirituale. Se spune că are vibrații ale solului și al focului, combinație puternică.",
        "healing": "Agatul Indian stimulează conexiunea cu natură și cu energia pământului. Este ideal pentru persoanele căutătoare de sens și pentru stabilizarea energetică după tulburări.",
        "uses": ["Trabalungă și călătorii spirituale", "Protecție în situații dificile", "Reîntoarcerea la ritmul natural"],
        "care": "Curățați cu argilită și apă curată. Programați lunar cu soare lunar.",
        "combinations": ["Cu Jasper roșu pentru energie", "Cu Clear Quartz pentru amplificare"],
        "affirmation": "Sunt în armonie cu natura și protejat în toate călătoriile mele.",
        "image": "/images/crystals/agat-indian.jpg",
        "featured": False
    }
]

# Generate MDX files
import os

output_dir = "src/content/crystals"
os.makedirs(output_dir, exist_ok=True)

for crystal in crystals:
    frontmatter = f"""---
name: "{crystal['name']}"
slug: "{crystal['slug']}"
category: {crystal['category']}
chemicalFormula: "{crystal['chemicalFormula']}"
hardness: {crystal['hardness']}
crystalSystem: "{crystal['crystalSystem']}"
chakras: {crystal['chakras']}
zodiac: {crystal['zodiac']}
element: {crystal['element']}
planet: "{crystal['planet']}"
origin: {crystal['origin']}
rarity: "{crystal['rarity']}"
color: {crystal['color']}
properties: {crystal['properties']}
description: "{crystal['description']}"
history: "{crystal['history']}"
healing: "{crystal['healing']}"
uses: {crystal['uses']}
care: "{crystal['care']}"
combinations: {crystal['combinations']}
affirmation: "{crystal['affirmation']}"
image: "{crystal['image']}"
featured: {str(crystal['featured']).lower()}
---

# {crystal['name']} — Cristal de {crystal['properties'][0] if crystal['properties'] else ''}

## Informații de bază

| Câmp | Valoare |
|------|---------|
| **Categorie** | {', '.join(crystal['category'])} |
| **Sistem cristalin** | {crystal['crystalSystem']} |
| **Dureță (Mohs)** | {crystal['hardness']}/10 |
| **Formula chimică** | {crystal['chemicalFormula']} |
| **Raritate** | {crystal['rarity']} |
| **Planetă** | {crystal['planet']} |
| **Origine** | {', '.join(crystal['origin'])} |

## Culori
{', '.join(crystal['color'])}

## Chakre
{crystal['chakras'][0] if crystal['chakras'] else 'N/A'}

## Semne zodiacale
{', '.join(crystal['zodiac']) if crystal['zodiac'] else 'Universal'}

## proprietăți energetice
{' '.join([f"- {p}" for p in crystal['properties']])}

---

## Istorie

{crystal['history']}

## Vindecare

{crystal['healing']}

## Folosințe

{' '.join([f"1. {u}" for u in crystal['uses']])}

## Îngrijire

{crystal['care']}

## Combinații

{' '.join([f"- {c}" for c in crystal['combinations']])}

## Afirmație

> "{crystal['affirmation']}"
"""
    
    with open(f"{output_dir}/{crystal['slug']}.mdx", "w", encoding="utf-8") as f:
        f.write(frontmatter)

print(f"Generated {len(crystals)} MDX files")
print("Run this script with full crystal data to generate all 52 files!")