// Infos clés de l'événement : à modifier ici, elles alimentent le compte à rebours et le lien agenda.
const EVENT = {
  title: "Flatchr — Keynote & soirée de lancement",
  start: "2026-11-05T18:30:00+01:00",
  end: "2026-11-05T23:00:00+01:00",  
  location: "Flatchr, 79 rue Marcel Dassault, 92100 Boulogne-Billancourt, France",
  details: "Keynote, démo et soirée networking avec l'équipe Flatchr. Programme : voir le site de l'événement.",
  rsvpUrl: "" // Lien du formulaire d'inscription (ex. formulaire HubSpot). Vide = bouton pointant vers la section infos.
};

(function () {
  // Lien d'inscription
  document.querySelectorAll("[data-rsvp]").forEach(function (a) {
    if (EVENT.rsvpUrl) { a.href = EVENT.rsvpUrl; a.target = "_blank"; a.rel = "noopener"; }
  });

  // Lien "Ajouter à Google Agenda"
  var toGcal = function (iso) { return new Date(iso).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); };
  var gcal = "https://calendar.google.com/calendar/render?action=TEMPLATE" +
    "&text=" + encodeURIComponent(EVENT.title) +
    "&dates=" + toGcal(EVENT.start) + "/" + toGcal(EVENT.end) +
    "&details=" + encodeURIComponent(EVENT.details) +
    "&location=" + encodeURIComponent(EVENT.location);
  document.querySelectorAll("[data-gcal]").forEach(function (a) {
    a.href = gcal; a.target = "_blank"; a.rel = "noopener";
  });

  // Compte à rebours
  var box = document.querySelector("[data-countdown]");
  if (!box) return;
  var target = new Date(EVENT.start).getTime();
  var cells = {
    d: box.querySelector("[data-d]"), h: box.querySelector("[data-h]"), m: box.querySelector("[data-m]")
  };
  var tick = function () {
    var diff = Math.max(0, target - Date.now());
    if (diff === 0) { box.innerHTML = "<div><b>C'est ce soir</b><span>on vous attend</span></div>"; return; }
    cells.d.textContent = Math.floor(diff / 864e5);
    cells.h.textContent = String(Math.floor(diff / 36e5) % 24).padStart(2, "0");
    cells.m.textContent = String(Math.floor(diff / 6e4) % 60).padStart(2, "0");
  };
  tick();
  setInterval(tick, 30000);
})();
