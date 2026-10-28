# -*- coding: utf-8 -*-
"""首页题目列表 + 每道题长出来的新问题。"""

# 首页：所有题目（按学习顺序），meta 说明它现在是什么状态
QLIST = [
    dict(n="01", t="HashMap 到底是个什么东西？", a="一个桶数组，每个桶挂一条短链；冲突就排队，满了就扩容。",
         m="第 1 题", href="questions/java-hashmap.html"),
    dict(n="02", t="一个 key 怎么就跑到某个桶里？", a="先算 hash，再 h & (n-1) 取下标——所以容量必须是 2 的幂。",
         m="第 4 课", href="basics/hash.html"),
    dict(n="03", t="两个 key 撞进同一个桶，怎么办？", a="排队挂成链表；到 8 个、容量够 64 就转红黑树。",
         m="第 2–3 课", href="basics/tree.html"),
    dict(n="04", t="桶快满了呢？", a="装到 75% 翻倍，每个 key 要么原位、要么 +n，不用重算 hash。",
         m="第 5 课", href="basics/big-o.html"),
    dict(n="05", t="两个线程同时 put 会怎样？", a="丢数据；JDK 7 还会成环把 CPU 打满。换 ConcurrentHashMap。",
         m="第 7 课", href="basics/threads.html"),
    dict(n="06", t="工作中怎么拿它当缓存用？", a="Redis 挡在数据库前面——以及缓存咬你的三种方式。",
         m="待写", href=""),
    dict(n="07", t="微信回调同时来三条，怎么办？", a="幂等表 → 状态 CAS → 再上锁，三层顺序不能反。",
         m="第 2 题", href="questions/pay-callback.html"),
    dict(n="08", t="一万人抢一千件，怎么不超卖？", a="先在 Redis 预扣，数据库做最后一道闸，再拿延时队列关单。",
         m="待写", href=""),
]

# 每道题页尾：这个问题长出来的新问题
DERIVED = {
    "questions/java-hashmap.html": [
        ("为什么容量必须是 2 的幂？", "因为 h & (n-1) 等价于取模，只有在 n 是 2 的幂时成立。", "basics/hash.html"),
        ("为什么要先用 hash 的高 16 位异或一次？", "让高位也参与定位，减少碰撞；否则高位信息浪费。", "basics/hash.html"),
        ("为什么链表到 8 才转红黑树，而不是 4？", "泊松分布下 8 的概率约千万分之六，到 8 说明 hash 有问题；转树也要够贵才划算。", "basics/tree.html"),
        ("为什么退化阈值是 6，不是 7？", "留一格缓冲，避免在 7–8 之间来回转换。", "basics/tree.html"),
        ("为什么负载因子是 0.75？", "空间和冲突的折中：太低浪费内存，太高链变长。", "basics/big-o.html"),
        ("JDK 7 的死循环具体怎么成的？", "头插法 + 并发扩容，两条链互相指向，get 时永远转不出来。", "basics/threads.html"),
        ("并发场景到底用哪个？", "ConcurrentHashMap：桶级锁 + CAS，读不加锁。", "basics/threads.html"),
        ("它能当缓存用吗？", "本机临时缓存可以，但它没上限、没过期、不是线程安全——正经缓存用 Redis。", ""),
        ("缓存会出什么问题？", "穿透、击穿、雪崩，三种根因不同、治法不同。", ""),
    ],
    "questions/pay-callback.html": [
        ("为什么用唯一索引当锁，而不是先查再插？", "两个线程能同时查出“不存在”；唯一索引是数据库自己把门的。", ""),
        ("幂等记录插进去了，但业务崩了怎么办？", "靠状态 CAS 兜底：只允许 PENDING → PAID，重试时影响 0 行就按已处理返回。", ""),
        ("钱到了但订单已经关闭，怎么处理？", "CAS 影响 0 行且状态是 CLOSED → 走退款，不能悄悄吞掉。", ""),
        ("Redisson 的 watchdog 到底在续什么？", "续的是锁的租约；线程活着才续，进程挂掉租约自动过期。", ""),
        ("主从切换把锁丢了怎么办？", "靠数据库兜底：唯一索引 + CAS 仍然守得住。", ""),
        ("MQ 消费重复，和这个是一回事吗？", "机制一样：消费端幂等（业务唯一键 / 状态机），别指望队列只投一次。", ""),
        ("那库存怎么保证只扣一次、还不超卖？", "预扣 + 条件更新（qty >= 1）+ 延时关单回滚。", ""),
        ("缓存和数据库不一致怎么办？", "Cache Aside：写库后删缓存，加延迟补偿与过期兜底。", ""),
    ],
}

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
