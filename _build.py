# -*- coding: utf-8 -*-
"""生成全站（中/英/中英）。跑完可删。"""
import io
import _render as R
from _content_a import INDEX, L1, L2, L3, L4
from _content_b import L5, L6, L7, QUESTION, ABOUT, GLOSSARY
from _content_terms import TERMS_PAGE
from _terms import TERMS as TERM_DICTS
from _content_a import SPINE
from _content_q2 import QUESTION2, QINDEX
from _content_q3 import QUESTION3
from _content_q4 import QUESTION4
from _content_speak import SPEAK
from _content_dir import QLIST, DERIVED, LESSONS, TOOLS
from _answers import ANSWERS, INDEX_QA_HEAD, INDEX_QA

R.write_assets()


def enrich(data):
    hit = ANSWERS.get(data["path"] if "path" in data else None)
    if hit:
        data["answer"] = hit.get("answer")
        data["answers"] = hit.get("answers", [])
    return data


for d in (INDEX, L1, L2, L3, L4, L5, L6, L7, QUESTION, ABOUT):
    enrich(d)
INDEX.setdefault("path", "index.html")
enrich(INDEX)

# 首页：把“主线”HTML 填进 01 节（从一个问题长出去）
def spine_html():
    out = ['    <ol class="spine">']
    for st in SPINE:
        live = bool(st["href"])
        cls = "live" if live else "soon"
        inner = (
            '<span class="dot">%s</span>'
            '<span class="q"><span class="in-en">%s</span><span class="in-zh">%s</span></span>'
            '<span class="a"><span class="bi-en">%s</span><span class="bi-zh">%s</span></span>'
            '<span class="go">%s</span>'
            % (st["n"], st["q_en"], st["q_zh"], st["a_en"], st["a_zh"], st["tag_zh"])
        )
        if live:
            out.append('      <li class="%s"><a href="%s">%s</a></li>' % (cls, st["href"], inner))
        else:
            out.append('      <li class="%s"><span class="st">%s</span></li>' % (cls, inner))
    out.append('    </ol>')
    return "\n".join(out)




# ============ 首页：题目列表 ============
QTPL = """    <div class="qlist2">
      <a href="{href}">
        <span class="num">{n}</span>
        <span class="t">{t}<span class="a">{a}</span></span>
        <span class="m">{m}</span>
      </a>
    </div>"""

SOONTPL = """    <div class="qlist2 soon">
      <span class="row">
        <span class="num">{n}</span>
        <span class="t">{t}<span class="a">{a}</span></span>
        <span class="m">{m}</span>
      </span>
    </div>"""


def qlist_html(rows):
    out = []
    for r in rows:
        if r["href"]:
            out.append(QTPL.format(**r))
        else:
            out.append(SOONTPL.format(**r))
    return "\n".join(out)


def lessons_html():
    links = " · ".join('<a href="%s">%s %s</a>' % (h, n, t) for n, t, h in LESSONS)
    return '    <p class="lnline">%s</p>' % links


def tools_html():
    out = ['    <div class="qlist2">']
    for t, a, h, m in TOOLS:
        out.append('      <a href="%s"><span class="num">T</span>'
                   '<span class="t">%s<span class="a">%s</span></span>'
                   '<span class="m">%s</span></a>' % (h, t, a, m))
    out.append('    </div>')
    return "\n".join(out)


GAME_CARD = """    <p class="lnline">
      <a href="../game/hashmap.html">玩装桶小游戏（3 关，电脑上玩）</a> ·
      <a href="../speak.html">高级程序员话术语录</a>
    </p>"""


def derived_section(path, number):
    items = DERIVED.get(path) or []
    if not items:
        return None
    rows = []
    for q, a, href in items:
        where = ('<a href="%s">打开</a>' % href) if href else '<span class="todoq">待写</span>'
        rows.append([(q, q), (a, a), (where, where)])
    return ("h2", number, "New questions this one opened", "这道题又长出了哪些新问题",
            [("note", "A good answer opens the next question. That is the whole method.",
              "一个答案会生出下一个问题——方法就是这个。"),
             ("table", [("Question", "新问题"), ("One line", "一句话"), ("", "")], rows)])


# ============ 高级程序员话术语录 ============
SAY_TPL = """    <div class="say">
      <span class="sc"><b>{n}</b>{scene}</span>
      <div class="vs">
        <div><span class="who">菜鸟说</span><span class="said">{junior}</span></div>
        <div><span class="who">老手说</span><span class="said senior">{senior}</span></div>
      </div>
      <div class="chips">{chips}</div>
      <ul class="whylist">
{why}
      </ul>
    </div>"""


