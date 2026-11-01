# -*- coding: utf-8 -*-
"""第 2 题「又长出来的问题」第 03–08 条：独立页。"""

from _content_d2 import BACK, CRUMB

D2B = []

# ---------------- 03 钱到了但订单已关闭 ----------------
D2B.append(dict(
    path="questions/d2-paid-but-closed.html",
    title=("Paid, but the order was already closed", "钱到了，单已经关了"),
    crumb=CRUMB + '<span class="in-en">Paid but closed</span><span class="in-zh">已付但已关</span>',
    kicker=("Follow-up 03", "追问 03"),
    h1=("Money landed on an order that timed out 30 seconds ago.",
        "钱到账了，可这单 30 秒前刚超时关掉。"),
    lede=("Do not swallow it, do not silently reopen it. Compare the timestamps, then refund or revive by rule.",
          "既不能吞掉，也不能偷偷重开。比时间戳，按规则退款或者复活。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("CAS returns 0 rows and the status is CLOSED, so this is “paid but cancelled”. Decide by rule: if the close "
            "time is later than the pay time, refund automatically and mark REFUNDING; never leave the money stuck.",
            "CAS 影响 0 行、状态是 CLOSED → 这就是“已付但已取消”。按规则处理：关单时间晚于支付时间就自动退款、"
            "置 REFUNDING；绝不能让钱卡在原地。"),
    blocks=[
        ("h2", "01", "Why it happens at all", "为什么会撞上", [
            ("ul", [
                ("The user paid at 29:58; the timeout job closed the order at 30:01; the callback arrived at 30:02.",
                 "用户 29:58 付款，超时任务 30:01 关单，回调 30:02 才到。"),
                ("Payment succeeded on the platform side even though your order is closed — the two systems decided "
                 "independently.",
                 "支付平台那边成功了，你的订单这边已关闭——两个系统各自独立判断。"),
                ("Clock skew between the pay server and your DB makes “who was first” a real question.",
                 "支付服务器和你数据库的时钟差异，让“谁先”变成一个真问题。"),
            ]),
        ]),
        ("h2", "02", "The decision table", "处理决策表", [
            ("table", [("Condition", "条件"), ("Action", "动作")], [
                [("close_time &lt; pay_time", "关单时间 &lt; 支付时间"),
                 ("the order was closed before the money arrived → refund", "先关单后付款 → 退款")],
                [("close_time &gt; pay_time (within grace)", "关单略晚于付款（容忍窗口内）"),
                 ("revive the order, ship as normal", "复活订单，正常发货")],
                [("product is out of stock by now", "此时货已卖完"),
                 ("refund + notify, offer a replacement", "退款 + 通知，给替代方案")],
            ]),
            ("p", "The grace window exists because closing an order is not instantaneous: you need a few seconds of "
                  "tolerance for callbacks that were already in flight.",
             "容忍窗口的意义：关单不是瞬时的，对“已经在路上的回调”要留几秒余地。"),
        ]),
        ("h2", "03", "Never “fix” it by force", "别用强制手段“修”", [
            ("ul", [
                ("Do not run <code>update orders set status='PAID'</code> without a condition — you lose the history "
                 "and any concurrent job can resurrect it again.",
                 "别不加条件地 <code>update ... set status='PAID'</code>——历史没了，别的任务再把它改回去。"),
                ("Do not return success and do nothing. The platform thinks it is handled; the customer waits forever.",
                 "别回成功却不做事。平台以为处理完了，客户永远等不到货。"),
                ("Refund must itself be idempotent: one out_refund_no per order, same unique-index trick.",
                 "退款本身也要幂等：一单一个 out_refund_no，还是唯一索引那一套。"),
            ]),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "CAS 影响 0 行先看状态：如果已经 CLOSED，说明钱到的时候单子刚关。我们比关单时间和支付时间，"
             "超时关单在前就自动退款、置 REFUNDING；容忍窗口内就复活订单正常发货。退款用一单一个退款号，同样幂等。",
             "CAS 影响 0 行先看状态：如果已经 CLOSED，说明钱到的时候单子刚关。我们比关单时间和支付时间，"
             "超时关单在前就自动退款、置 REFUNDING；容忍窗口内就复活订单正常发货。退款用一单一个退款号，同样幂等。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 04 watchdog 续什么 ----------------
D2B.append(dict(
    path="questions/d2-watchdog.html",
    title=("What the watchdog actually renews", "watchdog 到底在续什么"),
    crumb=CRUMB + '<span class="in-en">Watchdog</span><span class="in-zh">watchdog</span>',
    kicker=("Follow-up 04", "追问 04"),
    h1=("It renews a lease, not “the lock forever”.",
        "它续的是“租约”，不是“锁永久有效”。"),
    lede=("Default lease 30s, renewed every 10s while the holding thread is alive. Kill the process and the lease "
          "simply expires.", "默认 30 秒租约、持锁线程活着就每 10 秒续一次；进程一挂就不再续，30 秒后自动释放。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("Redisson's watchdog pushes the key's TTL back to 30s every 10s (1/3 of the lease) while the lock-holding "
            "thread is alive. It exists so a slow business operation does not lose the lock mid-way — it is not a "
            "promise that the lock never expires.",
            "Redisson 的 watchdog 在持锁线程活着时每 10 秒把 key 的过期时间重置回 30 秒（租约的 1/3）。"
            "它的意义是让慢业务不在中途丢锁，而不是承诺锁永不过期。"),
    blocks=[
        ("h2", "01", "Lease, not ownership", "租约，不是所有权", [
            ("table", [("Term", "概念"), ("Meaning", "含义")], [
                [("lockLeaseTime", "lockLeaseTime"), ("how long the key lives if nobody renews", "没人续的话 key 活多久")],
                [("watchdog period", "续期周期"), ("leaseTime / 3, i.e. every 10s", "leaseTime 的 1/3，即每 10 秒")],
                [("process dies", "进程挂了"), ("no renewal → key expires → lock released", "不再续 → key 过期 → 锁释放")],
            ]),
            ("note", "This is the whole point: a crashed holder must not block the world forever.",
             "核心就在这里：持锁方崩了，绝不能把所有人锁死。"),
        ]),
        ("h2", "02", "The three settings people confuse", "三个容易搞混的设置", [
            ("ul", [
                ("<code>lock.lock()</code> — no lease argument, watchdog enabled, renews forever while alive.",
                 "<code>lock.lock()</code>——不传租期，watchdog 生效，活着就一直续。"),
                ("<code>lock.lock(10, TimeUnit.SECONDS)</code> — fixed lease, <b>watchdog off</b>, unlock after 10s "
                 "even if you are still working.",
                 "<code>lock.lock(10, SECONDS)</code>——固定租期，<b>watchdog 关闭</b>，10 秒后即使你还在干活也会解锁。"),
                ("<code>tryLock(wait, lease, unit)</code> — you choose both; the smaller the lease, the more often "
                 "renewal must succeed.",
                 "<code>tryLock(wait, lease, unit)</code>——等待和租期都自己定；租期越短，续期越不能失败。"),
            ]),
            ("p", "Long jobs plus a fixed lease is the classic bug: the lock releases while the thread is still writing.",
             "长任务 + 固定租期是经典事故：线程还在写，锁已经没了。"),
        ]),
        ("h2", "03", "What it still cannot save you from", "它救不了什么", [
            ("ul", [
                ("A stop-the-world GC pause longer than the lease: the key expires, someone else takes the lock, "
                 "then your thread wakes up and keeps writing.",
                 "超过租期的 Full GC 停顿：key 过期、别人拿到锁，而你的线程醒来继续写。"),
                ("Network partition where renewal packets are lost but the thread is alive.",
                 "网络分区：续期包丢了，线程却还活着。"),
                ("Main-replica switchover: the new master never received the lock write.",
                 "主从切换：新主从来没收到那次加锁写入。"),
            ]),
            ("p", "That is why Redisson locks are a speed bump, not a correctness guarantee. The database's unique "
                  "index and conditional update are still the last line.",
             "所以 Redisson 锁只是减速带，不是正确性保证。兜底的还是数据库唯一索引和条件更新。"),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "watchdog 续的是租约：默认 30 秒，持锁线程活着就每 10 秒续一次，进程挂了自动过期释放。"
             "它的作用是让慢业务别中途丢锁，不是保证锁永不过期。真正兜底还是数据库那层：唯一索引加条件更新。",
             "watchdog 续的是租约：默认 30 秒，持锁线程活着就每 10 秒续一次，进程挂了自动过期释放。"
             "它的作用是让慢业务别中途丢锁，不是保证锁永不过期。真正兜底还是数据库那层：唯一索引加条件更新。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 05 主从切换丢锁 ----------------
D2B.append(dict(
    path="questions/d2-lock-lost-on-failover.html",
    title=("The lock is gone after a failover", "主从切换把锁丢了"),
    crumb=CRUMB + '<span class="in-en">Failover</span><span class="in-zh">主从切换</span>',
    kicker=("Follow-up 05", "追问 05"),
    h1=("Redis replication is asynchronous. The lock you just took may never reach the new master.",
        "Redis 主从是异步的。你刚拿的锁，可能根本没同步到新主。"),
    lede=("Two clients then hold “the same” lock and both walk into the critical section. No lock library can prevent "
          "that — only the storage layer can.", "于是两个客户端同时“持”着同一把锁，双双进临界区。这没法靠锁库解决，只能靠存储层。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("Async replication means an ack’d lock write can be lost on failover, so two holders may exist. Mitigate with "
            "a fencing token or keep the final guard in the database (unique index / conditional update).",
            "异步复制意味着已确认的加锁写入，切换后可能丢，于是可能出现两个持有者。缓解办法：fencing token，"
            "或者把最后一道防线留在数据库（唯一索引 / 条件更新）。"),
    blocks=[
        ("h2", "01", "The exact failure", "失败是怎么发生的", [
            ("pre", "1. C1 -> master: SET lock:order:1001 C1 NX PX 30000   -> OK\n"
                     "2. master crashes before replicating to the replica\n"
                     "3. replica promoted; the key is simply not there\n"
                     "4. C2 -> new master: SET lock:order:1001 C2 NX PX 30000  -> OK\n"
                     "5. C1 and C2 both believe they hold the lock"),
            ("p", "This is not a Redisson bug. It is the cost of using an in-memory store with asynchronous replication "
                  "as a lock service.",
             "这不是 Redisson 的 bug，而是“用异步复制的内存库当锁服务”必然付的代价。"),
        ]),
        ("h2", "02", "Fencing token: make the loser harmless", "fencing token：让输的那个无害", [
            ("ul", [
                ("Every lock acquisition gets a monotonically increasing number (the fencing token).",
                 "每次拿到锁都领一个单调递增的号（fencing token）。"),
                ("Every write carries it: <code>update sku_stock set qty = qty - 1, version = 12 "
                 "where sku_id = 1001 and version &lt; 12</code>.",
                 "每次写都带上它：<code>update ... where ... and version &lt; 12</code>。"),
                ("A stale holder's write is rejected by the storage layer, not by the lock.",
                 "过期持有者的写入会被存储层拒绝，而不是靠锁拒绝。"),
            ]),
            ("note", "This is the pattern Kleppmann argued for: the lock may be wrong, the write must not be.",
             "Kleppmann 争的就是这个：锁可以错，写入不能错。"),
        ]),
        ("h2", "03", "The cheaper version: let the DB decide", "更省事的版本：让数据库裁决", [
            ("pre", "-- 扣库存：条件更新本身就是幂等闸门\n"
                     "update sku_stock set qty = qty - 1\n"
                     " where sku_id = 1001 and qty >= 1;      -- 影响 0 行 = 卖完了\n\n"
                     "-- 一人一单：唯一索引兜底\n"
                     "insert into seckill_order(sku_id, user_id) values(1001, 7);  -- 重复直接拒绝"),
            ("p", "If the critical section is a single conditional update, you often do not need the distributed lock at "
                  "all — and then failover cannot hurt you.",
             "如果临界区就是一条条件更新，常常根本不需要分布式锁——那主从切换也伤不到你。"),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "Redis 主从是异步复制，加锁成功但没同步过去，切换后锁就没了，可能两个客户端都以为自己持锁。"
             "我们的做法是锁只当减速带，最后一道防线放数据库：条件更新影响行数、唯一索引，必要时带 fencing token。"
             "锁失效时，写入依然只会成功一次。",
             "Redis 主从是异步复制，加锁成功但没同步过去，切换后锁就没了，可能两个客户端都以为自己持锁。"
             "我们的做法是锁只当减速带，最后一道防线放数据库：条件更新影响行数、唯一索引，必要时带 fencing token。"
             "锁失效时，写入依然只会成功一次。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 06 MQ 消费重复 ----------------
D2B.append(dict(
    path="questions/d2-mq-duplicate.html",
    title=("MQ delivery is at-least-once", "MQ 消费重复"),
    crumb=CRUMB + '<span class="in-en">MQ duplicate</span><span class="in-zh">MQ 重复</span>',
    kicker=("Follow-up 06", "追问 06"),
    h1=("Same disease, different delivery channel.", "同一个病，只是换了个投递渠道。"),
    lede=("A queue guarantees “at least once”, never “exactly once”. So the consumer must be idempotent — the pattern "
          "is the same one you used for the payment callback.", "队列保证的是“至少一次”，不是“恰好一次”。所以消费端必须幂等——和你处理支付回调是同一套。"),
    tags=[("must know", "必背"), ("2 min", "2 分钟")],
    answer=("Duplicate consumption comes from ack loss, rebalance, producer retry, or manual re-delivery. Fix it in the "
            "consumer: a business unique key or a state machine — never rely on the queue to deliver once.",
            "重复消费来自 ack 丢失、rebalance、生产端重试、人工重投。在消费端解决：业务唯一键或状态机——"
            "不能指望队列“只投一次”。"),
    blocks=[
        ("h2", "01", "Where duplicates come from", "重复从哪来", [
            ("table", [("Cause", "原因"), ("What happens", "发生什么")], [
                [("ack lost", "ack 丢了"), ("message redelivered although processed", "处理过了但被重投")],
                [("consumer rebalance", "消费者 rebalance"),
                 ("unacked messages go to another consumer", "未 ack 的消息转给别人")],
                [("producer retry", "生产端重试"), ("same logical event sent twice", "同一个业务事件发两次")],
                [("manual replay", "人工重放"), ("ops re-sends from the console", "运维在控制台重投")],
            ]),
        ]),
        ("h2", "02", "The consumer skeleton", "消费端骨架", [
            ("pre", "@RabbitListener(queues = \"order.paid\")\n"
                     "public void onPaid(OrderPaidEvent e) {\n"
                     "    // ① 业务唯一键去重（和支付回调同一个思路）\n"
                     "    int n = mapper.insertIgnore(e.getBizNo());\n"
                     "    if (n == 0) { ack(); return; }        // 处理过，直接 ack\n\n"
                     "    // ② 状态机只允许往前走一步\n"
                     "    if (orderMapper.casToPaid(e.getOrderNo()) == 0) { ack(); return; }\n\n"
                     "    // ③ 真正的业务，本身也要幂等\n"
                     "    stockService.deduct(e.getSkuId());\n"
                     "    ack();"),
            ("note", "Two things must both be true: the message may repeat, and the handler must not care.",
             "两件事同时成立：消息可能重复，处理逻辑必须不介意。"),
        ]),
        ("h2", "03", "Do not do these", "别这么做", [
            ("ul", [
                ("“The queue says it delivers once.” It does not. No mainstream MQ does.",
                 "“队列说只投一次。”它没说。主流 MQ 都没有。"),
                ("Deduplicating by message id only. The same business event may arrive with different ids.",
                 "只按 message id 去重。同一个业务事件，id 可能不同。"),
                ("Ack before the work finishes. A crash then loses the message for good.",
                 "活没干完先 ack。崩了就永久丢消息。"),
            ]),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "所有 MQ 都是至少一次投递，重复来自 ack 丢失、rebalance、生产端重试。我们在消费端做幂等："
             "业务唯一键插入去重，再走状态 CAS，最后业务本身也是条件更新。队列只管不丢，去重是消费方的责任。",
             "所有 MQ 都是至少一次投递，重复来自 ack 丢失、rebalance、生产端重试。我们在消费端做幂等："
             "业务唯一键插入去重，再走状态 CAS，最后业务本身也是条件更新。队列只管不丢，去重是消费方的责任。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 07 库存只扣一次、不超卖 ----------------
D2B.append(dict(
    path="questions/d2-stock-once.html",
    title=("Deduct stock once, never oversell", "库存只扣一次、不超卖"),
    crumb=CRUMB + '<span class="in-en">Stock</span><span class="in-zh">库存</span>',
    kicker=("Follow-up 07", "追问 07"),
    h1=("One conditional update does both jobs.",
        "一条条件更新，同时解决“只扣一次”和“不超卖”。"),
    lede=("`where qty >= 1` prevents overselling. Its idempotence comes from the caller: the deduction only runs "
          "after you have won the state transition.",
          "`where qty >= 1` 防超卖；它的幂等来自调用方——只有抢到了状态流转，才允许扣。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("Oversell is prevented by the condition (qty >= 1 → 0 rows means sold out). Deduct-once is guaranteed by "
            "only deducting after the CAS to PAID succeeds — the second callback never reaches the deduction.",
            "防超卖靠条件（qty >= 1，影响 0 行就是卖完）；只扣一次靠“CAS 改状态成功之后才扣”——"
            "第二条回调根本走不到扣减那一步。"),
    blocks=[
        ("h2", "01", "Two guarantees, two mechanisms", "两个保证，两个机制", [
            ("table", [("Goal", "目标"), ("Mechanism", "机制")], [
                [("never oversell", "不超卖"), ("<code>where qty &gt;= 1</code> + check affected rows", "条件 + 看影响行数")],
                [("deduct once", "只扣一次"), ("only after CAS PENDING→PAID returns 1", "CAS 成功之后才扣")],
                [("roll back on cancel", "取消回滚"), ("compensating update with the same condition", "同一条件的补偿更新")],
            ]),
            ("note", "A conditional update is self-checking: it either changes one row or tells you why not.",
             "条件更新自带检查：要么改了一行，要么告诉你为什么不行。"),
        ]),
        ("h2", "02", "Redis first, DB last", "Redis 先挡，数据库兜底", [
            ("pre", "-- ① Redis 预扣（挡流量，不保证最终正确）\n"
                     "Long left = redis.decrement(\"stock:1001\");   // &lt; 0 就直接返回售罄\n\n"
                     "-- ② 数据库扣减（最终裁决）\n"
                     "update sku_stock set qty = qty - 1\n"
                     " where sku_id = 1001 and qty >= 1;      // 0 行 = 真没了，回滚 Redis 并告警\n\n"
                     "-- ③ 取消/关单：把扣掉的加回去\n"
                     "update sku_stock set qty = qty + 1\n"
                     " where sku_id = 1001 and order_no = ?;  -- 带订单号防重复回滚"),
            ("p", "Redis is the bouncer (fast, approximate). MySQL is the judge (slow, exact). Never trust the bouncer "
                  "for the final count.",
             "Redis 是门卫（快、近似），MySQL 是法官（慢、精确）。最终数字绝不能只信门卫。"),
        ]),
        ("h2", "03", "The classic oversell story", "经典超卖怎么来的", [
            ("ul", [
                ("Read qty, check in Java, then write qty-1. Two threads read 1, both write 0, both sold.",
                 "先读 qty、在 Java 里判断、再写 qty-1。两个线程都读到 1，都写成 0，都卖出去了。"),
                ("Fix: move the check into the WHERE clause so the database does it atomically.",
                 "修法：把判断挪进 WHERE，让数据库原子地做。"),
                ("Or lock the row (<code>for update</code>) — correct but slower, and it serialises the hot SKU.",
                 "或者锁行（<code>for update</code>）——正确但更慢，而且把热点 SKU 串行化。"),
            ]),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "防超卖靠一条带条件的更新：qty >= 1，影响 0 行就是卖完，不需要先查。只扣一次靠顺序："
             "只有状态 CAS 从 PENDING 改成 PAID 成功的那一次回调，才允许扣库存，第二条回调根本走不到扣减。"
             "取消就做反向补偿，带订单号防重复回滚。",
             "防超卖靠一条带条件的更新：qty >= 1，影响 0 行就是卖完，不需要先查。只扣一次靠顺序："
             "只有状态 CAS 从 PENDING 改成 PAID 成功的那一次回调，才允许扣库存，第二条回调根本走不到扣减。"
             "取消就做反向补偿，带订单号防重复回滚。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 08 还有哪些索引 ----------------
D2B.append(dict(
    path="questions/d2-index-types.html",
    title=("What other indexes exist", "还有哪些索引"),
    crumb=CRUMB + '<span class="in-en">Other indexes</span><span class="in-zh">其他索引</span>',
    kicker=("Follow-up 08", "追问 08"),
    h1=("Unique is one of seven. Most of the value is in three of them.",
        "唯一索引只是七种之一，真正天天用的是其中三种。"),
    lede=("Split by purpose first, then by structure. Interviewers usually want the purpose list plus why B+tree won.",
          "先按作用分，再按结构分。面试官通常想听作用那七种，以及 B+ 树为什么赢。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("By purpose: primary (clustered), unique, normal, composite (leftmost prefix), covering, prefix, fulltext. "
            "By structure: mostly B+tree; Memory engine has hash; InnoDB adds adaptive hash. Daily work uses primary + "
            "composite on query order + covering; every index slows writes.",
            "按作用：主键（聚簇）、唯一、普通、联合（最左前缀）、覆盖、前缀、全文。按结构：基本 B+ 树，"
            "Memory 引擎有哈希，InnoDB 还有自适应哈希。生产天天用的是主键 + 按查询顺序的联合索引 + 覆盖索引；"
            "索引越多写入越慢。"),
    blocks=[
        ("h2", "01", "Seven by purpose", "按作用分七种", [
            ("table", [("Index", "索引"), ("What it is for", "干什么用")], [
                [("primary / clustered", "主键 / 聚簇"),
                 ("the table itself in InnoDB; leaf holds the whole row", "InnoDB 里就是表本身，叶子存整行")],
                [("unique", "唯一"), ("enforces uniqueness; NULL is not equal to NULL",
                                      "管唯一性；NULL 彼此不相等")],
                [("normal (secondary)", "普通（二级）"), ("speeds up lookups, leaf holds the primary key",
                                                          "只加速查询，叶子存主键")],
                [("composite", "联合"), ("multi-column, usable by leftmost prefix", "多列，按最左前缀生效")],
                [("covering", "覆盖"), ("all selected columns inside the index, no row lookup",
                                        "查询列全在索引里，不回表")],
                [("prefix", "前缀"), ("long strings indexed by the first N chars", "长字符串只索引前几位")],
                [("fulltext", "全文"), ("inverted index for search", "倒排索引，做搜索")],
            ]),
        ]),
        ("h2", "02", "Why B+tree won", "B+ 树为什么赢", [
            ("ul", [
                ("Short tree: three or four levels cover tens of millions of rows, so three disk reads.",
                 "树矮：三四层覆盖几千万行，也就是三次磁盘读。"),
                ("Leaves are linked in order, so range scans and <code>order by</code> read sequentially.",
                 "叶子有序且相连，范围扫描和 order by 都是顺序读。"),
                ("Hash is O(1) but only equality — no range, no sorting, no leftmost prefix.",
                 "哈希是 O(1) 但只支持等值——没有范围、没有排序、没有最左前缀。"),
            ]),
            ("note", "So: hash for a pure point lookup in memory, B+tree for everything else.",
             "结论：纯内存点查可以用哈希，其余一律 B+ 树。"),
        ]),
        ("h2", "03", "Clustered vs secondary, in one picture", "聚簇 vs 二级，一张图", [
            ("pre", "primary key (clustered):   leaf -> (id, name, price, qty, ...)    整行\n"
                    "secondary index on name:   leaf -> (name, id)  ->  拿 id 回主键树再查一次（回表）\n"
                    "covering (name, price):    leaf -> (name, price)  ->  够了，不回表"),
            ("p", "“Covering” is just a secondary index that already holds everything the query needs. It is the cheapest "
                  "big win in real systems.",
             "“覆盖”就是二级索引里已经带齐了查询要的列——这是线上最便宜的一次大优化。"),
        ]),
        ("h2", "04", "The rules that matter in practice", "实战里真正要记的", [
            ("ul", [
                ("Build composite indexes in the order you filter: equality columns first, range last.",
                 "联合索引按查询顺序建：等值列在前，范围列放最后。"),
                ("Each extra index costs write throughput and disk. Keep the ones that earn their keep.",
                 "多一个索引就多一份写放大和磁盘，只留真正有用的。"),
                ("Watch the plan: <code>explain</code> shows whether the index is used, and “Using index” means covering.",
                 "看执行计划：<code>explain</code> 里 key 是关键，“Using index” 就是覆盖。"),
            ]),
        ]),
        ("h2", "05", "Say it like this", "面试这么说", [
            ("quote", "read",
             "索引按作用分七种：主键、唯一、普通、联合、覆盖、前缀、全文；按结构基本是 B+ 树，"
             "Memory 引擎有哈希，InnoDB 有自适应哈希。生产里真正天天用的是主键加按查询顺序建的联合索引，"
             "再加覆盖索引避免回表。索引不是越多越好，每个都在拖慢写入。",
             "索引按作用分七种：主键、唯一、普通、联合、覆盖、前缀、全文；按结构基本是 B+ 树，"
             "Memory 引擎有哈希，InnoDB 有自适应哈希。生产里真正天天用的是主键加按查询顺序建的联合索引，"
             "再加覆盖索引避免回表。索引不是越多越好，每个都在拖慢写入。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 09 MySQL 的锁 ----------------
D2B.append(dict(
    path="questions/d2-mysql-locks.html",
    title=("What locks exist in MySQL", "MySQL 里的锁"),
    crumb=CRUMB + '<span class="in-en">MySQL locks</span><span class="in-zh">MySQL 的锁</span>',
    kicker=("Follow-up 09", "追问 09"),
    h1=("Every lock in MySQL, on three axes.", "MySQL 里到底有几种锁，各是什么意思。"),
    lede=("Do not memorise the list. Hang it on three axes: granularity — who is locked; mode — how; idea — optimistic or pessimistic.",
          "别背名词。按三根轴搭骨架：粒度（锁谁）、模式（怎么锁）、思想（乐观还是悲观）。"),
    tags=[("must know", "必背"), ("5 min", "5 分钟")],
    answer=("Three levels of granularity: global, table (table lock, MDL, intention lock IS/IX), and row (record lock, gap lock, next-key lock, insert intention lock). Two modes: S shared and X exclusive. And the part that actually bites: row locks sit on index entries — no index, and you lock everything you scan.",
            "粒度三级：全局锁、表级（表锁、MDL 元数据锁、意向锁 IS/IX）、行级（记录锁、间隙锁、临键锁、插入意向锁）。模式两种：S 共享、X 排他。最要命的一句：行锁加在索引上——没走索引，锁的就是扫描到的所有行。"),
    blocks=[
        ("h2", "01", "Three axes, one table", "三根轴，一张表", [
            ("table", [("Axis", "轴"), ("Values", "取值"), ("What it means", "什么意思")], [
                [("granularity", "粒度"), ("global / table / row", "全局 / 表级 / 行级"),
                 ("InnoDB's day job is row level; the other two show up in DDL and backups",
                  "InnoDB 日常用的是行级；另两级出现在 DDL 和备份场景")],
                [("mode", "模式"), ("S shared / X exclusive", "S 共享 / X 排他"),
                 ("S is compatible with S; every other combination is mutually exclusive",
                  "S 与 S 兼容，其余组合一律互斥")],
                [("idea", "思想"), ("optimistic / pessimistic", "乐观 / 悲观"),
                 ("optimistic is a version number or CAS in your code, not an engine lock",
                  "乐观锁是代码里的版本号或 CAS，不是引擎的锁")],
            ]),
            ("note", "Interviewers start with “name the locks” and then drill into row locks. Answer the axes first, then the details — it shows you have a map, not a list.",
             "面试官通常先问“说说有哪些锁”，再往行锁里钻。先答三根轴，再补细节——说明你有地图，不是背清单。"),
        ]),
        ("h2", "02", "The four row locks", "行锁的四种形态", [
            ("ul", [
                ("<b>Record lock</b>: locks one index record. A unique-index equality hit degenerates to exactly this.",
                 "<b>记录锁</b>：锁住一条索引记录。唯一索引等值命中时，加的就是它。"),
                ("<b>Gap lock</b>: locks the open interval between two index records, so it only blocks inserts.",
                 "<b>间隙锁</b>：锁住两条索引记录之间的开区间，只拦插入，不拦别人读。"),
                ("<b>Next-key lock</b>: record lock plus the gap in front of it. The default shape under RR, and what stops phantom reads.",
                 "<b>临键锁</b>：记录锁加上它前面的间隙。RR 下的默认形态，防幻读靠的就是它。"),
                ("<b>Insert intention lock</b>: taken on a gap before inserting, meaning “I am about to insert here”. It conflicts with gap locks held by others.",
                 "<b>插入意向锁</b>：插入前在间隙上加，表示“我要往这里插”。它和别人的间隙锁冲突。"),
            ]),
            ("note", "Gap locks only matter at RR and above. Under RC there is basically only the record lock — which is why RC sees fewer deadlocks and shorter lock waits.",
             "间隙锁只在 RR 及以上有意义。RC 下基本只有记录锁——所以高并发服务里 RC 的死锁和锁等待都更少。"),
        ]),
        ("h2", "03", "The three table-level ones", "表级的三把锁", [
            ("ul", [
                ("<b>Table lock</b> (<code>lock tables ... read/write</code>): the whole table at once. A MyISAM-era tool that InnoDB rarely needs.",
                 "<b>表锁</b>（<code>lock tables ... read/write</code>）：一次锁整表。MyISAM 时代的工具，InnoDB 很少主动用。"),
                ("<b>MDL metadata lock</b>: added automatically. DML takes a read MDL, DDL takes a write MDL — so one long uncommitted transaction can block <code>alter table</code>, and everything queues behind it.",
                 "<b>MDL 元数据锁</b>：自动加的。DML 拿读 MDL、DDL 拿写 MDL——所以一个长事务不提交，就能把 <code>alter table</code> 堵住，后面所有查询跟着排队。"),
                ("<b>Intention lock</b> IS/IX: a table-level flag meaning “some row here is locked”. Without it, deciding whether a table lock is allowed would mean scanning every row.",
                 "<b>意向锁</b> IS/IX：表级的一个标志，说明“这张表里有行被锁了”。没有它，判断能不能加表锁得逐行扫。"),
            ]),
        ]),
        ("h2", "04", "The one people get wrong: locks live on indexes", "最容易答错的一题：锁加在索引上", [
            ("ul", [
                ("With an index, <code>update orders set status = 'PAID' where order_no = 'T100'</code> locks that one entry (or that range).",
                 "有索引时，<code>update orders set status = 'PAID' where order_no = 'T100'</code> 只锁这一条（或这一段）。"),
                ("Without an index, <code>where remark = 'x'</code> scans the whole table — and every scanned row gets locked. That is the “delete without a where clause” of the production world.",
                 "没索引时，<code>where remark = 'x'</code> 全表扫描——扫到多少行就锁多少行。这就是线上版的“不带 where 的 delete”。"),
                ("Debugging: <code>show engine innodb status</code> for LOCK WAIT, and <code>information_schema.innodb_trx</code> to find who is holding it.",
                 "排查：<code>show engine innodb status</code> 看 LOCK WAIT，<code>information_schema.innodb_trx</code> 找谁占着锁。"),
            ]),
            ("note", "A unique-index equality hit only needs a record lock — no gap. That is why “update one row by primary key” is the cheapest write you can make.",
             "唯一索引等值命中只需要记录锁、不加间隙。所以“按主键改一行”是你能写出的最便宜的写操作。"),
        ]),
        ("h2", "05", "Say it like this", "面试这么说", [
            ("quote", "read",
             "Locks split into three granularities: global, table and row — InnoDB works at row level. Four row locks: record, gap, next-key, insert intention. RR takes next-key by default, which is what prevents phantom reads; RC is basically record locks only. At table level the two that matter are MDL and intention locks, and MDL is the main reason DDL and DML fight. The key point: row locks sit on index entries, so an update without an index locks everything it scans.",
             "锁按粒度分三级：全局、表级、行级，InnoDB 日常用的是行级。行级有四种：记录锁、间隙锁、临键锁、插入意向锁；RR 下默认临键锁，防幻读靠的就是它，RC 下基本只有记录锁。表级里真正要记的是 MDL 和意向锁，MDL 是 DDL 和 DML 打架的主要原因。最关键的一点：行锁加在索引上，update 不走索引就会锁住扫到的所有行。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))
