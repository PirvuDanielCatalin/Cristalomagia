# Cristalomagia — Design Document

## Intent & Why

Un site web static pentru a prezenta colecția personală de 52 de cristale, fiecare cu o descriere detaliată, frumoasă și educativă. Site-ul va fi deployat pe Cloudflare Pages și va servi ca bază pentru creșteri viitoare: forum modern, autentificare, "CV cristal" (portofoliu personal bazat pe cristalele posedate).

## Goals

- **Primary**: Site static performant, SEO-friendly, cu 52 pagini de cristale + pagini de categorii + pagină principală
- **Content**: Fiecare cristal are descriere bogată (istorie, mineralogie, chakre, zodiac, element, folosințe, îngrijire, combinații)
- **Design**: Natural/Organic — tons pământ, texturi subtile, forme organice, tipografie elegantă
- **Tech**: Astro static, Content Collections (type-safe), MDX pentru flexibilitate, Cloudflare Pages adapter
- **Performance**: 100/100 Lighthouse, zero-JS by default, imagini optimizate

## Non-Goals

- Nu e magazin online (nu vinde)
- Nu are backend acum (forumul vine după)
- Nu e aplicație complexă — e site de conținut

## Anti-Goals

- Dependențe grele (React apps, Next.js bundle)
- JavaScript inutil pe pagini static
- Design generic/bootstrap — trebuie să aibă personalitate

## Constraints

- Deploy pe Cloudflare Pages (adapter `@astrojs/cloudflare`)
- Conținut în română
- 52 cristale unice (din Google Sheets)
- Categorii: Cristale, Pendule, Brățari, Pandanțive, Obelisc, Piramide, Îngerași, Copacel, Colier
- Imagini: placeholder-uri acum, real később

## Approaches Considered

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Astro + Content Collections + MDX** | Type-safe, MDX, Islands, Cloudflare native, scalabil | Curbă ușoară învățare | **ALES** |
| Vite + Vanilla TS | Simplu, control total | Totul manual, greu de scalat | Respins |
| Next.js static export | React familiar | Greu pe Cloudflare, overhead | Respins |
| 11ty | Simplu, flexibil | Nu e la fel de modern pentru creștere | Respins |

## Architecture

```
cristalomagia/
├── src/
│   ├── content/
│   │   ├── config.ts          # Content Collections schema
│   │   ├── crystals/          # 52 fișiere .mdx (un per cristal)
│   │   └── categories/        # Categorii (opțional)
│   ├── components/
│   │   ├── layout/            # Header, Footer, Navigation
│   │   ├── crystal/           # CrystalCard, CrystalDetail, CrystalGrid
│   │   ├── ui/                # Button, Card, Badge, Container
│   │   └── home/              # Hero, FeaturedCategories, Intro
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── CrystalLayout.astro
│   │   └── CategoryLayout.astro
│   ├── pages/
│   │   ├── index.astro        # Homepage
│   │   ├── cristale/
│   │   │   ├── index.astro    # Listă toate cristalele
│   │   │   └── [slug].astro   # Detaliu cristal (dynamic route)
│   │   ├── categorii/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   └── rss.xml.js
│   ├── styles/
│   │   ├── global.css         # CSS custom properties, reset, base
│   │   ├── tokens.css         # Design tokens (culori, spacing, type)
│   │   └── components.css     # Component styles
│   └── utils/
│       ├── crystal.ts         # Helper funcții (sort, filter, search)
│       └── seo.ts             # SEO helpers
├── public/
│   ├── images/
│   │   └── crystals/          # Imagini cristale (placeholder acum)
│   └── favicon.ico
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── wrangler.toml              # Cloudflare Pages config
```

## Content Schema (Content Collections)

```typescript
// src/content/config.ts
const crystalSchema = z.object({
  name: z.string(),
  slug: z.string(),
  category: z.array(z.string()),  // ["Cristale", "Brățari"]
  chemicalFormula: z.string().optional(),
  hardness: z.number().min(1).max(10).optional(),
  crystalSystem: z.string().optional(),
  chakras: z.array(z.string()),
  zodiac: z.array(z.string()),
  element: z.array(z.string()),   // ["Pământ", "Apă", "Foc", "Aer", "Eter"]
  planet: z.string().optional(),
  origin: z.array(z.string()),    // Țări de origine
  rarity: z.enum(["Comun", "Rar", "Foarte rar", "Unic"]),
  color: z.array(z.string()),
  properties: z.array(z.string()),    // Proprietăți energetice (din Sheets)
  description: z.string(),            // Descriere scurtă (hero)
  history: z.string(),                // Istorie, legende, folosințe vechi
  healing: z.string(),                // Vindecare fizică/emoțională/spirituală
  uses: z.array(z.string()),          // Meditație, bijuterii, gride, elixire, etc.
  care: z.string(),                   // Curățare, încărcare, programare
  combinations: z.array(z.string()),  // Cristale care se potrivesc bine
  affirmation: z.string().optional(), // Afirmație pentru cristal
  image: z.string().optional(),       // Path la imagine
  featured: z.boolean().default(false),
});
```

