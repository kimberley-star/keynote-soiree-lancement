"""Aperçu de la page agent IA : nos modules + imitation des modules du thème (zig-zag, Découvrez la suite, FAQ).

Usage : python3 hubspot/tools/build_preview.py <fichier de sortie.html> [--theme-css chemin/theme.css]
Le fichier produit est au format artifact (sans <html>/<head>) ; --theme-css ajoute le CSS réel du thème pour tester les conflits.
"""
import sys, os, re, io, base64, html as H, argparse
import jinja2
from PIL import Image

TOOLS = os.path.dirname(os.path.abspath(__file__))
HS = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
from spec import MODULES, STEPS, ZIGZAG, DISCOVER, FAQ, FAQ_TITLE

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--theme-css")
args = ap.parse_args()

spec = {s: f for s, _, _, f in MODULES}
env = jinja2.Environment(undefined=jinja2.ChainableUndefined)


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


decor = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 500"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#01aec8" stop-opacity=".9"/><stop offset="1" stop-color="#dbfaff" stop-opacity=".3"/></linearGradient></defs>'
         '<path d="M0 500 C80 380 260 420 380 300 C470 210 560 230 600 180 L600 260 C540 300 470 290 400 360 C300 460 140 430 60 500Z" fill="url(#g)"/>'
         '<path d="M0 420 C120 330 230 360 330 250 C400 170 480 120 560 110 L560 160 C470 180 420 230 360 300 C250 420 120 380 0 480Z" fill="url(#g)" opacity=".7"/></svg>')
decor_src = "data:image/svg+xml;base64," + base64.b64encode(decor.encode()).decode()


def mod(slug, over=None, i=0):
    m = {f["name"]: f.get("default") for f in spec[slug]}
    m.update(over or {})
    if slug == "flatchr-mascotte-coucou":
        for k, f in [("peek_face", "face"), ("peek_left", "gauche"), ("peek_right", "droite"), ("peek_up", "haut")]:
            m[k] = {"src": b64(f"{HS}/visuels/mascotte-coucou-{f}.webp", "image/webp")}
    if slug == "agent-ia-whatsapp":
        m["mascot_image"] = {"src": b64(f"{HS}/visuels/mascotte-salut.webp", "image/webp")}
    if slug == "agent-ia-lancement":
        m["mascot_idle"] = {"src": b64(f"{HS}/visuels/mascotte-neutre.webp", "image/webp")}
    if slug == "agent-ia-hero":
        for k, f in [("mascot_idle", "neutre"), ("mascot_wave", "salut"), ("mascot_wink", "clin-oeil"), ("mascot_fly", "vol")]:
            m[k] = {"src": b64(f"{HS}/visuels/mascotte-{f}.webp", "image/webp")}
    return env.from_string(open(f"{HS}/modules/{slug}.module/module.html").read()).render(module=m, name=f"m{i}")


def zigzag():
    rows = []
    for k, z in enumerate(ZIGZAG):
        im = Image.open(f"{HS}/visuels/{z['image']}").convert("RGBA")
        im.thumbnail((760, 760))
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=82)
        img = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
        cap = "".join(f"<p>{H.escape(p)}</p>" for p in z["caption"])
        cta = f'<div class="cta"><a class="terciary-arrow" href="{z["cta_link"]}" target="_blank" rel="noopener">En savoir plus</a></div>' if z["cta_link"] else ""
        rows.append(f'<div class="zz-col{" swap-col" if k % 2 else ""}"><div class="image"><img src="{img}" alt="{H.escape(z["title"])}" loading="lazy"></div>'
                    f'<div class="content"><h2>{H.escape(z["title"])}</h2><div class="caption">{cap}</div>{cta}</div></div>')
    return f'<section class="zig-zag-sec"><div class="zz-container">{"".join(rows)}</div></section>'


def discover():
    cards = "".join(
        f'<div class="tcsc-col"><a href="{c["cta_link"]}" target="_blank" rel="noopener"><div class="col-box"><div class="icon-title"><div class="icon">'
        f'<img src="{b64(f"{TOOLS}/assets/{c["icon"]}", "image/svg+xml")}" alt="" width="48" height="48"></div><h3>{H.escape(c["title"])}</h3></div>'
        f'<div class="text"><p>{H.escape(c["text"])}</p></div><div class="cta"><span class="terciary-arrow">En savoir plus</span></div></div></a></div>'
        for c in DISCOVER["cards"])
    return f'<section class="tcsc-sec"><div class="zz-container"><div class="main-title"><h2>{DISCOVER["title"]}</h2></div><div class="tcsc-wrap">{cards}</div></div></section>'


