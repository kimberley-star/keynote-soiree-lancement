# Page HubSpot « Agent IA Flatchr » — plan validé par Kimberley

Statut : validé. Le connecteur Claude ↔ HubSpot n'a pas les droits d'écriture : création manuelle via le guide `hubspot/guide-hubspot-agent-ia.html`.
Code des modules : `hubspot/modules/*.module/` (import direct possible : `hs upload hubspot/modules "Agent IA"`).
Textes et champs : source unique `hubspot/tools/spec.py` (relancer `python3 hubspot/tools/spec.py` puis `python3 hubspot/tools/build_guide.py` après modification).

## Page
- Type : page de site web, **brouillon (ne pas publier)**
- Modèle : `Flatchr theme mar2024/pages/templates/site-flex.html` (Flex : menu + footer globaux du site)
- Nom interne : `Agent IA Flatchr — Lancement (brouillon)`
- Slug : `agent-ia-recrutement`
- Titre SEO : « Agent IA de recrutement pour vos managers terrain | Flatchr »
- Méta-description : « Vos managers terrain recrutent depuis WhatsApp grâce à l'agent IA Flatchr. Disponible le 1er janvier. Accès gratuit. »

## Modules, dans l'ordre
1. **Agent IA - Hero prompt** (nouveau module) : code dans `hubspot/modules/hero-prompt.*`
2. **Agent IA - Vidéo de vision** (nouveau) : surtitre, titre, sous-titre, lien vidéo (YouTube / Vimeo / .mp4)
3. **Agent IA - Démo WhatsApp** (nouveau) : titre, texte, 3 puces, nom de l'agent, messages répétables (expéditeur manager/agent, texte, carte, heure)
4. **Bénéfices** : module « Agent IA - Cartes » (icônes)
5. **Comment ça marche** : module « Agent IA - Cartes » (numéroté, fond gris)
6. **Agent IA - Lancement** (nouveau) : « Disponible le 1er janvier », texte, date du compte à rebours, 2 boutons

Design et textes de référence : `agent-ia.html` (aperçu : https://claude.ai/artifact/KAGHm8QposPBzecUeNvF2v).
À vérifier : lien d'accès gratuit `https://app.flatchr.io/signup`, mention « Sans carte bancaire », vidéo de vision.
