"""Crée la version « vitrine » du prototype WhatsApp de l'équipe produit, à intégrer en iframe.

Usage : python3 tools/build_proto_vitrine.py <prototype.html> <sortie.html>
Le fichier d'origine n'est pas modifié : on ajoute seulement un bloc <style> + <script> dans le <head> qui
- masque les éléments internes (titre « Proto cliquable », badge MEP, « Recommencer », bloc « Si diffuser… », consigne),
- rend le fond transparent et compacte les onglets de scénarios,
- réduit le téléphone sur les écrans étroits,
- envoie sa hauteur à la page HubSpot pour que l'iframe s'ajuste toute seule.
"""
import sys

INJECT = r"""
<!-- Flatchr : mode vitrine (ajouté pour l'intégration HubSpot) -->
<style id="flatchr-vitrine-src">
  html, body { background: transparent !important; min-height: 0 !important; display: block !important; overflow: hidden !important; }
  #__bundler_thumbnail { background: transparent !important; }
  #__bundler_loading { display: none !important; }
  .sc-host > div { min-height: 0 !important; padding: 4px 8px 48px !important; background: transparent !important; gap: 16px !important; }
  .flv-hide { display: none !important; }
  .flv-tabs > div { box-shadow: none !important; padding: 6px !important; gap: 4px !important; }
  .flv-tabs button { height: 30px !important; padding: 0 11px !important; font-size: 13px !important; }
</style>
<script>
(function () {
  var last = 0, CSS = '<style id="flatchr-vitrine">' + document.getElementById('flatchr-vitrine-src').textContent + '</style>';
  function tidy() {
    var wrap = document.querySelector('.sc-host > div');
    if (!wrap) return;
    // Les styles de la page sont parfois réinjectés au démarrage : on force aussi en ligne
    if (!document.getElementById('flatchr-vitrine')) document.head.insertAdjacentHTML('beforeend', CSS);
    wrap.style.setProperty('min-height', '0', 'important');
    wrap.style.setProperty('padding', '4px 8px 48px', 'important');
    wrap.style.setProperty('background', 'transparent', 'important');
    Array.prototype.forEach.call(wrap.children, function (el) {
      var t = (el.innerText || '').trim();
      if (el.querySelector('h1') || /^SI\s*«/i.test(t) || el.tagName === 'P') el.classList.add('flv-hide');
      else if (el.querySelectorAll('button').length > 3 && !el.querySelector('input')) el.classList.add('flv-tabs');
      else if (el.querySelector('input')) {
        // Le téléphone : réduit si l'iframe est plus étroite que lui
        var w = el.offsetWidth || 372, k = Math.min(1, (window.innerWidth - 16) / w);
        el.style.zoom = k < 1 ? k.toFixed(3) : '';
      }
    });
    var h = Math.ceil(wrap.getBoundingClientRect().height);
    if (h && Math.abs(h - last) > 2 && window.parent !== window) {
      last = h;
      window.parent.postMessage({ type: 'flatchr-proto-height', height: h }, '*');
    }
  }
  var mo = new MutationObserver(function () { requestAnimationFrame(tidy); });
  document.addEventListener('DOMContentLoaded', function () { mo.observe(document.body, { childList: true, subtree: true }); tidy(); });
  window.addEventListener('resize', tidy);
  setInterval(tidy, 1000);
})();
</script>
"""

src, out = sys.argv[1], sys.argv[2]
html = open(src, encoding="utf-8").read()
assert html.count("</head>") >= 1 and "flatchr-vitrine" not in html
html = html.replace("</head>", INJECT + "</head>", 1)
open(out, "w", encoding="utf-8").write(html)
print("ok", len(html))
