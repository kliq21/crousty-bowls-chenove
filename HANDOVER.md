# Handover — infos à récupérer auprès de Jihane

État au 2026-07-10. Le site est en prod avec les vraies photos de la gérante. Restent quelques infos pour clôturer le projet.

Chaque item ci-dessous précise **quoi demander**, **où l'insérer dans le code**, et **format attendu**.

---

## 🔴 Bloquant mise en ligne finale

### 1. URL Uber Eats de la fiche resto

- **Format** : `https://www.ubereats.com/fr/store/…`
- **À insérer** : `index.html` — chercher `data-todo="real-ubereats-url"`
- Remplacer `href="#"` par la vraie URL, supprimer l'attribut `data-todo`.

### 2. URL Deliveroo de la fiche resto

- **Format** : `https://deliveroo.fr/fr/menu/…`
- **À insérer** : `index.html` — chercher `data-todo="real-deliveroo-url"`
- Remplacer `href="#"` par la vraie URL, supprimer l'attribut `data-todo`.

### 3. Horaires exacts

- **Actuel** : `11h-14h · 18h-22h · 7j/7` marqué "(horaires à confirmer)"
- **À modifier** :
  - `index.html` section `#commander` : chercher `(horaires à confirmer)`
  - `index.html` bloc JSON-LD en haut du fichier : chercher `OpeningHoursSpecification` (2 blocs à ajuster)
- Format demandé : jours de fermeture éventuels, horaires par jour si variable.

### 4. Coordonnées légales (mentions légales)

À demander à Jihane :
- Raison sociale complète (ex : `SAS Crousty Bowls`, `Jihane XXX EI`, `SARL Machin`)
- SIRET (14 chiffres)
- Forme juridique
- Nom du gérant / dirigeant
- Adresse siège social (si différente de 63 Rue Maxime Guillot)
- Email de contact pro
- Numéro de TVA intracommunautaire (si assujettie)

**À faire ensuite** :
- Créer `mentions-legales.html` à la racine du repo
- Remplacer dans `index.html` le lien `<a href="#">Mentions légales</a>` (footer, ligne ~1311) par `<a href="/mentions-legales.html">`
- Ajouter l'URL dans `sitemap.xml`

### 5. Logo vectoriel

- **Actuel** : SVG recréé à 90% de fidélité (dans `<symbol id="cb-logo">` en haut de `index.html`)
- **À demander** : fichier `.svg`, `.ai` ou `.eps` du logo officiel
- **À faire** : remplacer le contenu du `<symbol id="cb-logo">` par le vrai vectoriel

### 6. Email de contact

- Actuellement absent du site
- **À insérer** :
  - Footer bloc "Infos"
  - Section commander (ajouter à côté du tel)
  - Mentions légales

---

## 🟡 Optionnel — enrichissement

### 7. Photos manquantes

Si Jihane peut fournir plus tard, on peut réactiver des blocs supprimés faute de photos :

| Photo | Réactive |
|-------|----------|
| Un vrai crousty (riz + poulet croustillant + sauce) | Bowl signature dédié dans la section CROUSTY |
| Poutine Karaage | La carte "Karaage Chicken" (supprimée) |
| Poutine Montagnard | La carte "Montagnard" (supprimée) |
| Poutine Chèvre | La carte "Chèvre" (supprimée) |
| Plateaux sushis (Découverte, Cœur, Premium) | Photos dans les 3 cartes de la section SUSHIS |
| Nem's, samoussas, brochettes, dynamites | Photos ardoise section ENTRÉES |
| Salle en situation (buffet, anniversaire) | Remplacer les photos actuelles de salle vide |
| Portrait de Jihane + petite bio | Section MAISON (humaniser) |

### 8. Réseaux sociaux supplémentaires

- Facebook (si compte existe) → ajouter dans footer + `sameAs` du JSON-LD
- TikTok (si compte existe) → idem

### 9. Google Business Profile

- Créer/vérifier la fiche Google Business
- Ajouter les photos (les mêmes que sur le site)
- Bien remplir les horaires et catégories
- Impact SEO local très important

---

## 🌐 Nom de domaine (à faire par Victor)

### Achat

- Vérifier dispo `crousty-bowls-chenove.fr` (préféré, cohérent avec URL Vercel)
- Ou `crousty-bowls.fr`
- Ou `croustybowls.fr`
- Registrar : OVH, Gandi, ou Cloudflare Registrar

### Branchement Vercel

1. Dashboard Vercel → projet `crousty-bowls-chenove` → Settings → Domains
2. Ajouter le domaine (ex : `crousty-bowls-chenove.fr` + `www.crousty-bowls-chenove.fr`)
3. Vercel donne les enregistrements DNS à créer chez le registrar :
   - Enregistrement A pour `crousty-bowls-chenove.fr` → `76.76.21.21`
   - Enregistrement CNAME pour `www` → `cname.vercel-dns.com`
4. Attendre la propagation (~10min à quelques heures)
5. Vercel émet automatiquement le certificat SSL

### Mise à jour du code après branchement

Dans `index.html` :
- `<link rel="canonical" href="https://crousty-bowls-chenove.vercel.app/" />` → nouveau domaine
- Bloc JSON-LD `"url"` → nouveau domaine
- `<meta property="og:url">` → nouveau domaine
- Toutes les URLs absolues (OG image, etc.)

Dans `sitemap.xml` :
- Toutes les `<loc>` → nouveau domaine

Dans `robots.txt` :
- Ligne `Sitemap:` → nouveau domaine

---

## 🧪 Vérifications avant livraison finale

- [ ] Toutes les URLs `href="#"` avec `data-todo` remplacées
- [ ] `(horaires à confirmer)` supprimé du site + JSON-LD à jour
- [ ] Page mentions légales créée + liée dans footer + sitemap
- [ ] Logo vectoriel remplacé
- [ ] Email de contact ajouté
- [ ] Domaine custom branché, certificat SSL actif
- [ ] Toutes les URLs canoniques mises à jour vers le nouveau domaine
- [ ] Test rapide sur PageSpeed Insights (viser 90+ mobile)
- [ ] Test rapide sur securityheaders.com (viser A ou A+)
- [ ] Fiche Google Business créée et vérifiée
