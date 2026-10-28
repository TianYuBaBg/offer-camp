# -*- coding: utf-8 -*-
"""渲染器：把 _content_a / _content_b 里的双语内容渲染成 HTML。"""
import io, os, urllib.parse

BASE = "https://tianyubabg.github.io/offer-camp/"

CSS_EXTRA = """
/* ===== 语言切换 ===== */
html[data-lang="zh"] .bi-en, html[data-lang="zh"] .in-en { display: none !important; }
html[data-lang="en"] .bi-zh, html[data-lang="en"] .in-zh { display: none !important; }
.bi-en { display: block; }
.bi-zh { display: block; }
.in-en, .in-zh { display: inline; }
html[data-lang="both"] .bi-zh { color: var(--ink-2); font-size: .94em; }
html[data-lang="both"] p.bi-zh, html[data-lang="both"] li > .bi-zh,
html[data-lang="both"] blockquote .bi-zh { border-left: 2px solid var(--line); padding-left: 12px; margin-top: 6px; }
html[data-lang="both"] .in-zh { color: var(--ink-3); font-size: .9em; margin-left: .35em; }
html[data-lang="both"] .in-zh::before { content: " " }
html[data-lang="both"] .word .bi-en, html[data-lang="both"] .word .bi-zh { display: inline; }
html[data-lang="both"] .word .bi-zh { color: var(--ink-3); margin-left: .4em; font-size: .92em; }
/* 表格里中英并排，不要上下堆 */
html[data-lang="both"] .ledger .bi-en, html[data-lang="both"] .ledger .in-en { display: inline; }
html[data-lang="both"] .ledger .bi-zh, html[data-lang="both"] .ledger .in-zh {
  display: inline; font-size: .9em; color: var(--ink-3); margin-left: .4em;
}
/* ===== 答案 ===== */
.answerbox{
  border: 1px solid var(--line-strong); border-left: 4px solid var(--seal);
  background: var(--paper-2); padding: 14px 18px; margin: 22px 0 0;
}
.answerbox b{ display:block; font-family:var(--sans); font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--seal); margin-bottom:6px; }
.answerbox .bi-en, .answerbox .bi-zh{ font-size:15.5px; line-height:1.7; }
details.answers{ border-top:1px solid var(--line); padding-top:10px; }
details.answers summary{
  cursor:pointer; font-family:var(--sans); font-size:11px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--seal); padding:6px 0; list-style:none;
}
details.answers summary::-webkit-details-marker{ display:none }
details.answers summary::before{ content:"＋ " }
details.answers[open] summary::before{ content:"－ " }
.ans{ display:grid; grid-template-columns:34px 1fr; gap:10px; padding:10px 0; border-bottom:1px dotted var(--line); }
.ans .an{ font-family:var(--mono); font-size:11px; color:var(--seal); padding-top:3px; }
/* 首页九问表：控制列宽 */
.ledger.qa{ table-layout: fixed }
.ledger.qa th:nth-child(1){ width: 26% }
.ledger.qa th:nth-child(2){ width: 64% }
.ledger.qa th:nth-child(3){ width: 10%; white-space: nowrap }
.ledger.qa td:nth-child(2){ white-space: normal; font-family: var(--serif); letter-spacing: 0; font-size: 14.5px }
.ledger.qa td:nth-child(3){ white-space: nowrap; font-family: var(--mono); font-size: 12px }
/* ===== 表格：长文字一律允许换行（首页九问表需要） ===== */
.ledger{ table-layout: auto; }
.ledger th, .ledger td{ white-space: normal; word-break: break-word; }
.ledger td:nth-child(1){ white-space: normal; }
/* ===== 手机端表格：不隐藏列，改成能读的小字 ===== */
@media (max-width:820px){
  .ledger th:nth-child(3), .ledger td:nth-child(3){ display: table-cell; }
  .ledger{ font-size: 11.5px; width: 100%; }
  .ledger th, .ledger td{ padding: .8mm 1.1mm; white-space: normal; }
  .ledger td:nth-child(1){ font-size: 13px; white-space: normal; }
  .ledger td:nth-child(2){ white-space: normal; }
  .wordlist{ grid-template-columns: 1fr; gap: 3px; }
  .wordlist .word{ grid-template-columns: 1fr; }
  .wordlist .links{ margin-top: 2px; }
}
.mh-nav a.nav-game span{color:#A33}
.mh-nav a.nav-game{border:1px solid #d9b7ae;border-radius:2px;padding:1px 6px;margin-left:2px}
.mh-nav a.nav-game:hover{border-color:#A33}

/* 首页“玩装桶小游戏”按钮 */
.playbtn{display:inline-block;font-family:var(--sans);font-size:14px;letter-spacing:.04em;
         padding:10px 18px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);
         text-decoration:none;border-radius:2px}
.playbtn:hover{background:#3a342c;border-color:#3a342c;color:#fff}



/* ===== 首页 / 题目列表 ===== */
.qlist2{margin:0;border-bottom:1px solid var(--line)}
.qlist2 a,.qlist2 .row{display:grid;grid-template-columns:44px 1fr 76px;gap:16px;align-items:baseline;
  padding:18px 6px 17px;text-decoration:none;color:inherit}
.qlist2:first-of-type{border-top:1px solid var(--rule)}
.qlist2 a:hover{background:rgba(255,255,255,.6)}
.qlist2 .num{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:#A33;
  border:0;padding:0;background:none;display:inline}
.qlist2 .t{font-family:var(--serif);font-size:19px;font-weight:700;line-height:1.42;display:block}
.qlist2 .a{display:block;font-family:var(--serif);font-weight:400;color:var(--ink-2);
  font-size:13.5px;line-height:1.7;margin-top:5px}
.qlist2 .m{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);text-align:right;white-space:nowrap}
.qlist2.soon{opacity:.5}
.lnline{font-family:var(--mono);font-size:11.5px;line-height:2.6;color:var(--ink-2)}
.lnline a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
.lnline a:hover{border-bottom-color:#A33}
.todoq{font-family:var(--mono);font-size:10.5px;color:var(--ink-3)}

/* ===== 首页目录 ===== */
.dir{margin:14px 0 0}
.dir .grp{margin:30px 0 0}
.dir .gt{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid var(--rule);padding-bottom:8px;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;color:#8a8378;text-transform:uppercase}
.dir .gt .zh{font-family:var(--serif);font-size:15px;letter-spacing:.06em;color:var(--ink);text-transform:none}
.dir a,.dir .row{display:grid;grid-template-columns:40px 1fr 96px;gap:16px;align-items:baseline;
  padding:15px 6px;border-bottom:1px solid var(--line);text-decoration:none;color:inherit}
.dir a:hover{background:rgba(255,255,255,.6)}
.dir .n{font-family:var(--mono);font-size:11px;color:#A33;letter-spacing:.06em}
.dir .t{font-family:var(--serif);font-size:18.5px;font-weight:700;line-height:1.42}
.dir .a{display:block;color:var(--ink-2);font-size:13.5px;line-height:1.65;margin-top:4px}
.dir .m{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);text-align:right;white-space:nowrap}
.dir .soon{opacity:.5}
.dir .ln{font-family:var(--mono);font-size:11.5px;line-height:2.3;color:var(--ink-2)}
.dir .ln a{display:inline;padding:0;border:0;text-decoration:none;color:var(--ink);border-bottom:1px solid var(--rule)}
.dir .ln a:hover{background:none;border-bottom-color:#A33}

/* ===== 高级程序员话术语录 ===== */
.say{border-top:1px solid var(--line);padding:24px 0 6px}
.say .sc{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-3)}
.say .sc b{color:#A33;font-weight:400;margin-right:8px}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:14px 0 0;border:1px solid var(--rule-soft)}
.vs > div{padding:14px 16px}
.vs > div + div{border-left:1px solid var(--rule-soft);background:var(--paper-2)}
.vs .who{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;
  color:var(--ink-faint);margin-bottom:8px}
.vs .said{font-size:14.5px;line-height:1.8;color:var(--ink-2)}
.vs .said.senior{font-family:var(--serif);font-size:16.5px;line-height:2;color:var(--ink)}
.vs .said.senior .kw{border-bottom:1px solid #E0C9C2;font-weight:700}
.chips{margin:12px 0 0}
.chips span{display:inline-block;margin:0 6px 6px 0;padding:2px 8px;border:1px solid var(--rule);
  font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;color:var(--ink-2)}
.whylist{margin:12px 0 0;padding-left:18px}
.whylist li{font-size:13.8px;line-height:1.8;color:var(--ink-2);margin-bottom:6px}

/* 照念稿（blockquote.read） */
blockquote.read{margin:0; padding:20px 24px; background:var(--paper-2);
  border-left:3px solid var(--red); font-family:var(--serif); font-size:16.5px;
  line-height:1.95; color:var(--ink)}
blockquote.read .lbl{display:block; margin-bottom:10px; font-family:var(--mono);
  font-size:10px; letter-spacing:.18em; color:var(--red)}
blockquote.read p{margin:0 0 14px}
blockquote.read p:last-child{margin-bottom:0}
/* 首页主线（一个问题的分支） */
.spine{list-style:none;margin:12px 0 0;padding:0;position:relative}
.spine:before{content:"";position:absolute;left:14px;top:12px;bottom:18px;width:2px;background:#CFC4AF}
.spine li{position:relative;padding-left:44px}
.spine .dot{position:absolute;left:6px;top:17px;width:19px;height:19px;border-radius:50%;
            border:1px solid #B9AD99;background:#F4EFE3;display:flex;align-items:center;
            justify-content:center;font-family:var(--mono);font-size:8.5px;color:var(--ink-3)}
.spine li.live .dot{border-color:#A33;color:#A33;background:#FBF1EC}
.spine a,.spine .st{display:block;padding:13px 0 14px;border-bottom:1px solid var(--line);
                    text-decoration:none;color:inherit}
.spine a:hover{background:rgba(255,255,255,.55)}
.spine .q{display:block;font-family:var(--serif);font-size:19px;font-weight:700;line-height:1.35;margin-bottom:5px}
.spine .a{display:block;color:var(--ink-2);font-size:14.5px;line-height:1.7}
.spine .go{display:inline-block;margin-top:7px;font-family:var(--mono);font-size:10px;
           letter-spacing:.1em;color:var(--ink-3)}
.spine li.live .go{color:#A33}
.spine li.soon{opacity:.55}
/* ===== 题目列表 ===== */
.qlist{list-style:none;padding:0;margin:16px 0 0}
.qlist li{border-bottom:1px solid var(--line)}
.qlist a{display:block;padding:18px 0;text-decoration:none;color:inherit}
.qlist a:hover{background:rgba(255,255,255,.55)}
.qlist .num{font-family:var(--mono);font-size:10.5px;color:#A33;letter-spacing:.12em}
.qlist .t{display:block;font-family:var(--serif);font-size:20px;font-weight:700;margin:7px 0 5px;line-height:1.35}
.qlist .m{display:block;color:var(--ink-2);font-size:14px;line-height:1.7}
/* 导航与标签里的中文用细体 */
.in-zh { font-family: var(--serif); }
.langswitch { display: inline-flex; border: 1px solid var(--line-strong); }
.langswitch button {
  font: inherit; font-size: 11px; letter-spacing: .04em; padding: 4px 9px;
  background: transparent; color: var(--ink-3); border: 0; cursor: pointer;
}
.langswitch button + button { border-left: 1px solid var(--line); }
.langswitch button.on { background: var(--ink); color: var(--paper); }
.mh-right { display: flex; align-items: center; gap: 14px; }
"""