def emphasize(text, words):
    """把关键词标粗（长词优先，只在还没标过的位置上标）。"""
    for w in sorted(words, key=len, reverse=True):
        if w and w in text and ('>' + w + '<') not in text:
            text = text.replace(w, '<b class="kw">%s</b>' % w, 1)
    return text


def speak_html(items):
    out = []
    for it in items:
        why = "\n".join("        <li>%s</li>" % w for w in it["why"])
        chips = "".join("<span>%s</span>" % k for k in it["keywords"])
        senior = emphasize(it["senior"], it["keywords"])
        out.append(SAY_TPL.format(n=it["n"], scene=it["scene_zh"], junior=it["junior"],
                                  senior=senior, chips=chips, why=why))
    return "\n".join(out)

SPEAK_PAGE = {
    "path": "speak.html",
    "title": ("Senior phrasing", "高级程序员话术语录"),
    "crumb": '<a href="index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Phrasing</span><span class="in-zh">话术语录</span>',
    "kicker": ("Phrasing · same thing, said by a senior", "话术语录 · 同一件事，老手怎么说"),
    "h1": ("同一件事，换一种说法。", "同一件事，换一种说法。"),
    "lede": ("Left is how a junior says it. Right is how a senior says the same thing — "
             "and the reasons under each card are what makes it land. Read them out loud.",
             "左边是菜鸟的说法，右边是老手的说法。每张卡下面的三条，是这句话为什么站得住。要出声念。"),
    "tags": [("27 entries", "27 条"), ("15 from your CV", "15 条来自你简历"), ("read aloud", "都要念")],
    "on": "s",
    "plain": True,
    "blocks": [
        ("h2", "01", "General phrasing: same thing, two people",
         "通用话术：同一件事，两个人怎么说",
         [
             ("note", "Do not memorize the whole sentence. Memorize the <b>three bold words</b> in each senior line — "
                      "then say it in your own order.",
              "不要整句背。记住老手那段的<b>三个关键词</b>，然后用你自己的顺序讲出来。"),
             ("html", "__SPEAK_OLD__"),
         ]),
        ("h2", "02", "From your own CV: the 15 that will actually be asked",
         "从你简历里挖出来的 15 条（最可能被问）",
         [
             ("note", "Each card is a line on your CV. If you cannot say the senior version, that CV line is a liability.",
              "每张卡对应你简历上的一行。老手那句说不出来，那一行就是负债——面试官一追就露。"),
             ("html", "__SPEAK_NEW__"),
         ]),
        ("h2", "03", "How to use this page", "怎么用这一页",
         [
             ("ol", [
                 ("Read the left column first — that is probably what you would have said.",
                  "先读左栏——那大概就是你会说的话。"),
                 ("Read the right column out loud, twice. The words must come out of your mouth.",
                  "右栏出声念两遍。词必须从你嘴里出来。"),
                 ("Cover the right column and retell it using only the keyword chips.",
                  "盖住右栏，只看下面的关键词，用自己的话重讲一遍。"),
                 ("If a keyword means nothing to you, that is the next lesson to read.",
                  "哪个关键词看不懂，那就是你下一节该去看的内容。"),
             ]),
             ("note", "Start with the 15 CV cards — those are the ones you will actually be asked. Three minutes each, one evening.",
              "先念那 15 张简历卡：那些才是你真会被问的。一张三分钟，一晚上能过完。"),
         ]),
    ],
    "words": [],
    "checks": [],
    "next": '<a href="questions/index.html"><span class="in-en">Go use it on a question →</span>'
            '<span class="in-zh">拿一道题去用 →</span></a>',
}


# 七课
for lesson in (L1, L2, L3, L4, L5, L6, L7):
    R.page(lesson["path"], lesson, on="b")

# 题目
def page_tail(page, with_tools=True):
    """返回放在页面最底部（自测之后）的块：动手练 + 新问题。"""
    tail = []
    n = len([b for b in page["blocks"] if b[0] == "h2"]) + 1
    if with_tools:
        tail.append(("h2", "%02d" % n, "Practice", "动手练", [
            ("p", "Play the buckets game, or read how a senior says the same thing.",
             "想动手就玩装桶游戏；想学怎么说就翻话术语录。"),
            ("html", GAME_CARD),
        ]))
        n += 1
    sec = derived_section(page["path"], "%02d" % n)
    if sec:
        tail.append(sec)
    return tail


