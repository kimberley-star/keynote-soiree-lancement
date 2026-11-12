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
