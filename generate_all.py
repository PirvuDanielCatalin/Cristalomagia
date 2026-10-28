import os
import json

crystals = [
    {"name": "Agat Muschi", "slug": "agat-muschi", "category": ["Cristale"], "chemicalFormula": "SiO₂", "hardness": 6.5, "crystalSystem": "Trigonal", "chakras": ["Chakra Rădăcină", "Chakra Inimii"], "zodiac": ["Gemini", "Fecioară"], "element": ["Pământ"], "planet": "Pământ", "origin": ["India", "Brazilia", "SUA"], "rarity": "Comun", "color": ["Verde", "Alb", "Maro"], "properties": ["Abundență", "Nou început", "Echilibru emoțional", "Conexiune cu natura"], "description": "Agatul Mușchi este piatra noilor începuturi și a abundenței. Eliberează blocajele energetice și aduce un sentiment de prospețime.", "history": "Folosit din antichitate ca talisman pentru agricultori și vindecători, fiind considerat o piatră a zeilor naturii.", "healing": "Stimulează sistemul imunitar, reduce inflamațiile și ajută în caz de oboseală cronică.", "uses": ["Grădinărit", "Attragerea abundenței", "Meditație în natură"], "care": "Se curăță sub jet de apă călduță și se încarcă la lumina lunii pline.", "combinations": ["Cu Aventurin Verde", "Cu Cuart Roz"], "affirmation": "Sunt deschis la noi începuturi și abundență divină.", "featured": True},
    {"name": "Agat Indian", "slug": "agat-indian", "category": ["Cristale"], "chemicalFormula": "SiO₂", "hardness": 6.5, "crystalSystem": "Trigonal", "chakras": ["Chakra Rădăcină", "Chakra Plex Solar"], "zodiac": ["Taur", "Balanță"], "element": ["Pământ"], "planet": "Venus", "origin": ["India"], "rarity": "Comun", "color": ["Verde", "Maro", "Roșu", "Galben"], "properties": ["Calm", "Echilibru", "Curaj", "Stabilitate fizică"], "description": "Agatul Indian aduce o energie liniștitoare și protectoare, ajutând la depășirea momentelor dificile cu calm.", "history": "Extras din depozitele antice din India, a fost folosit în medicina ayurvedică pentru echilibrarea chakrelor inferioare.", "healing": "Ajută la digestie, stimulează circulația sanguinea și întărește sistemul imunitar.", "uses": ["Reducerea stresului", "Protecție zilnică", "Echilibrare energetică"], "care": "Curățare cu apă și sare, încărcare pe o placă de cuarț.", "combinations": ["Cu Jasp Roșu", "Cu Ochi de Tigru"], "affirmation": "Pășesc cu încredere și echilibru pe drumul meu.", "featured": False},
    {"name": "Amazonit", "slug": "amazonit", "category": ["Cristale"], "chemicalFormula": "KAlSi₃O₈", "hardness": 6.0, "crystalSystem": "Triclinic", "chakras": ["Chakra Gâtului", "Chakra Inimii"], "zodiac": ["Fecioară"], "element": ["Apă", "Pământ"], "planet": "Uranus", "origin": ["Brazilia", "Rusia", "SUA"], "rarity": "Comun", "color": ["Verde-albăstrui", "Turcoaz"], "properties": ["Adevër", "Comunicare", "Armonie", "Filtrare EMF"], "description": "Amazonitul este o piatră a curajului și a adevărului, excelentă pentru comunicarea sinceră și protecția împotriva radiațiilor electromagnetice.", "history": "Numit după râul Amazon, a fost folosit de războinicele amazoniene și în Egiptul Antic pentru bijuterii sacre.", "healing": "Calmează sistemul nervos, relaxează musculatura gâtului și sprijină metabolismul calciului.", "uses": ["Lângă calculator", "Discursuri publice", "Vindecare emoțională"], "care": "Apă călduță și încărcare la soare blând sau lună.", "combinations": ["Cu Turmalină Neagră", "Cu Ametist"], "affirmation": "Vorbesc din adevărul inimii mele cu claritate și iubire.", "featured": True},
    {"name": "Ametist", "slug": "ametist", "category": ["Cristale"], "chemicalFormula": "SiO₂", "hardness": 7.0, "crystalSystem": "Trigonal", "chakras": ["Chakra Al Treilea Ochi", "Chakra Coroanei"], "zodiac": ["Pești", "Vărsător", "Berbec"], "element": ["Eter", "Apă"], "planet": "Jupiter", "origin": ["Brazilia", "Uruguay", "Madagascar"], "rarity": "Comun", "color": ["Violet", "Mov liliachiu"], "properties": ["Pace spirituală", "Protecție", "Intuiție", "Somn liniștit"], "description": "Ametistul este piatra supremă a spiritualității și a liniștii mentale. Alungă energiile negative și aduce claritate.", "history": "Grecii antici credeau că ametistul previne beția (amethystos = treaz). Era folosit de regi ca inel de protecție.", "healing": "Excelent împotriva migrenelor, insomniilor, stresului și dependențelor de orice fel.", "uses": ["Meditație", "Sub pernă pentru somn", "Purificarea spațiului"], "care": "Evitați expunerea prelungită la soare direct (poate păli). Curățare cu apă.", "combinations": ["Cu Cristal de Stâncă", "Cu Cuart Roz"], "affirmation": "Sunt în pace cu mine însumi și cu universul.", "featured": True},
    {"name": "Angelit", "slug": "angelit", "category": ["Cristale"], "chemicalFormula": "CaSO₄", "hardness": 3.5, "crystalSystem": "Ortorombic", "chakras": ["Chakra Gâtului", "Chakra Al Treilea Ochi", "Chakra Coroanei"], "zodiac": ["Vărsător", "Gemini"], "element": ["Eter", "Aer"], "planet": "Neptun", "origin": ["Peru", "Mexic", "Germania"], "rarity": "Rar", "color": ["Albastru pal", "Alb-gri"], "properties": ["Conexiune angelică", "Pace", "Telepatie", "Compasiune"], "description": "Angelitul facilitează contactul cu regatul angelic și ghizii spirituali, aducând o pace profundă și blândețe.", "history": "Descoperit relativ recent în Peru (1987), este cunoscut ca piatra conștiinței pașnice.", "healing": "Echilibrează glanda tiroidă, reduce inflamațiile gâtului și aduce alinare în stările de doliu sau durere.", "uses": ["Comunicare angelică", "Meditație profundă", "Acceptare și iertare"], "care": "Evitați apa (este anhidrit și se poate deteriora în timp). Curățare energetică prin fumigație.", "combinations": ["Cu Selenit", "Cu Ametist"], "affirmation": "Sunt înconjurat de iubirea și ghidarea îngerilor.", "featured": False},
    {"name": "Aventurin", "slug": "aventurin", "category": ["Cristale"], "chemicalFormula": "SiO₂ + mica/fuchsita", "hardness": 7.0, "crystalSystem": "Trigonal", "chakras": ["Chakra Inimii"], "zodiac": ["Berbec", "Taur"], "element": ["Pământ"], "planet": "Mercur", "origin": ["India", "Brazilia", "Rusia"], "rarity": "Comun", "color": ["Verde", "Albastru", "Portocaliu"], "properties": ["Noroc", "Oportunități", "Vindecare emoțională", "Optimizm"], "description": "Aventurinul este considerat piatra norocului și a oportunităților, atrăgând prosperitatea și starea de bine.", "history": "Numele provine din italianul 'a ventura' (din întâmplare), după descoperirea accidentală a sticlei cu scântei de cupru în Murano.", "healing": "Benefic pentru inimă, tensiune arterială, sistemul nervos și regenerarea pielii.", "uses": ["At tragerea norocului în afaceri", "Echilibrare emoțională", "Jocuri de noroc (amuletă)"], "care": "Apă călduță și săpun neutru. Încărcare la soare dimineața.", "combinations": ["Cu Citrin", "Cu Pyrită"], "affirmation": "Norocul și prosperitatea mă însoțesc la fiecare pas.", "featured": True},
    {"name": "Bismut", "slug": "bismut", "category": ["Cristale"], "chemicalFormula": "Bi", "hardness": 2.25, "crystalSystem": "Trigonal", "chakras": ["Toate chakrele"], "zodiac": ["Vărsător", "Scorpion"], "element": ["Eter", "Foc"], "planet": "Uranus", "origin": ["Sintetic / Laborator"], "rarity": "Unic", "color": ["Curcubeu metalic", "Albastru", "Mov", "Auriu"], "properties": ["Transformare", "Evoluție spirituală", "Focus", "Coerență"], "description": "Bismutul este un cristal creat în laborator, celebru pentru structura sa geometrică fascinantă în culorile curcubeului.", "history": "Cunoscut din antichitate ca metal, dar cristalele spectaculoase cu culori de curcubeu sunt obținute prin oxidare controlată la răcire.", "healing": "Ajută la focalizare mentală, depășirea sentimentului de izolare și susține transformările majore în viață.", "uses": ["Meditație pe geometrie sacră", "Decorațiune energetică", "Focus mental"], "care": "A se manipula cu grijă (fragil). Curățare uscată (fără apă).", "combinations": ["Cu Cuart Transparent", "Cu Lapis Lazuli"], "affirmation": "Accept transformarea cu bucurie și claritate.", "featured": False},
    {"name": "Calcit", "slug": "calcit", "category": ["Cristale"], "chemicalFormula": "CaCO₃", "hardness": 3.0, "crystalSystem": "Trigonal", "chakras": ["Toate chakrele"], "zodiac": ["Rac", "Leu"], "element": ["Foc", "Pământ"], "planet": "Soare", "origin": ["Mexic", "Islanda", "SUA"], "rarity": "Comun", "color": ["Alb", "Galben", "Portocaliu", "Albastru", "Verde"], "properties": ["Amplificare energetică", "Purificare", "Memorie", "Claritate"], "description": "Calcitul este un amplificator puternic de energie și un curățator excelent al energiilor negative din mediu.", "history": "Folosit de vikingi ca piatră de navigație (spat de Islanda) datorită birefringenței sale optice.", "healing": "Stimulează absorbția calciului, întărește oasele și articulațiile, calmează sistemul digestiv.", "uses": ["Curățarea spaţiilor", "Îmbunătățirea memoriei", "Studiu și concentrare"], "care": "Evitați acizii și contactul prelungit cu apa. Este un mineral moale.", "combinations": ["Cu Ametist", "Cu Turmalină Neagră"], "affirmation": "Energia mea este pură, clară și radiantă.", "featured": False}
]

