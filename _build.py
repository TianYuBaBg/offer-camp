# -*- coding: utf-8 -*-
"""生成全站（中/英/中英）。跑完可删。"""
import io
import _render as R
from _content_a import INDEX, L1, L2, L3, L4
from _content_b import L5, L6, L7, QUESTION, ABOUT, GLOSSARY

R.write_assets()

# 首页
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
GLOSSARY["plain"] = True
R.page("glossary.html", GLOSSARY, on="w")
print("all pages built")
