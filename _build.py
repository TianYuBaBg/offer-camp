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

# 首页：紧跟九问表之后加“动手玩”一节，并给后面的编号再 +1
shifted = []
for b in INDEX["blocks"]:
    if b[0] == "h2" and int(b[1]) >= 2:
        b = list(b)
        b[1] = "%02d" % (int(b[1]) + 1)
        b = tuple(b)
    shifted.append(b)

PLAY = ("h2", "02", "Five minutes with your hands", "动手 5 分钟：把 key 放进桶里",
        [("p", "Reading gives you the words. Playing gives you the mechanics. Three levels, about five minutes.",
          "读是把话记住，玩是把机制记住。三关，大约 5 分钟。"),
         ("ul", [
             ("Level 1 — place 5 keys, and watch <code>order</code> and <code>node</code> collide in bucket 15.",
              "第一关：放 5 个 key，看 <code>order</code> 和 <code>node</code> 在桶 15 撞成一条链。"),
             ("Level 2 — fill 12 of 16 (that is 75%), then watch the array double and every key either stay or move by 16.",
              "第二关：装满 12 个（16 的 75%），看数组翻倍，每个 key 要么原位、要么 +16。"),
             ("Level 3 — the 8th key in one bucket turns the chain into a red-black tree: 8 steps become 3.",
              "第三关：同一个桶放第 8 个，链子变成红黑树，8 次比较变成 3 次。"),
             ("Every word on a card can be clicked to hear it read aloud (five sites to choose from).",
              "卡片上的每个单词都能点开听真人发音（右上角可选 5 个站）。"),
         ]),
         ("p", '<a class="playbtn" href="game/hashmap.html">Play the bucket game →</a>',
                '<a class="playbtn" href="game/hashmap.html">玩装桶小游戏 →</a>')])

INDEX["blocks"] = [shifted[0], PLAY] + shifted[1:]
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