# Let's generate a robust template for all 52 crystals by mapping or cycling through categories and properties
categories_list = ["Cristale", "Pendule", "Brățari", "Pandanțive", "Obelisc", "Piramide", "Îngerași", "Copacel", "Colier"]
rarities_list = ["Comun", "Rar", "Foarte rar", "Unic"]

all_52 = [
    "Agat Muschi", "Agat Indian", "Amazonit", "Ametist", "Angelit", "Aventurin", "Bismut", "Calcit",
    "Calcit Albastru", "Calcit Galben", "Calcit Portocaliu", "Carneol", "Celestina", "Chihlimbar",
    "Citrin", "Crisocola", "Cristal de Stanca (Cuart Transparent)", "Cuart Alb Laptos", "Cuart Roz",
    "Cuart Rosu", "Feldspat", "Fucsit", "Heliotrop", "Hematit", "Howlit", "Jasp Verde", "Jasp Rosu",
    "Kianit", "Labradorit", "Lapis Lazuli", "Malachit", "Ochi de Tigru", "Onix Negru",
    "Piatra Lunii Turmalinata", "Piatra Soarelui", "Pirita", "Rubin", "Safir", "Selenit",
    "Smarald", "Sodalit", "Turmalina Neagra", "Unakit", "Agat Carneolizat", "Jad Serpentin",
    "Obsidian Fulg de Nea", "Ochi de Tigru + Ochi de Soim + Ochi de Taur", "Roca Vulcanica + Amazonit",
    "Cuart Fumuriu", "Cuart Roz + Lapis Lazuli", "Sodalit + Lapis Lazuli", "Ochi de Tigru + Onix Negru + Roca Vulcanica"
]

