# Clerk + portofoliu de cristale — design

Data: 2026-10-30
Status: propus, așteaptă aprobare

## Scop

Oricine își face cont pe Crystalica și își ține evidența cristalelor:

- **Portofoliu** — cristalele pe care le are.
- **Listă de dorințe** — cristalele pe care și le dorește.

Pe `/cristale`, fiecare card primește un contur colorat în funcție de stare:
neutru (nu există în nicio listă), verde (portofoliu), galben (wishlist).
La hover (și la focus, pentru tastatură), sub card apare o zonă cu acțiuni.
Pe pagina unui cristal, aceleași acțiuni apar sub imagine.

## Non-goals

- Profil public / link partajabil către portofoliu.
- Feed social, comentarii, urmăriri între useri.
- Backend propriu sau bază de date externă în această etapă.
- Migrarea site-ului la SSR.

## Constrângeri

- Site-ul este static: `output: 'static'`, 288 pagini prerandate, deploy pe
  Cloudflare Pages cu output `dist/client`. Integrarea nu are voie să schimbe
  acest model.
- SDK-ul oficial `@clerk/astro` cere `output: 'server'` — exclus pentru acum.
- Fără cheie secretă în browser. Se folosește doar publishable key.
- Clerk limitează metadata la 8KB per user.
- Nu se fac commit-uri sau push-uri; modificările rămân în working tree.

## Abordări analizate

### A. `@clerk/clerk-js` client-side + `unsafeMetadata` (aleasă)

Clerk rulează în browser cu publishable key. Datele stau în
`user.unsafeMetadata`. Site-ul rămâne 100% static, deploy-ul actual rămâne
valid, nu există secret pe server.

- **Plus:** zero schimbări de infrastructură, implementare rapidă, funcționează
  cu Cloudflare Pages ca acum.
- **Minus:** datele sunt scrise din client (userul își poate modifica propriile
  liste — acceptabil, sunt datele lui); limita de 8KB.

### B. `@clerk/astro` + SSR

Integrarea oficială: `clerkMiddleware()`, componente server-rendered,
endpoint-uri server pentru scrieri în metadata privată.

- **Plus:** auth randat pe server, metadata privată, pattern oficial.
- **Minus:** toate cele 288 de pagini devin dinamice; deploy-ul Cloudflare
  trece de la assets statice la Worker SSR; necesită cheie secretă și
  autentificare CLI. Migrare de infrastructură, risc de regresii pe deploy.

### C. Clerk + bază de date (Cloudflare KV/D1)

Clerk pentru identitate, KV/D1 pentru liste.

- **Plus:** scalabil, fără limita de 8KB.
- **Minus:** binding-uri Cloudflare configurate manual în dashboard, mediu
  local de dezvoltare mai complicat, muncă suplimentară necerută acum.

**Decizie:** A. Dacă pe viitor listele depășesc metadata sau apar cerințe de
profil public, migrăm la C fără să schimbăm UI-ul.

## Model de date

În `user.unsafeMetadata`:

```json
{
  "collections": "actinolit:p,agat:w"
}
```

- `p` = portofoliu, `w` = wishlist, absența slug-ului = nu există.
- Reprezentare compactă, ca string: toate cele 287 de slug-uri încap lejer sub
  limita de 8KB (aproximativ 4–5KB în cel mai rău caz), iar Clerk înlocuiește
  valoarea întreagă la fiecare salvare — ștergerile sunt garantate, indiferent
  de semantica de merge a metadata-ei.
- Citirea acceptă și formatul vechi de obiect, pentru compatibilitate.
- Scrierea se face cu `user.update({ unsafeMetadata: { ...user.unsafeMetadata, collections } })`,
  ca să nu atingem alte chei viitoare.
- Actualizare optimistă în UI; la eroare se revine la starea anterioară și se
  afișează un mesaj discret.

## Componente și fișiere

