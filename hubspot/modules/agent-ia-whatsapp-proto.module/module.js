// Le Gestionnaire de fichiers HubSpot sert les .html en texte brut : on lit donc le fichier
// et on l'injecte dans l'iframe (srcdoc). Chargement quand la section approche de l'écran.
(function () {
  var frames = document.querySelectorAll('[data-aip-frame]');
  if (!frames.length) return;

  function candidates(url) {
    var list = [], i = url.indexOf('/hubfs/');
    // Même domaine que le site (www.flatchr.io/hubfs/...) en priorité : pas de blocage CORS
    if (i > -1 && /^https?:/.test(url)) list.push(location.origin + url.slice(i));
    list.push(url);
    return list;
  }
  function load(frame) {
    if (frame.dataset.loaded) return;
    frame.dataset.loaded = '1';
    var urls = candidates(frame.getAttribute('data-src'));
    (function next(k) {
      if (k >= urls.length) { frame.closest('.aip-stage').classList.add('aip-failed'); return; }
      fetch(urls[k], { credentials: 'omit' })
        .then(function (r) { if (!r.ok) throw 0; return r.text(); })
        .then(function (html) {
          if (!/<html|<!doctype/i.test(html.slice(0, 500))) throw 0;
          frame.srcdoc = html;
          // Filet de sécurité : on affiche le prototype même s'il ne signale pas qu'il est prêt
          setTimeout(function () { frame.classList.add('is-ready'); }, 5000);
        })
        .catch(function () { next(k + 1); });
    })(0);
  }
  frames.forEach(function (f) {
    if (!('IntersectionObserver' in window)) return load(f);
    var io = new IntersectionObserver(function (e) { if (e[0].isIntersecting) { io.disconnect(); load(f); } }, { rootMargin: '600px 0px' });
    io.observe(f);
  });

  // Le prototype envoie sa hauteur : l'iframe s'ajuste (pas de barre de défilement) puis apparaît
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (!d || d.type !== 'flatchr-proto-height' || typeof d.height !== 'number') return;
    frames.forEach(function (f) {
      if (f.contentWindow !== e.source) return;
      f.style.height = Math.max(300, Math.min(2000, Math.round(d.height) + 4)) + 'px';
      // Le prototype est prêt et mis en forme : on l'affiche en fondu (pas d'étape intermédiaire visible)
      requestAnimationFrame(function () { f.classList.add('is-ready'); });
    });
  });
})();
