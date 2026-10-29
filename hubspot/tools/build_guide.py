"""Génère guide-hubspot-agent-ia.html (kit pas à pas + code à copier) à partir des modules et de spec.py."""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from spec import MODULES, STEPS, ZIGZAG, DISCOVER

ROOT = os.path.join(os.path.dirname(__file__), "..")
e = html.escape
TYPE = {"image": "Image", "text": "Texte", "boolean": "Booléen (case à cocher)", "choice": "Choix", "group": "Groupe (répéteur)"}

def fields_rows(fields, indent=False):
    out = []
    for f in fields:
        pre = '<span class="sub">↳</span> ' if indent else ""
        extra = ""
        if f["type"] == "choice":
            extra = "<br><small>Options : " + " · ".join(f"<code>{e(v)}</code> ({e(l.split(' (')[0])})" for v, l in f["choices"]) + "</small>"
        if f["type"] == "group":
            extra = "<br><small>Groupe répété : crée d'abord les champs ci-dessous, puis regroupe-les (voir encadré). Active « Répéter ».</small>"
        elif "occurrence" in f:
            extra = "<br><small>Dans les options du champ, active « Répéter » (occurrences multiples).</small>"
        out.append(f'<tr><td>{pre}{e(f["label"])}</td><td><code class="cp" title="Cliquer pour copier">{e(f["name"])}</code></td><td>{TYPE[f["type"]]}{extra}</td></tr>')
        if f["type"] == "group":
            out += fields_rows(f["children"], True)
    return out

def content_list(fields, values):
    out = []
    for f in fields:
        v = values.get(f["name"], f.get("default"))
        if "occurrence" in f and f["type"] != "group":
            items = "".join(f"<li><span class='n'>{i}</span><div>{fmt(f, x)}</div></li>" for i, x in enumerate(v or [], 1))
            out.append(f'<div class="kv"><dt>{e(f["label"])}</dt><dd><ol class="items">{items}</ol></dd></div>')
        elif f["type"] == "group":
            items = []
            for i, it in enumerate(v or [], 1):
                parts = [f'<b>{e(c["label"].split(" (")[0])}</b> : {fmt(c, it.get(c["name"], ""))}' for c in f["children"] if it.get(c["name"], "") not in ("", None)]
                items.append(f"<li><span class='n'>{i}</span><div>{'<br>'.join(parts)}</div></li>")
            out.append(f'<div class="kv"><dt>{e(f["label"])}</dt><dd><ol class="items">{"".join(items)}</ol></dd></div>')
        elif f["type"] == "image":
            out.append(f'<div class="kv"><dt>{e(f["label"].split(" (")[0])}</dt><dd>{fmt(f, v)}</dd></div>')
        elif v not in ("", None):
            out.append(f'<div class="kv"><dt>{e(f["label"].split(" (")[0])}</dt><dd>{fmt(f, v)}</dd></div>')
    return "".join(out)

def fmt(f, v):
    if f["type"] == "boolean": return "✅ coché" if v else "☐ non coché"
    if f["type"] == "choice": return e(dict(f["choices"])[v])
    if f["type"] == "image": return "Choisis ton illustration (ex. les tentacules) dans le gestionnaire de fichiers"
    return f'<span class="val">{e(str(v))}</span>'

def code(label, path, lang):
    src = open(path).read().strip()
    if not src: return f'<div class="code empty"><div class="code-bar"><span>{label}</span></div><p>Rien à coller : laisse ce panneau vide.</p></div>'
    return f'<div class="code"><div class="code-bar"><span>{label}</span><button class="copy" type="button">Copier</button></div><pre><code>{e(src)}</code></pre></div>'