JS = r"""
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
"""

PAGE = """<!doctype html>
<html lang="zh-CN" data-lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · Java Notes</title>
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="__CSS__">
</head>
<body>
<div class="grain" aria-hidden="true"></div>

<header class="masthead">
  <div class="mh-left">
    <a class="mh-mark" href="__HOME__">Java Notes</a>
    <nav class="mh-nav">
      <a href="__QIDX__"__ON_Q__><span class="in-en">Questions</span><span class="in-zh">题目</span></a>
      <a href="__BASICS__"__ON_B__><span class="in-en">Basics</span><span class="in-zh">基础</span></a>
      <a href="__GLOSS__"__ON_W__><span class="in-en">Words</span><span class="in-zh">词表</span></a>
      <a href="__SPEAK__"__ON_S__><span class="in-en">Phrasing</span><span class="in-zh">话术</span></a>
      <a class="nav-game" href="__GAME__"><span class="in-en">Play</span><span class="in-zh">游戏</span></a>
    </nav>
  </div>
  <div class="mh-right">
    <span class="langswitch">
      <button type="button" data-lang-set="zh">中文</button>
      <button type="button" data-lang-set="both">中英</button>
      <button type="button" data-lang-set="en">English</button>
    </span>
  </div>
</header>

<main>
  <p class="crumb">__CRUMB__</p>

  <div class="qhead">
    <p class="kicker"><span class="in-en">__KICKER_EN__</span><span class="in-zh">__KICKER_ZH__</span></p>
    <h1><span class="in-en">__H1_EN__</span><span class="in-zh">__H1_ZH__</span></h1>
    <p class="lede"><span class="in-en">__LEDE_EN__</span><span class="in-zh">__LEDE_ZH__</span></p>
    __ANSWERBOX__
    <p class="tags">__TAGS__</p>
    <button class="listen" data-listen type="button">🔊</button>
  </div>

__BODY__

  <p class="log-tip">__NEXT__</p>
</main>

<footer>
  <div class="f-left"><span class="in-en">Written for learning English · Wang Tianyu</span><span class="in-zh">为学英语而写 · 王天宇</span></div>
  <div class="f-right"><a href="__HOME__"><span class="in-en">Home</span><span class="in-zh">首页</span></a><span class="sep">·</span><a href="https://github.com/TianYuBaBg/offer-camp">GitHub</a></div>
</footer>
<script src="__JS__"></script>
</body>
</html>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def bisp(en, zh, tag="p", cls=""):
    c = ' class="%s"' % cls if cls else ""
    return '<%s%s><span class="bi-en">%s</span><span class="bi-zh">%s</span></%s>' % (
        tag, c, en, zh, tag)


def render_blocks(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "h2":
            out.append('  <section class="sec">\n    <h2><span class="num">%s</span>'
                       '<span class="in-en">%s</span><span class="in-zh">%s</span></h2>'
                       % (b[1], b[2], b[3]))
            body = b[4] if len(b) > 4 else []
            for x in body:
                out.append(render_one(x))
            out.append('  </section>')
        else:
            out.append(render_one(b))
    return "\n".join(out)


def render_one(b):
    k = b[0]
    if k == "p":
        return "    " + bisp(b[1], b[2])
    if k == "ul":
        lis = "\n".join('      <li><span class="bi-en">%s</span><span class="bi-zh">%s</span></li>' % (e, z) for e, z in b[1])
        return "    <ul>\n%s\n    </ul>" % lis
    if k == "ol":
        lis = "\n".join('      <li><span class="bi-en">%s</span><span class="bi-zh">%s</span></li>' % (e, z) for e, z in b[1])
        return '    <ol class="steps">\n%s\n    </ol>' % lis
    if k == "pre":
        return "    <pre><code>%s</code></pre>" % b[1]
    if k == "quote":
        head = '<span class="in-en">%s</span><span class="in-zh">%s</span>' % (b[2], b[3])
        ps = "\n".join("      " + bisp(e, z) for e, z in b[4])
        return '    <blockquote class="%s"><span class="lbl">%s</span>\n%s\n    </blockquote>' % (b[1], head, ps)
    if k == "analogy":
        return ('    <div class="analogy"><b><span class="in-en">%s</span><span class="in-zh">%s</span></b>'
                '<span class="bi-en">%s</span><span class="bi-zh">%s</span></div>' % (b[1], b[2], b[3], b[4]))
    if k == "table":
        extra = (" " + b[3]) if len(b) > 3 and b[3] else ""
        def cell_th(e, z):
            return "<th>%s</th>" % e if e == z else ("<th><span class=\"in-en\">%s</span><span class=\"in-zh\">%s</span></th>" % (e, z))
        head = "".join(cell_th(e, z) for e, z in b[1])
        rows = []
        for r in b[2]:
            def cell_td(e, z):
                return "<td>%s</td>" % e if e == z else ("<td><span class=\"bi-en\">%s</span><span class=\"bi-zh\">%s</span></td>" % (e, z))
            rows.append("<tr>" + "".join(cell_td(e, z) for e, z in r) + "</tr>")
        return ('    <table class="ledger%s">\n      <thead><tr>%s</tr></thead>\n      <tbody>\n        %s\n      </tbody>\n    </table>'
                % (extra, head, "\n        ".join(rows)))
    if k == "figure":
        return "    " + b[1]
    if k == "html":
        return b[1]
    if k == "note":
        return '    <p class="note"><span class="bi-en">%s</span><span class="bi-zh">%s</span></p>' % (b[1], b[2])
    if k == "links":
        items = "".join('<li><a href="%s"><span class="in-en">%s</span><span class="in-zh">%s</span></a></li>' % (h, e, z) for h, e, z in b[1])
        return '    <ul class="deeper">\n      %s\n    </ul>' % items
    raise ValueError("unknown block %r" % (k,))


def words_html(words):
    out = []
    for term, ipa, en, zh in words:
        q = urllib.parse.quote(term.replace(" ", "%20")) if " " in term else urllib.parse.quote(term)
        out.append(
            '      <div class="word">\n'
            '        <span class="w">%s</span>\n'
            '        <span class="ipa">%s</span>\n'
            '        <span class="mean"><span class="bi-en">%s</span><span class="bi-zh">%s</span></span>\n'
            '        <span class="links">'
            '<a class="say" href="https://youglish.com/pronounce/%s/english" target="_blank" rel="noopener">▶ hear it</a>'
            '<button class="spk" data-say="%s" type="button" aria-label="say %s">🔊</button>'
            '</span>\n'
            '      </div>' % (term, ipa, en, zh, q, term, term))
    return "\n".join(out)


def answers_html(answers):
    if not answers:
        return ""
    out = []
    for i, (e, z) in enumerate(answers, 1):
        out.append('      <div class="ans"><span class="an">%02d</span>'
                   '<span class="bi-en">%s</span><span class="bi-zh">%s</span></div>' % (i, e, z))
    return "\n".join(out)


def checks_html(checks):
    return "\n".join('      <li><span class="bi-en">%s</span><span class="bi-zh">%s</span></li>' % (e, z)
                     for e, z in checks)


def page(path, data, on=""):
    depth = path.count("/")
    up = "../" * depth
    tags = "".join(
        '<span class="tag"><span class="in-en">%s</span><span class="in-zh">%s</span></span>' % (e, z)
        for e, z in data["tags"])

    body = render_blocks(data["blocks"])
    if not data.get("plain"):
        body += """
  <section class="sec">
    <h2><span class="num">→</span><span class="in-en">New words</span><span class="in-zh">新词</span></h2>
    <div class="wordlist">
