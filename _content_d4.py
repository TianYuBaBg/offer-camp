# -*- coding: utf-8 -*-
"""第 4 题（订单超时关单）的 6 个追问，各自成页。"""

CRUMB = ('<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
         '<a href="order-timeout.html"><span class="in-en">Q4</span><span class="in-zh">第 4 题</span></a> / ')

BACK = ('<a href="order-timeout.html"><span class="in-en">&#8592; Back to question 4</span>'
        '<span class="in-zh">&#8592; 回到第 4 题</span></a>')


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


D4 = [
    P("d4-zset-as-delay-queue.html", 1, "ZSet as a delay queue", "ZSet 当延时队列",
      "A sorted set is a timer with an index.", "有序集合就是“带索引的定时器”。",
      "score is the due timestamp, so the earliest-due orders sit at the front of the range.",
      "score 就是到期时间戳，所以最早到期的单永远排在范围查询的最前面。",
      "ZADD puts an order in with score = due time (ms). ZRANGEBYSCORE ... LIMIT pulls the ones already due. "
      "Ordering is maintained by the skiplist, so “what is due now” is O(log N) instead of a full scan.",
      "ZADD 入队时把 score 设成到期时间戳；ZRANGEBYSCORE 按 score 范围取已到期的。"
      "有序性由跳表维护，所以“现在谁到期了”是 O(log N)，不用扫全表。",
      "ZSet 天然按 score 有序，score 存到期时间戳，就能按时间取到期的单；入队和取件都是 O(log N)，"
      "比每分钟扫全表省得多，也不需要多一个中间件。",
      "ZSet 天然按 score 有序，score 存到期时间戳，就能按时间取到期的单；入队和取件都是 O(log N)，"
      "比每分钟扫全表省得多，也不需要多一个中间件。",
      [
          ("The four commands", "四条命令搞定", [
              ("pre", "-- 入队：到期时间作为 score\n"
                      "ZADD order:delay <due_ms> \"<orderNo>\"\n\n"
                      "-- 取件：score <= now 的，最多 100 条\n"
                      "ZRANGEBYSCORE order:delay 0 <now_ms> LIMIT 0 100\n\n"
                      "-- 处理成功后移除\n"
                      "ZREM order:delay \"<orderNo>\"\n\n"
                      "-- 取消订单时也移除\n"
                      "ZREM order:delay \"<orderNo>\""),
              ("p", "Nothing else is needed: no table scan, no scheduler table, no polling of the orders table.",
               "不需要别的：不扫表、不建定时任务表、不轮询订单表。"),
          ]),
          ("Compared with a DB scan", "和扫表比", [
              ("table", [("", ""), ("DB scan every minute", "每分钟扫表"), ("Redis ZSet", "Redis ZSet")], [
                  [("cost", "成本"), ("full scan hits rows", "扫到整张表"), ("range query only", "只查范围内")],
                  [("precision", "精度"), ("up to 60s late", "最多晚 60 秒"), ("sub-second", "亚秒级")],
                  [("extra component", "额外组件"), ("none", "无"), ("Redis (usually already there)", "Redis（一般已有）")],
              ]),
          ]),
      ]),

    P("d4-two-instances.html", 2, "Two instances", "两个实例重复关单",
      "The lock reduces collisions; the CAS removes them.", "锁减少碰撞，CAS 消除碰撞。",
      "Both instances may pull the same order id. A per-order lock makes one of them skip; the CAS makes the "
      "second one harmless even if the lock fails.",
      "两个实例可能同时取到同一个订单号。按单加锁让其中一个让路；就算锁失效，CAS 也让第二个变空操作。",
      "Lock key is per order (lock:order:close:<id>), not global — a global lock serialises the whole system. "
      "Inside the lock: read status, conditional update, restore stock, ZREM. Outside: nothing.",
      "锁的 key 按订单维度（lock:order:close:<id>），不能全局——全局锁会把整站串起来。"
      "锁内做：读状态、条件更新、回补库存、ZREM；锁外不做业务。",
      "两个实例同时捞到同一单：先按订单号加 Redisson 锁，只有一个进去；进去再走状态 CAS，"
      "只有 PENDING 能改 CLOSED。锁丢了也不怕，CAS 让第二个变成空操作。",
      "两个实例同时捞到同一单：先按订单号加 Redisson 锁，只有一个进去；进去再走状态 CAS，"
      "只有 PENDING 能改 CLOSED。锁丢了也不怕，CAS 让第二个变成空操作。",
      [
          ("Inside the lock", "锁里做什么", [
              ("pre", "lock = redisson.getLock(\"lock:order:close:\" + orderNo);\n"
                      "if (!lock.tryLock(0, 10, TimeUnit.SECONDS)) return;   // 别人在处理，跳过\n"
                      "try {\n"
                      "    int n = mapper.casClose(orderNo);            // where status='PENDING'\n"
                      "    if (n == 0) return;                         // 已经关过 / 已支付\n"
                      "    stockMapper.restore(skuId);                 // 回补库存\n"
                      "    redis.zrem(\"order:delay\", orderNo);        // 出队\n"
                      "} finally { lock.unlock(); }"),
              ("note", "Try-lock with zero wait: if another instance is already on it, skipping is the correct behaviour.",
               "等待时间设 0：别人正在处理，跳过就是正确行为。"),
          ]),
      ]),

    P("d4-race-with-callback.html", 3, "Race with the callback", "关单和回调撞上",
      "Two writers, one row, one winner.", "两个写者、一行数据、一个赢家。",
      "Both the close job and the payment callback try to move the same order. Whoever's CAS returns 1 wins; "
      "the other sees the new status and takes the other branch.",
      "关单任务和支付回调都在改同一个订单。谁的条件更新先成功谁赢；另一个读到新状态，走另一条分支。",
      "Close first: status becomes CLOSED, then the callback's CAS gets 0 rows and it refunds. "
      "Callback first: status becomes PAID, then the close job's CAS gets 0 rows and it does nothing.",
      "关单先成功：状态是 CLOSED，回调的 CAS 影响 0 行，走退款。"
      "回调先成功：状态是 PAID，关单任务的 CAS 影响 0 行，什么都不做。",
      "关单和支付回调撞上，靠 where status='PENDING' 决出胜负：先成功的赢，后到的看状态走退款或直接退出。"
      "这也是为什么定时器里必须带 CAS，不能直接 update。",
      "关单和支付回调撞上，靠 where status='PENDING' 决出胜负：先成功的赢，后到的看状态走退款或直接退出。"
      "这也是为什么定时器里必须带 CAS，不能直接 update。",
      [
          ("The two orders", "两种顺序", [
              ("table", [("Order of events", "先后"), ("Result", "结果")], [
                  [("close wins", "关单先"), ("CLOSED → callback sees 0 rows → refund", "CLOSED → 回调 0 行 → 退款")],
                  [("callback wins", "回调先"), ("PAID → close sees 0 rows → nothing", "PAID → 关单 0 行 → 什么都不做")],
              ]),
              ("p", "Note the asymmetry: one branch must refund, the other must do nothing. Both are “safe”, "
                    "but only one is correct behaviour.",
               "注意两边不对称：一边必须退款，一边必须什么都不做。都“安全”，但只有一个是对的。"),
          ]),
      ]),

    P("d4-zset-size.html", 4, "Ten thousand entries", "ZSet 十万条",
      "Split the key by minute; never hold one giant ZSet.", "按分钟分 key，不要一个巨型 ZSet。",
      "A single ZSet with millions of members is fine for range queries but expensive to inspect and impossible "
      "to expire per-shard.", "单个 ZSet 存几百万条，范围查询还行，但排查困难、也没法按片过期。",
      "Shard by due-minute: order:delay:2026102905:37. Writes go to the shard; the poller only scans the current "
      "and previous minute shards, then deletes empty ones. Memory stays bounded and inspection stays easy.",
      "按到期分钟分片：order:delay:2026102905:37。写入进分片；轮询只看当前和上一分钟的分片，"
      "空了就删。内存有界，排查也容易。",
      "十万条本身不是问题，问题是排查和过期。我们按分钟分 key，轮询只看当前和上一分钟，"
      "处理完删空分片，单个 key 始终很小。",
      "十万条本身不是问题，问题是排查和过期。我们按分钟分 key，轮询只看当前和上一分钟，"
      "处理完删空分片，单个 key 始终很小。",
      [
          ("Shard by minute", "按分钟分片", [
              ("pre", "-- 入队\n"
                      "String shard = \"order:delay:\" + dueMinute(orderNo);   // yyyyMMddHHmm\n"
                      "redis.zadd(shard, dueMs, orderNo);\n\n"
                      "-- 轮询：只看这两个分片\n"
                      "for (String s : List.of(shardOf(now), shardOf(now - 60_000))) {\n"
                      "    ids = redis.zrangeByScore(s, 0, nowMs, 0, 100);\n"
                      "}\n\n"
                      "-- 分片空了就删，避免无限增长\n"
                      "if (redis.zcard(s) == 0) redis.del(s);"),
              ("note", "Also cap the batch (LIMIT 100): a million due at once should become ten thousand pulls, "
                       "not one giant transaction.",
               "每批还要限额（LIMIT 100）：一次到期一百万，应该是一万次拉取，而不是一个巨型事务。"),
          ]),
      ]),

    P("d4-rabbitmq-ttl.html", 5, "RabbitMQ delay", "RabbitMQ 延迟",
      "TTL + dead-letter, or the delayed-message plugin.", "TTL + 死信，或者 delayed-message 插件。",
      "RabbitMQ has no native delay. Either let a message expire into a dead-letter exchange, or install the "
      "delayed-message plugin.", "RabbitMQ 没有原生延迟。要么让消息在队列里过期进死信交换机，要么装延迟消息插件。",
      "Option A: publish with per-message TTL (or a queue TTL) and route expired messages to a DLX consumer — "
      "cheap, no plugin, but a long-TTL message at the head blocks shorter ones behind it (head-of-line). "
      "Option B: rabbitmq_delayed_message_exchange plugin supports arbitrary delay per message, but you must "
      "install and operate it.", "方案 A：消息带 TTL（或队列 TTL），过期后进死信交换机被消费——不用装插件，"
      "但长 TTL 消息在队头会阻塞后面的短 TTL（队头阻塞）。"
      "方案 B：装 rabbitmq_delayed_message_exchange 插件，支持任意延迟，但要多运维一个插件。",
      "RabbitMQ 做延迟两种：TTL + 死信交换机（不用装插件，但队长 TTL 会阻塞），"
      "或者 delayed-message 插件（灵活，要多运维）。我们项目里已有 Redis，就直接用 ZSet。",
      "RabbitMQ 做延迟两种：TTL + 死信交换机（不用装插件，但队长 TTL 会阻塞），"
      "或者 delayed-message 插件（灵活，要多运维）。我们项目里已有 Redis，就直接用 ZSet。",
      [
          ("Side by side", "两种方式对比", [
              ("table", [("", ""), ("TTL + DLX", "TTL + 死信"), ("delayed plugin", "延迟插件")], [
                  [("install", "安装"), ("none", "不用"), ("needs plugin", "要装插件")],
                  [("per-message delay", "每条不同延迟"), ("yes (queue-level TTL differs)", "可以，但要注意队头"), ("yes", "可以")],
                  [("risk", "风险"), ("head-of-line blocking", "队头阻塞"), ("plugin ops cost", "插件运维成本")],
              ]),
              ("note", "This is exactly the trade the interview wants to hear: choice plus what you gave up.",
               "面试想听的正是这个：选了哪个、放弃了什么。"),
          ]),
      ]),

    P("d4-message-loss.html", 6, "Message loss", "消息丢了兜底",
      "Every queue is a cache, not a ledger.", "队列只是缓存，不是账本。",
      "Assume the delay message can be lost (Redis restart, failover, bug), so the DB must be able to find "
      "stale orders by itself.", "假设延迟消息会丢（Redis 重启、主从切换、代码 bug），所以数据库自己也要能找出超时单。",
      "Daily compensation scan: find PENDING orders older than 35 minutes and close them through the same CAS path. "
      "Because closing is idempotent, double-processing is harmless — the scan is the safety net, the ZSet is the "
      "fast path.", "每日补偿扫描：找出超过 35 分钟还是 PENDING 的单，走同一条 CAS 关单路径。"
      "因为关单幂等，重复处理无害——ZSet 是快路，扫描是安全网。",
      "队列丢了不能靠重发解决，要靠补偿：每天扫一遍“超过 35 分钟还是待支付”的单，走同一套 CAS 关单；"
      "再加支付对账，保证钱和单不会长期不一致。",
      "队列丢了不能靠重发解决，要靠补偿：每天扫一遍“超过 35 分钟还是待支付”的单，走同一套 CAS 关单；"
      "再加支付对账，保证钱和单不会长期不一致。",
      [
          ("The safety net", "安全网长什么样", [
              ("pre", "-- 每天凌晨扫一次（走索引：status + create_time）\n"
                      "select order_no from orders\n"
                      " where status = 'PENDING'\n"
                      "   and create_time < now() - interval 35 minute\n"
                      " limit 500;\n\n"
                      "-- 逐条走同一套关单逻辑（锁 + CAS + 回补库存 + ZREM）"),
              ("ul", [
                  ("The scan is allowed to be slow — it runs once a day, not every second.",
                   "扫描允许慢——一天一次，不是每秒。"),
                  ("35 minutes, not 30: leave a grace window for in-flight callbacks.",
                   "用 35 分钟而不是 30：给在途回调留容忍窗口。"),
                  ("Same code path as the fast path — one implementation, no drift.",
                   "和快路走同一段代码——只有一份实现，不会走偏。"),
              ]),
          ]),
      ]),
]
