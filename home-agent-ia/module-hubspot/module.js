/* Module « Agent IA – encart home » · Flatchr : onglets + démo animée */
(function(){
  function init(root){
    if(root.dataset.faReady) return; root.dataset.faReady='1';
    var tabs=[].slice.call(root.querySelectorAll('.fa-tab'));
    var scenes=[].slice.call(root.querySelectorAll('template.fa-scene'));
    var demo=root.querySelector('.fa-demo'), q=root.querySelector('[data-q]'), a=root.querySelector('[data-a]');
    if(!tabs.length||!demo) return;
    var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var DUR=parseInt(root.getAttribute('data-dur'),10)||7000, cur=0, timer=null, typingT=null, paused=false, visible=false;

    function show(i, focus){
      cur=i;
      tabs.forEach(function(t,k){ var on=k===i; t.setAttribute('aria-selected',on); t.tabIndex=on?0:-1; });
      demo.setAttribute('aria-labelledby',tabs[i].id);
      if(focus) tabs[i].focus();
      var sc=scenes[i]; if(!sc) return;
      q.textContent=sc.getAttribute('data-q')||'';
      clearTimeout(typingT);
      if(reduce){ a.innerHTML=sc.innerHTML; return; }
      demo.classList.add('is-typing'); a.innerHTML='';
      typingT=setTimeout(function(){ a.innerHTML=sc.innerHTML; demo.classList.remove('is-typing'); },900);
    }
    function schedule(){
      clearTimeout(timer);
      if(reduce||paused||!visible||tabs.length<2) return;
      timer=setTimeout(function(){ show((cur+1)%tabs.length); schedule(); },DUR);
    }
    function setPaused(p){ paused=p; root.classList.toggle('is-paused',p); schedule(); }

    root.style.setProperty('--fa-dur',DUR+'ms');
    tabs.forEach(function(t,k){
      t.addEventListener('click',function(){ show(k); schedule(); });
      t.addEventListener('keydown',function(e){
        var n=null;
        if(e.key==='ArrowDown'||e.key==='ArrowRight') n=(k+1)%tabs.length;
        if(e.key==='ArrowUp'||e.key==='ArrowLeft') n=(k-1+tabs.length)%tabs.length;
        if(e.key==='Home') n=0; if(e.key==='End') n=tabs.length-1;
        if(n!==null){ e.preventDefault(); show(n,true); schedule(); }
      });
    });
    var grid=root.querySelector('.fa-grid');
    grid.addEventListener('mouseenter',function(){setPaused(true)});
    grid.addEventListener('mouseleave',function(){setPaused(false)});
    grid.addEventListener('focusin',function(){setPaused(true)});
    grid.addEventListener('focusout',function(){setPaused(false)});
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es){ visible=es[0].isIntersecting; root.classList.toggle('is-paused',!visible||paused); schedule(); },{threshold:.35}).observe(grid);
    } else { visible=true; }
    show(0); schedule();
  }
  function boot(){ [].forEach.call(document.querySelectorAll('.fa-agent'),init); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot); else boot();
})();
