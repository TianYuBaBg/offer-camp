# -*- coding: utf-8 -*-
"""生成全站（中/英/中英）。跑完可删。"""
import io
import _render as R
from _content_a import INDEX, L1, L2, L3, L4
from _content_b import L5, L6, L7, QUESTION, ABOUT, GLOSSARY
from _content_a import SPINE
from _content_q2 import QUESTION2, QINDEX
from _content_speak import SPEAK
from _content_dir import DIRECTORY, LESSONS, TOOLS
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




# ============ 首页目录 ============
def directory_html():
    out = []
    for zh, en, rows in DIRECTORY:
        out.append('    <div class="dir">')
        out.append('    <div class="grp"><div class="gt"><span class="zh">%s</span><span>%s</span></div>' % (zh, en))
        for r in rows:
            row = ('<span class="n">%s</span>'
                   '<span class="t">%s<span class="a">%s</span></span>'
                   '<span class="m">%s</span>' % (r["n"], r["t"], r["a"], r["m"]))
            if r["href"]:
                out.append('    <a href="%s">%s</a>' % (r["href"], row))
            else:
                out.append('    <div class="row soon">%s</div>' % row)
        out.append('    </div>')
    # 七节课
    links = " · ".join('<a href="%s">%s %s</a>' % (h, n, t) for n, t, h in LESSONS)
    out.append('    <div class="grp"><div class="gt"><span class="zh">地基：七节课</span><span>Lessons</span></div>')
    out.append('    <div class="row"><span class="n">L</span><span class="t" style="font-size:14px;font-weight:400"'
               '><span class="ln">%s</span></span><span class="m">7 页</span></div>' % links)
    out.append('    </div>')
    # 工具
    out.append('    <div class="grp"><div class="gt"><span class="zh">工具与练习</span><span>Tools</span></div>')
    for t, a, h, m in TOOLS:
        out.append('    <a href="%s"><span class="n">T</span>'
                   '<span class="t">%s<span class="a">%s</span></span>'
                   '<span class="m">%s</span></a>' % (h, t, a, m))
    out.append('    </div>')
    out.append('    </div>')
    return "\n".join(out)


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
    "tags": [("12 entries", "12 条"), ("read aloud", "都要念"), ("interview-ready", "背完就能说")],
    "on": "s",
    "plain": True,
    "blocks": [
        ("h2", "01", "Phrasebook: same thing, two people",
         "对照表：同一件事，两个人怎么说",
         [
             ("note", "Do not memorize the whole sentence. Memorize the <b>three bold words</b> in each senior line — "
                      "then say it in your own order.",
              "不要整句背。记住老手那段的<b>三个关键词</b>，然后用你自己的顺序讲出来。"),
             ("html", "__SPEAK__"),
         ]),
        ("h2", "02", "How to use this page", "怎么用这一页",
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
             ("note", "Twelve cards, three minutes each — one evening. After that, every answer sounds different.",
              "十二张卡，一张三分钟，一个晚上。之后你所有回答听起来都不一样。"),
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
R.page(QUESTION["path"], QUESTION, on="q")
R.page(QUESTION2["path"], QUESTION2, on="q")
R.page(QINDEX["path"], QINDEX, on="q")
_speak = speak_html(SPEAK)
_sb = []
for b in SPEAK_PAGE["blocks"]:
    if b[0] == "h2":
        body = [("html", _speak) if (x[0] == "html" and x[1] == "__SPEAK__") else x for x in b[4]]
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
print("all pages built")


# ============ 首页（必须在 directory_html 定义之后） ============
_dir = directory_html()
_fixed = []
for b in INDEX["blocks"]:
    if b[0] == "h2":
        body = list(b[4])
        body = [("html", _dir) if (x[0] == "html" and x[1] == "__DIRECTORY__") else x for x in body]
        b = (b[0], b[1], b[2], b[3], body)
    _fixed.append(b)
INDEX["blocks"] = _fixed
INDEX_BLOCKS = []
for b in INDEX["blocks"]:
    INDEX_BLOCKS.append(b)
R.page("index.html", INDEX, on="")
