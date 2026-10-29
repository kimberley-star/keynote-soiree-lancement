"""Source unique des champs des modules HubSpot « Agent IA » : génère fields.json et meta.json."""
import json, os

def T(name, label, default=""): return {"name": name, "label": label, "type": "text", "default": default}
def TA(name, label, default=""): return T(name, label, default)  # champ texte long (type « Texte » dans HubSpot)
def B(name, label, default=False): return {"name": name, "label": label, "type": "boolean", "default": default}
def CH(name, label, choices, default): return {"name": name, "label": label, "type": "choice", "display": "select", "choices": choices, "default": default}
def R(name, label, default): return {"name": name, "label": label, "type": "text", "occurrence": {"min": 0, "default": len(default)}, "default": default}
def RT(name, label, default=""): return {"name": name, "label": label, "type": "richtext", "default": default}
def G(name, label, children, default): return {"name": name, "label": label, "type": "group", "occurrence": {"min": 0, "default": len(default)}, "children": children, "default": default}

FREE = "https://app.flatchr.io/signup"

MODULES = [
 ("agent-ia-hero", "Agent IA - Hero prompt", "Champ de saisie façon ChatGPT + lien vers l'accès gratuit", [
   T("badge", "Badge", "Nouveau · L'agent IA Flatchr"),
   T("title", "Titre (début)", "Agent IA de recrutement\u00a0:"),
   T("title_highlight", "Titre (partie en couleur)", "recrutez en une conversation."),
   TA("lead", "Texte d'accroche", "Dites à l'agent IA Flatchr ce dont vous avez besoin, à l'écrit ou à la voix. Il rédige vos offres, retrouve les bons profils dans votre CVthèque et prépare vos comptes rendus. Vous, vous gérez votre équipe."),
   T("placeholder", "Texte d'exemple dans le champ", "Ex. : Je cherche 2 vendeurs en CDI pour mon magasin de Lyon, dispo dès lundi…"),
   T("hint", "Mention sous le champ", "✨ L'agent IA Flatchr démarre votre recrutement"),
   R("chips", "Exemples de demandes", ["Rédige une offre de serveur pour ce week-end", "Trouve un vendeur dans ma CVthèque", "Aide-moi à choisir parmi les candidats"]),
   T("cta_text", "Texte du bouton", "Essayer gratuitement"),
   T("cta_url", "Lien de l'accès gratuit", FREE),
   T("note", "Mention sous le bouton", "Sans carte bancaire · Accès gratuit"),
   {"name": "decor_image", "label": "Illustration de fond (facultatif)", "type": "image", "default": {"src": "", "alt": "", "loading": "eager"}},
   CH("decor_side", "Côté de l'illustration", [["left", "Gauche"], ["right", "Droite"]], "left"),
 ]),
 ("agent-ia-video", "Agent IA - Vidéo de vision", "Vidéo YouTube, Vimeo ou .mp4, avec encart d'attente", [
   T("eyebrow", "Surtitre", "Notre vision"),
   T("title", "Titre", "Notre vision de l'agent IA de recrutement"),
   T("subtitle", "Sous-titre", "Le RH pilote, le manager recrute, l'IA accélère. Pourquoi nous l'avons conçu pour celles et ceux qui recrutent sur le terrain."),
   T("video_url", "Lien de la vidéo (YouTube, Vimeo ou .mp4) — vide = encart d'attente", ""),
   T("placeholder_title", "Encart d'attente : titre", "Vidéo de vision"),
   T("placeholder_text", "Encart d'attente : texte", "Bientôt disponible"),
 ]),
 ("agent-ia-whatsapp", "Agent IA - Démo WhatsApp", "Téléphone avec conversation animée manager / agent", [
   T("eyebrow", "Surtitre", "Démo"),
   T("title", "Titre", "Recruter depuis WhatsApp, entre deux clients"),
   TA("intro", "Texte d'introduction", "Pas de nouveau logiciel à apprendre : vos managers écrivent à leur agent IA de recrutement comme à un collègue, depuis l'appli qu'ils utilisent déjà."),
   R("points", "Points clés", ["Une offre rédigée à partir d'une simple phrase", "Un CV ajouté en le prenant en photo", "Un compte rendu d'entretien dicté en note vocale"]),
   T("agent_name", "Nom affiché dans WhatsApp", "Agent IA Flatchr"),
   G("messages", "Messages de la conversation", [
       CH("sender", "Envoyé par", [["manager", "Manager (bulle verte, à droite)"], ["agent", "Agent IA (bulle blanche, à gauche)"]], "manager"),
       T("message", "Message"),
       T("card", "Encadré sous le message (facultatif, <br> pour aller à la ligne)"),
       T("time", "Heure", "09:12")],
     [{"sender": "manager", "message": "Salut ! J'ai besoin d'un commis de cuisine en CDI à Bordeaux, dispo vite 🙏", "card": "", "time": "09:12"},
      {"sender": "agent", "message": "C'est noté 👍 J'ai rédigé l'offre à partir de votre modèle. Elle vous convient ?", "card": "📄 Commis de cuisine H/F – CDI 35h – Bordeaux", "time": "09:12"},
      {"sender": "manager", "message": "Parfait. Tu as déjà des profils dans la CVthèque ?", "card": "", "time": "09:13"},
      {"sender": "agent", "message": "Oui, 3 profils correspondent :", "card": "⭐ Yanis B. — 2 ans en brasserie<br>⭐ Inès D. — dispo immédiatement<br>⭐ Hugo L. — CAP cuisine", "time": "09:13"},
      {"sender": "manager", "message": "📷 Photo d'un CV déposé ce matin", "card": "", "time": "11:40"},
      {"sender": "agent", "message": "CV de Julie R. ajouté à votre CVthèque et rattaché à l'offre ✅", "card": "", "time": "11:40"},
      {"sender": "manager", "message": "🎤 Note vocale · 0:42", "card": "", "time": "18:05"},
      {"sender": "agent", "message": "Compte rendu de l'entretien avec Yanis enregistré sur sa fiche 📝", "card": "", "time": "18:05"}]),
 ]),
 ("agent-ia-cartes", "Agent IA - Cartes", "3 cartes : bénéfices (icônes) ou étapes (numérotées)", [
   T("eyebrow", "Surtitre", "Pour le terrain"),
   T("title", "Titre", "Pourquoi adopter un agent IA de recrutement ?"),
   T("subtitle", "Sous-titre (facultatif)", "Pensé pour les managers terrain et les réseaux de franchise."),
   B("numbered", "Cartes numérotées (étapes) au lieu des icônes", False),
   B("soft_background", "Fond gris clair", False),
   G("cards", "Cartes", [T("card_icon", "Icône (emoji, ignorée si numérotée)"), T("card_tag", "Étiquette (facultatif)"), T("card_title", "Titre de la carte"), TA("card_text", "Texte de la carte")],
     [{"card_icon": "⏱️", "card_tag": "Managers terrain", "card_title": "Du temps rendu au terrain", "card_text": "Rédaction des offres, recherche de profils, comptes rendus : l'agent s'occupe de l'administratif. Le manager garde la main sur la décision finale."},
      {"card_icon": "💬", "card_tag": "Managers terrain", "card_title": "Zéro formation", "card_text": "Un message WhatsApp suffit. Pas de logiciel à ouvrir, pas de mot de passe à retenir : l'adoption est immédiate."},
      {"card_icon": "🏬", "card_tag": "Réseaux de franchise", "card_title": "Un réseau autonome, une marque cohérente", "card_text": "Chaque point de vente recrute en autonomie, avec vos modèles d'annonces et vos process. Le siège garde une vision consolidée."}]),
 ]),
 ("agent-ia-confiance", "Agent IA - Confiance", "Bloc souveraineté des données, RGPD et AI Act", [
   T("eyebrow", "Surtitre", "Souveraineté et conformité"),
   T("title", "Titre", "Un agent IA de recrutement de confiance, avec vos données en France"),
   TA("intro", "Introduction", "Recruter avec l'IA ne doit jamais se faire au détriment de vos candidats ni de vos données. L'agent IA Flatchr est conçu pour respecter le RGPD et les principes de l'AI Act européen."),
   R("badges", "Badges", ["Données hébergées en France", "Datacenters ISO 27001", "SOC 2", "RGPD", "Principes de l'AI Act"]),
   G("pillars", "Piliers", [T("pillar_icon", "Icône (emoji)"), T("pillar_title", "Titre du pilier"), RT("pillar_text", "Texte du pilier")],
     [{"pillar_icon": "🇫🇷", "pillar_title": "Vos données restent en France",
       "pillar_text": "<p>Les données personnelles de vos candidats sont hébergées en France, dans des centres de données certifiés ISO 27001 et conformes SOC 2.</p><p>Flatchr ne partage jamais les informations personnelles de vos candidats : vous gardez la maîtrise de vos données de recrutement.</p>"},
      {"pillar_icon": "🛡️", "pillar_title": "RGPD dès la conception",
       "pillar_text": "<ul><li>Gestion des consentements des candidats</li><li>Archivage automatique des candidatures</li><li>Outil d'anonymisation</li><li>Accès aux données selon le rôle de chaque utilisateur</li><li>Accord de traitement des données (DPA) sur demande</li></ul>"},
      {"pillar_icon": "⚖️", "pillar_title": "Conçu selon les principes de l'AI Act",
       "pillar_text": "<p>L'AI Act européen encadre de près l'IA utilisée pour recruter. L'agent est conçu autour de ses principes :</p><ul><li>L'humain décide toujours : aucun candidat écarté automatiquement</li><li>Uniquement des critères liés au poste, jamais de données sensibles</li><li>Transparence : vous voyez les critères de chaque analyse</li><li>Aucune analyse des émotions des candidats</li></ul>"}]),
   T("cta_text", "Texte du lien", "Découvrir notre politique de sécurité"),
   T("cta_url", "Lien", "https://www.flatchr.io/security"),
 ]),
 ("agent-ia-lancement", "Agent IA - Lancement", "Bloc « Disponible le 1er janvier » avec compte à rebours", [
   T("eyebrow", "Surtitre", "Lancement"),
   T("title", "Titre (début)", "Disponible le"),
   T("title_highlight", "Titre (partie en orange)", "1er janvier"),
   TA("text", "Texte", "Activez votre accès gratuit dès maintenant et soyez parmi les premiers à recruter avec l'agent IA de recrutement Flatchr."),
   T("launch_date", "Date du compte à rebours (format 2027-01-01T00:00:00+01:00 — vide = pas de compte à rebours)", "2027-01-01T00:00:00+01:00"),
   T("cta1_text", "Bouton 1 : texte", "Obtenir mon accès gratuit"),
   T("cta1_url", "Bouton 1 : lien", FREE),
   T("cta2_text", "Bouton 2 : texte", "Demander une démo"),
   T("cta2_url", "Bouton 2 : lien", "https://www.flatchr.io/demo"),
 ]),
]

