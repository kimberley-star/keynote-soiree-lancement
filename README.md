# Site — Keynote & soirée de lancement Flatchr

Site statique (HTML/CSS/JS, sans build) aux couleurs de Flatchr.

| Page | Contenu |
|---|---|
| `index.html` | Invitation, compte à rebours, infos pratiques, inscription |
| `programme.html` | Déroulé détaillé de la soirée |
| `intervenants.html` | Présentation des intervenants |
| `evenement.html` | Page simple : l'essentiel de l'événement + lien vers le site (à partager par e-mail, LinkedIn…) |

## Pages masquées
`programme.html` et `intervenants.html` existent toujours mais ne sont plus liées. Pour les réafficher, retirer les commentaires `<!-- MASQUÉ … -->` dans `index.html` (menu et résumé du programme).

## Mettre à jour
- **Date, horaires, lieu, lien d'inscription, vidéo** : objet `EVENT` en haut de `assets/site.js` (alimente le compte à rebours et le bouton « Ajouter à mon agenda »), puis les textes des pages.
- **Contenus provisoires** : repérés par la classe `a-completer` (soulignés en orange). Une fois validés, retirer la classe et le bandeau `draft-note` en haut de chaque page.
- **Couleurs** : variables en haut de `assets/style.css`.

## Mise en ligne
GitHub Pages via `.github/workflows/pages.yml` (publie `index.html`, `evenement.html` et `assets/` à chaque push). Activation unique : *Settings > Pages > Source : GitHub Actions*.
Adresse : https://kimberley-star.github.io/keynote-soiree-lancement/

## Aperçu local
Ouvrir `index.html` dans un navigateur. Hébergement possible tel quel (GitHub Pages, Netlify, HubSpot…).
