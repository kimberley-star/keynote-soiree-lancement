// Mascotte « coucou » : la tête est en place dès le chargement et regarde en l'air.
// Sur ordinateur, elle suit la souris du regard ; sur mobile, elle regarde autour d'elle toute seule.
document.querySelectorAll('[data-flp]').forEach(function (sec) {
  var head = sec.querySelector('.flp-head');
  if (!head) return;
  var poses = {};
  head.querySelectorAll('.flp-p').forEach(function (img) { poses[img.dataset.pose] = img; });
  var rest = poses.up ? 'up' : 'face', current = rest;
  function show(name) {
    if (!poses[name] || name === current) return;
    current = name;
    Object.keys(poses).forEach(function (k) { poses[k].classList.toggle('is-on', k === name); });
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches, idle = null, visible = false, started = false;
  new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
    if (visible && !fine && !started) {
      started = true;
      var seq = ['left', 'face', 'right', 'face', 'up'].filter(function (p) { return poses[p]; }), i = 0;
      setInterval(function () { if (visible) show(seq[i++ % seq.length]); }, 1600);
    }
  }, { threshold: 0.3 }).observe(sec);
  if (fine) {
    var raf = 0;
    document.addEventListener('mousemove', function (e) {
      if (!visible || raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = head.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        var dx = e.clientX - cx, dy = e.clientY - cy;
        if (dy < -r.height * 1.5 && Math.abs(dx) < r.width * 1.2) show('up');
        else if (dx < -r.width * 0.45) show('left');
        else if (dx > r.width * 0.45) show('right');
        else show('face');
        clearTimeout(idle);
        idle = setTimeout(function () { show(rest); }, 3000);
      });
    });
  }
});

// Mode « regard » : chaque pupille vise précisément le pointeur (angle + distance), avec un léger amorti
document.querySelectorAll('[data-flp-gaze]').forEach(function (head) {
  var sec = head.closest('[data-flp]');
  var eyes = Array.prototype.map.call(head.querySelectorAll('.flp-eye'), function (el) {
    return { el: el, pupil: el.querySelector('.flp-pupil'), cur: { x: 0, y: -0.45 }, tgt: { x: 0, y: -0.45 } };
  });
  var rest = { x: 0, y: -0.45 }, visible = true, idle = null, mouse = null, hx = 0;
  function aim() {
    eyes.forEach(function (e) {
      if (!mouse) { e.tgt.x = rest.x; e.tgt.y = rest.y; return; }
      var r = e.el.getBoundingClientRect(), dx = mouse.x - (r.left + r.width / 2), dy = mouse.y - (r.top + r.height / 2);
      var d = Math.sqrt(dx * dx + dy * dy) || 1, k = d / (d + r.width * 0.6); // proche = petit écart, loin = bord du verre
      e.tgt.x = dx / d * k; e.tgt.y = dy / d * k;
    });
  }
  function apply() {
    var sx = 0;
    eyes.forEach(function (e) {
      var w = e.el.offsetWidth, h = e.el.offsetHeight;
      e.pupil.style.setProperty('--px', (e.cur.x * w * 0.24).toFixed(1) + 'px');
      e.pupil.style.setProperty('--py', (e.cur.y * h * 0.26).toFixed(1) + 'px');
      sx += e.cur.x;
    });
    hx += (sx / eyes.length - hx) * 0.08;
    head.style.setProperty('--hx', (hx * 6).toFixed(2) + 'px');
    head.style.setProperty('--hr', (hx * 3).toFixed(2) + 'deg');
  }
  apply();
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  head.querySelectorAll('.flp-pupil').forEach(function (p) { p.style.transition = 'none'; });
  function tick() {
    if (visible) {
      eyes.forEach(function (e) { e.cur.x += (e.tgt.x - e.cur.x) * 0.3; e.cur.y += (e.tgt.y - e.cur.y) * 0.3; });
      apply();
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }, { threshold: 0 }).observe(sec);
  // Clignement des yeux toutes les 3 à 6 secondes
  (function blink() {
    setTimeout(function () {
      eyes.forEach(function (e) { e.pupil.style.setProperty('--blink', '0.08'); });
      setTimeout(function () { eyes.forEach(function (e) { e.pupil.style.setProperty('--blink', '1'); }); blink(); }, 130);
    }, 3000 + Math.random() * 3000);
  })();
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var onMove = function (x, y) {
      mouse = { x: x, y: y }; aim();
      clearTimeout(idle); idle = setTimeout(function () { mouse = null; aim(); }, 4000);
    };
    document.addEventListener('mousemove', function (e) { onMove(e.clientX, e.clientY); });
    window.addEventListener('scroll', function () { if (mouse) aim(); }, { passive: true });
    document.addEventListener('mouseleave', function () { mouse = null; aim(); });
  } else {
    // Mobile : le regard se promène tout seul
    var spots = [[-0.9, 0.1], [0, -0.8], [0.9, 0], [0.4, -0.6], [-0.5, -0.5], [0, 0.2]], k = 0;
    setInterval(function () {
      if (!visible) return;
      var s = spots[k++ % spots.length];
      eyes.forEach(function (e) { e.tgt.x = s[0]; e.tgt.y = s[1]; });
    }, 1700);
  }
});
