// Champ de saisie : ouvre l'accès gratuit dans un nouvel onglet avec la demande en ?prompt=
document.querySelectorAll('.aia-hero').forEach(function (h) {
  var url = h.dataset.url, f = h.querySelector('[data-aia-form]'), t = f.querySelector('textarea');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = t.value.trim();
    if (!q) { t.focus(); return; }
    window.open(url + (url.indexOf('?') < 0 ? '?' : '&') + 'prompt=' + encodeURIComponent(q), '_blank', 'noopener');
  });
  t.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); f.requestSubmit(); }
  });
  h.querySelectorAll('.aia-chip').forEach(function (c) {
    c.addEventListener('click', function () { t.value = c.textContent; t.focus(); });
  });
});

// Mascotte : arrive en volant, se pose, salue, puis clin d'œil / salut de temps en temps
document.querySelectorAll('.aia-hero [data-aia-mascot]').forEach(function (m) {
  var poses = { idle: m.querySelector('.aia-m-idle'), wave: m.querySelector('.aia-m-wave'), wink: m.querySelector('.aia-m-wink') };
  function show(name, ms) {
    if (!poses[name]) return;
    Object.keys(poses).forEach(function (k) { if (poses[k]) poses[k].classList.toggle('is-on', k === name); });
    if (ms) setTimeout(function () { show('idle'); }, ms);
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  function loop() {
    var n = 0;
    setInterval(function () { n++; show(n % 2 ? 'wink' : 'wave', n % 2 ? 900 : 1500); }, 6000);
  }
  var fly = m.querySelector('.aia-m-fly');
  if (fly) {
    m.classList.add('is-flying');
    setTimeout(function () { m.classList.remove('is-flying'); show('wave', 1600); loop(); }, 1300);
  } else { show('wave', 1600); loop(); }
});