# Contenu de la 2e instance du module Cartes (« Comment ça marche »)
STEPS = {"eyebrow": "Comment ça marche", "subtitle": "", "title": "Comment fonctionne l'agent IA de recrutement Flatchr ?", "numbered": True, "soft_background": True,
  "cards": [{"card_title": "Exprimez votre besoin", "card_text": "Par écrit ou par la voix, sur WhatsApp ou dans Flatchr : décrivez votre besoin comme vous le feriez à un collègue."},
            {"card_title": "L'agent passe à l'action", "card_text": "Il rédige l'offre, cherche dans votre CVthèque et vous aide à sélectionner les candidats sur des critères liés au poste."},
            {"card_title": "Vous choisissez, vous recrutez", "card_text": "Vous rencontrez les candidats et dictez votre compte rendu en note vocale : tout est centralisé dans Flatchr."}]}

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..", "modules")
    for slug, label, _, fields in MODULES:
        d = os.path.join(root, slug + ".module")
        json.dump(fields, open(os.path.join(d, "fields.json"), "w"), ensure_ascii=False, indent=2)
        json.dump({"label": label, "css_assets": [], "external_js": [], "global": False, "host_template_types": ["PAGE"],
                   "is_available_for_new_content": True, "smart_type": "NOT_SMART", "tags": [], "other_assets": []},
                  open(os.path.join(d, "meta.json"), "w"), ensure_ascii=False, indent=2)
    print("ok")

