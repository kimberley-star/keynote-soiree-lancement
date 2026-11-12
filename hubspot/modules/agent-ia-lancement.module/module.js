// Compte à rebours jusqu'à la date de lancement (format 2027-01-01T00:00:00+01:00)
document.querySelectorAll('.aia-launch-sec .aia-countdown').forEach(function (cd) {
  var target = new Date(cd.dataset.date).getTime();
  if (isNaN(target)) { cd.hidden = true; return; }
  function tick() {
    var s = Math.max(0, Math.floor((target - Date.now()) / 1000));
    cd.querySelector('[data-d]').textContent = Math.floor(s / 86400);
    cd.querySelector('[data-h]').textContent = Math.floor(s % 86400 / 3600);
    cd.querySelector('[data-m]').textContent = Math.floor(s % 3600 / 60);
  }
  tick(); setInterval(tick, 30000);
});

// Mascotte : arrive en volant quand le bloc devient visible, salue, puis clin d'œil / salut de temps en temps
document.querySelectorAll('.aia-launch-sec [data-aia-mascot]').forEach(function (m) {
  var poses = { idle: m.querySelector('.aia-m-idle'), wave: m.querySelector('.aia-m-wave'), wink: m.querySelector('.aia-m-wink') };
  function show(name, ms) {
    if (!poses[name]) return;
    Object.keys(poses).forEach(function (k) { if (poses[k]) poses[k].classList.toggle('is-on', k === name); });
    if (ms) setTimeout(function () { show('idle'); }, ms);
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  function loop() {
    var n = 0;
    setInterval(function () { n++; show(n % 2 ? 'wink' : 'wave', n % 2 ? 900 : 1500); }, 6000);
  }
  var fly = m.querySelector('.aia-m-fly');
  if (fly) m.classList.add('is-waiting');
  var obs = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return;
    obs.disconnect();
    if (fly) {
      m.classList.remove('is-waiting'); m.classList.add('is-flying');
      setTimeout(function () { m.classList.remove('is-flying'); show('wave', 1600); loop(); }, 1300);
    } else { show('wave', 1600); loop(); }
  }, { threshold: 0.4 });
  obs.observe(m);
});
