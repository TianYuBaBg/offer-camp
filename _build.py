# -*- coding: utf-8 -*-
"""生成全站（中/英/中英）。跑完可删。"""
import io
import _render as R
from _content_a import INDEX, L1, L2, L3, L4
from _content_b import L5, L6, L7, QUESTION, ABOUT, GLOSSARY
from _content_a import SPINE
from _content_q2 import QUESTION2, QINDEX
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

_spine = spine_html()
_fixed = []
for b in INDEX["blocks"]:
    if b[0] == "h2":
        body = list(b[4])
        body = [("html", _spine) if (x[0] == "html" and x[1] == "__SPINE__") else x for x in body]
        b = (b[0], b[1], b[2], b[3], body)
    _fixed.append(b)
INDEX["blocks"] = _fixed
R.page("index.html", INDEX, on="")

# 七课
for lesson in (L1, L2, L3, L4, L5, L6, L7):
    R.page(lesson["path"], lesson, on="b")

# 题目
R.page(QUESTION["path"], QUESTION, on="q")
R.page(QUESTION2["path"], QUESTION2, on="q")
R.page(QINDEX["path"], QINDEX, on="q")

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
