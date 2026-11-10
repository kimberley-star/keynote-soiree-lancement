# Encart « Agent IA » — home flatchr.io

Remplace la section « Choisissez Flatchr pour recruter l'équipe de vos rêves ».

| Fichier | Rôle |
|---|---|
| `encart-agent-ia.html` | Le code à coller dans HubSpot (HTML + CSS + JS, autonome) |
| `apercu.html` | Aperçu dans une home simulée (régénéré par `build-apercu.sh`) |

## Intégration HubSpot (≈ 10 min)
1. Pages du site > Home > **Modifier** (travailler sur un brouillon).
2. Supprimer la section « Choisissez Flatchr… ».
3. À sa place : ajouter un module **HTML personnalisé**, puis coller `encart-agent-ia.html` en entier.
4. Remplacer `href="/agent-ia"` par l'URL de la page dédiée de l'agent.
5. Hero : ajouter un 2ᵉ bouton **« Rencontrer notre agent IA »** qui pointe vers `#agent-ia` (ancre de l'encart) ou vers la page dédiée.
6. Prévisualiser en desktop et en mobile, puis publier.

Si l'éditeur HubSpot retire le `<script>`, le coller dans Paramètres de la page > Avancé > « HTML du pied de page ». Sans JS, l'encart s'affiche quand même (1ᵉʳ onglet), mais sans animation.

## Contenu de l'encart
- Accroche reprise du hero : *Le RH pilote, le manager recrute, l'agent IA accélère.*
- 3 cartes RH / Manager / Dirigeant : on garde le positionnement de la section supprimée.
- 5 capacités en onglets qui défilent tout seuls (pause au survol), avec une démo animée façon chat à droite (équivalent de la vidéo de Leo chez Digitaleo).
- Preuve chiffrée : « jusqu'à 70 % » (chiffre déjà publié sur /fonctionnalites-ia-flatchr).
- Message de confiance : l'IA propose, vous décidez + RGPD.
- 2 boutons : Découvrir l'agent IA / Demander une démo.

## Points à valider
- Nom produit de l'agent : le texte dit « l'agent IA Flatchr ».
- Les 5 capacités reprennent les fonctionnalités IA existantes. Si l'agent fait plus (actions autonomes, relances, planification), mettre les onglets à jour.
- Démo : données fictives et anonymisées, mention « Exemple illustratif » affichée.
