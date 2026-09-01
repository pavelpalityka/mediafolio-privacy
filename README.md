# MediaFolio — Privacy Policy (GitHub Pages)

Static privacy policy site for **MediaFolio** (`com.palityka.mediafolio`).

**Live URL:** https://pavelpalityka.github.io/mediafolio-privacy/

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Shell page, language picker |
| `styles.css` | MediaFolio teal theme |
| `app.js` | Loads `content/{lang}.json`, renders sections |
| `content/en.json` | English policy (source of truth) |
| `content/ru.json`, `content/uk.json` | Hand-maintained translations |
| `content/*.json` | Other locales — English + localized fallback notice |
| `generate_content.py` | Regenerates non-hand-maintained locale files from `en.json` |

## Update policy text

1. Edit `content/en.json` (and `ru.json` / `uk.json` if needed).
2. Run: `python generate_content.py`
3. Commit and push — GitHub Pages updates automatically.

## GitHub Pages setup

1. Create a **public** repo: `pavelpalityka/mediafolio-privacy`
2. Push this folder to the `main` branch (root contains `index.html`).
3. Repo **Settings → Pages → Build and deployment** → Source: **Deploy from a branch** → Branch `main`, folder **/ (root)**.
4. Wait 1–2 minutes. Site: `https://pavelpalityka.github.io/mediafolio-privacy/`

Test: `?lang=ru`, mailto links, mobile layout.

## Play Console

**App content → Privacy policy** → paste:

`https://pavelpalityka.github.io/mediafolio-privacy/`

## app-ads.txt

Appodeal `app-ads.txt` lives in the **user** Pages repo (not this folder):

`https://pavelpalityka.github.io/app-ads.txt`

## Contact

pavelpalityka@gmail.com
