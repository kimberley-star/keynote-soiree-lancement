// Infos clés de l'événement : à modifier ici, elles alimentent le compte à rebours et le lien agenda.
const EVENT = {
  title: "Flatchr — Soirée de lancement",
  start: "2026-11-05T18:30:00+01:00",
  end: "2026-11-05T23:00:00+01:00",  
  location: "Flatchr, 79 rue Marcel Dassault, 92100 Boulogne-Billancourt, France",
  details: "Découverte de la nouvelle version de l'IA agentique Flatchr et soirée pour célébrer nos 10 ans : roadmap agentique, DJ set, traiteur italien et invité surprise.",
  rsvpUrl: "https://survey.refiner.io/mqggze-m46jk0", // Questionnaire d'inscription Refiner : tous les boutons « Je confirme ma venue » y mènent.
  videoUrl: "https://www.youtube.com/shorts/XbYt7-mBWto" // Lien YouTube (vidéo, Short), Vimeo, Google Drive (partagé « Tous les utilisateurs disposant du lien ») ou fichier .mp4. Vide = encart "Vidéo à venir".
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

  // Encart vidéo
  var frame = document.querySelector("[data-video]");
  if (frame && EVENT.videoUrl) {
    var url = EVENT.videoUrl, yt = url.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/), vimeo = url.match(/vimeo\.com\/(?:video\/)?(\d+)/), drive = url.match(/drive\.google\.com\/file\/d\/([\w-]+)/);
    if (/\.(mp4|webm)(\?|$)/i.test(url)) {
      frame.innerHTML = '<video controls playsinline autoplay muted loop src="' + url + '"></video>';
    } else if (yt || vimeo || drive) {
      // Lecture automatique : les navigateurs ne l'autorisent qu'en muet (le visiteur active le son d'un clic)
      var src = yt ? "https://www.youtube-nocookie.com/embed/" + yt[1] + "?rel=0&autoplay=1&mute=1&playsinline=1&loop=1&playlist=" + yt[1]
        : vimeo ? "https://player.vimeo.com/video/" + vimeo[1] + "?autoplay=1&muted=1&loop=1"
        : "https://drive.google.com/file/d/" + drive[1] + "/preview";
      frame.innerHTML = '<iframe src="' + src + '" title="Vidéo de présentation de la soirée" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>';
    }
  }

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
