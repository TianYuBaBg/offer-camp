window.TERMS = {
"CAS": {
"k": "CAS",
"read": "凯斯",
"ipa": "/kæs/",
"en": "compare-and-swap: change the value only if it still looks like this.",
"zh": "比较并交换：先比一下还是不是这个样子，是才允许改——所以“判断+修改”是一条 SQL。"
},
"ack": {
"k": "ack",
"read": "阿克",
"ipa": "/æk/",
"en": "acknowledge: the consumer tells the queue “I finished this one”.",
"zh": "确认：消费者告诉队列“这条我处理完了”，没 ack 就会被重投。"
},
"nack": {
"k": "nack",
"read": "那克",
"ipa": "/næk/",
"en": "negative ack: the consumer says “this one failed”.",
"zh": "否认确认：消费者说“这条处理失败了”，配合死信队列做重试。"
},
"TTL": {
"k": "TTL",
"read": "提提艾尔",
"ipa": "/ˌtiː tiː ˈel/",
"en": "time to live: how long a key or message is allowed to exist.",
"zh": "存活时间：一个 key / 一条消息最多活多久，到点就自动消失。"
},
"QPS": {
"k": "QPS",
"read": "扣皮艾斯",
"ipa": "/ˌkjuː piː ˈes/",
"en": "queries per second: how many requests land in one second.",
"zh": "每秒请求数：衡量流量大小的最常用单位。"
},
"P95": {
"k": "P95",
"read": "P 九五",
"ipa": "",
"en": "the 95th percentile latency: 95% of requests are faster than this.",
"zh": "95 分位延迟：100 个请求里 95 个比它快——看尾部体验，比平均值有用。"
},
"MQ": {
"k": "MQ",
"read": "艾姆扣",
"ipa": "/ˌem ˈkjuː/",
"en": "message queue: producer puts a message in, consumer takes it out.",
"zh": "消息队列：生产方塞消息，消费方异步取走处理，用来解耦、削峰。"
},
"RPC": {
"k": "RPC",
"read": "阿尔皮西",
"ipa": "/ˌɑːr piː ˈsiː/",
"en": "remote procedure call: call a function that lives on another machine.",
"zh": "远程调用：像调本地方法一样调另一台机器上的接口。"
},
"API": {
"k": "API",
"read": "诶皮艾",
"ipa": "/ˌeɪ piː ˈaɪ/",
"en": "application programming interface: the set of endpoints you can call.",
"zh": "接口：别人能调你的那些方法/地址。"
},
"SQL": {
"k": "SQL",
"read": "艾斯扣艾尔",
"ipa": "/ˌes kjuː ˈel/",
"en": "structured query language: the language you talk to a relational database in.",
"zh": "结构化查询语言：跟关系型数据库说话用的语言。"
},
"JVM": {
"k": "JVM",
"read": "J 威艾姆",
"ipa": "/ˌdʒeɪ viː ˈem/",
"en": "Java virtual machine: the thing that runs your .class files.",
"zh": "Java 虚拟机：跑你编译出来的 class 文件的那台“虚拟电脑”。"
},
"GC": {
"k": "GC",
"read": "G 西",
"ipa": "/ˌdʒiː ˈsiː/",
"en": "garbage collection: the JVM freeing objects you no longer use.",
"zh": "垃圾回收：JVM 自动把没人引用的对象清掉，所以要少制造垃圾。"
},
"ZSet": {
"k": "ZSet",
"read": "泽赛特",
"ipa": "/ˈzed set/",
"en": "Redis sorted set: members kept in order by a score.",
"zh": "有序集合：Redis 里按 score 排好序的结构，score 存时间戳就是延时队列。"
},
"Redis": {
"k": "Redis",
"read": "瑞迪斯",
"ipa": "/ˈredɪs/",
"en": "an in-memory key-value store, usually used as a cache.",
"zh": "内存数据库，常用来做缓存、分布式锁、延时队列。"
},
"MySQL": {
"k": "MySQL",
"read": "买艾斯扣艾尔",
"ipa": "/ˌmaɪ es kjuː ˈel/",
"en": "the relational database almost every small company uses.",
"zh": "最常用的关系型数据库，数据最终都存在这里。"
},
"RabbitMQ": {
"k": "RabbitMQ",
"read": "瑞比特 MQ",
"ipa": "/ˈræbɪt ˌem ˈkjuː/",
"en": "a message broker: exchanges, queues, acks, dead-letter boxes.",
"zh": "消息中间件：交换机 + 队列 + 确认机制，适合可靠投递而不是高吞吐日志。"
},
"Redisson": {
"k": "Redisson",
"read": "瑞迪森",
"ipa": "/ˈredɪsən/",
"en": "a Redis client that implements proper distributed locks with a watchdog.",
"zh": "Redis 的客户端库，提供带 watchdog 续期的分布式锁。"
},
"idempotent": {
"k": "idempotent",
"read": "艾登坡腾特",
"ipa": "/ˌaɪdemˈpoʊtnt/",
"en": "running it twice has the same effect as running it once.",
"zh": "幂等：执行两次和执行一次，结果一样。"
},
"watchdog": {
"k": "watchdog",
"read": "沃奇道格",
"ipa": "/ˈwɑːtʃdɔːɡ/",
"en": "a background timer that keeps renewing a lock's lease while you are alive.",
"zh": "看门狗：进程还活着就自动给锁续租，进程一死就不再续。"
},
"幂等": {
"k": "幂等",
"zh": "同一个操作执行一次和执行多次，结果一样；靠唯一索引或状态判断做到。"
},
"幂等性": {
"k": "幂等性",
"zh": "接口被重复调用也不会出错的属性。"
},
"幂等表": {
"k": "幂等表",
"zh": "专门记录“这笔业务处理过没有”的表，靠唯一索引去重，插不进去就说明是重复。"
},
"唯一索引": {
"k": "唯一索引",
"zh": "数据库里“这一列不允许重复”的索引；插入重复值会直接被数据库拒绝，这就是最硬的锁。"
},
"uk_trade": {
"k": "uk_trade",
"zh": "幂等表上的唯一键，作用是让第二条回调插不进去。"
},
"状态 CAS": {
"k": "状态 CAS",
"zh": "用 where status='PENDING' 这种条件去改状态，影响 1 行表示抢到，0 行表示别人做过了。"
},
"消息队列": {
"k": "消息队列",
"zh": "生产方塞消息、消费方异步取走处理的中间件，用来解耦、削峰、异步。"
},
"延迟队列": {
"k": "延迟队列",
"zh": "到点才把任务交出来的队列，订单 30 分钟关单就是典型用法。"
},
"延时队列": {
"k": "延时队列",
"zh": "到点才把任务交出来的队列，订单 30 分钟关单就是典型用法。"
},
"死信队列": {
"k": "死信队列",
"zh": "处理失败太多次的消息被转存的地方，避免它一直卡在队头重试。"
},
"分布式锁": {
"k": "分布式锁",
"zh": "多台机器之间互斥的一把锁，通常用 Redis 或 ZooKeeper 实现。"
},
"状态机": {
"k": "状态机",
"zh": "订单只能按 PENDING → PAID / CLOSED 这类规则流转，不能乱跳。"
},
"乐观锁": {
"k": "乐观锁",
"zh": "不加锁，改的时候带个版本号或状态条件，改不到就重试。"
},
"悲观锁": {
"k": "悲观锁",
"zh": "先锁住再改，`select ... for update` 就是它。"
},
"缓存穿透": {
"k": "缓存穿透",
"zh": "查一个根本不存在的数据，缓存没有、数据库也没有，每次都空跑。"
},
"缓存击穿": {
"k": "缓存击穿",
"zh": "一个热点 key 过期瞬间，上千个线程同时回源重建。"
},
"缓存雪崩": {
"k": "缓存雪崩",
"zh": "大批 key 同一秒过期，或者 Redis 整个挂了。"
},
"布隆过滤器": {
"k": "布隆过滤器",
"zh": "一个很小的位数组，能立刻回答“这个 key 一定不存在”，用来挡穿透。"
},
"覆盖索引": {
"k": "覆盖索引",
"zh": "查询要的列全在索引里，不用回表再查一次。"
},
"回表": {
"k": "回表",
"zh": "索引里没有要的列，得拿着主键再回主表查一次。"
},
"慢查询": {
"k": "慢查询",
"zh": "执行时间超过阈值的 SQL，通常要开慢日志才能抓到。"
},
"预扣库存": {
"k": "预扣库存",
"zh": "先在 Redis 里把库存减掉，下单成功后再慢慢落库。"
},
"回滚库存": {
"k": "回滚库存",
"zh": "订单取消/关闭时把之前预扣的库存加回去。"
},
"事务": {
"k": "事务",
"zh": "一组操作要么全成功、要么全失败；本地事务靠数据库，跨服务要靠补偿。"
},
"主从切换": {
"k": "主从切换",
"zh": "主库挂了，从库顶上——切换瞬间可能有数据没同步过去。"
},
"分库分表": {
"k": "分库分表",
"zh": "一张表数据太大，按某个维度拆到多个库/表里。"
},
"分片广播": {
"k": "分片广播",
"zh": "XXL-Job 把一次任务分给多台执行器各跑一片，用来并行处理大数据量。"
},
"断点续跑": {
"k": "断点续跑",
"zh": "任务中途失败，下次从上次的进度继续，不用从头再来。"
},
"心跳": {
"k": "心跳",
"zh": "设备每隔几秒发一个包报平安，几个周期没收到就认为掉线。"
},
"长连接": {
"k": "长连接",
"zh": "TCP 连接建立后一直不断，双方随时可以推消息。"
},
"组播": {
"k": "组播",
"zh": "一份数据发给一组接收者，UDP 组播常用于设备状态广播。"
},
"限流": {
"k": "限流",
"zh": "超过阈值的请求直接拒绝，保护后面的系统。"
},
"熔断": {
"k": "熔断",
"zh": "下游一直失败就先断开一段时间，别让请求堆在那里。"
},
"降级": {
"k": "降级",
"zh": "关键链路挂了，返回一个兜底结果，而不是报错。"
},
"回源": {
"k": "回源",
"zh": "缓存没命中，回过头去数据库查。"
},
"脏数据": {
"k": "脏数据",
"zh": "从缓存或副本里读到的旧值，和数据库不一致。"
},
"推模式": {
"k": "推模式",
"zh": "服务端变化后主动推给客户端，而不是等客户端来拉。"
},
"间隙锁": {
"k": "间隙锁",
"read": "间隙锁",
"zh": "要锁一个“不存在的行”时，InnoDB 锁住的是一段索引区间而不是一行——并发下容易锁等待和死锁。"
},
"页锁": {
"k": "页锁",
"read": "页锁",
"en": "latch: a short internal mutex InnoDB holds while touching a page.",
"zh": "InnoDB 内部的一把短锁，改一个数据页时用；检查和插入都在它保护下，所以中间插不进别的会话。"
}
};
