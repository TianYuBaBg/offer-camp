# -*- coding: utf-8 -*-
"""构建期术语注解：把页面上出现的术语包成 <span class="tm" data-t="...">。

规则：
- 英文按整词匹配（RabbitMQ 里的 MQ 不会被单独标）
- 中文按子串匹配
- 同一页同一个术语只标第一次，避免满屏下划线
- 不标 <code> <a> <pre> 里面的内容
"""
import html
import re

from _terms import TERMS

DIC = {t["k"]: t for t in TERMS}
KEYS = sorted(DIC, key=len, reverse=True)

ASCII_RE = re.compile(r"^[A-Za-z0-9_+.\-]+$")
EN_PATTERNS = {
    k: re.compile(r"(?<![A-Za-z0-9_])" + re.escape(k) + r"(?![A-Za-z0-9_])")
    for k in KEYS if ASCII_RE.match(k)
}
CJK_KEYS = [k for k in KEYS if not ASCII_RE.match(k)]

TAG_RE = re.compile(r"(<[^>]+>)")
SKIP_TAGS = {"code", "a", "pre", "h1", "h2", "script", "style", "textarea"}

used = {"en": set(), "zh": set()}


def reset():
    used["en"].clear()
    used["zh"].clear()


def _wrap(key, text_seen):
    safe = html.escape(key, quote=True)
    return '<span class="tm" data-t="%s">%s</span>' % (safe, text_seen)


def _annotate_plain(part, bucket="zh", limit=3):
    """在一段纯文本里标最多 limit 个不同的术语。"""
    seen = used[bucket]
    hits = []
    for k in KEYS:
        if k in seen:
            continue
        if k in EN_PATTERNS:
            m = EN_PATTERNS[k].search(part)
            if not m:
                continue
            s, e = m.start(), m.end()
        else:
            s = part.find(k)
            if s < 0:
                continue
            e = s + len(k)
        hits.append((s, e, k))

    if not hits:
        return part

    # 从前往后取，互相不重叠
    hits.sort()
    picked, cursor = [], -1
    for s, e, k in hits:
        if s < cursor:
            continue
        picked.append((s, e, k))
        cursor = e
        if len(picked) >= limit:
            break

    out, pos = [], 0
    for s, e, k in picked:
        out.append(part[pos:s])
        out.append(_wrap(k, part[s:e]))
        pos = e
        seen.add(k)
    out.append(part[pos:])
    return "".join(out)


LANG_TAGS = {"bi-en": "en", "in-en": "en", "bi-zh": "zh", "in-zh": "zh"}


def annotate(text):
    if not text:
        return text
    parts = TAG_RE.split(text)
    out = []
    stack = []          # [(tag_name, bucket)]
    bucket = "zh"
    for i, part in enumerate(parts):
        if i % 2 == 1:  # 是一个标签
            out.append(part)
            m = re.match(r"</?\s*([A-Za-z0-9]+)", part)
            if m:
                name = m.group(1).lower()
                if part.startswith("</"):
                    for j in range(len(stack) - 1, -1, -1):
                        if stack[j][0] == name:
                            bucket = stack[j - 1][1] if j > 0 else "zh"
                            del stack[j:]
                            break
                elif not part.endswith("/>"):
                    new_bucket = bucket
                    for cls, lang in LANG_TAGS.items():
                        if cls in part:
                            new_bucket = lang
                            break
                    stack.append((name, bucket))
                    bucket = new_bucket
            continue
        if any(t in SKIP_TAGS for t in [x[0] for x in stack]):
            out.append(part)
            continue
        out.append(_annotate_plain(part, bucket))
    return "".join(out)
