# -*- coding: utf-8 -*-
"""首页目录：一个问题一条，点进去学。"""

DIRECTORY = [
    ("从 HashMap 出发", "The HashMap line", [
        dict(n="01", t="HashMap 到底是个什么东西？", a="一个桶数组，每个桶挂一条短链。",
             m="第 1 题", href="questions/java-hashmap.html"),
        dict(n="02", t="一个 key 怎么就跑到某个桶里？", a="先算 hash，再 h & (n-1) 取下标。",
             m="第 4 课", href="basics/hash.html"),
        dict(n="03", t="两个 key 撞进同一个桶怎么办？", a="排队挂链表；到 8 个转成红黑树。",
             m="第 2–3 课", href="basics/tree.html"),
        dict(n="04", t="桶快满了呢？", a="装到 75% 翻倍，每个 key 要么原位、要么 +n。",
             m="第 5 课", href="basics/big-o.html"),
        dict(n="05", t="两个线程同时 put 会怎样？", a="丢数据，JDK 7 还会成环；换 ConcurrentHashMap。",
             m="第 7 课", href="basics/threads.html"),
    ]),
    ("缓存", "Cache", [
        dict(n="06", t="工作中怎么拿它当缓存用？", a="Redis 挡在数据库前面——以及缓存咬你的三种方式。",
             m="待写", href=""),
    ]),
    ("支付与并发", "Payments and concurrency", [
        dict(n="07", t="微信回调同时来三条，怎么办？", a="幂等表 → 状态 CAS → 再上锁。",
             m="第 2 题", href="questions/pay-callback.html"),
        dict(n="08", t="一万人抢一千件，怎么不超卖？", a="先在 Redis 预扣，数据库做最后一道闸。",
             m="待写", href=""),
    ]),
]

LESSONS = [
    ("1", "数组", "basics/array.html"),
    ("2", "链表", "basics/linked-list.html"),
    ("3", "树 / 红黑树", "basics/tree.html"),
    ("4", "key / hash / 冲突", "basics/hash.html"),
    ("5", "O(1) / O(n) / O(log n)", "basics/big-o.html"),
    ("6", "HashMap 常用方法", "basics/hashmap-methods.html"),
    ("7", "为什么线程不安全", "basics/threads.html"),
]

TOOLS = [
    ("高级程序员话术语录", "12 条：同一件事，老手怎么说", "speak.html", "12 条"),
    ("面试题（2 道）", "每题：一句话答案 + 机制 + 追问 + 60 秒稿", "questions/index.html", "2 页"),
    ("术语词表", "47 个词：音标 + 意思 + 真人发音", "glossary.html", "47 词"),
    ("装桶小游戏", "三关：放进去 / 扩容 / 树化，电脑上玩", "game/hashmap.html", "3 关"),
]
