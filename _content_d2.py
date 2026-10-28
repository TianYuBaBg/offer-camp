# -*- coding: utf-8 -*-
"""第 2 题「又长出来的问题」——每条一个独立页，比折叠答案讲得更深。"""

BACK = ('<a href="pay-callback.html"><span class="in-en">&#8592; Back to question 2</span>'
        '<span class="in-zh">&#8592; 回到第 2 题</span></a>')

CRUMB = ('<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
         '<a href="pay-callback.html"><span class="in-en">Q2</span><span class="in-zh">第 2 题</span></a> / ')

D2 = []

# ---------------- 01 唯一索引当锁 ----------------
D2.append(dict(
    path="questions/d2-unique-index.html",
    title=("Why a unique index works as a lock", "为什么唯一索引能当锁"),
    crumb=CRUMB + '<span class="in-en">Unique index as a lock</span><span class="in-zh">唯一索引当锁</span>',
    kicker=("Follow-up 01", "追问 01"),
    h1=("Why check-then-insert is broken, and the index is not.",
        "为什么“先查再插”有漏洞，而唯一索引没有。"),
    lede=("The window is not in your code — it sits between two statements. The database closes it for you.",
          "漏洞不在你的代码里，而在两条 SQL 之间。数据库替你把这段窗口关掉了。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("Two transactions can both see “not there yet” and both move on. The unique index does the conflict test "
            "inside the B+tree at insert time, atomically — so exactly one wins and the other gets a duplicate-key error.",
            "两个事务都能查到“不存在”，于是都往下走。唯一索引把冲突检测放进 B+tree、放进 insert 那一刻，是原子的——"
            "所以只有一个能成，另一个拿到 duplicate key。"),
    blocks=[
        ("h2", "01", "The window you cannot see", "看不见的那段窗口", [
            ("p", "Under READ COMMITTED a plain <code>select</code> cannot see another transaction's uncommitted row, "
                  "so “check” and “insert” are two separate moments with a gap between them.",
             "READ COMMITTED 下普通 <code>select</code> 看不见别人未提交的行，所以“查”和“插”是两个时刻，中间有缝。"),
            ("pre", "T1: select * from pay_idempotent where out_trade_no = 'T100'   -- 空\n"
                     "T2: select * from pay_idempotent where out_trade_no = 'T100'   -- 也是空\n"
                     "T1: insert ...                                                  -- 成功\n"
                     "T2: insert ...                                                  -- 被唯一索引拒绝\n\n"
                     "-- 先查再插：两个都通过了检查，第二个插进去时才发现重复\n"
                     "-- 唯一索引把它变成数据库层的互斥，不需要你先查"),
            ("p", "Repeating the check inside a transaction does not help either. To make the check meaningful you would "
                  "need <code>select ... for update</code> — a pessimistic lock. If you are going to lock anyway, "
                  "the unique index is cheaper and harder to get wrong.",
             "在事务里再查一次也没用。要让“查”有意义，得 <code>select ... for update</code> 变成悲观锁——"
             "既然都要锁，唯一索引更便宜也更不容易写错。"),
        ]),
        ("h2", "02", "What the index actually does", "索引到底做了什么", [
            ("ul", [
                ("InnoDB keeps the unique key in a B+tree. The insert walks to the leaf and must not find an equal key.",
                 "InnoDB 把唯一键放在 B+tree 里。insert 走到叶子节点，必须找不到相同的键。"),
                ("The check happens <b>inside</b> the insert — there is no gap for another session to sneak in.",
                 "这个检查发生在 insert <b>内部</b>——没有缝给别的会话钻。"),
                ("The loser gets error 1062 (Duplicate entry) and can treat it as “someone else already owns this”.",
                 "输的那个拿到 1062（Duplicate entry），可以直接当成“这份活已经有人认领”。"),
            ]),
            ("note", "One statement, one decision. That is why it is the strongest layer you have.",
             "一条语句一个决定。这就是它比任何应用层判断都硬的原因。"),
        ]),
        ("h2", "03", "The code you actually write", "代码就这么写", [
            ("pre", "try {\n"
                     "    mapper.insert(new PayIdempotent(outTradeNo, source));\n"
                     "} catch (DuplicateKeyException e) {\n"
                     "    return OK;              // 第二条回调：不干活，但必须回成功\n"
                     "}\n\n"
                     "-- 或者一条 SQL 搞定，用影响行数判断\n"
                     "insert into pay_idempotent(out_trade_no, source, created_at)\n"
                     "values(?, ?, now())\n"
                     "on duplicate key update source = source;   -- 0 行 = 重复"),
            ("p", "Both versions give you the same thing: a single statement whose result tells you whether you own this job.",
             "两种写法结果一样：一条语句，返回值就告诉你这份活归不归你。"),
        ]),
        ("h2", "04", "Where people get it wrong", "最容易踩的坑", [
            ("ul", [
                ("Using the auto-increment id as the unique key. Use the <b>business number</b> (out_trade_no), "
                 "or a retry slips straight through.",
                 "拿自增 id 当唯一键。要用<b>业务号</b>（out_trade_no），否则重试能溜过去。"),
                ("A composite unique key containing a nullable column. In MySQL, NULL is never equal to NULL — "
                 "duplicates get in.",
                 "联合唯一键里带可空列。MySQL 里 NULL 不等于 NULL，重复能溜进来。"),
                ("Catching the duplicate and then <b>not</b> answering success. The platform keeps retrying for hours.",
                 "捕到重复却<b>不回成功</b>。平台会一直重试，重试到明天。"),
            ]),
        ]),
        ("h2", "05", "Say it like this", "面试这么说", [
            ("quote", "read",
             "两个事务都能查到“不存在”，所以先查再插一定有窗口。我们用唯一索引把冲突检测交给数据库，"
             "插入那一刻就决定了归属；捕到 duplicate key 就直接回成功，但业务一步都不做。",
             "两个事务都能查到“不存在”，所以先查再插一定有窗口。我们用唯一索引把冲突检测交给数据库，"
             "插入那一刻就决定了归属；捕到 duplicate key 就直接回成功，但业务一步都不做。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))

# ---------------- 02 崩在中间 ----------------
D2.append(dict(
    path="questions/d2-crash-after-idempotent.html",
    title=("Crash after the idempotent record", "幂等记录写了，业务崩了"),
    crumb=CRUMB + '<span class="in-en">Crash in the middle</span><span class="in-zh">崩在中间</span>',
    kicker=("Follow-up 02", "追问 02"),
    h1=("The idempotent record proves it arrived. It proves nothing was finished.",
        "幂等记录只证明“来过了”，不证明“做完了”。"),
    lede=("So a retry must be able to continue from wherever the last attempt stopped. That is the state machine's job.",
          "所以重试必须能从上次停下的地方接着做——这是状态机的活。"),
    tags=[("must know", "必背"), ("3 min", "3 分钟")],
    answer=("The idempotent table deduplicates. The order status says how far the work got. On retry: insert is rejected, "
            "read the status, then continue (PENDING), return success (PAID), or refund (CLOSED).",
            "幂等表负责去重，订单状态负责“做到哪一步”。重试时插入被拒，就看状态：还是 PENDING 就接着做，"
            "已经 PAID 就返回成功，CLOSED 就走退款。"),
    blocks=[
        ("h2", "01", "Four places it can die", "四个可能崩的点", [
            ("table", [("Step", "步骤"), ("If it dies here", "崩在这里会怎样")], [
                [("insert idempotent", "插幂等记录"), ("retry rejected → must continue", "重试被拒 → 必须接着做")],
                [("CAS PENDING→PAID", "改状态 CAS"), ("0 rows on retry → already done", "重试 0 行 → 已处理")],
                [("deduct stock", "扣库存"), ("conditional update is idempotent", "条件更新天然幂等")],
                [("ship / notify", "发货/通知"), ("status is PAID → check shipped flag", "状态已 PAID → 看发货标记")],
            ]),
            ("p", "Each row is a place a process can vanish. The rule: <b>every step can be re-run safely</b>, "
                  "and “where am I” lives in durable storage, not in memory.",
             "每一行都是进程可能消失的地方。原则：<b>每一步都能安全重跑</b>，而“我做到哪了”要落在持久存储里，不在内存里。"),
        ]),
        ("h2", "02", "What the retry actually does", "重试时到底怎么走", [
            ("pre", "-- 回调进来\n"
                     "insert into pay_idempotent(out_trade_no) values(?)   -- 被唯一键拒绝\n\n"
                     "-- 读取当前状态\n"
                     "select status from orders where order_no = ?\n\n"
                     "-- PENDING：上次没做完 → 继续（CAS 改状态、扣库存）\n"
                     "-- PAID   ：已经做完     → 直接回 success\n"
                     "-- CLOSED ：单已关       → 走退款"),
            ("note", "Never branch on “did I see this before”. Branch on “where is the order now”. "
                     "The first is memory; the second is a fact.",
             "不要按“我之前见过没有”分支，要按“订单现在在哪一步”分支。前者是记忆，后者是事实。"),
        ]),
        ("h2", "03", "Why not one big transaction", "为什么不干脆一个大事务", [
            ("ul", [
                ("Stock may live in Redis and shipping calls a third party. Neither joins a local transaction.",
                 "库存可能在 Redis，发货要调第三方，两者都进不了本地事务。"),
                ("Long transactions hold row locks and hurt throughput exactly when traffic is highest.",
                 "长事务握着行锁，偏偏在流量最高的时候拖吞吐。"),
                ("Even a perfect local transaction cannot cover “killed after commit, before the reply”.",
                 "就算本地事务完美，也盖不住“提交后、回复前进程被杀”。"),
            ]),
        ]),
        ("h2", "04", "Say it like this", "面试这么说", [
            ("quote", "read",
             "幂等表只解决重复，不解决做到一半。状态机是第二道闸：只有 PENDING 能改成 PAID，"
             "重试的时候影响 0 行就说明有人做完了，直接返回；状态是 CLOSED 就走退款。所以崩了以后重试是安全的。",
             "幂等表只解决重复，不解决做到一半。状态机是第二道闸：只有 PENDING 能改成 PAID，"
             "重试的时候影响 0 行就说明有人做完了，直接返回；状态是 CLOSED 就走退款。所以崩了以后重试是安全的。"),
        ]),
    ],
    words=[], checks=[], answers=[],
    next=BACK,
))
