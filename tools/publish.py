#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""发布闸门：每天最多 push 一次（GitHub Pages 有构建次数限制）。

用法：
    python tools/publish.py            # 今天没发过就 push，发过就拒绝
    python tools/publish.py --check    # 只看状态，什么都不做
    python tools/publish.py --force    # 强制发（救急用，事后补一条原因）

状态记在 publish-log.json：每发一次，追加一条 {date, time, sha, note}。
"""
import json
import os
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "publish-log.json")
TODAY = datetime.now().strftime("%Y-%m-%d")


def load_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG, encoding="utf-8") as f:
        return json.load(f)


def save_log(rows):
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")


def git(*args, capture=True):
    return subprocess.run(["git", "-C", ROOT] + list(args),
                          capture_output=capture, text=True)


def today_entry(rows):
    for r in rows:
        if r.get("date") == TODAY:
            return r
    return None


def main():
    check_only = "--check" in sys.argv
    force = "--force" in sys.argv
    rows = load_log()
    hit = today_entry(rows)

    if hit and not force:
        print("今天已经发布过：%s %s（%s）" % (hit["date"], hit["time"], hit.get("sha", "")[:7]))
        print("每天只发一次。改动继续本地 commit，明天一起发。")
        print("急用可加 --force，但记得在 publish-log.json 里补 note。")
        return 0

    if check_only:
        print("今天还没发布，可以发。" if not hit else "今天已发布。")
        return 0

    dirty = git("status", "--porcelain").stdout.strip()
    if dirty:
        print("工作区没干净，先 commit：\n" + dirty)
        return 2

    head = git("rev-parse", "--short", "HEAD").stdout.strip()
    print("推送到 GitHub Pages：%s" % head)
    r = git("push", "origin", "main", capture=True)
    sys.stdout.write(r.stdout + r.stderr)
    if r.returncode != 0:
        print("推送失败，没记日志。")
        return 3

    rows.append({
        "date": TODAY,
        "time": datetime.now().strftime("%H:%M"),
        "sha": head,
        "note": "forced" if force else "",
    })
    save_log(rows)
    print("\n已记录到 publish-log.json。今天不再发布。")
    print("GitHub Pages 约 30–60 秒生效：https://tianyubabg.github.io/offer-camp/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