# Modules du thème Flatchr réutilisés tels quels (comme sur les pages fonctionnalités)
# « Zig zag » (/Flatchr theme mar2024/pages/modules/zig-zag) : 4 blocs texte + visuel alternés
ZIGZAG = [
 {"title": "Rédigez vos offres d'emploi en une phrase",
  "caption": ["Décrivez le poste comme vous le feriez à un collègue : intitulé, contrat, lieu, date de démarrage. L'agent IA de recrutement rédige une offre complète à partir de vos modèles et de vos meilleures annonces.",
              "Missions, profil recherché, avantages : tout y est, dans le ton de votre marque employeur. Vous relisez, ajustez si besoin et validez."],
  "image": "agent-ia-redaction-offre.png", "cta_link": "https://www.flatchr.io/fonctionnalites-ia-flatchr"},
 {"title": "Donnez vos instructions à l'agent par la voix",
  "caption": ["Entre deux clients ou sur la route, pas besoin d'écrire : envoyez une note vocale à l'agent, comme à un collègue.",
              "L'agent comprend votre demande et passe à l'action : rédiger une offre, chercher un profil, préparer un message à un candidat."],
  "image": "agent-ia-instructions-vocales.png", "cta_link": ""},
 {"title": "Retrouvez le bon profil dans votre CVthèque",
  "caption": ["Posez simplement la question : « Tu as un serveur dispo le week-end près de Lille ? ». L'agent fouille votre CVthèque et vous présente les profils qui correspondent.",
              "Vos anciens candidats deviennent une vraie source de recrutement : vous ne repartez plus de zéro à chaque nouveau poste."],
  "image": "agent-ia-recherche-cvtheque.png", "cta_link": "https://www.flatchr.io/cvtheque"},
 {"title": "Ajoutez un CV à partir d'une simple photo",
  "caption": ["Un candidat vous tend un CV papier en boutique ? Prenez-le en photo et envoyez-le à l'agent.",
              "L'agent lit le CV, crée la fiche du candidat dans votre CVthèque et la rattache à l'offre en cours. Plus aucun CV perdu au fond d'un tiroir."],
  "image": "agent-ia-cv-photo.png", "cta_link": "https://www.flatchr.io/cvtheque"},
 {"title": "Une aide à la sélection conforme au RGPD et sans biais",
  "caption": ["L'agent compare chaque candidature aux critères de votre offre : expérience, compétences, disponibilités. Il vous aide à repérer les profils les plus pertinents, sans jamais décider à votre place.",
              "L'analyse repose uniquement sur des critères liés au poste, pour limiter les biais et respecter le RGPD. Aucun candidat n'est écarté automatiquement : vous gardez la main."],
  "image": "agent-ia-aide-selection-rgpd.png", "cta_link": "https://www.flatchr.io/matching-tri-cv-offre-emploi"},
 {"title": "Vos comptes rendus d'entretien en note vocale",
  "caption": ["À la sortie d'un entretien, dictez vos impressions en quelques secondes. L'agent transforme votre note vocale en compte rendu structuré : points forts, points de vigilance, avis.",
              "Le compte rendu est enregistré sur la fiche du candidat et partagé avec les RH. Fini les notes prises sur un coin de table."],
  "image": "agent-ia-compte-rendu-vocal.png", "cta_link": "https://www.flatchr.io/evaluation"},
 {"title": "Des messages aux candidats reformulés par l'IA",
  "caption": ["Écrivez votre message comme il vient : l'agent le reformule pour vos candidats, de façon claire, polie et fidèle à votre marque employeur.",
              "Réponse positive, refus ou demande d'information : vous relisez et envoyez en un clic. Chaque candidat reçoit une réponse soignée, même quand le temps manque."],
  "image": "agent-ia-reformulation-messages.png", "cta_link": "https://www.flatchr.io/messagerie"},
]
# « Three col cards with stroke cta » : bloc « Découvrez la suite » (mêmes cartes que sur /multidiffusion)
DISCOVER = {"title": "Découvrez la suite", "cards": [
 {"icon": "hub-3.svg", "title": "Sourcez des top talents", "text": "Sourcez en quelques clics avec Flatchr pour trouver le candidat idéal", "cta_link": "https://www.flatchr.io/sourcing"},
 {"icon": "collections_bookmark-1.svg", "title": "Gérez vos candidatures", "text": "Centralisez toutes les candidatures sur une plateforme unique pour simplifier vos recrutements", "cta_link": "https://www.flatchr.io/ats"},
 {"icon": "supervised_user_circle-3.svg", "title": "Vos talents dans la CVthèque", "text": "Créez votre vivier de talents et maximisez vos chances de trouver le bon candidat à tout moment", "cta_link": "https://www.flatchr.io/cvtheque"}]}

