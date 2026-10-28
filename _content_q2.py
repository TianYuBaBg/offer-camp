# -*- coding: utf-8 -*-
"""第 2 题：支付回调幂等 + 题目列表页。"""

QUESTION2 = {
    "path": "questions/pay-callback.html",
    "title": ("Same callback, three times", "同一条回调，来了三条"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Question 2: payment callback</span><span class="in-zh">第 2 题：支付回调</span>',
    "kicker": ("Question 2 · must know · payments", "第 2 题 · 必背 · 支付链路"),
    "h1": ("WeChat fires the callback three times: ship once, deduct once.",
           "微信回调同时来三条：只发一次货、库存只扣一次。"),
    "lede": ("One payment, three callbacks. Two of them must do nothing — and must still answer OK.",
             "一次支付，三条回调。其中两条必须什么都不做，而且还得回“成功”。"),
    "tags": [("Must know", "必背"), ("payments", "支付"), ("speak 60s", "60 秒口播"), ("4 follow-ups", "追问 4 个")],
    "on": "q",
    "answer": ("Three layers, in this order: a unique-index idempotent table catches the duplicate, "
               "a status CAS makes the order move forward exactly once, and a distributed lock only covers "
               "the small critical section that touches stock.",
               "三层，顺序不能反：唯一索引的幂等表拦住重复；状态 CAS 让订单只能往前走一次；"
               "分布式锁只包住动库存的那一小段。"),
    "blocks": [
        ("h2", "01", "Why three callbacks at all", "为什么会来三条", [
            ("p", "The payment platform is not rude — it is <b>built to be unreliable</b>. "
                  "If it does not hear an OK, it keeps knocking.",
             "支付平台不是没礼貌，它是<b>按不可靠来设计的</b>：没收到成功应答就一直敲。"),
            ("ul", [
                ("WeChat retries on a schedule: 15s, 15s, 30s, 3m, 10m, 20m, 30m … until it hears success.",
                 "微信按节奏重试：15 秒、15 秒、30 秒、3 分、10 分……一直敲到你说成功。"),
                ("Our own gateway may resend when the response times out.",
                 "我们回包超时，自己的网关也会再发一次。"),
                ("A message queue redelivers when the consumer never acknowledged.",
                 "消息队列没收到 ack，会重投。"),
                ("Two app instances can receive it at the same moment — that is a real race, not a retry.",
                 "两台机器同时收到，这不是重试，是并发。"),
            ]),
            ("note", "So “it will not come twice” is never true. The only useful question is: what happens the second time?",
             "所以“不会来两次”永远不成立。唯一有用的问题是：第二次来的时候，会发生什么？"),
        ]),
        ("h2", "02", "Layer one: the idempotent table", "第一层：幂等表（拿唯一索引当锁）", [
            ("p", "Before doing any work, try to <b>insert a row</b> keyed by the platform trade number. "
                  "The database rejects the second insert — and that rejection <i>is</i> the lock.",
             "干活之前，先拿平台流水号<b>插一行记录</b>。第二次插会被数据库拒掉——这个“拒掉”就是锁。"),
            ("pre", "create table pay_idempotent (\n"
                    "  id           bigint auto_increment primary key,\n"
                    "  out_trade_no varchar(64) not null,   -- 微信/支付宝流水号\n"
                    "  source       varchar(16) not null,   -- wechat / alipay\n"
                    "  created_at   datetime    not null,\n"
                    "  unique key uk_trade (out_trade_no, source)\n"
                    ");"),
            ("p", 'In code it is just <code>insert</code>, and on <code>DuplicateKeyException</code> return success. '
                  'The second callback <b>does no work</b> and still tells the platform “done”.',
             '代码里就是 insert，撞到 <code>DuplicateKeyException</code> 就直接回成功：第二条回调<b>不干活</b>，'
             '却仍然告诉平台“已处理”。'),
            ("note", "Why not <code>select</code> then <code>insert</code>: two threads can both see “not there”. "
                     "The unique index is the only thing the database itself polices.",
             "为什么不用 <code>select</code> 再 <code>insert</code>：两个线程能同时查出“不存在”。"
             "唯一索引是数据库自己把门的东西。"),
        ]),
        ("h2", "03", "Layer two: status CAS", "第二层：状态 CAS（比较再交换）", [
            ("p", "The idempotent row stops duplicates, but it cannot stop a crash halfway. "
                  "The order state machine is the second guard:",
             "幂等表拦得住重复，拦不住“做到一半崩了”。订单状态机是第二道闸："),
            ("pre", "update orders\n"
                    "   set status = 'PAID', pay_time = now()\n"
                    " where order_no = ? and status = 'PENDING';   -- 只有待支付才能改成已支付"),
            ("table", [("Rows updated", "影响行数"), ("What it means", "说明")], [
                [("1", "1"), ("I won — deduct stock, then ship", "我抢到了：扣库存、发货")],
                [("0", "0"), ("Someone already did it — just return OK", "别人处理过：直接回成功")],
                [("0, and status is CLOSED", "0，且状态是已关闭"), ("Money arrived but the order closed — refund", "钱到了但单子关了：走退款")],
            ]),
            ("note", "Check and change live in one statement, so there is no gap for another thread. "
                     "That is also why retrying after a crash is safe.",
             "判断和修改在同一条语句里，中间没有缝给别人插进来。这也是“崩了以后重试是安全的”的原因。"),
        ]),
        ("h2", "04", "Layer three: the lock, only where it is needed", "第三层：锁，只加在该加的地方", [
            ("p", "A Redisson lock is <b>not</b> the first line of defence. It protects the critical section: "
                  "read stock, check, deduct, write back.",
             "Redisson 锁<b>不是</b>第一道防线，它护的是临界区：读库存、判断、扣减、写回。"),
            ("ul", [
                ("The lock key is the <b>business</b> key: <code>lock:stock:{skuId}</code>, not the order number.",
                 "锁的 key 是<b>业务</b>维度：<code>lock:stock:{skuId}</code>，不是订单号。"),
                ("It is held for a few milliseconds of database work — never across an HTTP call.",
                 "只包几毫秒的数据库操作，绝不横跨一次 HTTP 调用。"),
                ("watchdog renews the lease while the thread lives; if the JVM dies, the lease expires.",
                 "watchdog 在线程活着时自动续期；JVM 挂了，租约自然过期。"),
                ("A distributed lock is not free — if one transaction can do it, skip the lock.",
                 "分布式锁不是免费的：一个事务能搞定的事，就别上锁。"),
            ]),
        ]),
        ("h2", "05", "Four follow-ups, one line each", "四个追问，一句话一个", [
            ("table", [("Follow-up", "追问"), ("One-line answer", "一句话答")], [
                [("Where is the lock, and what is the key?", "锁加在哪，key 是什么？"),
                 ("Around the stock deduction only; the key is the sku id.", "只包扣库存那段；key 是 sku id。")],
                [("What if the holder dies?", "持锁的进程挂了怎么办？"),
                 ("The lease expires; watchdog stops renewing. Never rely on a bare expire.", "租约自动过期，watchdog 不再续期。别用裸的 expire。")],
                [("Master fails over and the lock is lost?", "主从切换丢锁怎么办？"),
                 ("Fall back on the database: unique key and CAS still hold.", "靠数据库兜底：唯一键和 CAS 仍然守得住。")],
                [("Could you do it without a lock?", "能不能不上锁？"),
                 ("Yes: <code>update stock set qty = qty - 1 where qty &gt; 0</code>, then check the rows.", "能：<code>update ... where qty &gt; 0</code>，看影响行数。")],
            ]),
        ]),
        ("h2", "06", "The 60-second answer", "60 秒照念稿", [
            ("quote", "read", "Say it in this order", "照着念，再换成自己的话", [
                ("First: duplicates are normal. The platform retries until it hears success, and two instances can get it at once.",
                 "先说重复是常态：平台没收到成功就一直重试，两台机器也可能同时收到。"),
                ("Layer one: insert the trade number into a table with a unique index; a duplicate key just returns success.",
                 "第一层：拿流水号往唯一索引的幂等表里插，撞键就直接回成功。"),
                ("Layer two: a status CAS — only PENDING may become PAID; zero rows means someone else already did it.",
                 "第二层：状态 CAS，只有待支付能改成已支付；影响 0 行说明别人做过了。"),
                ("Layer three: a Redisson lock keyed by sku id around the deduct and write-back; if it is lost on failover, the first two layers still hold.",
                 "第三层：Redisson 按 sku 加锁护住扣减写回；就算主从切换丢锁，前两层还兜着。"),
                ("Stock is deducted once because the CAS decides which callback owns the order, and the idempotent row turns the rest into cheap no-ops.",
                 "库存只扣一次，是因为 CAS 决定这条回调归谁，幂等表把其余的变成廉价空转。"),
            ]),
        ]),
        ("h2", "07", "How to say it as mine", "怎么挂到我自己的项目上", [
            ("p", "Only use what is really on the resume — this hangs on the order system, WeChat Native pay, and Redisson:",
             "只挑简历上真有的。这题挂在订单系统、微信 Native 支付、Redisson 上："),
            ("ul", [
                ("Order system: the state machine plus the unique index on <code>out_trade_no</code>.",
                 "订单系统：状态机 + <code>out_trade_no</code> 唯一索引。"),
                ("WeChat Native pay: the callback is the only place that marks an order paid.",
                 "微信 Native 支付：回调是唯一把订单改成已支付的地方。"),
                ("Redisson: used for the stock critical section, not for the callback entry.",
                 "Redisson：用在库存临界区，不用在回调入口。"),
            ]),
        ]),
        ("h2", "08", "Three things not to say", "三句别说", [
            ("ul", [
                ("“I add a lock, done.” — A lock does not survive a crash or a failover.",
                 "“加个锁就完事了。”——锁挡不住崩溃和主从切换。"),
                ("“I check the order status first, then ship.” — That is the race itself.",
                 "“我先查订单状态，再发货。”——这就是竞态本身。"),
                ("“MQ guarantees no duplicates.” — Most queues give at-least-once, not exactly-once.",
                 "“MQ 能保证不重复。”——多数队列是至少一次，不是恰好一次。"),
            ]),
            ("note", "When you do not know a piece, say how you would check: “I would confirm whether the retry body is re-signed…” "
                     "Honest with a direction beats guessing.",
             "真不会的时候，说你会怎么确认：“我会先确认重试报文是否重新签名……”诚实加方向，比硬编强。"),
        ]),
    ],
    "words": [
        ("idempotent", "/ˌaɪdemˈpoʊtnt/", "Running it twice is the same as running it once.", "幂等：执行两次和执行一次一样"),
        ("callback", "/ˈkɔːlbæk/", "The platform calls us back to say it is paid.", "回调：平台回头通知“已付款”"),
        ("duplicate", "/ˈduːplɪkət/", "The same thing arriving again.", "重复：同一件事又来了"),
        ("unique index", "/juˈniːk ˈɪndeks/", "The database refuses a second copy.", "唯一索引：数据库拒绝第二份"),
        ("compare-and-swap", "/kəmˈper ən swɑːp/", "Change it only if it still looks like this.", "CAS：还是这个样子才允许改"),
        ("oversell", "/ˌoʊvərˈsel/", "Selling more than you have.", "超卖：卖出去的比库存还多"),
    ],
    "checks": [
        ("Why must the second callback still answer success?", "第二条回调为什么必须回成功？"),
        ("What does “0 rows updated” mean in the CAS?", "CAS 影响 0 行是什么意思？"),
        ("Name two things that make a retry after a crash safe.", "崩了以后重试为什么安全？说出两个兜底。"),
    ],
    "next": '<a href="java-hashmap.html"><span class="in-en">← Question 1: HashMap</span>'
            '<span class="in-zh">← 第 1 题：HashMap</span></a>',
}

QINDEX = {
    "path": "questions/index.html",
    "title": ("Questions", "面试题"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Questions</span><span class="in-zh">题目</span>',
    "kicker": ("Questions · one page, one 60-second answer", "面试题 · 一页一道，60 秒讲完"),
    "h1": ("Answer first, then explain why.", "先给结论，再讲为什么。"),
    "lede": ("Every question has the same shape: the one-line answer, the mechanism, the follow-ups, "
             "and a script you can read out loud.",
             "每道题结构一样：一句话答案、机制、追问、一份能照着念的稿。"),
    "tags": [("2 questions", "2 道题"), ("both live", "都已上线")],
    "on": "q",
    "plain": True,
    "blocks": [
        ("h2", "01", "Pick one", "选一道", [
            ("html", '<ul class="qlist">\n'
                     '  <li><a href="java-hashmap.html">\n'
                     '    <span class="num">Question 01 · live</span>\n'
                     '    <span class="t"><span class="in-en">How does HashMap work?</span>'
                     '<span class="in-zh">HashMap 是怎么工作的？</span></span>\n'
                     '    <span class="m"><span class="in-en">Buckets, collisions, resize, thread safety — the opening question.</span>'
                     '<span class="in-zh">桶数组、冲突、扩容、线程安全——开场最常问的那道。</span></span>\n'
                     '  </a></li>\n'
                     '  <li><a href="pay-callback.html">\n'
                     '    <span class="num">Question 02 · live</span>\n'
                     '    <span class="t"><span class="in-en">Same callback three times: ship once, deduct once</span>'
                     '<span class="in-zh">回调来三条：只发一次货、库存只扣一次</span></span>\n'
                     '    <span class="m"><span class="in-en">Idempotent table, status CAS, distributed lock — the payment question.</span>'
                     '<span class="in-zh">幂等表、状态 CAS、分布式锁——支付链路那道。</span></span>\n'
                     '  </a></li>\n'
                     '</ul>'),
            ("note", "New questions are added to the line on the home page. A question gets a page only when it can be said out loud in 60 seconds.",
             "新题会挂到首页那条线上。能 60 秒出声讲完，才配一页。"),
        ]),
    ],
    "words": [],
    "checks": [],
    "next": '<a href="../index.html"><span class="in-en">See the whole line →</span><span class="in-zh">回到首页那条线 →</span></a>',
}
