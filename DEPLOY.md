# Cristalomagia - Deployment Guide

Acest document descrie comenzile necesare pentru dezvoltare locală, construirea site-ului și deploy pe Cloudflare Pages.

## Comenzi esențiale

### 1. Build (Construire)

```bash
npm run build
```

Această comandă generează site-ul static în directorul `dist/`. Este comanda folosită automat de Cloudflare Pages când face push pe `main`.

### 2. Deploy (Publicare)

Nu este nevoie de comandă manuală de deploy. Proiectul este configurat pentru **Continuous Deployment** prin integrarea GitHub - Cloudflare Pages:

- Când faci push pe `main`, Cloudflare detectează automat schimbarea și pornește build-ul.
- Odată build-ul finalizat cu succes, site-ul este publicat automat.

Pentru deploy manual (opțional), poți folosi:
```bash
# Prin Cloudflare CLI (wrangler)
npx wrangler pages deploy dist
```

### 3. Preview (Previzualizare)

```bash
npm run preview
```

Aceasta lansează un server local care servește build-ul actual (din `dist/`). Este util pentru a testa cum arată site-ul înainte de a face push către main.

## Development

```bash
# Instalează dependențele
npm install

# Lansează serverul de developare cu hot-reload
npm run dev
```

Serverul va fi disponibil la `http://localhost:4321`.

## Configurație Cloudflare Pages

Când configurezi repository-ul pe [Cloudflare Dashboard](https://dash.cloudflare.com):

- **Framework preset**: Astro
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` ( rădăcina repository-ului )

Site-ul va fi disponibil la:
- **Preview URL**: `https://cristalomagia.pages.dev` (sau branch-specific)
- **Production URL**: `https://cristalomagia.com` (după ce configurezi domeniul custom)

## Branch Protection

Repository-ul are branch protection activat pe `main`. Toate modificările trebuie făcute pe feature branches:

```bash
# Creează un branch nou pentru feature
git checkout -b feat/nume-feature

# Make changes...
git add .
git commit -m "Descriere schimbare"
git push origin feat/nume-feature

# Creează PR către main
```

## Scripts de generare cristale

Proiectul include scripturi Python pentru generarea conținutului cristalelor:

```bash
# Generează toate fișierele MDX din crystal-data.json
python3 generate-crystals.py

# Sau folosește varianta simplifica (doar 8 cristale demo)
python3 generate_all.py
```

Fișierul `crystal-data.json` conține datele complete pentru toate cele 52 de cristale.

## Troubleshooting

### Build eșuează
- Verifică dacă ai rulat `npm install`
- Asigură-te că ai Node.js >= 22.23.4
- Run `npm run build` local pentru a vedea erorile

### Imaginile nu apar
- Verifică dacă imaginile sunt în `public/images/crystals/`
- Asigură-te că numele fișierelor corespund cu `image` din crystal-data.json

### Preview nu arată schimbările
- Rulează din nou `npm run build` înainte de `npm run preview`
