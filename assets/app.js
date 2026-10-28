
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
