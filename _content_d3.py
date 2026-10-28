# -*- coding: utf-8 -*-
"""第 3 题（Redis 缓存）的 6 个追问，各自成页。"""

CRUMB = ('<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
         '<a href="redis-cache.html"><span class="in-en">Q3</span><span class="in-zh">第 3 题</span></a> / ')

BACK = ('<a href="redis-cache.html"><span class="in-en">&#8592; Back to question 3</span>'
        '<span class="in-zh">&#8592; 回到第 3 题</span></a>')


def P(slug, n, name_en, name_zh, h1_en, h1_zh, lede_en, lede_zh,
      ans_en, ans_zh, talk_en, talk_zh, secs):
    blocks = []
    for i, (h_en, h_zh, items) in enumerate(secs, 1):
        blocks.append(("h2", "%02d" % i, h_en, h_zh, items))
    blocks.append(("h2", "%02d" % (len(secs) + 1), "Say it like this", "面试这么说",
                   [("quote", "read", talk_en, talk_zh)]))
    return dict(
        path="questions/" + slug,
        title=(h1_en, h1_zh),
        crumb=CRUMB + '<span class="in-en">%s</span><span class="in-zh">%s</span>' % (name_en, name_zh),
        kicker=("Follow-up %02d" % n, "追问 %02d" % n),
        h1=(h1_en, h1_zh),
        lede=(lede_en, lede_zh),
        tags=[("must know", "必背"), ("3 min", "3 分钟")],
        answer=(ans_en, ans_zh),
        blocks=blocks,
        words=[], checks=[], answers=[],
        next=BACK,
    )


