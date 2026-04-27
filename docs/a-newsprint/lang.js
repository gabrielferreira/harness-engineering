// Centralized language switcher for Harness Engineering site.
// Detection precedence: localStorage("he-lang") → navigator.language → "en"
// PT only when navigator.language starts with "pt"; everything else defaults to EN.
(function(){
  function detect(){
    try {
      const saved = localStorage.getItem('he-lang');
      if (saved === 'pt' || saved === 'en') return saved;
    } catch(e){}
    const langs = (navigator.languages && navigator.languages.length)
      ? navigator.languages
      : [navigator.language || 'en'];
    for (const l of langs) {
      if (!l) continue;
      const low = l.toLowerCase();
      if (low.startsWith('pt')) return 'pt';
      if (low.startsWith('en')) return 'en';
    }
    return 'en';
  }
  function apply(lang){
    document.body.dataset.lang = lang;
    document.documentElement.lang = (lang === 'pt') ? 'pt-BR' : 'en';
    document.querySelectorAll('.lang button').forEach(b=>{
      b.classList.toggle('on', b.dataset.lang === lang);
    });
  }
  function init(){
    apply(detect());
    document.querySelectorAll('.lang button').forEach(b=>{
      b.addEventListener('click', ()=>{
        const lang = b.dataset.lang;
        try { localStorage.setItem('he-lang', lang); } catch(e){}
        apply(lang);
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  // Expose helpers in case a page needs them after async render.
  window.HE_LANG = { detect, apply };
})();
