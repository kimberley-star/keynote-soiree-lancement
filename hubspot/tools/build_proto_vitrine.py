"""Crée la version « vitrine » du prototype WhatsApp de l'équipe produit, à intégrer en iframe.

Usage : python3 tools/build_proto_vitrine.py <prototype.html> <sortie.html>
Le fichier d'origine n'est pas modifié : on ajoute seulement un bloc <style> + <script> dans le <head> qui
- masque les éléments internes (titre « Proto cliquable », badge MEP, « Recommencer », bloc « Si diffuser… », consigne),
- rend le fond blanc (comme la section HubSpot, pour éviter tout effet d'encadré) et compacte les onglets de scénarios et les place sous le téléphone,
- réduit le téléphone sur les écrans étroits,
- envoie sa hauteur à la page HubSpot pour que l'iframe s'ajuste toute seule.
"""
import sys

INJECT = r"""
<!-- Flatchr : mode vitrine (ajouté pour l'intégration HubSpot) -->
<style id="flatchr-vitrine-src">
  /* Tout est géré en CSS pour éviter les sauts : un élément interne n'apparaît jamais, même une fraction de seconde */
  html, body { background: #fff !important; color-scheme: light; min-height: 0 !important; display: block !important; overflow: hidden !important; }
  html.flv-wait body { visibility: hidden; }
  #__bundler_thumbnail, #__bundler_loading { display: none !important; }
  .sc-host > div { min-height: 0 !important; padding: 4px 8px 48px !important; background: #fff !important; gap: 16px !important;
                   display: flex !important; flex-direction: column !important; align-items: center !important; }
  /* On ne garde que le téléphone (il contient le champ de saisie) et la barre de scénarios (4 boutons ou plus) */
  .sc-host > div > :not(:has(input)):not(:has(button ~ button ~ button ~ button)) { display: none !important; }
  .sc-host > div > :has(input) { order: 1 !important; }
  .sc-host > div > :not(:has(input)):has(button ~ button ~ button ~ button) { order: 2 !important; }
  .sc-host > div > :not(:has(input)):has(button ~ button ~ button ~ button) > div { box-shadow: none !important; padding: 6px !important; gap: 4px !important; }
  .sc-host > div > :not(:has(input)):has(button ~ button ~ button ~ button) button { height: 30px !important; padding: 0 11px !important; font-size: 13px !important; }
</style>
<script>
(function () {
  var last = 0, CSS = '<style id="flatchr-vitrine">' + document.getElementById('flatchr-vitrine-src').textContent + '</style>';
  document.documentElement.classList.add('flv-wait');
  function wrapEl() { return document.querySelector('.sc-host > div'); }
  function fit() {
    // Le téléphone est réduit si l'iframe est plus étroite que lui (largeur de référence fixe : pas d'effet yoyo)
    var wrap = wrapEl(); if (!wrap || window.innerWidth < 100) return;
    Array.prototype.forEach.call(wrap.children, function (el) {
      if (!el.querySelector('input')) return;
      var base = parseFloat(el.style.width) || 372, k = Math.min(1, (window.innerWidth - 16) / base);
      var z = k < 1 ? k.toFixed(3) : '';
      if (el.style.zoom !== z) el.style.zoom = z;
    });
  }
  function report() {
    var wrap = wrapEl(); if (!wrap) return;
    var h = Math.ceil(wrap.getBoundingClientRect().height);
    if (h > 200 && Math.abs(h - last) > 2 && window.parent !== window) {
      last = h;
      window.parent.postMessage({ type: 'flatchr-proto-height', height: h }, '*');
    }
  }
  function tick() {
    var wrap = wrapEl(); if (!wrap) return;
    // Les styles de la page sont parfois réinjectés au démarrage : on les remet si besoin
    if (!document.getElementById('flatchr-vitrine')) document.head.insertAdjacentHTML('beforeend', CSS);
    fit(); report();
    // Le prototype remplace le document au démarrage : on cible toujours le document courant
    var root = document.documentElement;
    if (root.classList.contains('flv-wait')) {
      var show = function () { fit(); report(); root.classList.remove('flv-wait'); };
      (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () { requestAnimationFrame(show); });
    }
  }
  var pending = false;
  var mo = new MutationObserver(function () { if (!pending) { pending = true; requestAnimationFrame(function () { pending = false; tick(); }); } });
  mo.observe(document, { childList: true, subtree: true });
  document.addEventListener('DOMContentLoaded', tick);
  window.addEventListener('resize', function () { fit(); report(); });
  setTimeout(function () { document.documentElement.classList.remove('flv-wait'); }, 4000); // filet de sécurité
  setInterval(tick, 2000);
})();
</script>
"""

src, out = sys.argv[1], sys.argv[2]
html = open(src, encoding="utf-8").read()
assert html.count("</head>") >= 1 and "flatchr-vitrine" not in html
html = html.replace("</head>", INJECT + "</head>", 1)
open(out, "w", encoding="utf-8").write(html)
print("ok", len(html))
