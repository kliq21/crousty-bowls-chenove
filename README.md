# Crousty Bowls Chenôve

Site vitrine du restaurant **Crousty Bowls** — street-food croustillante à Chenôve, aux portes de Dijon.
Bowls croustillants signature, poutines, yakisoba, sushis.

- **Live** : https://crousty-bowls-chenove.vercel.app
- **Adresse** : 63 Rue Maxime Guillot, 21300 Chenôve
- **Instagram** : [@crousty_bowls_chenove](https://www.instagram.com/crousty_bowls_chenove/)

## Stack

Site statique pur, déployé sur Vercel.

- HTML5 statique (un seul `index.html` servable directement)
- Tailwind CSS via CDN (`cdn.tailwindcss.com`) avec config étendue (palette custom, breakpoints)
- GSAP + ScrollTrigger via CDN pour animations scroll & parallax
- Google Fonts : Anton (display), Manrope (sans), Caveat (handwritten)
- SVG sprite custom pour le logo CB et les pictos
- Schema.org JSON-LD Restaurant (SEO + GEO/AI Overviews)

Aucun build, aucune dépendance npm.

## Design

- Direction artistique éditoriale type magazine food (numérotation de sections, étiquettes-tampons obliques, halftone dots, asymétrie assumée)
- Mobile-first (≥90% du trafic restaurant)
- Palette stricte : noir profond + accents rouge / magenta / violet / indigo. Zéro jaune.
- CTA primaire : appel téléphonique direct (`tel:`) pour conversion immédiate

## Conventions

- Auteur des commits : `kliqwebcontact@gmail.com` (compatibilité Vercel Hobby)
- Owner repo : `kliq21`
- Branche prod : `main` (Vercel auto-deploy)

---

Site conçu et développé par [Kliq](https://kliqweb.fr).