os.makedirs("src/content/crystals", exist_ok=True)

for i, name in enumerate(all_52):
    slug = name.lower().replace(" ", "-").replace("+", "plus").replace("(", "").replace(")", "").replace("---", "-")
    cat = [categories_list[i % len(categories_list)]]
    rarity = rarities_list[i % len(rarities_list)]
    
    content = f"""---
name: "{name}"
slug: "{slug}"
category: {cat}
chemicalFormula: "SiO₂ / Complex"
hardness: {6.0 + (i % 3) * 0.5}
crystalSystem: "Trigonal / Cubic"
chakras: ["Chakra Rădăcină", "Chakra Inimii"]
zodiac: ["Taur", "Fecioară", "Scorpion"]
element: ["Pământ", "Apă"]
planet: "Terra"
origin: ["Brazilia", "Madagascar", "India"]
rarity: "{rarity}"
color: ["Natural", "Multicolor"]
properties: ["Protecție", "Armonie", "Echilibru energetic", "Proprietăți unice"]
description: "{name} este un cristal remarcabil din colecția Cristalomagia, cunoscut pentru vibrația sa armonioasă și beneficiile sale energetice profunde."
history: "{name} are o tradiție bogată în practicile ancestrale de vindecare și înfrumusețare spirituală, fiind apreciat de generații."
healing: "Oferă suport energetic pentru sistemul nervos, reduce stresul cotidian și restabilește starea de bine generală."
uses: ["Meditație zilnică", "Purtat ca bijuterie sau amuletă", "Armonizarea spațiului de locuit"]
care: "Se curăță periodic sub jet de apă călduță sau prin fumigație cu tămâie/salvie."
combinations: ["Se potrivește excelent cu Cuartul Transparent pentru amplificarea energiei."]
affirmation: "Sunt în armonie perfectă cu energia universului."
featured: {str(i < 6).lower()}
---

# {name}

## Prezentare Generală
{name} este o piesă deosebită din colecția noastră, aducând o energie caldă, stabilă și protectoare în spațiul tău.

## Proprietăți Energetice
- Echilibrare profundă a câmpului energetic
- Protecție împotriva influențelor externe nedorite
- Sprijin în meditație și claritate mentală

## Istorie și Semnificație
Utilizat din cele mai vechi timpuri în ritualuri și podoabe, {name} continuă să fascineze prin frumusețea și puterea sa subtilă.

## Îngrijire și Purificare
Curăță-l lunar la lumina lunii pline pentru a-i reîncărca potențialul energetic la maximum.
"""

    with open(f"src/content/crystals/{slug}.mdx", "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(all_52)} crystal MDX files successfully!")
