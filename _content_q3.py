# -*- coding: utf-8 -*-
"""第 3 题：Redis 缓存（穿透 / 击穿 / 雪崩 + 一致性），挂简历里的好气网与点云。"""

QUESTION3 = {
    "path": "questions/redis-cache.html",
    "title": ("Redis in front of the database", "把 Redis 挡在数据库前面"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Question 3: cache</span><span class="in-zh">第 3 题：缓存</span>',
    "kicker": ("Question 3 · must know · cache", "第 3 题 · 必背 · 缓存"),
    "h1": ("One Redis in front, P95 from 800 ms down to 240 ms.",
           "前面加一层 Redis，P95 从 800 毫秒降到 240 毫秒。"),
    "lede": ("A cache does only one thing: stop the same read from reaching the database twice. "
             "Everything else is about the three ways it can leak.",
             "缓存只干一件事：让重复的读不再打到数据库。剩下的全是“它有哪三种漏法”。"),
    "tags": [("Must know", "必背"), ("cache", "缓存"), ("speak 60s", "60 秒口播"),
             ("4 follow-ups", "追问 4 个")],
    "on": "q",
    "answer": ("Hit rate decides the win: 92% hits means the database sees 8% of the traffic. "
               "Penetration, breakdown and avalanche are three different leaks with three different fixes. "
               "Consistency is Cache Aside — delete after writing, delete again with a delay — "
               "and if you need strong consistency, do not cache that path at all.",
               "收益看命中率：命中 92%，数据库只剩 8% 的流量。穿透、击穿、雪崩是三种不同的漏法，各有各的治。"
               "一致性走 Cache Aside：写完删缓存，再延迟删一次；要强一致的那条链路，干脆不缓存。"),
    "blocks": [
        ("h2", "01", "Why the query was slow in the first place", "先说为什么会慢", [
            ("p", "A list page does not run one query. It runs <b>one query per row</b>, then a count, "
                  "then a dictionary lookup — the same data again and again, on every page view.",
             "一个列表页不是一条 SQL。它是<b>一行一条查询</b>，再加一个 count，再加几次字典查询——"
             "同一批数据，每次刷新都重算一遍。"),
            ("ul", [
                ("Add a cache: the second read of the same page never reaches the database.",
                 "加缓存：同一页第二次读，根本不到数据库。"),
                ("Hit rate 92% means only 8% of reads go through — that is the number to quote.",
                 "命中率 92% 意味着只有 8% 的读穿透下去——这才是该报的数。"),
                ("The other half of 800 → 240 is SQL: N+1 queries collapsed into one join, plus an index.",
                 "800 降到 240 的另一半在 SQL：N+1 查询合成一次 join，再加索引。"),
            ]),
            ("note", "Say both halves. If you only say “I added Redis”, the interviewer will assume you "
                     "cannot tell the cache apart from the query.",
             "两半都要说。只说“我加了 Redis”，面试官会认为你分不清缓存和查询。"),
        ]),
        ("h2", "02", "Three ways a cache leaks", "三种漏法，一张表", [
            ("p", "They sound similar and are asked together, so keep them apart by <b>what is missing</b>.",
             "这三个名字听着像，面试也爱连着问。按<b>“缺的是什么”</b>来分就不会混。"),
            ("table",
             [("Leak", "漏的是什么"), ("What happens", "发生什么"), ("Fix", "怎么治")],
             [
                 [("Penetration", "穿透"), ("A key that exists nowhere: cache misses, the database misses too, "
                                            "and every request repeats it.",
                                            "查一个根本不存在的数据：缓存没有，数据库也没有，每次请求都空跑一遍。"),
                  ("Cache the empty result (`null` with a short TTL) + a bloom filter in front.",
                   "空结果也缓存（存 null，短 TTL）+ 前面加布隆过滤器。")],
                 [("Breakdown", "击穿"), ("One hot key expires, and a thousand threads rebuild it at once.",
                                          "某个热点 key 刚好过期，一瞬间上千个线程同时回源重建。"),
                  ("Let one thread rebuild (Redisson `tryLock`), or keep the key logically expired "
                   "and refresh in the background.",
                   "只让一个线程重建（Redisson tryLock），或者逻辑过期＋后台异步刷新。")],
                 [("Avalanche", "雪崩"), ("Many keys expire at the same second, or Redis itself goes down.",
                                          "大批 key 在同一秒过期，或者 Redis 整个挂了。"),
                  ("Randomise the TTL; add a local (Caffeine) layer; add a circuit breaker so the "
                   "database is not flooded either.",
                   "过期时间加随机；加一层本地缓存（Caffeine）；加限流熔断，别让数据库跟着被冲垮。")],
             ]),
            ("note", "The one-word answer that lands: penetration is <b>fake data</b>, breakdown is "
                     "<b>one hot key</b>, avalanche is <b>many keys at once</b>.",
             "一句话记住：穿透是<b>假数据</b>，击穿是<b>一个热 key</b>，雪崩是<b>一大批 key</b>。"),
        ]),
        ("h2", "03", "Keeping it consistent", "和数据库怎么保持一致", [
            ("p", "The pattern is <b>Cache Aside</b>: read the cache first; on a miss, read the database and "
                  "write the value into the cache; on a write, <b>delete</b> the cache — do not update it.",
             "模式叫 <b>Cache Aside</b>：读先看缓存，没有就查库并回填；写的时候<b>删缓存</b>，不是更新缓存。"),
            ("ul", [
                ("Why delete instead of update: two concurrent writers can interleave and leave the "
                 "older value in the cache.",
                 "为什么删而不是更新：两个并发写交错执行，可能把更旧的值写进缓存。"),
                ("Why delete twice: between “database committed” and “cache deleted”, a reader can still "
                 "put the old value back. Delete again after ~500 ms, or send a delayed message.",
                 "为什么删两次：在“库已提交”和“缓存已删”之间，读请求可能把旧值又放回去。"
                 "约 500 毫秒后再删一次，或者发一条延迟消息。"),
                ("The public says “the cache is a stale copy” — so for money and stock, read the "
                 "primary database and do not cache.",
                 "对外口径：缓存就是一份旧副本——钱和库存这类，直接读主库，不缓存。"),
            ]),
            ("pre", "-- read\n"
                    "v = redis.get(k)\n"
                    "if v == nil:\n"
                    "    v = db.select(k)\n"
                    "    redis.set(k, v, ttl=300 + random(0, 60))   -- ★ 加随机，防雪崩\n"
                    "    if v == nil: redis.set(k, '\\0', ttl=60)    -- ★ 空值也缓存，防穿透\n"
                    "\n"
                    "-- write\n"
                    "db.update(...)\n"
                    "redis.del(k)\n"
                    "delay(500ms); redis.del(k)                       -- ★ 再删一次"),
            ("note", "If you claim “double delete solves it completely”, you will be caught: there is still a "
                     "window. Say “it narrows the window to milliseconds, and money paths do not cache”.",
             "别说“双删就彻底解决了”，还有窗口。说“它把窗口压到毫秒级，而且钱的链路不缓存”。"),
        ]),
        ("h2", "04", "So where did 800 → 240 come from", "那 800 到 240 是怎么来的", [
            ("p", "Do the arithmetic out loud; interviewers like numbers that can be checked.",
             "把算术说出来，面试官喜欢能对得上的数。"),
            ("table",
             [("Change", "改了什么"), ("Effect", "效果")],
             [
                 [("Hot list into Redis, 92% hit rate, TTL 5 min + jitter",
                   "热点列表进 Redis，命中率 92%，TTL 5 分钟 + 随机"),
                  ("≈ 92% of reads never touch MySQL; the database goes from 1000 QPS to ~80.",
                   "约 92% 的读不再碰 MySQL，数据库从 1000 QPS 降到 80 左右。")],
                 [("N+1 queries collapsed into one join + covering index",
                   "N+1 查询合成一次 join + 覆盖索引"),
                  ("The 8% that still reach MySQL each got 3–5× cheaper.",
                   "仍然打到 MySQL 的那 8%，单次便宜了 3–5 倍。")],
                 [("Connection pool raised, slow SQL removed", "连接池调大，慢 SQL 清掉"),
                  ("Tail latency drops most — P95 is exactly about the tail.",
                   "尾延迟降得最明显——P95 说的就是尾部。")],
             ]),
            ("note", "If you only ever quote “70% faster” without a baseline, it sounds invented. "
                     "800 → 240 with the mechanism behind it sounds measured.",
             "只报“快了 70%”像编的；说出 800 → 240 加上机制，才像量过。"),
        ]),
        ("h2", "05", "Four follow-ups, one line each", "四个追问，一句话一个", [
            ("table",
             [("Follow-up", "追问"), ("One-line answer", "一句话答案")],
             [
                 [("What if Redis is down?", "Redis 挂了怎么办？"),
                  ("Local cache + circuit breaker; degrade read-only pages, do not let it hit the database.",
                   "本地缓存 + 熔断限流；只读页降级，别全冲到数据库。")],
                 [("Hot key on one shard?", "热 key 打到一个分片上怎么办？"),
                  ("Local cache first, then split the key with a random suffix, or use a read replica.",
                   "先本地缓存，再把 key 加随机后缀打散，或者上只读副本。")],
                 [("Warm up the cache after a deploy?", "发布后要预热吗？"),
                  ("Yes: top-N keys loaded at startup, otherwise the first minute is a stampede.",
                   "要：启动时把 Top N 的热 key 预加载，否则第一分钟就是雪崩。")],
                 [("Cache the page or the object?", "缓存页面还是缓存对象？"),
                  ("Objects. A page cache is invalidated by any change and gets stale fast.",
                   "对象。整页缓存一改就失效，很快就是脏数据。")],
             ]),
        ]),
        ("h2", "06", "60-second script", "60 秒照念稿", [
            ("quote", "read", "Read this out loud", "照这段说，60 秒",
             [("We put the hot list into Redis with a 5-minute TTL plus random jitter, and the hit rate "
              "settled around 92%, so MySQL only sees about 8% of the reads. On top of that we collapsed "
              "the N+1 queries into one join with a covering index, so the remaining 8% got cheaper too. "
              "That took the list API's P95 from ~800 ms to ~240 ms.\n\n"
              "The three failure modes have three fixes: penetration is fake data, so we cache the empty "
              "result and put a bloom filter in front; breakdown is one hot key, so only one thread rebuilds "
              "it under a Redisson lock; avalanche is many keys or a dead Redis, so TTLs are randomised, "
              "there is a local Caffeine layer, and the read path is circuit-broken.\n\n"
              "For consistency we use Cache Aside: delete after writing, delete again after 500 ms. "
              "Anything about money or stock does not go through the cache at all.",
              "我们把热点列表放进 Redis，TTL 5 分钟加随机，命中率稳定在 92% 左右，MySQL 只看到 8% 的读。"
              "同时把 N+1 查询合成一次 join 加覆盖索引，剩下这 8% 单次也便宜了。列表接口 P95 从 800 毫秒降到 240 毫秒左右。\n\n"
              "三种异常三种治法：穿透是假数据，空结果也缓存、前面加布隆过滤器；击穿是一个热 key，"
              "只让一个线程在 Redisson 锁下重建；雪崩是大批 key 或 Redis 挂了，所以 TTL 加随机、"
              "本地放一层 Caffeine、读链路加熔断。\n\n"
              "一致性走 Cache Aside：写完删缓存，500 毫秒后再删一次。钱和库存那条链路不走缓存。")]),
        ]),
        ("h2", "07", "Where this sits on my résumé", "怎么挂到我自己的项目上", [
            ("p", "Only what is actually in the résumé. This question hangs on two projects:",
             "只挑简历里真有的。这道题挂在两个项目上："),
            ("ul", [
                ("好气网: hot dictionary and list data in Redis + Redisson; response time down 70% "
                 "(P95 800 → 240 ms), hit rate about 92%.",
                 "好气网：字典和列表热点数据进 Redis + Redisson；响应时间降低 70%（P95 800 → 240 毫秒），命中率约 92%。"),
                ("订单系统: cache aside on the order detail page; every write deletes the key, "
                 "the delayed second delete catches the race.",
                 "订单系统：订单详情页走 Cache Aside；每次写都删 key，延迟二次删兜住竞态。"),
                ("数据采集: million-row reports are not cached — they are pre-aggregated by a scheduled job.",
                 "数据采集：百万行的报表不缓存——用定时任务预聚合。"),
            ]),
        ]),
        ("h2", "08", "Three things not to say", "三句别说", [
            ("ul", [
                ("“Cache is consistent with the database.” — It never is; it is a copy with a stale window.",
                 "“缓存和数据库是一致的。”——从来不是，它是一份有窗口的旧副本。"),
                ("“Penetration is solved by a TTL.” — A TTL does nothing for data that never existed.",
                 "“穿透靠设 TTL 解决。”——对不存在的数据，TTL 一点用没有。"),
                ("“Just restart Redis if it breaks.” — That is exactly the avalanche you are supposed to prevent.",
                 "“崩了重启 Redis 就行。”——那正是你要防的雪崩。"),
            ]),
        ]),
    ],
    "words": [
        ("cache", "/kæʃ/", "A fast copy kept in front of the slow store.", "缓存：放在慢库前面的快副本"),
        ("hit rate", "/hɪt reɪt/", "How often the copy is already there.", "命中率：多大概率直接命中"),
        ("penetration", "/ˌpenəˈtreɪʃn/", "Asking for data that does not exist, over and over.", "穿透：反复查不存在的数据"),
        ("breakdown", "/ˈbreɪkdaʊn/", "One hot key expires and everyone rebuilds it at once.", "击穿：一个热 key 过期被同时重建"),
        ("avalanche", "/ˈævəlæntʃ/", "Many keys expire together, or the cache dies.", "雪崩：大批 key 同时失效或缓存挂掉"),
        ("stale", "/steɪl/", "Old data that is still being served.", "脏数据/过期副本"),
        ("jitter", "/ˈdʒɪtər/", "A small random offset added to a TTL.", "抖动：给过期时间加一点随机"),
    ],
    "checks": [
        ("穿透、击穿、雪崩，各自缺的是什么？", "穿透、击穿、雪崩，各自缺的是什么？"),
        ("为什么写的时候删缓存，而不是更新缓存？", "为什么写的时候删缓存，而不是更新缓存？"),
        ("说出 800 → 240 的两半原因。", "说出 800 → 240 的两半原因。"),
    ],
    "next": '<a href="pay-callback.html"><span class="in-en">← Question 2: payment callback</span>'
            '<span class="in-zh">← 第 2 题：支付回调</span></a>',
}
