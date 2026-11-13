// Le prototype envoie sa hauteur : l'iframe s'ajuste pour éviter toute barre de défilement
(function () {
  var frames = document.querySelectorAll('[data-aip-frame]');
  if (!frames.length) return;
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (!d || d.type !== 'flatchr-proto-height' || typeof d.height !== 'number') return;
    frames.forEach(function (f) {
      if (f.contentWindow === e.source) f.style.height = Math.max(300, Math.min(2000, Math.round(d.height) + 4)) + 'px';
    });
  });
})();