def faq():
    items = "".join(f'<details class="faq-item"><summary class="q">{H.escape(q)}</summary><div class="a">{"".join(f"<p>{H.escape(x)}</p>" for x in a)}</div></details>' for q, a in FAQ)
    return f'<section class="fqtc-sec"><div class="zz-container"><div class="faq-column"><div class="title"><h2>{H.escape(FAQ_TITLE)}</h2></div><div class="faq">{items}</div></div></div></section>'


order = [mod("agent-ia-hero", i=0), mod("flatchr-video", i=1), mod("agent-ia-whatsapp", i=2), zigzag(),
         mod("agent-ia-cartes", i=3), mod("agent-ia-cartes", STEPS, i=4), mod("agent-ia-confiance", i=6), discover(),
         mod("agent-ia-lancement", i=5), faq(), mod("flatchr-mascotte-coucou", i=7)]
css = "".join(open(f"{HS}/modules/{s}.module/module.css").read() for s in spec)
js = "".join(open(f"{HS}/modules/{s}.module/module.js").read() for s in spec)
# Dans l'aperçu claude.ai, window.open est bloqué : on passe par un vrai lien
js = js.replace("window.open(url + (url.indexOf('?') < 0 ? '?' : '&') + 'prompt=' + encodeURIComponent(q), '_blank', 'noopener');",
                "var l = document.createElement('a'); l.href = url + (url.indexOf('?') < 0 ? '?' : '&') + 'prompt=' + encodeURIComponent(q); l.target = '_blank'; l.rel = 'noopener'; document.body.appendChild(l); l.click(); l.remove();")
assert "l.click()" in js

logo = b64(f"{TOOLS}/assets/logo.png", "image/png")
header = (f'<header class="fl-header"><div class="fl-wrap"><a class="fl-logo" href="https://www.flatchr.io/" target="_blank" rel="noopener"><img src="{logo}" alt="Flatchr" width="151" height="46"></a>'
          '<nav class="fl-nav" aria-label="Menu du site"><span>Solutions ▾</span><span>Fonctionnalités ▾</span><span>Clients</span><span>Tarifs</span><span>Ressources ▾</span></nav>'
          '<div class="fl-actions"><a class="fl-ghost" href="https://app.flatchr.io/login" target="_blank" rel="noopener">Se connecter</a><a class="fl-cta" href="https://www.flatchr.io/demo" target="_blank" rel="noopener">Demander une démo</a></div></div></header>')