order_note = {"agent-ia-cartes": "Utilisé 2 fois sur la page : bénéfices, puis « Comment ça marche »."}
mods = []
for i, (slug, label, desc, fields) in enumerate(MODULES, 1):
    d = os.path.join(ROOT, "modules", slug + ".module")
    note = f'<p class="note">{order_note[slug]}</p>' if slug in order_note else ""
    mods.append(f"""
<details class="module" id="m-{slug}"{' open' if i == 1 else ''}>
  <summary><span class="badge">Module {i}</span><span class="mname">{e(label)}</span><span class="mdesc">{e(desc)}</span></summary>
  <div class="mbody">
    {note}
    <ol class="mini">
      <li><b>Fichier → Nouveau fichier → Module</b>. Utilisé dans : <b>Pages</b>. Type : module <b>local</b> (pas global). Dossier : <b>Agent IA</b>. Nom : <code class="cp">{e(label)}</code></li>
      <li>Colle le code ci-dessous dans les 3 panneaux de l'éditeur : <b>module.html</b>, <b>module.css</b>, <b>module.js</b>.</li>
      <li>Crée les champs du tableau (barre latérale « Ajouter un champ »). Le <b>nom HubL</b> doit être recopié à l'identique : clique dessus pour le copier.</li>
      <li>Clique sur <b>Publier les modifications</b> : ça rend le module disponible dans l'éditeur de page, ça ne publie rien sur le site.</li>
    </ol>
    <div class="tablewrap"><table><thead><tr><th>Libellé</th><th>Nom HubL</th><th>Type</th></tr></thead><tbody>{''.join(fields_rows(fields))}</tbody></table></div>
    {code("module.html (HTML + HubL)", d + "/module.html", "html")}
    {code("module.css", d + "/module.css", "css")}
    {code("module.js", d + "/module.js", "js")}
  </div>
</details>""")

spec = {s: (l, f) for s, l, _, f in MODULES}
def theme_zigzag():
    rows = []
    for k, z in enumerate(ZIGZAG, 1):
        cap = "".join(f"<p>{e(p)}</p>" for p in z["caption"])
        rows.append(f'<li><span class="n">{k}</span><div><b>Titre</b> : <span class="val">{e(z["title"])}</span><br><b>Légende</b> (texte enrichi, 2 paragraphes) :<div class="val">{cap}</div><b>Image</b> : <code class="cp">{e(z["image"])}</code> (déjà dans tes fichiers HubSpot)<br><b>Texte du bouton</b> : <span class="val">En savoir plus</span> · <b>Lien</b> : <code class="cp">{e(z["cta_link"])}</code><br><b>Inverser les colonnes</b> : {"✅ coché" if k % 2 == 0 else "☐ non coché"}</div></li>')
    return f'<p class="note">Module du thème « Zig zag » (déjà utilisé sur /multidiffusion) : rien à coder. Ajoute 4 éléments dans « zig_zag_group ».</p><ol class="items">{"".join(rows)}</ol>'
def theme_discover():
    rows = "".join(f'<li><span class="n">{k}</span><div><b>Icône</b> : <code class="cp">{e(c["icon"])}</code><br><b>Titre</b> : <span class="val">{e(c["title"])}</span><br><b>Texte</b> : <span class="val">{e(c["text"])}</span><br><b>Bouton</b> : En savoir plus · <code class="cp">{e(c["cta_link"])}</code></div></li>' for k, c in enumerate(DISCOVER["cards"], 1))
    return f'<p class="note">Module du thème « Three col cards with stroke cta » : le plus simple est de copier les cartes de la page /multidiffusion.</p><div class="kv"><dt>Titre</dt><dd><span class="val">{e(DISCOVER["title"])}</span></dd></div><ol class="items">{rows}</ol>'
page_order = [("agent-ia-hero", {}, "En-tête avec champ de saisie"), ("agent-ia-video", {}, "Vidéo de vision"),
              ("agent-ia-whatsapp", {}, "Démo WhatsApp"), ("theme:Zig zag (thème Flatchr)", theme_zigzag, "4 fonctionnalités en détail"),
              ("agent-ia-cartes", {}, "3 bénéfices"), ("agent-ia-cartes", STEPS, "Comment ça marche"),
              ("theme:Three col cards with stroke cta (thème Flatchr)", theme_discover, "Découvrez la suite"),
              ("agent-ia-lancement", {}, "Disponible le 1er janvier")]
