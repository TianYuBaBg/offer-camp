# -*- coding: utf-8 -*-
"""第 4 题：订单 30 分钟自动关单（Redis 延时队列），为什么不走 MQ 延迟队列。"""

QUESTION4 = {
    "path": "questions/order-timeout.html",
    "title": ("Close an unpaid order after 30 minutes", "三十分钟没付就自动关单"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Question 4: order timeout</span><span class="in-zh">第 4 题：订单超时</span>',
    "kicker": ("Question 4 · must know · orders and queues", "第 4 题 · 必背 · 订单与队列"),
    "h1": ("An order is left unpaid for 30 minutes. How does it close itself?",
           "订单 30 分钟没付，怎么自动关掉？"),
    "lede": ("A scheduled scan of the whole table melts the database. Something has to remember "
             "“this order is due at 10:47” — and be right when the payment callback arrives at the same second.",
             "每分钟扫一次全表会把数据库扫垮。得有个东西记住“这一单 10:47 到期”，"
             "还要在支付回调同一秒到达时不出错。"),
    "tags": [("Must know", "必背"), ("orders", "订单"), ("speak 60s", "60 秒口播"),
             ("4 follow-ups", "追问 4 个")],
    "on": "q",
    "answer": ("Put the order id into a Redis sorted set at checkout, with score = the due timestamp. "
               "A once-a-second job pulls what is due, takes a Redisson lock, and closes the order with a "
               "status CAS that also rolls the stock back. No RabbitMQ delay queue because the project "
               "already had Redis and a plugin or a TTL+DLX topology is extra machinery to run — the price "
               "is polling and no delivery guarantee, so a compensation scan and the CAS cover it.",
               "下单时把订单号塞进 Redis 的 ZSet，score 存到期时间戳；一个每秒跑的任务捞出到期的，"
               "先拿 Redisson 锁，再用状态 CAS 关单并回滚库存。不用 RabbitMQ 延迟队列，是因为项目里本来就有 Redis，"
               "而 TTL+DLX 或延迟插件是多一套要运维的东西；代价是轮询和不保证投递，所以加了补偿扫描和 CAS 兜底。"),
    "blocks": [
        ("h2", "01", "Why not just scan the table every minute", "为什么不能每分钟扫全表", [
            ("p", "The naive version is one query: <code>select id from orders where status='PENDING' "
                  "and create_time &lt; now() - interval 30 minute</code>. Every minute. Forever.",
             "最朴素的写法就是一条 SQL：<code>select id from orders where status='PENDING' "
             "and create_time &lt; now() - interval 30 minute</code>。每分钟一次，永远跑。"),
            ("ul", [
                ("It scans rows that are <b>not</b> due yet — most of the table, most of the time.",
                 "它扫的是<b>还没到期</b>的行——绝大多数时候，扫的是整张表。"),
                ("The index only helps if you also store a “due at” column; with <code>create_time + 30m</code> "
                 "the range is not sargable.",
                 "索引只有在有“到期时间”这一列时才帮得上；用 <code>create_time + 30 分钟</code> 算出来的范围用不上索引。"),
                ("Latency is up to one interval: an order can sit open for 30 minutes and 59 seconds.",
                 "精度最差差一个周期：30 分 59 秒才发现该关。"),
                ("In a flash sale, the scan and the business traffic fight for the same database.",
                 "大促时，这个扫描和业务流量抢同一个数据库。"),
            ]),
            ("note", "So the real requirement is not “scan often”, it is <b>“wake me exactly when this order is due”</b>.",
             "所以真正的需求不是“扫得勤”，而是<b>“这一单到点时叫醒我”</b>。"),
        ]),
        ("h2", "02", "Three ways to be woken up on time", "三条路，各自的代价", [
            ("table",
             [("Approach", "做法"), ("Good", "好处"), ("Price", "代价")],
             [
                 [("Scan the table", "定时扫全表"),
                  ("Dead simple, no new component.", "最简单，不需要新组件。"),
                  ("Database pressure, coarse precision, poor use of the index.",
                   "压数据库、精度差、用不上索引。")],
                 [("MQ delay queue", "MQ 延迟队列"),
                  ("Accurate, retries built in, dead-letter box.", "精度高，自带重试和死信。"),
                  ("Another component to run; TTL+DLX or a plugin for RabbitMQ; "
                   "you still must handle duplicate delivery.",
                   "多一套中间件；RabbitMQ 要靠 TTL+DLX 或插件；重复投递还是得自己兜。")],
                 [("Redis sorted set", "Redis ZSet"),
                  ("Already in the project, one line to enqueue, second-level precision, one query to pull due items.",
                   "项目里已有；入队一行代码；秒级精度；一条命令捞出到期的。"),
                  ("Polling; no delivery guarantee — a failover can lose an entry, so you need a "
                   "compensation scan.",
                   "要轮询；不保证投递——主从切换可能丢条目，所以要补偿扫描。")],
             ]),
            ("note", "The interview answer that scores: pick one, then say what you gave up and how you covered it. "
                     "“We used Redis because we already had it; we covered the reliability gap with a nightly "
                     "compensation scan.”",
             "能拿分的说法：选一个，然后说清放弃了什么、怎么补上。“选 Redis 是因为项目已有；"
             "可靠性缺口用每日补偿扫描兜住。”"),
        ]),
        ("h2", "03", "The whole mechanism is four lines", "整套机制就四行", [
            ("pre", "-- at checkout: enqueue with the due time as score\n"
                    "ZADD order:delay  1730000000000  \"SO20261029001\"\n"
                    "\n"
                    "-- every second: pull what is due\n"
                    "ids = ZRANGEBYSCORE order:delay  0  now   LIMIT  0  100\n"
                    "\n"
                    "-- for each id: lock, check, close, remove\n"
                    "lock = redisson.getLock(\"lock:order:close:\" + id)\n"
                    "if lock.tryLock():\n"
                    "    n = db.update(\"update orders set status='CLOSED' \"\n"
                    "                 \"where id=? and status='PENDING'\", id)\n"
                    "    if n == 1: db.update(\"update sku_stock set qty=qty+1 where sku_id=?\", skuId)\n"
                    "    redis.zrem(\"order:delay\", id)\n"
                    "    lock.unlock()"),
            ("ul", [
                ("<b>score is the due timestamp</b> — that is why a sorted set is the right structure: "
                 "it is already sorted by time.",
                 "<b>score 就是到期时间戳</b>——这就是为什么用有序集合：它本身按时间排好了。"),
                ("<b>LIMIT 100</b>: never pull everything at once; a burst of 10k due orders becomes 100 "
                 "batches instead of one long transaction.",
                 "<b>LIMIT 100</b>：一次不捞太多；一万单到期变成 100 批，而不是一个长事务。"),
                ("<b>zrem only after success</b>: if the process dies mid-way, the entry is still there and "
                 "the next tick retries it.",
                 "<b>成功才 zrem</b>：进程中途挂了条目还在，下一秒自然重试。"),
                ("<b>lock is per order</b>: not one global lock, or you serialise every order in the system.",
                 "<b>锁按订单加</b>：不要一把全局锁，否则全站订单排队。"),
            ]),
        ]),
        ("h2", "04", "The two races you must name", "必须点名的两个竞态", [
            ("p", "Anyone can build the timer. The senior part is what happens when the callback and the "
                  "timer land together.",
             "定时器谁都会做。真正分水平的是：支付回调和关单任务撞在同一秒时怎么办。"),
            ("table",
             [("Race", "竞态"), ("Who wins", "谁赢"), ("What you do", "怎么做")],
             [
                 [("Timer closes it, then the payment callback arrives",
                   "关单先改成功，支付回调后到"),
                  ("The order is already CLOSED, so the CAS updates 0 rows.",
                   "订单已是 CLOSED，CAS 影响 0 行。"),
                  ("Money arrived for a closed order — <b>refund</b>, and say it out loud in the interview.",
                   "钱到了但单子关了——<b>走退款</b>，面试时要把这句话说出来。")],
                 [("Callback marks it PAID, then the timer fires",
                   "回调先改成 PAID，定时任务后到"),
                  ("The CAS condition <code>status='PENDING'</code> fails, so the timer does nothing.",
                   "CAS 条件是 <code>status='PENDING'</code>，不成立，定时任务什么都不做。")],
             ]),
            ("note", "Both directions are handled by the same <code>where status='PENDING'</code>. "
                     "That is why the interview answer must include the CAS even though the question is about a timer.",
             "两个方向都被同一个 <code>where status='PENDING'</code> 挡住了。"
             "所以哪怕问的是定时器，答案里也必须带 CAS。"),
            ("p", "And the second race: two app instances polling the same Redis. Both see the same order id.",
             "第二个竞态：两个实例轮询同一个 Redis，同时捞到同一个订单号。"),
            ("ul", [
                ("The distributed lock makes only one of them work on it.",
                 "分布式锁让只有一个实例真的去处理。"),
                ("Even if the lock is lost (failover), the CAS still makes the second one a no-op.",
                 "就算锁丢了（主从切换），CAS 也会让第二个变成空操作。"),
                ("Two layers, and neither of them is “I added a lock, done”.",
                 "两层，而且都不是“我加了把锁就完事”。"),
            ]),
        ]),
        ("h2", "05", "Four follow-ups, one line each", "四个追问，一句话一个", [
            ("table",
             [("Follow-up", "追问"), ("One-line answer", "一句话答案")],
             [
                 [("Why not sleep a thread for 30 minutes?", "为什么不直接 sleep 30 分钟？"),
                  ("One thread per order; 100k orders is 100k threads, and a restart loses them all.",
                   "一单一个线程；十万单就是十万个线程，重启全丢。")],
                 [("What if an entry is lost from Redis?", "Redis 丢了条目怎么办？"),
                  ("A daily compensation scan over PENDING orders older than 30 minutes — it is the safety net, "
                   "and it is allowed to be slow.",
                   "每天一次补偿扫描，捞 30 分钟前还没结束的 PENDING 单——它是安全网，可以慢。")],
                 [("What about the RabbitMQ delay queue?", "RabbitMQ 的延迟队列怎么做？"),
                  ("Two ways: per-message TTL + dead-letter exchange, or the delayed-message plugin. "
                   "The first has head-of-line blocking; the second is an extra plugin.",
                   "两种：消息 TTL + 死信交换机，或延迟插件。前者会队头阻塞，后者要装插件。")],
                 [("100k due at once?", "十万单同时到期？"),
                  ("Bit by minute: keys like <code>order:delay:2026102910:47</code>, and enqueue batch updates.",
                   "按分钟分桶：<code>order:delay:2026102910:47</code>，入队用批量写。")],
             ]),
        ]),
        ("h2", "06", "60-second script", "60 秒照念稿", [
            ("quote", "read", "Read this out loud", "照这段说，60 秒",
             [("We do not scan the table. At checkout the order id goes into a Redis sorted set with the due "
               "timestamp as the score; a job runs once a second, pulls up to 100 due ids, and for each one "
               "takes a Redisson lock, closes it with an update whose where-clause is status='PENDING', rolls the "
               "stock back, and only then removes the entry from the set.\n\n"
               "The where-clause is the important part: if the payment callback already marked it paid, the "
               "update touches 0 rows and we do nothing; if we closed it first and the callback arrives after, "
               "the money is there for a closed order and we refund.\n\n"
               "We chose this over a RabbitMQ delay queue because the project already had Redis and adding "
               "TTL+DLX or the delayed-message plugin is another thing to operate. The trade-off is polling and "
               "no delivery guarantee, so there is a daily compensation scan over stale pending orders, and the "
               "CAS makes a double close harmless.",
               "我们不扫表。下单时把订单号写进 Redis 有序集合，score 存到期时间戳；一个每秒跑的任务一次捞最多 100 个"
               "到期的 id，逐个加 Redisson 锁，用 where 条件里带 status='PENDING' 的更新去关单、回滚库存，成功后才从集合里删掉。\n\n"
               "那个 where 条件是关键：如果支付回调已经把它改成已支付，这条更新影响 0 行，我们什么都不做；"
               "如果我们先关了、回调后到，钱到了但单子已关，就走退款。\n\n"
               "没选 RabbitMQ 延迟队列，是因为项目里本来就有 Redis，而 TTL+DLX 或延迟插件是多一套要运维的东西。"
               "代价是轮询和不保证投递，所以加了每天一次的补偿扫描，并且用 CAS 让重复关单变得无害。")]),
        ]),
        ("h2", "07", "Where this sits on my résumé", "怎么挂到我自己的项目上", [
            ("p", "One line on the résumé, four things you can now defend:",
             "简历上只有一行，现在你能守住四件事："),
            ("ul", [
                ("The line: “用 Redis 延时队列做订单超时关单，替代轮询：超时 30 分钟自动取消并回滚库存”.",
                 "原句：“用 Redis 延时队列做订单超时关单，替代轮询：超时 30 分钟自动取消并回滚库存”。"),
                ("Why not scan: index, pressure, one-cycle latency.",
                 "为什么不扫表：用不上索引、压库、差一个周期。"),
                ("Why not MQ: the project already had Redis; TTL+DLX or a plugin is extra machinery.",
                 "为什么不用 MQ：项目已有 Redis；TTL+DLX 或插件是多出来的运维。"),
                ("How it stays safe: per-order lock + status CAS + daily compensation scan.",
                 "怎么保证不出错：按单加锁 + 状态 CAS + 每日补偿扫描。"),
            ]),
            ("note", "订单系统和好气网都用了 Redisson, so “I know Redisson” is already on the résumé — "
                     "this question is where it turns from a keyword into a mechanism.",
             "订单系统和好气网都写了 Redisson，所以“我会 Redisson”本来就在简历上——"
             "这道题就是把那个词变成机制的地方。"),
        ]),
        ("h2", "08", "Three things not to say", "三句别说", [
            ("ul", [
                ("“I run a scheduled job every minute.” — Then you scan the whole table; say how you avoid it.",
                 "“我起个定时任务每分钟跑一次。”——那就是扫全表；要说出你怎么避免。"),
                ("“Redis is reliable, so nothing is lost.” — A failover can drop entries; name the compensation.",
                 "“Redis 很可靠，不会丢。”——主从切换会丢；要说出补偿。"),
                ("“The lock guarantees it closes once.” — Locks fail; the CAS is what makes it once.",
                 "“加锁就能保证只关一次。”——锁会失效；保证“只关一次”的是 CAS。"),
            ]),
        ]),
    ],
    "words": [
        ("delay queue", "/dɪˈleɪ kjuː/", "A queue that hands an item back at a chosen time.", "延时队列：到点才把任务交出来"),
        ("sorted set", "/ˈsɔːrtɪd set/", "A Redis structure kept in order by a score.", "有序集合：按 score 排好序的集合"),
        ("poll", "/poʊl/", "Ask again and again on a timer.", "轮询：定着时间反复问"),
        ("compensation", "/ˌkɑːmpenˈseɪʃn/", "A slow backup job that fixes what was missed.", "补偿：事后兜底的慢任务"),
        ("dead letter", "/ded ˈletər/", "A message that failed too many times.", "死信：重试太多次的消息"),
        ("head-of-line blocking", "/hed əv laɪn/", "One slow item blocks everything behind it.", "队头阻塞：前面卡住，后面全堵"),
    ],
    "checks": [
        ("为什么不每分钟扫全表？说出三个代价。", "为什么不每分钟扫全表？说出三个代价。"),
        ("关单和支付回调撞在同一秒，两种顺序各怎么处理？", "关单和支付回调撞在同一秒，两种顺序各怎么处理？"),
        ("为什么不用 RabbitMQ 延迟队列？说清代价和你怎么补。", "为什么不用 RabbitMQ 延迟队列？说清代价和你怎么补。"),
    ],
    "next": '<a href="redis-cache.html"><span class="in-en">← Question 3: cache</span>'
            '<span class="in-zh">← 第 3 题：缓存</span></a>',
}
