# -*- coding: utf-8 -*-
"""术语表页：把正文里可点的 56 个术语，按主题分组做成可学习的清单。"""

TERMS_PAGE = dict(
    path="terms.html",
    title=("Terms on this site", "全站术语"),
    crumb=('<a href="index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a>'
           ' / <span class="in-en">Terms</span><span class="in-zh">术语</span>'),
    kicker=("Terms · 56", "术语 · 56 个"),
    next=('<a href="questions/index.html"><span class="in-en">Back to the questions</span>'
          '<span class="in-zh">回到题目</span></a>'),
    words=[],
    checks=[],
    h1=("Every term on this site, in one place.",
        "全站出现过的术语，都在这一页。"),
    lede=("Fifty-six terms. Read the 谐音 out loud first, then the meaning. Do not memorise — recognise.",
          "五十六个词。先照着谐音读出来，再看含义。不用背，认得就行。"),
    tags=[("56 terms", "56 个"), ("20 English", "20 个英文"), ("36 中文", "36 中文")],
    groups=[
        ("English abbreviations", "英文缩写", [
            "CAS", "ack", "nack", "idempotent", "uk_trade",
            "TTL", "QPS", "P95", "MQ", "RPC", "API", "SQL", "JVM", "GC",
        ]),
        ("Tools and components", "组件与名字", [
            "Redis", "MySQL", "RabbitMQ", "Redisson", "ZSet", "watchdog",
        ]),
        ("Idempotency and payments", "幂等与支付", [
            "幂等", "幂等性", "幂等表", "唯一索引", "状态 CAS", "状态机",
            "乐观锁", "悲观锁",
        ]),
        ("Queues and jobs", "消息与任务", [
            "消息队列", "延迟队列", "延时队列", "死信队列", "推模式", "分片广播", "断点续跑",
        ]),
        ("Cache and stock", "缓存与库存", [
            "缓存穿透", "缓存击穿", "缓存雪崩", "布隆过滤器", "回源", "脏数据",
            "预扣库存", "回滚库存",
        ]),
        ("Database and stability", "数据库与稳定性", [
            "覆盖索引", "回表", "慢查询", "分库分表", "事务", "主从切换",
            "分布式锁", "限流", "熔断", "降级", "长连接", "心跳", "组播",
        ]),
    ],
)
