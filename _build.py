# -*- coding: utf-8 -*-
"""生成全站（中/英/中英）。跑完可删。"""
import io
import _render as R
from _content_a import INDEX, L1, L2, L3, L4
from _content_b import L5, L6, L7, QUESTION, ABOUT, GLOSSARY
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

# 首页：把“九个问题 → 一句话答案”插到最前面，并给后面的编号 +1
rows = []
for q_en, q_zh, a_en, a_zh, where, href in INDEX_QA:
    rows.append([(("%s" % q_en), q_zh), ((a_en), a_zh),
                 (('<a href="%s">%s</a>' % (href, where)), where)])
seen = []
for b in INDEX["blocks"]:
    if b[0] == "h2":
        b = list(b)
        b[1] = "%02d" % (int(b[1]) + 1)
        seen.append(tuple(b))
    else:
        seen.append(b)
INDEX["blocks"] = [("h2", "01", "Your questions, answered in one line",
                    "你的问题，先用一句话回答",
                    [("note", "Every question below has a full page. This table is the 60-second version.",
                      "下面每个问题都有完整的一页；这张表是 60 秒版。"),
                     ("table", INDEX_QA_HEAD, rows, "qa")])] + seen
R.page("index.html", INDEX, on="")

# 七课
for lesson in (L1, L2, L3, L4, L5, L6, L7):
    R.page(lesson["path"], lesson, on="b")

# 题目
R.page(QUESTION["path"], QUESTION, on="q")

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