# « FAQ two col » (/Flatchr theme mar2024/pages/modules/faq-two-col), tout en bas de la page.
# Champs « Heading » et « Text » du module laissés VIDES (sinon titre en H1) ; le titre passe par la colonne (H2).
FAQ_TITLE = "Questions fréquentes sur l'agent IA de recrutement"
FAQ = [
 ("Qu'est-ce qu'un agent IA de recrutement ?",
  ["Un agent IA de recrutement est un assistant basé sur l'intelligence artificielle qui prend en charge les tâches répétitives du recrutement à partir d'une simple demande, écrite ou orale.",
   "Avec Flatchr, l'agent rédige vos offres d'emploi, retrouve des profils dans votre CVthèque, ajoute des CV, prépare vos comptes rendus d'entretien et reformule vos messages aux candidats. Vous gardez toujours la décision finale."]),
 ("Comment fonctionne l'agent IA de recrutement Flatchr ?",
  ["Vous échangez avec l'agent comme avec un collègue, sur WhatsApp ou depuis Flatchr, par message écrit ou par note vocale. Il comprend votre demande et l'exécute dans votre ATS.",
   "Tout ce qu'il produit (offres, fiches candidats, comptes rendus, messages) est enregistré dans Flatchr : les RH et les managers travaillent sur les mêmes informations."]),
 ("Faut-il installer une application pour utiliser l'agent ?",
  ["Non. Vos managers utilisent l'application qu'ils ont déjà dans leur poche : il suffit d'écrire ou d'envoyer une note vocale à l'agent. Aucun nouveau logiciel à apprendre, aucune formation nécessaire."]),
 ("L'agent IA prend-il des décisions à la place du manager ?",
  ["Non. L'agent prépare, propose et vous fait gagner du temps, mais c'est toujours vous qui validez : une offre avant sa mise en ligne, un message avant son envoi, un candidat avant de le retenir."]),
 ("L'agent IA de recrutement est-il conforme au RGPD ?",
  ["Oui. L'agent fonctionne au sein de l'ATS Flatchr, conforme au RGPD dès sa conception : gestion des consentements des candidats, archivage automatique des candidatures et outil d'anonymisation.",
   "L'aide à la sélection repose uniquement sur des critères liés au poste, et un accord de traitement des données (DPA) vous est fourni sur demande."]),
 ("Où sont hébergées les données traitées par l'agent IA ?",
  ["Les données personnelles de vos candidats restent en France, dans des centres de données certifiés ISO 27001 et conformes SOC 2, comme pour le reste de l'ATS Flatchr.",
   "Flatchr ne partage jamais les informations personnelles de vos candidats : vous gardez la maîtrise de vos données de recrutement."]),
 ("Comment l'agent protège-t-il les données sensibles ?",
  ["Chaque utilisateur n'accède qu'aux informations dont il a besoin selon son rôle : un manager voit ses recrutements, les RH gardent une vision d'ensemble.",
   "L'agent n'utilise aucune donnée sensible (santé, origine, opinions, vie privée) pour vous aider à sélectionner les candidats : seuls les critères liés au poste comptent."]),
 ("Les données de mes candidats servent-elles à entraîner l'IA ?",
  ["Non. Les CV, notes vocales et échanges traités par l'agent servent uniquement à vos recrutements. Ils ne sont pas utilisés pour entraîner des modèles d'intelligence artificielle."]),
 ("Comment l'agent limite-t-il les biais dans la sélection des candidats ?",
  ["L'agent compare chaque candidature aux seuls critères de votre offre, sans tenir compte d'informations sans rapport avec le poste. Aucun candidat n'est écarté automatiquement : toutes les candidatures restent consultables et la décision reste humaine."]),
 ("Que se passe-t-il quand j'envoie la photo d'un CV ?",
  ["L'agent lit le CV, crée la fiche du candidat dans votre CVthèque et peut la rattacher à l'offre en cours. Le CV papier remis en boutique ou en agence ne se perd plus."]),
 ("L'agent est-il adapté aux réseaux de franchise et aux entreprises multisites ?",
  ["Oui. Chaque manager de point de vente peut recruter en autonomie avec ses propres demandes, tandis que l'agent s'appuie sur vos modèles d'offres communs. Le siège ou les RH gardent une vision consolidée de tous les recrutements dans Flatchr."]),
 ("Quand l'agent IA de recrutement sera-t-il disponible ?",
  ["L'agent IA de recrutement Flatchr est disponible à partir du 1er janvier. Vous pouvez dès maintenant activer votre accès gratuit pour faire partie des premiers utilisateurs."]),
]

