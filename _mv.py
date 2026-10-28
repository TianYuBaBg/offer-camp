# -*- coding: utf-8 -*-
import io

p = "_content_b.py"
lines = io.open(p, encoding="utf-8").read().split("\n")

# 1) 定位被我错插进 GLOSSARY_GROUPS 的块：从第 508 行(h2 10)到第 566 行(]),)
start = None
end = None
for i, ln in enumerate(lines):
    if ln.startswith('    ("h2", "10", "Interview script"'):
        start = i
    if start is not None and ln.strip() == "])" and i > start:
        # 连续的最后一个 ]),（第 12 节结尾）
        if lines[i + 1].strip() == "]":
            end = i
            break
assert start is not None and end is not None, (start, end)
chunk = lines[start:end + 1]
print("取出的块行数:", len(chunk), "起:", start + 1, "止:", end + 1)

# 2) 从 GLOSSARY_GROUPS 里删掉这块
rest = lines[:start] + lines[end + 1:]

# 3) 插到 QUESTION 的 sections 收尾处（"    ]," 紧跟 "    \"words\": [" 之前）
target = None
for i, ln in enumerate(rest):
    if ln.strip() == '"words": [' and rest[i - 1].strip() == "],":
        target = i - 1
        break
assert target is not None, "找不到 QUESTION sections 收尾"
merged = rest[:target] + chunk + rest[target:]

io.open(p, "w", encoding="utf-8").write("\n".join(merged))
print("已移动到 QUESTION sections，插入位置行:", target + 1)
