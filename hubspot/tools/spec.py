"""Source unique des champs des modules HubSpot « Agent IA » : génère fields.json et meta.json."""
import json, os

def T(name, label, default=""): return {"name": name, "label": label, "type": "text", "default": default}
def TA(name, label, default=""): return T(name, label, default)  # champ texte long (type « Texte » dans HubSpot)
def B(name, label, default=False): return {"name": name, "label": label, "type": "boolean", "default": default}
def CH(name, label, choices, default): return {"name": name, "label": label, "type": "choice", "display": "select", "choices": choices, "default": default}
def R(name, label, default): return {"name": name, "label": label, "type": "text", "occurrence": {"min": 0, "default": len(default)}, "default": default}
def G(name, label, children, default): return {"name": name, "label": label, "type": "group", "occurrence": {"min": 0, "default": len(default)}, "children": children, "default": default}

FREE = "https://app.flatchr.io/signup"

MODULES = [
 ("agent-ia-hero", "Agent IA - Hero prompt", "Champ de saisie façon ChatGPT + lien vers l'accès gratuit", [
   T("badge", "Badge", "Nouveau · L'agent IA Flatchr"),
   T("title", "Titre (début)", "Agent IA de recrutement\u00a0:"),
   T("title_highlight", "Titre (partie en couleur)", "recrutez en une conversation."),
   TA("lead", "Texte d'accroche", "Dites à l'agent IA Flatchr ce dont vous avez besoin. Il rédige l'annonce, la diffuse, trie les candidats et cale les entretiens. Vous, vous gérez votre équipe."),
   T("placeholder", "Texte d'exemple dans le champ", "Ex. : Je cherche 2 vendeurs en CDI pour mon magasin de Lyon, dispo dès lundi…"),
   T("hint", "Mention sous le champ", "✨ L'agent IA Flatchr démarre votre recrutement"),
   R("chips", "Exemples de demandes", ["Recruter un serveur pour ce week-end", "Ouvrir un poste dans mes 12 franchises", "Trier les candidats de la semaine"]),
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
   R("points", "Points clés", ["L'agent rédige et publie l'annonce sur les bons jobboards", "Il présélectionne les candidats selon vos critères", "Il propose les créneaux d'entretien et relance pour vous"]),
   T("agent_name", "Nom affiché dans WhatsApp", "Agent IA Flatchr"),
   G("messages", "Messages de la conversation", [
       CH("sender", "Envoyé par", [["manager", "Manager (bulle verte, à droite)"], ["agent", "Agent IA (bulle blanche, à gauche)"]], "manager"),
       T("message", "Message"),
       T("card", "Encadré sous le message (facultatif, <br> pour aller à la ligne)"),
       T("time", "Heure", "09:12")],
     [{"sender": "manager", "message": "Salut ! J'ai besoin de 2 vendeurs en CDI pour le magasin de Lyon Part-Dieu, dispo vite 🙏", "card": "", "time": "09:12"},
      {"sender": "agent", "message": "C'est noté 👍 J'ai préparé l'annonce à partir de votre modèle « Vendeur·se ». Je la publie ?", "card": "📄 Vendeur·se H/F – CDI 35h – Lyon Part-Dieu", "time": "09:12"},
      {"sender": "manager", "message": "Oui, vas-y", "card": "", "time": "09:13"},
      {"sender": "agent", "message": "Publiée sur Indeed, France Travail et votre page carrière ✅ Je vous préviens dès que j'ai des profils.", "card": "", "time": "09:13"},
      {"sender": "agent", "message": "Bonne nouvelle : 14 candidatures depuis hier. Voici les 3 profils qui collent le mieux :", "card": "⭐ Sarah M. — 3 ans en retail<br>⭐ Yanis B. — dispo immédiatement<br>⭐ Léa D. — vente + caisse", "time": "18:40"},
      {"sender": "manager", "message": "Top, je veux voir Sarah et Yanis", "card": "", "time": "18:42"},
      {"sender": "agent", "message": "Entretiens calés jeudi à 10h et 11h, invitations envoyées 📅 Bonne soirée !", "card": "", "time": "18:42"}]),
 ]),
 ("agent-ia-cartes", "Agent IA - Cartes", "3 cartes : bénéfices (icônes) ou étapes (numérotées)", [
   T("eyebrow", "Surtitre", "Pour le terrain"),
   T("title", "Titre", "Pourquoi adopter un agent IA de recrutement ?"),
   T("subtitle", "Sous-titre (facultatif)", "Pensé pour les managers terrain et les réseaux de franchise."),
   B("numbered", "Cartes numérotées (étapes) au lieu des icônes", False),
   B("soft_background", "Fond gris clair", False),
   G("cards", "Cartes", [T("card_icon", "Icône (emoji, ignorée si numérotée)"), T("card_tag", "Étiquette (facultatif)"), T("card_title", "Titre de la carte"), TA("card_text", "Texte de la carte")],
     [{"card_icon": "⏱️", "card_tag": "Managers terrain", "card_title": "Du temps rendu au terrain", "card_text": "Annonce, tri, prise de rendez-vous : l'agent s'occupe de l'administratif. Le manager garde la main sur la décision finale."},
      {"card_icon": "💬", "card_tag": "Managers terrain", "card_title": "Zéro formation", "card_text": "Un message WhatsApp suffit. Pas de logiciel à ouvrir, pas de mot de passe à retenir : l'adoption est immédiate."},
      {"card_icon": "🏬", "card_tag": "Réseaux de franchise", "card_title": "Un réseau autonome, une marque cohérente", "card_text": "Chaque point de vente recrute en autonomie, avec vos modèles d'annonces et vos process. Le siège garde une vision consolidée."}]),
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
  "cards": [{"card_title": "Exprimez votre besoin", "card_text": "Par WhatsApp ou depuis Flatchr, décrivez le poste en quelques mots, comme vous le feriez à un collègue."},
            {"card_title": "L'agent passe à l'action", "card_text": "Il rédige l'annonce, la diffuse, analyse les candidatures et vous présente une shortlist."},
            {"card_title": "Vous choisissez, vous recrutez", "card_text": "Validez les profils, l'agent organise les entretiens. Vous rencontrez les bons candidats, sans perte de temps."}]}

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..", "modules")
    for slug, label, _, fields in MODULES:
        d = os.path.join(root, slug + ".module")
        json.dump(fields, open(os.path.join(d, "fields.json"), "w"), ensure_ascii=False, indent=2)
        json.dump({"label": label, "css_assets": [], "external_js": [], "global": False, "host_template_types": ["PAGE"],
                   "is_available_for_new_content": True, "smart_type": "NOT_SMART", "tags": [], "other_assets": []},
                  open(os.path.join(d, "meta.json"), "w"), ensure_ascii=False, indent=2)
    print("ok")
