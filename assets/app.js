/* Java Notes — read aloud + word buttons
   Uses the browser's built-in speech synthesis. No network, no tracking. */

(function () {
  var synth = window.speechSynthesis;
  if (!synth) return;

  var btn = document.querySelector('[data-listen]');
  var speaking = false;
  var queue = [];

  function pick() {
    var main = document.querySelector('main');
    if (!main) return [];
    var nodes = main.querySelectorAll('h1, h2, h3, p, li, .analogy, .word .w');
    var out = [];
    nodes.forEach(function (el) {
      if (el.closest('pre')) return;
      var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!t) return;
      if (el.tagName === 'H2' || el.tagName === 'H3') t = t + '.';
      t.split(/(?<=[.!?])\s+/).forEach(function (s) {
        if (s.trim().length > 1) out.push(s.trim());
      });
    });
    return out;
  }

  function stop() {
    speaking = false;
    queue = [];
    synth.cancel();
    if (btn) { btn.classList.remove('on'); btn.textContent = '🔊 Listen to this page'; }
  }

  function say(text, rate, lang) {
    var u = new SpeechSynthesisUtterance(text);
    u.lang = lang || 'en-US';
    u.rate = rate || 0.9;
    return u;
  }

  if (btn) {
    btn.addEventListener('click', function () {
      if (speaking) { stop(); return; }
      queue = pick();
      if (!queue.length) return;
      speaking = true;
      btn.classList.add('on');
      btn.textContent = '■ Stop';
      var i = 0;
      var next = function () {
        if (!speaking || i >= queue.length) { stop(); return; }
        var u = say(queue[i++], 0.9);
        u.onend = next;
        u.onerror = next;
        synth.speak(u);
      };
      next();
    });
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-say]');
    if (!el) return;
    synth.cancel();
    var text = el.getAttribute('data-say');
    synth.speak(say(text, 0.85));
  });
})();