content = []
for i, (slug, over, what) in enumerate(page_order, 1):
    if slug.startswith("theme:"):
        content.append(f'<details class="fill"><summary><span class="num">{i}</span><span><b>{e(slug[6:])}</b> <span class="what">· {e(what)}</span></span></summary><dl>{over()}</dl></details>')
        continue
    l, f = spec[slug]
    content.append(f'<details class="fill"><summary><span class="num">{i}</span><span><b>{e(l)}</b> <span class="what">· {e(what)}</span></span></summary><dl>{content_list(f, over)}</dl></details>')

page = f"""<title>Kit HubSpot Agent IA</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Mise en page : un guide de travail à suivre de haut en bas, aux couleurs Flatchr ; teal = repères, orange = points de vigilance. */
:root {{
  --bg: #ffffff; --surface: #f1f4f8; --line: #dee5ed; --fg: #182534; --muted: #5b6b7d;
  --accent: #019bb2; --accent-soft: #dbfaff; --warn: #c56f00; --warn-soft: #fff3e0; --code-bg: #12232f; --code-fg: #e3f1f5;
  --font: "Poppins", "Segoe UI", system-ui, sans-serif; --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #0e1a23; --surface: #152733; --line: #24404f; --fg: #e8f1f5; --muted: #9db3c0;
  --accent: #3cc8dc; --accent-soft: #10343f; --warn: #ffb24d; --warn-soft: #3a2a12; --code-bg: #08131a; --code-fg: #e3f1f5; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #0e1a23; --surface: #152733; --line: #24404f; --fg: #e8f1f5; --muted: #9db3c0;
  --accent: #3cc8dc; --accent-soft: #10343f; --warn: #ffb24d; --warn-soft: #3a2a12; --code-bg: #08131a; --code-fg: #e3f1f5; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--fg); font: 400 15px/1.6 var(--font); margin: 0; }}
.wrap {{ max-width: 58rem; margin: 0 auto; padding-inline: 16px; padding-block: 2.5rem 4rem; }}
h1, h2, h3 {{ line-height: 1.2; text-wrap: balance; margin: 0; }}
h1 {{ font-size: clamp(1.7rem, 4.5vw, 2.4rem); font-weight: 700; }}
h2 {{ font-size: 1.35rem; font-weight: 700; display: flex; gap: .7rem; align-items: center; }}
.step {{ display: inline-grid; place-items: center; width: 2rem; height: 2rem; border-radius: 50%; background: var(--accent); color: var(--bg); font-size: .95rem; flex: none; }}
p, li {{ max-width: 68ch; }}
.lead {{ color: var(--muted); margin-top: .6rem; font-size: 1.02rem; }}
.eyebrow {{ font-size: .75rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin: 0 0 .5rem; }}
section {{ margin-top: 2.75rem; display: grid; gap: 1rem; }}
code {{ font-family: var(--mono); font-size: .85em; background: var(--surface); border: 1px solid var(--line); border-radius: 5px; padding: .05rem .35rem; }}
code.cp {{ cursor: copy; }}
code.cp.ok {{ background: var(--accent-soft); border-color: var(--accent); }}
.routes {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
.route {{ border: 1px solid var(--line); border-radius: 14px; padding: 1.2rem 1.3rem; min-width: 0; }}
.route.main {{ border-color: var(--accent); background: var(--accent-soft); }}
.route h3 {{ font-size: 1rem; }}
.route p {{ margin: .4rem 0 0; color: var(--muted); font-size: .92rem; }}
.callout {{ border-left: 4px solid var(--warn); background: var(--warn-soft); border-radius: 8px; padding: .8rem 1rem; font-size: .93rem; }}
.callout b {{ color: var(--warn); }}
ol.mini {{ margin: 0; padding-left: 1.2rem; display: grid; gap: .35rem; }}
details.module {{ border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }}
details.module + details.module {{ margin-top: .1rem; }}
details > summary {{ cursor: pointer; list-style: none; }}
details > summary::-webkit-details-marker {{ display: none; }}
details.module > summary {{ display: grid; grid-template-columns: auto 1fr; gap: .1rem .8rem; padding: 1rem 1.2rem; background: var(--surface); align-items: center; }}
details.module > summary::after {{ content: "▸"; grid-column: 3; grid-row: 1 / span 2; color: var(--muted); transition: transform .15s; }}
details[open].module > summary::after {{ transform: rotate(90deg); }}
.badge {{ grid-row: 1 / span 2; font-size: .72rem; font-weight: 600; color: var(--accent); border: 1px solid var(--accent); border-radius: 999px; padding: .15rem .55rem; white-space: nowrap; }}
.mname {{ font-weight: 600; }}
.mdesc {{ color: var(--muted); font-size: .85rem; }}
.mbody {{ padding: 1.2rem; display: grid; gap: 1rem; min-width: 0; }}
.note {{ margin: 0; font-size: .9rem; color: var(--warn); font-weight: 500; }}
.tablewrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; }}
table {{ border-collapse: collapse; width: 100%; font-size: .88rem; }}
th, td {{ text-align: left; padding: .5rem .75rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); background: var(--surface); }}
tr:last-child td {{ border-bottom: 0; }}
td small {{ color: var(--muted); }}
.sub {{ color: var(--accent); padding-left: .6rem; }}
.code {{ border-radius: 10px; overflow: hidden; background: var(--code-bg); min-width: 0; }}
.code-bar {{ display: flex; justify-content: space-between; align-items: center; padding: .45rem .5rem .45rem .9rem; font: 600 .78rem var(--mono); color: #9fc3cf; border-bottom: 1px solid rgba(255,255,255,.08); }}
.code pre {{ margin: 0; padding: .9rem; max-height: 18rem; overflow: auto; }}
.code pre code {{ background: none; border: 0; padding: 0; color: var(--code-fg); font-size: .78rem; white-space: pre; }}
.code.empty p {{ margin: 0; padding: .8rem .9rem; color: #9fc3cf; font-size: .85rem; }}
.copy {{ font: 600 .78rem var(--font); background: #01aec8; color: #fff; border: 0; border-radius: 999px; padding: .35rem .9rem; cursor: pointer; }}
.copy:hover {{ background: #016d7d; }}
.copy.ok {{ background: #2e9d5b; }}
:focus-visible {{ outline: 2px solid #ff9c11; outline-offset: 2px; }}
details.fill {{ border-bottom: 1px solid var(--line); }}
details.fill > summary {{ display: flex; gap: .8rem; align-items: center; padding: .8rem .2rem; }}
.num {{ display: inline-grid; place-items: center; width: 1.6rem; height: 1.6rem; border-radius: 50%; border: 1.5px solid var(--accent); color: var(--accent); font-size: .8rem; font-weight: 600; flex: none; }}
.what {{ color: var(--muted); font-weight: 400; }}
dl {{ margin: 0 0 1rem 2.4rem; display: grid; gap: .55rem; }}
.kv {{ display: grid; grid-template-columns: 12rem 1fr; gap: .2rem 1rem; font-size: .9rem; }}
.kv dt {{ color: var(--muted); }}
.kv dd {{ margin: 0; min-width: 0; overflow-wrap: anywhere; }}
.val {{ background: var(--surface); border-radius: 4px; padding: 0 .3rem; }}
ol.items {{ list-style: none; padding: 0; margin: 0; display: grid; gap: .5rem; }}
ol.items li {{ display: flex; gap: .6rem; }}
ol.items .n {{ font-size: .75rem; font-weight: 600; color: var(--accent); min-width: 1rem; }}
.check {{ list-style: none; padding: 0; margin: 0; display: grid; gap: .55rem; }}
.check li {{ display: flex; gap: .6rem; align-items: flex-start; }}
.check input {{ margin-top: .3rem; accent-color: #01aec8; }}
.settings {{ display: grid; gap: .55rem; }}
@media (max-width: 600px) {{ .kv {{ grid-template-columns: 1fr; }} dl {{ margin-left: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">Flatchr · HubSpot · Usage interne</p>
  <h1>Créer la page Agent IA dans HubSpot</h1>
  <p class="lead">5 modules modifiables, puis une page en brouillon sur le modèle Flex du thème Flatchr (menu et footer du site inclus). Le rendu final est celui de la maquette validée.</p>
  <div class="routes">
    <div class="route main"><h3>Toi, dans le Gestionnaire de design</h3><p>Étapes 1 à 4 ci-dessous. Tu crées chaque module en collant le code, tu ajoutes ses champs, puis tu montes la page.</p></div>
    <div class="route"><h3>Raccourci avec Damien</h3><p>Depuis la branche <code>claude/nifty-fermi-at6wdw</code> du repo, une commande importe les 5 modules avec tous leurs champs et textes : <code class="cp">hs upload hubspot/modules "Agent IA"</code>. Tu passes ensuite directement à l'étape 3.</p></div>
  </div>
</header>

<section>
  <h2><span class="step">1</span>Ouvrir le Gestionnaire de design</h2>
  <ol class="mini">
    <li>Dans HubSpot : <b>Contenu → Outils de conception</b> (Design Manager). Selon ton interface, il peut être sous <b>Marketing → Fichiers et modèles</b>.</li>
    <li>Crée un dossier <code class="cp">Agent IA</code> à la racine : <b>Fichier → Nouveau dossier</b>.</li>
  </ol>
  <p class="callout"><b>À savoir :</b> les noms de menus peuvent varier légèrement selon la langue ou la version de HubSpot. Le principe reste le même.</p>
</section>

<section>
  <h2><span class="step">2</span>Créer les 5 modules</h2>
  <p>Pour chaque module : crée le fichier, colle le code, ajoute les champs, publie le module. Les champs n'ont pas besoin de valeur par défaut : les textes se saisissent à l'étape 3.</p>
  <p class="callout"><b>Le point qui fait tout marcher :</b> le <b>nom HubL</b> de chaque champ doit être identique à celui du tableau, sinon le texte n'apparaît pas. Le menu « Ajouter un champ » demande un <b>type</b> (ex. tape « Texte »), puis tu renseignes le libellé et le nom HubL dans les réglages du champ.</p>
  <p class="callout"><b>Champs répétés :</b> « Exemples de demandes » et « Points clés » sont de simples champs <b>Texte</b> avec l'option <b>Répéter</b> activée. Seuls 2 modules ont de vrais groupes (Démo WhatsApp : messages ; Cartes : cartes) : un groupe ne se crée pas depuis « Ajouter un champ », il se forme en regroupant des champs déjà créés.</p>
  {''.join(mods)}
</section>

<section>
  <h2><span class="step">3</span>Monter la page en brouillon</h2>
  <ol class="mini">
    <li><b>Contenu → Pages du site web → Créer</b>, domaine flatchr.io.</li>
    <li>Modèle : thème <b>Flatchr theme mar2024</b> → <b>Flex</b>. Le menu et le footer du site sont inclus automatiquement.</li>
    <li>Supprime les modules d'exemple présents dans la zone de contenu, s'il y en a.</li>
    <li>Glisse les modules dans cet ordre, puis saisis leurs textes (clique sur un module pour voir quoi saisir) :</li>
  </ol>
  <div>{''.join(content)}</div>
  <div class="settings">
    <p><b>Onglet Paramètres de la page :</b></p>
    <div class="kv"><dt>Nom interne</dt><dd><code class="cp">Agent IA Flatchr — Lancement (brouillon)</code></dd></div>
    <div class="kv"><dt>URL (slug)</dt><dd><code class="cp">agent-ia-recrutement</code></dd></div>
    <div class="kv"><dt>Titre de la page</dt><dd><code class="cp">Agent IA de recrutement pour vos managers terrain | Flatchr</code></dd></div>
    <div class="kv"><dt>Méta-description</dt><dd><code class="cp">Découvrez l'agent IA de recrutement Flatchr : vos managers terrain recrutent depuis WhatsApp, de l'annonce à l'entretien. Disponible le 1er janvier.</code></dd></div>
  </div>
  <p class="callout"><b>Ne clique pas sur Publier.</b> Enregistre et utilise <b>Aperçu</b> : la page reste en brouillon tant que tout n'est pas validé.</p>
</section>

<section>
  <h2><span class="step">4</span>Vérifier avant de publier</h2>
  <ul class="check">
    <li><input type="checkbox" id="c1"><label for="c1">Aperçu ordinateur et mobile : menu et footer du site présents, rien ne déborde.</label></li>
    <li><input type="checkbox" id="c2"><label for="c2">Champ de saisie : écrire une demande, appuyer sur Entrée, un onglet s'ouvre vers l'accès gratuit.</label></li>
    <li><input type="checkbox" id="c3"><label for="c3">Lien d'accès gratuit confirmé (aujourd'hui <code>app.flatchr.io/signup</code>, à vérifier avec Damien), dans le module 1 et le module 6.</label></li>
    <li><input type="checkbox" id="c4"><label for="c4">Mention « Sans carte bancaire » confirmée ou retirée.</label></li>
    <li><input type="checkbox" id="c5"><label for="c5">Lien de la vidéo de vision ajouté dans le module 2 (sinon l'encart « Bientôt disponible » s'affiche).</label></li>
    <li><input type="checkbox" id="c6"><label for="c6">Démo WhatsApp : la conversation se joue en arrivant dessus (puis se relance seule 10 min après). Prénoms et jobboards fictifs validés.</label></li>
    <li><input type="checkbox" id="c7"><label for="c7">Textes relus (bénéfices, étapes), compte à rebours sur la bonne date.</label></li>
  </ul>
  <p class="callout"><b>Si un texte n'apparaît pas :</b> compare le nom HubL du champ avec le tableau. <b>Si un module n'apparaît pas dans l'éditeur de page :</b> vérifie qu'il est utilisable dans les « Pages » et que tu as bien cliqué sur « Publier les modifications » dans le Gestionnaire de design.</p>
</section>
</div>

<script>
function copyText(text, el) {{
  var done = function () {{ el.classList.add('ok'); var t = el.textContent; if (el.tagName === 'BUTTON') el.textContent = 'Copié'; setTimeout(function () {{ el.classList.remove('ok'); if (el.tagName === 'BUTTON') el.textContent = t; }}, 1400); }};
  var fallback = function () {{ var r = document.createRange(); r.selectNodeContents(el.tagName === 'BUTTON' ? el.closest('.code').querySelector('pre code') : el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }};
  try {{ navigator.clipboard.writeText(text).then(done, fallback); }} catch (err) {{ fallback(); }}
}}
document.querySelectorAll('.copy').forEach(function (b) {{ b.addEventListener('click', function () {{ copyText(b.closest('.code').querySelector('pre code').textContent, b); }}); }});
document.querySelectorAll('code.cp').forEach(function (c) {{ c.addEventListener('click', function () {{ copyText(c.textContent, c); }}); }});
document.querySelectorAll('.check input').forEach(function (i) {{
  try {{ i.checked = localStorage.getItem('aia-' + i.id) === '1'; }} catch (err) {{}}
  i.addEventListener('change', function () {{ try {{ localStorage.setItem('aia-' + i.id, i.checked ? '1' : '0'); }} catch (err) {{}} }});
}});
</script>
"""
open(os.path.join(ROOT, "guide-hubspot-agent-ia.html"), "w").write(page)
print("ok", len(page))