## Design System (Natural/Organic)

### Color Palette
```css
:root {
  /* Earth tones */
  --color-earth-50: #faf8f5;
  --color-earth-100: #f3efe8;
  --color-earth-200: #e6e0d5;
  --color-earth-300: #d4cab8;
  --color-earth-400: #b8a890;
  --color-earth-500: #9d8b70;
  --color-earth-600: #82725a;
  --color-earth-700: #6b5c48;
  --color-earth-800: #564a3c;
  --color-earth-900: #453b31;
  --color-earth-950: #251f17;

  /* Accent - crystal tones */
  --color-crystal-amethyst: #9b7bd9;
  --color-crystal-rose: #e8b4c8;
  --color-crystal-golden: #d4a54a;
  --color-crystal-teal: #4db6ac;
  --color-crystal-clear: #f0f4f8;

  /* Semantic */
  --color-text: var(--color-earth-900);
  --color-text-muted: var(--color-earth-600);
  --color-bg: var(--color-earth-50);
  --color-bg-elevated: #ffffff;
  --color-border: var(--color-earth-200);
  --color-focus: var(--color-crystal-teal);
}
```

### Typography
- **Headings**: `Cormorant Garamond` (elegant, organic serif)
- **Body**: `DM Sans` (clean, readable sans)
- **Accent**: `Playfair Display` (pentru citate/afirmații)

### Spacing Scale
- Base: 8px (0.5rem)
- Scale: 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16 rem

### Visual Texture
- Subtle paper/noise texture pe fundaluri
- Border-radius organic (nu perfect rotunjit): `1rem 2rem 1rem 2rem`
- Box-shadow soft, layered (stratificate ca minerale)

## Pages Structure

| Route | Description |
|-------|-------------|
| `/` | Homepage: Hero, intro, featured cristale, categorii |
| `/cristale` | Grid toate cele 52 cristale (filterable, searchable) |
| `/cristale/[slug]` | Detaliu complet cristal |
| `/categorii` | Listă categorii cu counts |
| `/categorii/[slug]` | Cristale dintr-o categorie |
| `/despre` | Despre proiect, autor, metodologie |
| `/cautare` | Search page (Pagefind) |

## Components Key

- **CrystalCard** — card previzualizare (nume, imagine mică, 2-3 tags proprietăți, categorie)
- **CrystalDetail** — pagină completă: hero imagine, descriere, tabs (Istorie, Vindecare, Folosințe, Îngrijire, Combinații), sidebar cu meta (chakre, zodiac, element, dureță)
- **CategoryBadge** — badge colorat per categorie
- **ChakraIcon** — SVG chakre
- **FilterBar** — filtrare pe categorii, chakre, zodiac, element
- **SearchIndex** — Pagefind UI

## Future Extensibility (Forum + CV Cristal)

- **Astro Actions** + **Cloudflare D1** pentru forum (thread-uri, replies, reactions)
- **Auth** cu Lucia/Auth.js pe Cloudflare Workers
- **User profiles** → "CV Cristal": cristalele posedate, jurnal energetică, meditații trackate
- **Search** cu Pagefind (static) sau Algolia/Meilisearch (dynamic)
- **Newsletter** cu Resend (déjà configurat în Composio)

## Acceptance Criteria

- [ ] `npm run build` reușește fără erori
- [ ] `npm run preview` arată site-ul local
- [ ] Deploy pe Cloudflare Pages funcționează
- [ ] Toate 52 cristalele au pagini complete
- [ ] Lighthouse Performance ≥ 95, Accessibility ≥ 95, SEO ≥ 95
- [ ] Responsive: mobile, tablet, desktop
- [ ] Dark mode respectat (prefers-color-scheme)
- [ ] RSS feed generat pentru cristale noi
- [ ] Sitemap.xml generat

## Next Steps

1. ✅ Design doc aprobat
2. Inițializare proiect Astro cu TypeScript strict
3. Configurare Content Collections + schema cristale
4. Scriere 52 fișiere MDX cu conținut bogat
5. Componente UI + design system
6. Pagini (home, listă, detaliu, categorii)
7. SEO, RSS, sitemap, Pagefind
8. Deploy Cloudflare Pages