R.page(QUESTION["path"], QUESTION, on="q", tail_blocks=page_tail(QUESTION, with_tools=True))
R.page(QUESTION2["path"], QUESTION2, on="q", tail_blocks=page_tail(QUESTION2, with_tools=False))
R.page(QUESTION3["path"], QUESTION3, on="q", tail_blocks=page_tail(QUESTION3, with_tools=False))
R.page(QUESTION4["path"], QUESTION4, on="q", tail_blocks=page_tail(QUESTION4, with_tools=False))
QINDEX["blocks"] = [("h2", "01", "All questions", "全部题目", [
    ("p", "Same list as the home page. Each page ends with the new questions it opened.",
     "和首页同一张表。每页最后会列出“这道题又长出了哪些新问题”。"),
    ("html", qlist_html(QLIST)),
    ("note", "Grey rows are not written yet.",
     "灰色的是还没写的。"),
])]
R.page(QINDEX["path"], QINDEX, on="q")
from _speak_more import MORE as SPEAK_MORE
_speak_old = speak_html(SPEAK)
_speak_new = speak_html(SPEAK_MORE)
_sb = []
for b in SPEAK_PAGE["blocks"]:
    if b[0] == "h2":
        body = []
        for x in b[4]:
            if x[0] == "html" and x[1] == "__SPEAK_OLD__":
                body.append(("html", _speak_old))
            elif x[0] == "html" and x[1] == "__SPEAK_NEW__":
                body.append(("html", _speak_new))
            else:
                body.append(x)
        b = (b[0], b[1], b[2], b[3], body)
    _sb.append(b)
SPEAK_PAGE["blocks"] = _sb
R.page(SPEAK_PAGE["path"], SPEAK_PAGE, on="s")

# 关于
R.page(ABOUT["path"], ABOUT, on="")

# 词表（分组 + 不生成“新词/自测”两节）
blocks = []
for i, (en, zh, items) in enumerate(GLOSSARY["groups"], 1):
    rows = "\n".join(R.words_html([w]) for w in items)
    blocks.append(("h2", "%02d" % i, en, zh, [
        ("figure", '<div class="wordlist">\n%s\n    </div>' % rows),
    ]))
blocks.append(("note",
               "Pick five words a day. Click ▶ hear it, listen twice, say it three times, then look away and say the meaning.",
               "一天挑五个。点 ▶ hear it 听两遍，读三遍，然后移开视线说一遍意思。"))
GLOSSARY["blocks"] = blocks
enrich(GLOSSARY)
GLOSSARY["plain"] = True
R.page("glossary.html", GLOSSARY, on="w")

# 术语表（正文里可点的那些词，单独成页）
_TD = {t["k"]: t for t in TERM_DICTS}
_tb = []
for i, (en, zh, keys) in enumerate(TERMS_PAGE["groups"], 1):
    items = [_TD[k] for k in keys if k in _TD]
    rows = R.terms_html(items)
    _tb.append(("h2", "%02d" % i, en, zh, [
        ("figure", '<div class="wordlist">\n%s\n    </div>' % rows),
    ]))
_tb.append(("note",
            "Ten a day is plenty. Say the 谐音 out loud, then say what it means in one sentence.",
            "一天十个就够。照着谐音读出来，再用一句话说出它是什么意思。"))
TERMS_PAGE["blocks"] = _tb
TERMS_PAGE["plain"] = True
R.page("terms.html", TERMS_PAGE, on="t")
print("all pages built")


# ============ 首页（必须在 directory_html 定义之后） ============
_ql = qlist_html(QLIST)
_les = lessons_html()
_tls = tools_html()
_fixed = []
for b in INDEX["blocks"]:
    if b[0] == "h2":
        body = list(b[4])
        body = []
        for x in b[4]:
            if x[0] == "html" and x[1] == "__QLIST__":
                body.append(("html", _ql))
            elif x[0] == "html" and x[1] == "__LESSONS__":
                body.append(("html", _les))
            elif x[0] == "html" and x[1] == "__TOOLS__":
                body.append(("html", _tls))
            else:
                body.append(x)
        b = (b[0], b[1], b[2], b[3], body)
    _fixed.append(b)
INDEX["blocks"] = _fixed
INDEX_BLOCKS = []
for b in INDEX["blocks"]:
    INDEX_BLOCKS.append(b)
R.page("index.html", INDEX, on="")
