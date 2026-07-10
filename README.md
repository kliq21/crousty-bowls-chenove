# Crousty Bowls Chenôve

Site vitrine du restaurant **Crousty Bowls** — street-food croustillante à Chenôve, aux portes de Dijon.
Bowls croustillants signature, poutines, yakisoba, sushis.

- **Live** : https://crousty-bowls-chenove.vercel.app
- **Adresse** : 63 Rue Maxime Guillot, 21300 Chenôve
- **Instagram** : [@crousty_bowls_chenove](https://www.instagram.com/crousty_bowls_chenove/)

## Stack

Site statique pur, déployé sur Vercel — aucun build, aucune dépendance npm.

- HTML5 statique (un seul `index.html` servable directement)
- Tailwind CSS via CDN (`cdn.tailwindcss.com`) avec config étendue (palette custom, breakpoints)
- GSAP + ScrollTrigger via CDN (avec SRI) pour animations scroll & parallax
- Lenis via CDN (avec SRI) pour smooth scroll
- Google Fonts : Anton (display), Manrope (sans), Caveat (handwritten), Instrument Serif (menu-italic)
- SVG sprite custom pour le logo CB et les pictos
- Schema.org JSON-LD Restaurant (SEO + GEO/AI Overviews)

## Design (v3 — 2026-07-10)

- Direction artistique éditoriale type magazine food : numérotation de sections 01-06, étiquettes-tampons obliques pour les prix, halftone dots variants par section, watermarks, asymétries assumées
- **Hero néon** : panneau CHENÔVE détouré à gauche · wordmark CROUSTY BOWLS néon pulse+flicker au centre · bowl signature à droite · flèches rouges manuscrites "pute à clic" pointant les CTA
- Photos réelles fournies par la gérante (juillet 2026), optimisées via `_tools/optim_photos.py` (Pillow) en WebP 3 tailles + JPG fallback
- Palette stricte : noir profond (`#0A0A0F`) + accents rouge tomato / magenta / violet / indigo. **Zéro jaune**.
- Mobile-first (≥90% du trafic restaurant)
- CTA primaire : appel téléphonique direct (`tel:`) pour conversion immédiate

## Sécurité

Note A (audit 2026-07-10, `securityheaders.com`) :

- HSTS preload
- Content-Security-Policy restrictive (default-src 'self', script-src limité aux CDN utilisés)
- X-Frame-Options SAMEORIGIN, X-Content-Type-Options nosniff
- Referrer-Policy strict-origin-when-cross-origin
- Permissions-Policy camera/mic/geo bloqués
- SRI (integrity + crossorigin="anonymous") sur les 3 scripts CDN externes
- `.vercelignore` : le dossier `_tools/` (scripts Python de génération d'images) n'est pas déployé

## Structure

```
├─ index.html              # single-file, ~1500 lignes
├─ vercel.json             # headers de sécurité, cache immutable pour assets
├─ robots.txt              # Allow: /, sitemap
├─ sitemap.xml             # une seule URL (accueil)
├─ og.jpg                  # image Open Graph
├─ .vercelignore           # exclut _tools/ du déploiement
├─ assets/
│  ├─ img/                 # photos WebP 480/960/1600 + JPG fallback
│  │  ├─ crousty/          # bowl signature (Tasty.jpg)
│  │  ├─ poutine/          # gratinée (variantes topdown/side/large + sriracha)
│  │  ├─ yakisoba/         # nouilles (signature, flyer, topdown, closeup...)
│  │  ├─ salle/            # salle événements (3 photos)
│  │  ├─ lieu/             # façade, panneau CHENÔVE (croppé + détouré nobg)
│  │  └─ boissons/         # matcha duo
│  └─ js/                  # (vide — dead code retiré)
└─ _tools/                 # scripts Python de génération (non déployés)
   ├─ optim_photos.py      # génère WebP + JPG depuis les photos brutes
   ├─ crop_panneau.py      # crop panneau CHENÔVE serré
   ├─ panneau_nobg.py      # traite le PNG détouré du panneau
   └─ og_image.py          # génère og.jpg
```

## Conventions

- Auteur des commits : `kliqwebcontact@gmail.com` (compatibilité Vercel Hobby)
- Owner repo : `kliq21`
- Branche prod : `main`
- Deploy : `npx vercel --prod` depuis le repo local

## Reste à faire

Voir [`HANDOVER.md`](./HANDOVER.md) : liste précise des infos à récupérer auprès de la gérante et des étapes de branchement domaine.

---

Site conçu et développé par [Kliq](https://kliqweb.fr).