| Fișier | Rol |
|---|---|
| `src/scripts/clerk.ts` | Singleton Clerk (guard pe `window`), `load()`, helpers pentru citirea/scrierea colecțiilor, eveniment `crystalica:collections`. |
| `src/components/auth/AuthControls.astro` | Butoane Conectare / Cont nou, link „Portofoliul meu”, mount `UserButton`. Variantă desktop + mobil. |
| `src/components/collections/CrystalActions.astro` | Zona de acțiuni (portofoliu / wishlist / eliminare) pentru un slug. |
| `src/components/layout/Header.astro` | Include `AuthControls`. |
| `src/pages/cristale/index.astro` | Cardurile devin `shell` + link + zonă de acțiuni; `data-slug`, `data-name`. |
| `src/components/SearchBar.astro` | Filtrarea pe pagină trece de la `.az-card` la shell-uri (comportamentul confirmat rămâne identic). |
| `src/pages/cristale/[slug].astro` | `CrystalActions` sub imagine. |
| `src/pages/portofoliu.astro` | Pagina „Portofoliul meu”: listele userului, randate client-side. |
| `src/styles/global.css` | Contururi de stare, panou de acțiuni, stiluri auth, pagina portofoliu. |
| `.env` / Cloudflare Pages | `PUBLIC_CLERK_PUBLISHABLE_KEY`. |

## Comportament

### Signed out

- Toate cardurile au contur neutru; zonele de acțiuni sunt ascunse.
- Header: „Conectare” (ghost) + „Cont nou” (primar).
- `/portofoliu`: mesaj + buton de conectare.

### Signed in

- Header: link „Portofoliul meu” + avatar Clerk (`UserButton`).
- Card `/cristale`:
  - fără stare → contur neutru; hover/focus → butoane „Adaugă în portofoliu”,
    „Adaugă la wishlist”;
  - `p` → contur verde; hover/focus → „Elimină din portofoliu”;
  - `w` → contur galben; hover/focus → „Mută în portofoliu”, „Elimină din
    wishlist”.
- Pagina cristalului: aceleași butoane, vizibile permanent sub imagine, plus o
  etichetă de stare.
- Pe dispozitive fără hover (touch), acțiunile sunt vizibile permanent, compact.
- Schimbările se reflectă instant pe toate cardurile din pagină și persistă
  după reload (Clerk metadata).

### `/portofoliu`

- Două secțiuni: „Portofoliul meu” și „Lista de dorințe”.
- Fiecare item: imagine, nume, link către pagină, buton de eliminare/mutare.
- Datele cristalelor sunt embed-uite ca JSON (nume, slug, imagine), randarea
  este client-side după încărcarea Clerk.

## Vizual

- Neutru: `--color-border` (respectiv zinc în dark mode).
- Portofoliu: verde `--color-crystal-green`, contur + glow subtil.
- Wishlist: galben `--color-crystal-golden`, contur + glow subtil.
- Panoul de acțiuni: fundal `--color-bg-elevated`, border, shadow, colțuri
  `--radius-md`, butoane mici cu iconițe; apare cu fade + translate 4px.
- Clerk modal: appearance cu accentul teal al site-ului și fonturile existente.
- Culorile și stările trebuie să funcționeze în light și dark mode.

## Cazuri limită

- Publishable key lipsă → Clerk nu se inițializează, feature-ul rămâne ascuns,
  un warning în consolă; site-ul funcționează normal.
- Eroare la scrierea metadata (rețea/limită) → rollback vizual + mesaj.
- Flash inițial până la `clerk.load()` → stările se aplică după load; panourile
  rămân ascunse până atunci.
- Clerk încărcat de două ori (mai multe entry-uri de script) → singleton pe
  `window`.
- Semnare din alt tab → `clerk.addListener` re-randează.

## Verificare

- `npx astro build` → 288 pagini, fără erori, output `dist/client`.
- Manual, cu publishable key:
  1. signed out: contururi neutre, fără acțiuni, modal sign-in funcțional;
  2. sign-up + sign-in;
  3. adaugă în portofoliu → contur verde instant;
  4. adaugă în wishlist → contur galben;
  5. mută wishlist → portofoliu; elimină din ambele;
  6. reload → stările persistă;
  7. pagina cristalului și `/portofoliu` reflectă aceleași stări;
  8. dark mode + mobil (touch).

## Pași de setup externi (în afara codului)

1. Publishable key din Clerk Dashboard → API keys pentru aplicația
   `app_3LJZ2rvIYJobBSKu0m5roRAjFMZ`.
2. Adăugarea domeniilor în Clerk: `localhost:4321`, `crystalica.pages.dev`,
3. `PUBLIC_CLERK_PUBLISHABLE_KEY` în `.env` local și în Cloudflare Pages →
   Settings → Environment variables.
4. Metode de sign-in (email/parolă, social) — se configurează în dashboard.