%s
    </div>
    <p class="note"><span class="bi-en">Click <b>▶ hear it</b> for real people on YouGlish; <b>🔊</b> for the computer voice.</span><span class="bi-zh">点 <b>▶ hear it</b> 听真人发音（YouGlish）；点 <b>🔊</b> 听电脑朗读。</span></p>
  </section>

  <section class="sec">
    <h2><span class="num">✓</span><span class="in-en">Check yourself</span><span class="in-zh">自测</span></h2>
    <ol class="checks">
%s
    </ol>
    <p class="note"><span class="bi-en">Answer out loud first. Only then open the answers below.</span><span class="bi-zh">先自己出声答，再看下面的答案。</span></p>
  </section>

  <section class="sec">
    <details class="answers">
      <summary><span class="in-en">Answers</span><span class="in-zh">参考答案</span></summary>
%s
    </details>
  </section>
""" % (words_html(data["words"]), checks_html(data["checks"]), answers_html(data.get("answers", [])))

    subs = {
        "__TITLE__": data["title"][0], "__DESC__": data["title"][0],
        "__CSS__": up + "assets/style.css", "__JS__": up + "assets/app.js",
        "__HOME__": up + "index.html",
        "__QIDX__": up + "questions/index.html",
        "__BASICS__": up + "basics/array.html",
        "__GLOSS__": up + "glossary.html",
        "__GAME__": up + "game/hashmap.html",
        "__SPEAK__": up + "speak.html",
        "__ON_S__": ' class="on"' if on == "s" else "",
        "__ON_Q__": ' class="on"' if on == "q" else "",
        "__ON_B__": ' class="on"' if on == "b" else "",
        "__ON_W__": ' class="on"' if on == "w" else "",
        "__CRUMB__": data["crumb"],
        "__KICKER_EN__": data["kicker"][0], "__KICKER_ZH__": data["kicker"][1],
        "__H1_EN__": data["h1"][0], "__H1_ZH__": data["h1"][1],
        "__LEDE_EN__": data["lede"][0], "__LEDE_ZH__": data["lede"][1],
        "__TAGS__": tags, "__BODY__": body, "__NEXT__": data["next"],
        "__ANSWERBOX__": ('<div class="answerbox"><b><span class="in-en">Short answer</span>'
                          '<span class="in-zh">先给答案</span></b>'
                          '<span class="bi-en">%s</span><span class="bi-zh">%s</span></div>'
                          % (data["answer"][0], data["answer"][1])) if data.get("answer") else "",
    }
    html = PAGE
    for k, v in subs.items():
        html = html.replace(k, v)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(html)
    print("wrote", path)


def write_assets():
    css = io.open("assets/style.css", encoding="utf-8").read()
    if "/* ===== 语言切换 ===== */" in css:
        css = css[:css.index("/* ===== 语言切换 ===== */")]
    io.open("assets/style.css", "w", encoding="utf-8").write(css.rstrip() + "\n" + CSS_EXTRA)
    io.open("assets/app.js", "w", encoding="utf-8").write(JS)
    print("assets updated")
