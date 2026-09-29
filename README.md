# Site — Keynote & soirée de lancement Flatchr

Site statique (HTML/CSS/JS, sans build) aux couleurs de Flatchr.

| Page | Contenu |
|---|---|
| `index.html` | Invitation, compte à rebours, infos pratiques, inscription |
| `programme.html` | Déroulé détaillé de la soirée |
| `intervenants.html` | Présentation des intervenants |
| `evenement.html` | Page simple : l'essentiel de l'événement + lien vers le site (à partager par e-mail, LinkedIn…) |

## Mettre à jour
- **Date, horaires, lieu, lien d'inscription, vidéo** : objet `EVENT` en haut de `assets/site.js` (alimente le compte à rebours et le bouton « Ajouter à mon agenda »), puis les textes des pages.
- **Contenus provisoires** : repérés par la classe `a-completer` (soulignés en orange). Une fois validés, retirer la classe et le bandeau `draft-note` en haut de chaque page.
- **Couleurs** : variables en haut de `assets/style.css`.

## Aperçu local
Ouvrir `index.html` dans un navigateur. Hébergement possible tel quel (GitHub Pages, Netlify, HubSpot…).
