# -*- coding: utf-8 -*-
"""第 1 题（HashMap）的 9 个追问，各自成页。"""

CRUMB = ('<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
         '<a href="java-hashmap.html"><span class="in-en">Q1</span><span class="in-zh">第 1 题</span></a> / ')

BACK = ('<a href="java-hashmap.html"><span class="in-en">&#8592; Back to question 1</span>'
        '<span class="in-zh">&#8592; 回到第 1 题</span></a>')


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


D1 = [
    P("d1-capacity-power-of-two.html", 1, "Power of two", "容量是 2 的幂",
      "Why the capacity has to be a power of two.", "为什么容量必须是 2 的幂。",
      "The answer is one line of bit math — and it is also why resize can avoid rehashing.",
      "答案是一行位运算——也正是扩容时能避免重算 hash 的原因。",
      "If n is a power of two, (n-1) is all ones in binary, so h & (n-1) keeps the low bits and equals h % n — "
      "but much faster. If n is not a power of two, some low-bit patterns can never be produced and whole buckets stay empty.",
      "容量是 2 的幂时，n-1 的二进制全是 1，所以 h & (n-1) 等于 h % n，但快得多。"
      "如果不是 2 的幂，某些低位组合永远取不到，一批桶会空着，浪费空间又加剧冲突。",
      "容量必须是 2 的幂，因为定位用的是位运算 h & (n-1)，它只有在 n 是 2 的幂时才等于取模。"
      "顺带的好处是扩容时元素要么留在原位、要么挪到“原位 + 旧容量”。",
      "容量必须是 2 的幂，因为定位用的是位运算 h & (n-1)，它只有在 n 是 2 的幂时才等于取模。"
      "顺带的好处是扩容时元素要么留在原位、要么挪到“原位 + 旧容量”。",
      [
          ("Why not modulo", "为什么不用取模", [
              ("p", "Division is slow at the CPU level; a bitwise AND is one cycle. With 16 buckets that is "
                    "the difference between a fast put and a slower one on every single insert.",
               "除法在 CPU 里是慢指令，按位与只要一个周期。16 个桶的情况下，这个差别在每次 put 上都存在。"),
              ("pre", "n = 16\nh = 0x7f3a\nh & (n - 1)   ->  0x0a   (10)\nh % n         ->  10        // 结果一样\n\n// n = 15（不是 2 的幂）\nh & 14 永远取不到 15，最低位被吃掉"),
          ]),
          ("What it buys during resize", "扩容时白拿的好处", [
              ("ul", [
                  ("Because capacity doubles, the new mask is the old mask plus one bit.",
                   "因为容量翻倍，新掩码只比旧掩码多一位。"),
                  ("That new bit decides everything: 0 → stay, 1 → move to index + oldCap.",
                   "这一位决定一切：是 0 就留在原位，是 1 就挪到“原位 + 旧容量”。"),
                  ("So resize never recomputes hashCode — it re-splits the chain in two.",
                   "所以扩容从不重算 hashCode，只是把链撕成两条。"),
              ]),
          ]),
      ]),

    P("d1-hash-spread.html", 2, "Hash spreading", "为什么要异或高位",
      "Why spread the high bits into the low bits.", "为什么要把 hash 的高位异或下来。",
      "Only the low bits pick the bucket, so the top 16 bits are wasted — unless you fold them in.",
      "定位只用低位，高 16 位本来纯浪费——除非把它们折进低位。",
      "Because bucket index = hash & (n-1) only looks at the low bits. Most hashCodes (string, integer) "
      "differ mostly in the high bits, so folding h ^ (h >>> 16) brings that entropy down where it is used.",
      "因为桶下标 = hash & (n-1)，只看低位。而多数 hashCode（字符串、整数）的差异主要在高位，"
      "所以用 h ^ (h >>> 16) 把高位的熵搬到低位来用。",
      "JDK 8 里 put 之前先做 hash 扰动：h ^ (h >>> 16)，把高 16 位折到低 16 位。"
      "不这么做，很多 key 的低位一样，就全挤到一个桶里。",
      "JDK 8 里 put 之前先做 hash 扰动：h ^ (h >>> 16)，把高 16 位折到低 16 位。"
      "不这么做，很多 key 的低位一样，就全挤到一个桶里。",
      [
          ("A concrete case", "一个具体例子", [
              ("pre", "// 两个 key 只在高位不同\nh1 = 0x1234_0001\nh2 = 0xabcd_0001\n\nh1 & 15 = 1\nh2 & 15 = 1        // 同一个桶\n\nh1 ^ (h1>>>16) = 0x1234_1235  -> &15 = 5\nh2 ^ (h2>>>16) = 0xabcd_abcd  -> &15 = 13   // 分开了"),
              ("p", "One xor, one shift — and two keys that used to collide are now in different buckets.",
               "一次异或、一次移位——原本打架的两个 key 分开了。"),
          ]),
          ("Why not a stronger hash", "为什么不做更强的 hash", [
              ("note", "A full rehash (like Murmur) costs more than it saves; one xor-shift is enough for "
                       "“decent but not hostile” keys. Truly hostile keys need a tree, which is exactly the next follow-up.",
               "完整重哈希（如 Murmur）代价高于收益；一次异或移位对“正常但不友善”的 key 已经够。"
               "真正恶意构造的 key，靠的是树化，也就是下一条。"),
          ]),
      ]),

    P("d1-treeify-8.html", 3, "Treeify at 8", "为什么是 8",
      "Why the list turns into a tree only at 8.", "为什么链表要到 8 才转红黑树。",
      "Because 8 in one bucket is already statistically impossible for good hashes.",
      "因为对正常的 hash 来说，一个桶里挤到 8 个，本就是小概率事件。",
      "Under a good hash the chain length follows a Poisson distribution (λ≈0.5): 8 in one bucket happens about "
      "6 in 10 million times. Tree nodes cost more memory, so we only pay that when the hash is clearly bad.",
      "hash 均匀时链长近似泊松分布（λ≈0.5）：一个桶里到 8 个的概率约千万分之六。"
      "树节点更占内存，所以只有当 hash 明显有问题时才值得付这个代价。",
      "TreeNode 比 Node 大不少，平时用不上；8 这个阈值是统计出来的——到 8 说明 hash 有问题，"
      "这时候把 O(n) 降到 O(log n) 才划算。",
      "TreeNode 比 Node 大不少，平时用不上；8 这个阈值是统计出来的——到 8 说明 hash 有问题，"
      "这时候把 O(n) 降到 O(log n) 才划算。",
      [
          ("The Poisson table", "泊松分布那张表", [
              ("table", [("Chain length", "链长"), ("Probability", "概率")], [
                  [("2", "2"), ("~7.5%", "约 7.5%")],
                  [("4", "4"), ("~0.05%", "约 0.05%")],
                  [("8", "8"), ("~6e-7", "约 6e-7")],
              ]),
              ("p", "Also note the second condition: the array must be at least 64 long. Below that HashMap resizes "
                    "instead of treeifying — small tables are cheaper to grow than to convert.",
               "还有第二个条件：数组长度至少 64。不到 64 时优先扩容而不是树化——小表扩容比转换便宜。"),
          ]),
          ("Cost of a tree node", "树节点的代价", [
              ("ul", [
                  ("TreeNode keeps parent, left, right, red/black plus the original next pointer.",
                   "TreeNode 额外存 parent、left、right、红黑标记，还要保留 next。"),
                  ("That is roughly three times the memory of a plain Node, per entry.",
                   "大约是一个普通 Node 的三倍内存。"),
                  ("So the switch is a trade: pay memory only when the chain proves the hash is broken.",
                   "所以这是一笔交易：只有链长证明 hash 坏了，才付这份内存。"),
              ]),
          ]),
      ]),

    P("d1-untreeify-6.html", 4, "Untreeify at 6", "为什么退化是 6",
      "Why the tree degrades at 6 and not 7.", "为什么树缩回链表是 6，不是 7。",
      "A one-slot gap stops the bucket from flipping back and forth.",
      "留一格缓冲，防止同一个桶在 7 和 8 之间来回翻转。",
      "If treeify is at 8 and untreeify were at 7, one insert/remove around the boundary would convert the bucket "
      "twice in a row — pure overhead. 6 leaves a gap of one, so flapping requires two operations.",
      "如果树化是 8、退化是 7，边界上删一个插一个就会连续转换两次，纯开销。"
      "取 6 留一格，要抖动得做两次操作才行。",
      "阈值是 8 和 6，中间留一格：不然 7 和 8 之间来回插删，桶会反复转换，白烧 CPU。",
      "阈值是 8 和 6，中间留一格：不然 7 和 8 之间来回插删，桶会反复转换，白烧 CPU。",
      [
          ("How flapping happens", "抖动是怎么发生的", [
              ("pre", "链长 8 -> 树化 (8->tree)\n删一个 -> 7，若退化阈值是 7 就转回链表\n再插一个 -> 8，又树化\n…… 每次都是 O(n) 的重建"),
              ("note", "This is the same idea as hysteresis in control systems: two thresholds, not one.",
               "和控制里的“滞回”一个道理：用两个阈值，而不是一个。"),
          ]),
      ]),

    P("d1-load-factor.html", 5, "Load factor 0.75", "负载因子 0.75",
      "Why 0.75 and not 0.5 or 1.0.", "为什么负载因子是 0.75，不是 0.5 也不是 1。",
      "It is the point where space, collision rate and resize cost stop fighting each other.",
      "在这个点上，空间、冲突率、扩容成本三者不再互相拉扯。",
      "With 0.5 you waste half the array and resize twice as often. With 1.0 the chains get long before you grow, "
      "so lookups degrade. 0.75 keeps the expected chain short while still using three quarters of the memory.",
      "取 0.5 会浪费一半数组，扩容频率也翻倍；取 1.0 则链先变长、查询先变慢。"
      "0.75 既让期望链长很短，又用掉了四分之三的内存。",
      "0.75 是空间和冲突的折中：低于它浪费内存、扩容太频繁；高于它链变长、查询变慢。"
      "本质是拿空间换算次数。",
      "0.75 是空间和冲突的折中：低于它浪费内存、扩容太频繁；高于它链变长、查询变慢。"
      "本质是拿空间换算次数。",
      [
          ("Three costs, one knob", "三个成本，一个旋钮", [
              ("table", [("Load factor", "负载因子"), ("What you pay", "你付出什么")], [
                  [("0.5", "0.5"), ("double memory, double resizes", "内存翻倍，扩容翻倍")],
                  [("0.75", "0.75"), ("balanced (the default)", "平衡（默认值）")],
                  [("1.0", "1.0"), ("long chains, slow lookups, spikes at resize", "链变长、查询变慢、扩容尖峰")],
              ]),
              ("p", "Resize is O(n) and copies every entry, so a full table at 1.0 also means the next put pays "
                    "for a large copy right when the table is busiest.",
               "扩容是 O(n) 且要搬所有元素，所以装满的表在下一次 put 时，正好在最忙的时候付一大笔搬迁成本。"),
          ]),
      ]),

    P("d1-jdk7-infinite-loop.html", 6, "JDK 7 infinite loop", "JDK 7 死循环",
      "How JDK 7 turned a resize into a ring.", "JDK 7 是怎么把一次扩容变成环的。",
      "Head insertion plus concurrent resize can make two nodes point at each other forever.",
      "头插法碰上并发扩容，可能让两个节点互相指向，永远转不出来。",
      "JDK 7 linked new nodes at the head of the chain. Two threads resizing at once could interleave so that "
      "A.next = B and B.next = A. Any later get() into that bucket loops forever, burning 100% CPU.",
      "JDK 7 用头插法挂新节点。两个线程同时扩容时，可能交错成 A.next = B 且 B.next = A。"
      "之后任何 get 落到这个桶，就会在环里死转，CPU 打满。",
      "JDK 7 头插法 + 并发扩容会成环，get 永远转不出来，CPU 打满——这是最有名的 HashMap 事故。"
      "JDK 8 改成尾插 + 拆成 lo/hi 两条链，不会成环了，但并发 put 依然会丢数据。",
      "JDK 7 头插法 + 并发扩容会成环，get 永远转不出来，CPU 打满——这是最有名的 HashMap 事故。"
      "JDK 8 改成尾插 + 拆成 lo/hi 两条链，不会成环了，但并发 put 依然会丢数据。",
      [
          ("Why head insertion is the problem", "为什么问题出在头插法", [
              ("pre", "// 头插：新节点总插到链头\nfor (Entry e : oldTable[i]) {\n    Entry next = e.next;   // 记住下一个\n    e.next = newTable[j];  // 插到新表链头\n    newTable[j] = e;       // 成为新的头\n    e = next;\n}\n\n// 两个线程交错执行时，e.next 可能指回已经搬过的节点"),
              ("p", "JDK 8 keeps the relative order (tail insertion + lo/hi split), so a ring cannot form. "
                    "It still loses updates under concurrency — just without the infinite loop.",
               "JDK 8 保持相对顺序（尾插 + lo/hi 拆分），不会成环。但并发下依然会丢更新——只是不再死循环。"),
          ]),
          ("What to say about it", "面试怎么用这条", [
              ("note", "Question is usually “is HashMap thread safe?”. Answer: no; JDK 7 could hang, JDK 8 loses data. "
                       "Either way the fix is the same: use ConcurrentHashMap.",
               "这题通常问“HashMap 线程安全吗”。答：不安全；JDK 7 会挂死，JDK 8 会丢数据。"
               "不管哪种，解法都一样：换 ConcurrentHashMap。"),
          ]),
      ]),

    P("d1-concurrent-map.html", 7, "ConcurrentHashMap", "并发用哪个",
      "CAS plus a per-bucket lock, not a segmented lock.", "CAS 加“每个桶一把锁”，不是分段锁。",
      "JDK 8 threw away segments: one lock per bucket head, and reads never lock at all.",
      "JDK 8 把分段锁扔了：锁的是桶的头节点，读操作完全不加锁。",
      "Emptied bucket: CAS to install the first node. Occupied bucket: synchronized on the head node. "
      "Reads use volatile reads of the node array and the next pointers, so they never block.",
      "空桶：CAS 直接放第一个节点。非空桶：对头节点 synchronized。"
      "读操作走数组和 next 指针的 volatile 读，所以从不阻塞。",
      "并发用 ConcurrentHashMap：JDK 8 是 CAS 占空桶 + synchronized 锁桶头，锁粒度从段降到单个桶；"
      "reading 不加锁，靠 volatile 和 Node 的 val/next 不可变。",
      "并发用 ConcurrentHashMap：JDK 8 是 CAS 占空桶 + synchronized 锁桶头，锁粒度从段降到单个桶；"
      "reading 不加锁，靠 volatile 和 Node 的 val/next 不可变。",
      [
          ("Put, step by step", "put 的动作顺序", [
              ("ol", [
                  ("Bucket empty → CAS the new node in. No lock at all.",
                   "桶是空 → CAS 放新节点，完全不锁。"),
                  ("Bucket busy → synchronized(head) and walk the chain.",
                   "桶非空 → synchronize 头节点，沿着链走。"),
                  ("Size uses a base counter plus CounterCell[] to spread contention.",
                   "size 用 base + CounterCell[] 分散计数，避免所有线程抢一个计数。"),
              ]),
          ]),
          ("Why not segments", "为什么不用分段", [
              ("ul", [
                  ("Segments gave at most 16-way concurrency and wasted memory.",
                   "分段锁最多 16 路并发，还浪费内存。"),
                  ("Per-bucket locking scales with the table: more buckets, more parallelism.",
                   "按桶加锁，并发度随表大小走：桶越多越能并行。"),
                  ("Cost: no atomic “size across the whole map” for free, hence the counter cells.",
                   "代价：整体 size 不再是免费的原子操作，于是有了计数单元。"),
              ]),
          ]),
      ]),

    P("d1-as-cache.html", 8, "Can it be a cache", "能不能当缓存",
      "Fine as a scratch map. Wrong as a cache.", "当临时表可以，当缓存不对。",
      "A cache needs eviction, expiry and a memory bound. HashMap has none of the three.",
      "缓存需要淘汰、过期、内存上限——HashMap 三样都没有。",
      "HashMap grows without limit and never expires anything, so a long-running process fills the heap and dies. "
      "If you want a local cache, use Caffeine (bounded, TTL, LRU/LFU); if you need it shared, use Redis.",
      "HashMap 无上限、不过期，长时间运行会把堆撑爆。要本机缓存就用 Caffeine（有上限、TTL、淘汰策略）；"
      "要共享就用 Redis。",
      "本机临时缓存可以，但它没上限、没过期、不是线程安全——正经缓存用 Caffeine 或 Redis。"
      "面试里我一般说：HashMap 只是容器，缓存要的是淘汰策略和过期。",
      "本机临时缓存可以，但它没上限、没过期、不是线程安全——正经缓存用 Caffeine 或 Redis。"
      "面试里我一般说：HashMap 只是容器，缓存要的是淘汰策略和过期。",
      [
          ("What a cache needs", "缓存必须有的三件", [
              ("table", [("Need", "需要"), ("HashMap", "HashMap"), ("Caffeine / Redis", "Caffeine / Redis")], [
                  [("bounded size", "上限"), ("no", "没有"), ("yes", "有")],
                  [("expiry", "过期"), ("no", "没有"), ("yes", "有")],
                  [("eviction policy", "淘汰"), ("no", "没有"), ("LRU / LFU / TTL", "LRU / LFU / TTL")],
                  [("thread safety", "线程安全"), ("no", "没有"), ("yes", "有")],
              ]),
          ]),
      ]),

    P("d1-cache-problems.html", 9, "Cache failures", "缓存三坑",
      "Three names, three different root causes.", "三个名字，三种不同的根因。",
      "Penetration is missing data, breakdown is one hot key expiring, avalanche is many keys at once.",
      "穿透是数据不存在，击穿是一个热 key 过期，雪崩是一大批 key 同时失效。",
      "Penetration: query something that does not exist, so every request hits the DB — fix with a null cache "
      "or a Bloom filter. Breakdown: one hot key expires and thousands of threads rebuild it — fix with a lock "
      "or logical expiry. Avalanche: many keys expire together or Redis dies — fix with jittered TTL, local cache "
      "and a rate limiter.",
      "穿透：查根本不存在的数据，每次都打到库——用空值缓存或布隆过滤器。"
      "击穿：一个热 key 过期，上千线程同时重建——用锁或逻辑过期。"
      "雪崩：大批 key 同时过期或 Redis 挂了——用随机 TTL、本地缓存、限流。",
      "穿透是假数据、击穿是一个热 key、雪崩是一大批 key；治法分别是布隆/空值、重建加锁、随机过期加多级缓存。",
      "穿透是假数据、击穿是一个热 key、雪崩是一大批 key；治法分别是布隆/空值、重建加锁、随机过期加多级缓存。",
      [
          ("Side by side", "并排看", [
              ("table", [("Name", "名字"), ("Root cause", "根因"), ("Fix", "治法")], [
                  [("penetration", "穿透"), ("key 不存在，缓存也存不下", "布隆过滤器 / 空值缓存"),
                   ("bloom / null cache", "布隆 / 空值")],
                  [("breakdown", "击穿"), ("一个热 key 过期", "重建加锁 / 逻辑过期"),
                   ("lock / logical expire", "锁 / 逻辑过期")],
                  [("avalanche", "雪崩"), ("大批 key 同时过期 / Redis 挂", "随机 TTL / 多级缓存 / 限流"),
                   ("jitter / local cache", "抖动 / 本地缓存")],
              ]),
          ]),
      ]),
]