# Réponses à faire valider (produit / juridique) avant publication : question -> point à vérifier
FAQ_A_VALIDER = {
 "Où sont hébergées les données traitées par l'agent IA ?": "Confirmer que les traitements IA de l'agent (modèle utilisé, transcription des notes vocales) sont eux aussi hébergés en France, et préciser le cas des échanges WhatsApp, qui transitent par Meta. Attention : /security dit « en France », /faq dit « en Europe ».",
 "Comment l'agent protège-t-il les données sensibles ?": "Confirmer que l'agent ignore bien les données sensibles (santé, origine, opinions…) dans l'aide à la sélection.",
 "Les données de mes candidats servent-elles à entraîner l'IA ?": "Réponse à confirmer impérativement avec Damien : dépend du fournisseur du modèle IA et du contrat signé avec lui.",
 "Comment l'agent limite-t-il les biais dans la sélection des candidats ?": "Confirmer la formulation « sans tenir compte d'informations sans rapport avec le poste ».",
}

TRUST_A_VALIDER = "Pilier AI Act : faire valider par Damien et le DPO / juriste. Points à confirmer : critères affichés pour chaque analyse, aucune analyse des émotions (la reconnaissance des émotions au travail est interdite par l'AI Act depuis février 2025), aucune donnée sensible utilisée. Ne pas écrire « conforme à l'AI Act » sans validation juridique : le recrutement est classé « à haut risque » (annexe III)."
