// Vidéo : miniature + bouton lecture, la vidéo (YouTube, Vimeo ou .mp4) ne se charge qu'au clic
document.querySelectorAll('.flv .flv-player').forEach(function (box) {
  var url = (box.dataset.url || '').trim(), btn = box.querySelector('.flv-thumb');
  if (!url || !btn) return;
  var yt = url.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/), vimeo = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
  // Pas de miniature choisie : on reprend celle de YouTube
  if (yt && !btn.querySelector('img')) {
    var img = document.createElement('img');
    img.src = 'https://i.ytimg.com/vi/' + yt[1] + '/hqdefault.jpg'; img.alt = ''; img.loading = 'lazy';
    btn.insertBefore(img, btn.firstChild);
  }
  btn.addEventListener('click', function () {
    var title = box.dataset.title || 'Vidéo';
    if (/\.(mp4|webm)(\?|$)/i.test(url)) {
      box.innerHTML = '<video controls autoplay playsinline src="' + url + '"></video>';
    } else if (yt || vimeo) {
      var src = yt ? 'https://www.youtube-nocookie.com/embed/' + yt[1] + '?rel=0&autoplay=1' : 'https://player.vimeo.com/video/' + vimeo[1] + '?autoplay=1';
      var f = document.createElement('iframe');
      f.src = src; f.title = title; f.allow = 'autoplay; encrypted-media; fullscreen; picture-in-picture'; f.allowFullscreen = true;
      box.innerHTML = ''; box.appendChild(f);
    } else {
      window.open(url, '_blank', 'noopener');
    }
  });
});