footer = '<footer class="fl-footer"><div class="fl-wrap"><span>© Flatchr 2026 · Le logiciel de recrutement des managers de terrain</span><span>Pied de page global du site (simulé)</span></div></footer>'
site_css = """
:root{color-scheme:light}
body{margin:0;background:#fff;color:#182534;font-family:Poppins,"Segoe UI",system-ui,sans-serif}
.fl-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:#fff;border-bottom:1px solid #dee5ed}
.fl-wrap{max-width:76rem;margin:0 auto;padding:.75rem 16px;display:flex;align-items:center;justify-content:space-between;gap:1.5rem}
.fl-logo img{display:block;height:34px;width:auto}
.fl-nav{display:flex;gap:1.6rem;font-weight:600;font-size:.95rem}
.fl-actions{display:flex;gap:.6rem}
.fl-ghost,.fl-cta{font:600 .9rem Poppins,sans-serif;padding:.6rem 1.1rem;border-radius:8px;text-decoration:none;white-space:nowrap}
.fl-ghost{border:1.5px solid #01aec8;color:#019bb2}.fl-cta{background:#01aec8;color:#fff}
.fl-footer{background:#182534;color:#c7d2dd;font-size:.85rem}.fl-footer .fl-wrap{padding:1.6rem 16px;flex-wrap:wrap}
@media (max-width:980px){.fl-nav{display:none}}
@media (max-width:520px){.fl-ghost{display:none}.fl-cta{padding:.55rem .8rem;font-size:.8rem}}
/* Imitation des modules du thème : zig-zag, « Découvrez la suite », FAQ */
.zz-container{max-width:72rem;margin:0 auto;padding:0 clamp(1rem,4vw,2.5rem)}
.zig-zag-sec{padding:clamp(3rem,7vw,5rem) 0;background:#fff}
.zig-zag-sec .zz-col{display:flex;align-items:center;justify-content:space-between;gap:clamp(2rem,6vw,5rem);padding:clamp(1.5rem,4vw,2.5rem) 0}
.zig-zag-sec .zz-col.swap-col{flex-direction:row-reverse}
.zig-zag-sec .image{flex:1 1 50%;min-width:0;display:flex}
.zig-zag-sec .image img{width:100%;height:auto;max-height:480px;object-fit:contain;border-radius:32px}
.zig-zag-sec .content{flex:1 1 42%;min-width:0;display:grid;gap:1.25rem}
.zig-zag-sec h2{font-size:clamp(1.6rem,3.2vw,2.2rem);font-weight:700;line-height:1.2;margin:0;text-wrap:balance}
.zig-zag-sec .caption p{margin:0 0 1rem;color:#182534;line-height:1.65}
.zig-zag-sec .caption p:last-child{margin:0}
.terciary-arrow{font-weight:600;color:#019bb2;text-decoration:none}
.terciary-arrow:after{content:" →"}
.terciary-arrow:hover{color:#016d7d}
@media (max-width:860px){.zig-zag-sec .zz-col,.zig-zag-sec .zz-col.swap-col{flex-direction:column;align-items:stretch}}
.tcsc-sec{padding:2.5rem 0 5rem;background:#fff}
.tcsc-sec .main-title h2{font-size:1.5rem;line-height:2rem;text-align:center;margin:0 0 1.5rem}
.tcsc-sec .tcsc-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem}
.tcsc-sec .tcsc-col{border:1px solid #dee5ed;border-radius:12px;transition:box-shadow .3s}
.tcsc-sec .tcsc-col:hover{box-shadow:0 5px 5px rgba(43,67,94,.06)}
.tcsc-sec .tcsc-col a{display:block;height:100%;color:inherit;text-decoration:none}
.tcsc-sec .col-box{box-sizing:border-box;display:flex;flex-direction:column;gap:1rem;padding:1.5rem;height:100%}
.tcsc-sec .icon img{width:48px;height:48px}
.tcsc-sec h3{font-size:1.15rem;font-weight:700;margin:.75rem 0 0}
.tcsc-sec .text{flex:1}.tcsc-sec .text p{margin:0;font-weight:300}
.fqtc-sec{padding:clamp(3rem,7vw,4.5rem) 0 clamp(3.5rem,8vw,5rem);background:#fff}
.fqtc-sec .faq-column{max-width:56rem;margin:0 auto}
.fqtc-sec .title h2{font-size:clamp(1.6rem,3.2vw,2.2rem);font-weight:700;text-align:center;margin:0 0 2rem;text-wrap:balance}
.fqtc-sec .faq-item{border-top:1px solid #dee5ed}.fqtc-sec .faq-item:last-child{border-bottom:1px solid #dee5ed}
.fqtc-sec .q{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1rem clamp(.5rem,2vw,2rem);font-size:clamp(1rem,1.6vw,1.15rem);font-weight:700;color:#182534}
.fqtc-sec .q::-webkit-details-marker{display:none}
.fqtc-sec .q:after{content:"";flex:none;width:12px;height:12px;border-right:2px solid #182534;border-bottom:2px solid #182534;transform:rotate(45deg);transition:transform .2s;margin-top:-6px}
.fqtc-sec details[open] .q:after{transform:rotate(-135deg);margin-top:6px}
.fqtc-sec .a{padding:0 clamp(.5rem,2vw,2rem) 1.25rem;color:#182534;line-height:1.65}
.fqtc-sec .a p{margin:0 0 .8rem}.fqtc-sec .a p:last-child{margin:0}
"""
theme = f"<style>{open(args.theme_css).read()}</style>" if args.theme_css else ""
page = f"""<title>Agent IA Flatchr</title>
<meta name="description" content="Aperçu de la page agent IA de recrutement Flatchr.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap">
{theme}<style>{site_css}{css}</style>
{header}{"".join(order)}{footer}
<script>{js}</script>"""
open(args.out, "w").write(page)
print("ok", len(page))
