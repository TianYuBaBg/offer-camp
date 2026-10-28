
/* Java Notes — 语言切换 + 朗读 */
(function () {
  /* ---------- 语言 ---------- */
  var root = document.documentElement;
  var KEY = 'jn-lang';

  function apply(lang) {
    root.setAttribute('data-lang', lang);
    try { localStorage.setItem(KEY, lang); } catch (e) {}
    document.querySelectorAll('[data-lang-set]').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-lang-set') === lang);
    });
    var btn = document.querySelector('[data-listen]');
    if (btn && !btn.classList.contains('on')) setListenLabel('idle');
  }

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  apply(saved || root.getAttribute('data-lang') || 'zh');

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-lang-set]');
    if (t) { apply(t.getAttribute('data-lang-set')); }
  });

  /* ---------- 朗读 ---------- */
  var synth = window.speechSynthesis;
  if (!synth) return;
  var btn = document.querySelector('[data-listen]');
  var speaking = false, queue = [];

  function lang() { return root.getAttribute('data-lang') || 'zh'; }

  function visible(el) {
    var L = lang();
    if (el.closest('.bi-en, .in-en') && L === 'zh') return false;
    if (el.closest('.bi-zh, .in-zh') && L === 'en') return false;
    return true;
  }

  function pick() {
    var main = document.querySelector('main');
    if (!main) return [];
    var out = [];
    main.querySelectorAll('h1, h2, h3, p, li').forEach(function (el) {
      if (el.closest('pre')) return;
      if (el.querySelector('p, li')) return;          /* 只取叶子 */
      if (!visible(el)) return;
      var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!t) return;
      /* 只读当前语言的那一层，避免中英混读 */
      if (lang() === 'both') {
        var own = el.closest('.bi-zh, .in-zh') ? 'zh' : 'en';
        if (own === 'zh') return;
      }
      if (el.tagName === 'H2' || el.tagName === 'H3') t += lang() === 'zh' ? '。' : '.';
      t.split(/(?<=[.!?。？！])\s*/).forEach(function (s) {
        if (s.trim().length > 1) out.push(s.trim());
      });
    });
    return out;
  }

  function setListenLabel(state) {
    var b = btn || document.querySelector('[data-listen]');
    if (!b) return;
    var zh = lang() === 'zh';
    if (state === 'on') b.textContent = zh ? '■ 停止' : '■ Stop';
    else if (state === 'idle') b.textContent = zh ? '🔊 朗读本页' : '🔊 Listen to this page';
  }

  function stop() {
    speaking = false; queue = []; synth.cancel();
    if (btn) { btn.classList.remove('on'); setListenLabel('idle'); }
  }

  if (btn) {
    btn.addEventListener('click', function () {
      if (speaking) { stop(); return; }
      queue = pick();
      if (!queue.length) return;
      speaking = true;
      btn.classList.add('on');
      setListenLabel('on');
      var voiceLang = lang() === 'zh' ? 'zh-CN' : 'en-US';
      var i = 0;
      (function next() {
        if (!speaking || i >= queue.length) { stop(); return; }
        var u = new SpeechSynthesisUtterance(queue[i++]);
        u.lang = voiceLang;
        u.rate = voiceLang === 'zh-CN' ? 0.95 : 0.9;
        u.onend = next; u.onerror = next;
        synth.speak(u);
      })();
    });
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-say]');
    if (!el) return;
    synth.cancel();
    var u = new SpeechSynthesisUtterance(el.getAttribute('data-say'));
    u.lang = 'en-US'; u.rate = 0.85;
    synth.speak(u);
  });
})();

/* 题页「新问题」：带 hash 打开对应折叠块 */
(function(){
  function openHash(){
    var h = (location.hash || "").slice(1);
    if(!h) return;
    var el = document.getElementById(h);
    if(el && el.tagName === 'DETAILS'){
      el.open = true;
      setTimeout(function(){ el.scrollIntoView({block:'center'}); }, 60);
    }
  }
  window.addEventListener('hashchange', openHash);
  window.addEventListener('load', openHash);
})();

/* ===== 术语注解：点一下看谐音和含义 ===== */
(function(){
  var T = window.TERMS || {};
  var pop = document.createElement('div');
  pop.id = 'pop';
  document.body.appendChild(pop);
  var anchor = null;

  function dictUrl(key){
    var w = String(key).replace(/[^A-Za-z ]/g,'').trim() || key;
    return 'https://forvo.com/search/' + encodeURIComponent(w) + '/';
  }

  function place(){
    if(!anchor || pop.style.display !== 'block') return;
    var r = anchor.getBoundingClientRect();
    var vw = document.documentElement.clientWidth;
    var vh = window.innerHeight;
    var w = pop.offsetWidth || 330;
    var h = pop.offsetHeight || 190;
    var left = r.left;
    var top = r.bottom + 8;
    if(top + h > vh - 12) top = Math.max(12, r.top - h - 8);
    if(left + w > vw - 16) left = vw - w - 16;
    pop.style.top = Math.max(12, top) + 'px';
    pop.style.left = Math.max(12, left) + 'px';
  }

  function build(k){
    var d = T[k];
    if(!d) return '';
    var html = '<div class="hd"><span class="k">' + k + '</span>';
    if(d.read) html += '<span class="r">' + d.read + '</span>';
    if(d.ipa) html += '<span class="ipa">' + d.ipa + '</span>';
    html += '</div>';
    if(d.zh) html += '<div class="zh">' + d.zh + '</div>';
    if(d.en) html += '<div class="en">' + d.en + '</div>';
    html += '<div class="act">';
    if(d.read) html += '<button type="button" data-say="' + k + '">🔊 读一遍</button>';
    html += '<a href="' + dictUrl(k) + '" target="_blank" rel="noopener">▶ 真人发音</a>';
    html += '</div>';
    return html;
  }

  function open(el){
    var k = el.getAttribute('data-t');
    var html = build(k);
    if(!html) return;
    anchor = el;
    pop.innerHTML = html;
    pop.style.display = 'block';
    place();
    var btn = pop.querySelector('[data-say]');
    if(btn) btn.onclick = function(){ say(k); };
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(place);
    requestAnimationFrame(function(){ requestAnimationFrame(place); });
  }

  function say(text){
    if(!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US';
    u.rate = .85;
    speechSynthesis.speak(u);
  }

  function close(){ pop.style.display = 'none'; anchor = null; }

  document.addEventListener('click', function(e){
    var el = e.target.closest ? e.target.closest('.tm') : null;
    if(el){ e.preventDefault(); open(el); return; }
    if(e.target.closest && !e.target.closest('#pop')) close();
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });
  window.addEventListener('resize', close);
  window.addEventListener('wheel', close, {passive:true});
  window.addEventListener('touchmove', close, {passive:true});

  function autoOpen(){
    if(location.hash.indexOf('#t-') !== 0) return;
    var key = decodeURIComponent(location.hash.slice(3));
    var nodes = document.querySelectorAll('.tm[data-t="' + key + '"]');
    for(var i = 0; i < nodes.length; i++){
      if(nodes[i].getClientRects().length){ open(nodes[i]); return; }
    }
  }
  if(document.readyState === 'complete') autoOpen();
  else window.addEventListener('load', autoOpen);
})();