D3 = [
    P("d3-cache-consistency.html", 1, "Cache and DB consistency", "缓存和库不一致",
      "Delete the cache, do not update it — and delete it twice.", "写完删缓存，不要更新缓存；而且要删两次。",
      "Two concurrent writes can interleave so the older value lands in the cache last.",
      "两个并发写交错时，旧值可能最后落进缓存。",
      "Cache Aside: read → miss → load from DB → put with TTL; write → update DB → delete cache. "
      "Why delete instead of update: update needs a value that may itself be stale from a concurrent read. "
      "Why twice: a reader that loaded before your commit can write the old value back after your delete, "
      "so delete once more ~500ms later (or via a delayed message).",
      "Cache Aside：读 → 未命中 → 查库 → 回填带 TTL；写 → 更新库 → 删缓存。"
      "为什么删不更新：更新要用值，而这个值可能来自并发读的旧快照。"
      "为什么删两次：读请求可能在提交前拿到旧值，在你删除之后又写回缓存，所以约 500 毫秒后再删一次。",
      "一致性走 Cache Aside：写完删缓存，不更新缓存；再加一次延迟双删，大约 500 毫秒后再删一次。"
      "本质是最终一致——要说清“不一致窗口有多长”，别说“绝对一致”。",
      "一致性走 Cache Aside：写完删缓存，不更新缓存；再加一次延迟双删，大约 500 毫秒后再删一次。"
      "本质是最终一致——要说清“不一致窗口有多长”，别说“绝对一致”。",
      [
          ("The interleaving that bites", "会咬人的交错", [
              ("pre", "T1: update db  (value = 2)\n"
                      "T2: read db    (value = 1, still old snapshot)\n"
                      "T1: delete cache\n"
                      "T2: set cache = 1      <-- 旧值被写回，且不会自愈\n\n"
                      "-- 所以 500ms 后再删一次，把这段窗口压掉"),
              ("p", "This is also why “delete twice” is not paranoia — it is covering a specific interleaving.",
               "这也是“删两次”不是玄学的原因：它在盖一段具体的交错。"),
          ]),
          ("When not to cache at all", "什么时候干脆别缓存", [
              ("ul", [
                  ("Money, stock, and anything the user compares against a bank statement: read the master.",
                   "钱、库存、任何用户会拿去和流水核对的东西：直接读主库。"),
                  ("If the read is already fast and the write is frequent, the cache is pure overhead.",
                   "读本来就快、写又频繁，缓存纯粹是负担。"),
                  ("Say the boundary out loud: “strong consistency paths do not go through the cache”.",
                   "把边界说出来：“强一致的链路不走缓存”。"),
              ]),
          ]),
      ]),

    P("d3-penetration-vs-breakdown.html", 2, "Penetration vs breakdown", "穿透和击穿",
      "One is missing data; the other is a hot key expiring.", "一个是数据不存在，一个是热 key 过期。",
      "These two get mixed up in interviews more than any other pair.", "这两个在面试里被混得最多。",
      "Penetration: the key does not exist anywhere, so every request falls through to the DB — the cache cannot "
      "help by definition. Breakdown: the key exists and is hot, but it expires and thousands of threads rebuild "
      "it at once.", "穿透：这个 key 哪儿都不存在，缓存天然帮不上，每个请求都打到库。"
      "击穿：key 存在且很热，但恰好过期，上千线程同时重建。",
      "穿透查的是不存在的数据，缓存永远不命中，要用布隆过滤器或空值缓存；"
      "击穿是一个热 key 过期被同时重建，要用重建加锁或逻辑过期。",
      "穿透查的是不存在的数据，缓存永远不命中，要用布隆过滤器或空值缓存；"
      "击穿是一个热 key 过期被同时重建，要用重建加锁或逻辑过期。",
      [
          ("Same symptom, different fix", "症状像，治法完全不同", [
              ("table", [("", ""), ("Penetration 穿透", "Breakdown 击穿")], [
                  [("key exists?", "key 存在吗"), ("no, never", "不存在，从来没有"), ("yes, and it is hot", "存在，而且很热")],
                  [("cache role", "缓存作用"), ("no hit possible", "永远不命中"), ("hit until it expires", "命中到过期那一刻")],
                  [("fix", "治法"), ("bloom filter / null cache", "布隆 / 空值缓存"),
                   ("rebuild lock / logical expire", "重建加锁 / 逻辑过期")],
              ]),
              ("note", "A Bloom filter can say “definitely absent” with a few MB. That is why it fits penetration "
                       "and nothing else.", "布隆过滤器能用几 MB 断言“一定不存在”，所以它只对穿透有效。"),
          ]),
      ]),

    P("d3-redis-down.html", 3, "Redis is down", "Redis 挂了",
      "Do not let the cache outage become a database outage.", "别让缓存故障变成数据库故障。",
      "If every request suddenly hits MySQL, the cache being down turns into the whole site being down.",
      "如果所有请求瞬间都压到 MySQL，缓存挂就等于整站挂。",
      "Three moves: (1) local cache (Caffeine) to absorb reads for a short while; (2) circuit breaker + rate "
      "limiter so the DB never sees more than it can take; (3) degrade — read-only pages, or return a friendly "
      "“busy, retry” instead of hammering the DB.",
      "三步：(1) 本地缓存（Caffeine）先顶一段时间；(2) 熔断 + 限流，保证数据库不会被压垮；"
      "(3) 降级——只读页或直接返回友好提示，而不是硬压库。",
      "Redis 挂了先靠本地缓存顶，再加熔断限流，保证数据库不被打穿；同时降级：只读页继续，写链路排队或提示。"
      "缓存故障绝不能升级成数据库故障。",
      "Redis 挂了先靠本地缓存顶，再加熔断限流，保证数据库不被打穿；同时降级：只读页继续，写链路排队或提示。"
      "缓存故障绝不能升级成数据库故障。",
      [
          ("Layers of protection", "三层保护", [
              ("ol", [
                  ("Local cache with a short TTL absorbs the first wave.",
                   "本地缓存 + 短 TTL，挡住第一波。"),
                  ("Sentinel / circuit breaker: fail fast instead of queueing forever.",
                   "哨兵 + 熔断：快速失败，而不是无限排队。"),
                  ("Rate limit the DB path so a surge cannot take the database with it.",
                   "对数据库入口限流，避免雪崩式连带故障。"),
              ]),
              ("p", "Note what is not on the list: “just restart Redis”. Recovery takes minutes, the traffic does not wait.",
               "注意列表里没有“重启 Redis”：恢复要几分钟，流量不会等你。"),
          ]),
      ]),

    P("d3-hot-key.html", 4, "Hot key", "热 key",
      "One key, one shard, one core.", "一个 key，一个分片，一个核。",
      "Sharding by key does not help when a single key carries most of the traffic.",
      "按 key 分片对“单 key 扛住大部分流量”完全无效。",
      "Two moves: local cache on each application node (reads never leave the box), and split the key itself "
      "(key:1 … key:16) with a random suffix on write and a merge on read. Do not try to fix it with more shards.",
      "两招：每个应用节点加本地缓存（读不出机器），以及把 key 本身拆开（key:1…key:16），写时随机后缀、读时聚合。"
      "靠加更多分片解决不了单 key 热点。",
      "热 key 打到一个分片，那个分片的单核就满了。做法是本地缓存先兜读，再把 key 加随机后缀拆成多份，"
      "读的时候聚合；写链路不拆，避免计数不一致。",
      "热 key 打到一个分片，那个分片的单核就满了。做法是本地缓存先兜读，再把 key 加随机后缀拆成多份，"
      "读的时候聚合；写链路不拆，避免计数不一致。",
      [
          ("Where the CPU goes", "CPU 花在哪了", [
              ("table", [("Approach", "做法"), ("Helps?", "有用吗")], [
                  [("add more shards", "加更多分片"), ("no — one key lives on one node", "没用——一个 key 只在一个节点")],
                  [("read replicas", "读副本"), ("yes for reads", "读有效")],
                  [("local cache", "本地缓存"), ("yes, best first move", "有，首选")],
                  [("split the key", "拆 key"), ("yes, for counters/hot sets", "有，适合计数/热点集合")],
              ]),
          ]),
      ]),

    P("d3-warm-up.html", 5, "Warm up", "预热",
      "A cold cache is the same as no cache, at the worst moment.", "冷缓存等于没缓存，而且偏偏在最糟的时刻。",
      "Right after a deploy, every node has an empty local cache and Redis may have just been cleared.",
      "刚发布完，每个节点本地缓存是空的，Redis 也可能刚清过。",
      "Load the top N hot keys at startup (or by a one-off job), and warm the local cache on the first few "
      "requests via a slow-start. Without it, the first minute is a full-on avalanche.",
      "启动时加载 Top N 热 key（或跑一次性任务），并对前几分钟做慢启动预热本地缓存。"
      "不做的话，第一分钟就是一次小型雪崩。",
      "发布后要不要预热——要。启动时把 Top N 打进缓存，本地缓存慢启动，避免第一分钟全打到库；"
      "灰度发布也能把预热摊开。",
      "发布后要不要预热——要。启动时把 Top N 打进缓存，本地缓存慢启动，避免第一分钟全打到库；"
      "灰度发布也能把预热摊开。",
      [
          ("How to warm", "怎么预热", [
              ("ul", [
                  ("Startup job: read the top N keys from an offline statistic (or from the DB with a limit).",
                   "启动任务：按离线统计的 Top N 读回来（或带 limit 查库）。"),
                  ("Slow start: let local cache TTL grow from 10s to its normal value over a few minutes.",
                   "慢启动：本地缓存 TTL 从 10 秒逐步涨到正常值。"),
                  ("Canary: release to 5% first, watch DB QPS, then roll out.",
                   "灰度：先 5%，看数据库 QPS，再全量。"),
              ]),
              ("note", "The number that matters is DB QPS right after deploy. Watch it, not the cache hit rate.",
               "真正要看的是发布后的数据库 QPS，而不是缓存命中率。"),
          ]),
      ]),

    P("d3-page-or-object.html", 6, "Page or object", "缓页面还是对象",
      "Objects. Page-level caching invalidates too easily.", "缓存对象。整页缓存的失效太容易。",
      "One comment on the page and a whole page cache is useless.", "页面里多一条评论，整页缓存就白做了。",
      "Cache the object (product detail, category list) with a TTL, and compose the page. Page-level caching "
      "only works for truly static fragments — and then it is a CDN's job.",
      "按对象缓存（商品详情、分类列表）加 TTL，页面在应用层拼装。整页缓存只适合真正静态的片段，"
      "而那本来就该交给 CDN。",
      "缓的是对象，不是整页：整页里任何一块变化，整页就失效；对象粒度更稳，命中率也高。"
      "真正静态的片段直接用 CDN。",
      "缓的是对象，不是整页：整页里任何一块变化，整页就失效；对象粒度更稳，命中率也高。"
      "真正静态的片段直接用 CDN。",
      [
          ("Granularity trade-off", "粒度取舍", [
              ("table", [("Granularity", "粒度"), ("Hit rate", "命中率"), ("Invalidation", "失效成本")], [
                  [("whole page", "整页"), ("low (any block changes)", "低（任何一块变就废）"), ("high", "高")],
                  [("object", "对象"), ("high", "高"), ("low, one key", "低，一个 key")],
                  [("field", "字段"), ("highest", "最高"), ("complex to assemble", "拼装复杂")],
              ]),
          ]),
      ]),
]
