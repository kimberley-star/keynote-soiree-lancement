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
