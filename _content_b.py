# -*- coding: utf-8 -*-
"""内容 B：第 5–7 课 + HashMap 题 + 词表 + 关于。"""

L5 = {
    "path": "basics/big-o.html",
    "title": ("What is O(1), O(n), O(log n)", "什么是 O(1)、O(n)、O(log n)"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 5: Big O</span><span class="in-zh">第 5 课：复杂度</span>',
    "kicker": ("Lesson 5 · Complexity", "第 5 课 · 复杂度"),
    "h1": ("What is O(1), O(n), O(log n)?", "什么是 O(1)、O(n)、O(log n)？"),
    "lede": ("Big O is not about seconds. It is about how the cost grows when the data grows.",
             "大 O 说的不是几秒，而是“数据变多时，代价怎么变”。"),
    "tags": [("Basics", "基础"), ("complexity", "复杂度"), ("must know", "必背")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The idea", "先有一个画面", [
            ("analogy", "Think of it like this", "先这样想",
             "Finding a shoe. (1) You know the box number — open one box. (2) The boxes have no order — open one by one. "
             "(3) The boxes are sorted by size — cut the range in half each time.",
             "找鞋：(1) 你知道在哪一格——开一格； (2) 全乱堆着——一格一格开； (3) 按大小排好了——每次砍一半。"),
            ("p", "That is O(1), O(n), O(log n). The letter is the data size; the function is how many steps you need.",
             "这就是 O(1)、O(n)、O(log n)。字母是数据量，函数是需要的步数。"),
            ("table", [("Big O", "大 O"), ("Means", "意思"), ("n=1000 steps", "1000 个时要几步")],
             [[("O(1)", "O(1)"), ("one step, no matter how many", "不管多少，都是一步"), ("1", "1")],
              [("O(log n)", "O(log n)"), ("half each time", "每次砍一半"), ("about 10", "约 10")],
              [("O(n)", "O(n)"), ("one by one", "一个一个来"), ("1000", "1000")],
              [("O(n log n)", "O(n log n)"), ("sort by halving, n times", "每次砍一半、做 n 遍"), ("about 10000", "约 1 万")],
              [("O(n²)", "O(n²)"), ("every pair", "两两配对"), ("1,000,000", "100 万")]]),
        ]),
        ("h2", "02", "How to read it", "怎么读出来", [
            ("p", "“O” is said “big O”. “O(1)” is “big O of one, constant time”. “O(log n)” is “big O of log n”.",
             "“O”读作 big O；“O(1)”读 big O of one，也叫常数时间；“O(log n)”读 big O of log n。"),
            ("p", "We drop the small parts. <code>O(2n + 5)</code> is O(n); <code>O(n² + n)</code> is O(n²). "
                  "Big O cares about the shape of the curve, not the exact number.",
             "小项会被丢掉：<code>O(2n + 5)</code> 就是 O(n)，<code>O(n² + n)</code> 就是 O(n²)。"
             "大 O 只看曲线的形状，不看具体数字。"),
        ]),
        ("h2", "03", "Where you meet it", "你会在哪里遇到它", [
            ("ul", [
                ("HashMap get: O(1) on average, O(log n) in a bad bucket, O(n) in the worst case.",
                 "HashMap 的 get：平均 O(1)，桶里成了树是 O(log n)，最坏 O(n)。"),
                ("ArrayList get: O(1). Insert in the middle: O(n).",
                 "ArrayList 按下标读：O(1)；中间插入：O(n)。"),
                ("A double loop over the same list: O(n²) — too slow for big data.",
                 "对同一个列表写两层循环：O(n²)，数据一大就慢。"),
            ]),
            ("note", "In an interview, say the number <b>and</b> why: “O(1), because it computes the bucket from the hash.”",
             "面试时说数字，<b>并且</b>说原因：“O(1)，因为它是用 hash 直接算出桶的位置。”"),
        ]),
    ],
    "words": [
        ("time complexity", "/taɪm kəmˈpleksəti/", "How run time grows with data size.", "时间复杂度：耗时随数据量增长的方式"),
        ("Big O", "/bɪɡ oʊ/", "The notation for that growth.", "大 O：描述增长的量级记号"),
        ("constant", "/ˈkɑːnstənt/", "Does not grow: O(1).", "常数：不增长，O(1)"),
        ("linear", "/ˈlɪniər/", "Grows in a line: O(n).", "线性：成一条直线增长，O(n)"),
        ("logarithmic", "/ˌlɔːɡəˈrɪðmɪk/", "Grows very slowly: O(log n).", "对数：增长很慢，O(log n)"),
    ],
    "checks": [
        ("In your own words: what is O(n)?", "用你自己的话说：什么是 O(n)？"),
        ("Why is reading an array O(1)?", "为什么读数组是 O(1)？"),
        ("A bucket with 8 items: how many steps at most?", "桶里有 8 个元素：最多几步？"),
    ],
    "next": '<a href="hashmap-methods.html"><span class="in-en">Next: Lesson 6, HashMap methods →</span>'
            '<span class="in-zh">下一课：第 6 课，HashMap 方法 →</span></a>',
}

L6 = {
    "path": "basics/hashmap-methods.html",
    "title": ("HashMap methods in real code", "HashMap 的常用方法"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 6: HashMap methods</span><span class="in-zh">第 6 课：HashMap 方法</span>',
    "kicker": ("Lesson 6 · Use it", "第 6 课 · 拿来用"),
    "h1": ("HashMap methods, and how they look in real code", "HashMap 的常用方法，以及它们在真实代码里长什么样"),
    "lede": ("Six methods cover almost everything: put, get, getOrDefault, computeIfAbsent, merge, remove.",
             "六个方法能盖住几乎所有场景：put、get、getOrDefault、computeIfAbsent、merge、remove。"),
    "tags": [("Basics", "基础"), ("HashMap", "HashMap"), ("real code", "真实代码")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The six methods", "六个方法", [
            ("table", [("Method", "方法"), ("What it does", "做什么"), ("Where I use it", "我用在哪")],
             [[("put(k,v)", "put(k,v)"), ("add or replace", "添加或覆盖"),
               ("save a value by key", "按 key 存一个值")],
              [("get(k)", "get(k)"), ("read, null if missing", "读，没有则返回 null"),
               ("simple lookup", "简单查询")],
              [("getOrDefault(k,d)", "getOrDefault(k,d)"), ("read, <code>d</code> if missing", "读，没有就给默认值"),
               ("counters, optional config", "计数、可选配置")],
              [("computeIfAbsent(k,f)", "computeIfAbsent(k,f)"), ("compute and store only if missing", "没有才算并存入"),
               ("cache, grouping", "缓存、分组")],
              [("merge(k,v,f)", "merge(k,v,f)"), ("combine old and new", "合并新旧值"),
               ("sum, max, join", "求和、取最大、拼接")],
              [("remove(k)", "remove(k)"), ("delete", "删除"), ("clear, cancel", "清理、取消")]]),
        ]),
        ("h2", "02", "Real code: a cache", "真实代码：缓存", [
            ("pre", """// 没有就查数据库，再放进缓存（最常见的写法）
User user = cache.computeIfAbsent(userId, id -> userMapper.selectById(id));"""),
            ("p", "One line: read the cache, miss → query the database → write back. No null check, no two lookups.",
             "一行：读缓存，没命中——查库——写回。不用判空，也不用查两次。"),
            ("note", "In a real service add an expiry (Caffeine or Redis). computeIfAbsent keeps the map small, but it never forgets.",
             "真实服务里还要加过期（Caffeine 或 Redis）。computeIfAbsent 只是让它懒加载，但不会自己忘。"),
        ]),
        ("h2", "03", "Real code: counting", "真实代码：计数", [
            ("pre", """// 统计每个状态有多少单
Map<String,Integer> count = new HashMap<>();
for (Order o : orders) {
    count.merge(o.getStatus(), 1, Integer::sum);
}"""),
            ("p", "<code>merge</code> is the cleanest counter: old value + 1, or 1 if it is the first time.",
             "<code>merge</code> 是最干净的计数写法：老值 +1，第一次出现就给 1。"),
        ]),
        ("h2", "04", "Real code: grouping", "真实代码：分组", [
            ("pre", """// 按用户分组：Map<Long, List<Order>>
Map<Long,List<Order>> byUser = new HashMap<>();
for (Order o : orders) {
    byUser.computeIfAbsent(o.getUserId(), k -> new ArrayList<>()).add(o);
}"""),
            ("p", "Or with the stream API: <code>orders.stream().collect(Collectors.groupingBy(Order::getUserId))</code> — "
                  "it does the same thing internally.",
             "也可以用 stream：<code>orders.stream().collect(Collectors.groupingBy(Order::getUserId))</code>，"
             "内部做的就是同一件事。"),
        ]),
        ("h2", "05", "Four things that bite", "四个坑", [
            ("ul", [
                ("<b>get returns null</b> — use <code>getOrDefault</code> when the value may be missing.",
                 "<b>get 返回 null</b>——可能没有的时候用 <code>getOrDefault</code>。"),
                ("<b>Mutable keys</b> — if you change a field used in <code>hashCode()</code> after <code>put</code>, the key is lost.",
                 "<b>可变的 key</b>——put 之后改了参与 <code>hashCode()</code> 的字段，这个 key 就找不回来了。"),
                ("<b>No order</b> — HashMap does not keep order. Use <code>LinkedHashMap</code> or <code>TreeMap</code>.",
                 "<b>无序</b>——HashMap 不保证顺序，要顺序用 <code>LinkedHashMap</code> 或 <code>TreeMap</code>。"),
                ("<b>Not thread-safe</b> — lesson 7.",
                 "<b>线程不安全</b>——第 7 课讲。"),
            ]),
        ]),
    ],
    "words": [
        ("HashMap", "/hæʃ mæp/", "Map by key, built on an array of buckets.", "HashMap：用桶数组实现的键值表"),
        ("entry", "/ˈentri/", "One key-value pair.", "entry：一个键值对"),
        ("cache", "/kæʃ/", "A small fast copy of slow data.", "缓存：慢数据的一份快速副本"),
        ("merge", "/mɜːrdʒ/", "Combine two values.", "merge：合并两个值"),
        ("grouping", "/ˈɡruːpɪŋ/", "Putting items into groups by a field.", "分组：按字段归类"),
    ],
    "checks": [
        ("Difference between get and getOrDefault?", "get 和 getOrDefault 有什么区别？"),
        ("Write the one-liner cache with computeIfAbsent.", "用 computeIfAbsent 写出那一行缓存。"),
        ("How do you count occurrences cleanly?", "怎么干净地做计数？"),
    ],
    "next": '<a href="threads.html"><span class="in-en">Next: Lesson 7, threads →</span>'
            '<span class="in-zh">下一课：第 7 课，线程 →</span></a>',
}

L7 = {
    "path": "basics/threads.html",
    "title": ("Why HashMap is not thread-safe", "为什么 HashMap 线程不安全"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 7: Threads</span><span class="in-zh">第 7 课：线程</span>',
    "kicker": ("Lesson 7 · Concurrency", "第 7 课 · 并发"),
    "h1": ("Why is HashMap not thread-safe?", "为什么 HashMap 是线程不安全的？"),
    "lede": ("Two threads write at the same time, one write is lost. In JDK 7 it could even bend into a circle.",
             "两个线程同时写，就会丢掉一次写入；在 JDK 7 里甚至能把链表拧成一个圈。"),
    "tags": [("Basics", "基础"), ("concurrency", "并发"), ("must know", "必背")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The idea", "先有一个画面", [
            ("analogy", "Think of it like this", "先这样想",
             "Two people write on the same whiteboard at the same time. Both read “size = 10”, both write “size = 11”. "
             "One item was added, but the number only went up by one — the other add is invisible.",
             "两个人在同一块白板上同时写。两个人都读到 size = 10，都写下 size = 11。 "
             "明明加了两个，数字只涨了 1——另一次写入消失了。"),
            ("p", "<code>put</code> is not one instruction. It is a series of steps: pick a bucket, read the head, write the new node, "
                  "increase <code>size</code>. Another thread can jump in between any two steps.",
             "<code>put</code> 不是一条指令，而是一串步骤：选桶、读头节点、写新节点、<code>size++</code>。"
             "另一个线程可以在任意两步之间插进来。"),
        ]),
        ("h2", "02", "Three ways it breaks", "三种坏法", [
            ("ul", [
                ("<b>Lost update</b> — two <code>put</code>s increase size, one increase is overwritten. The map says 1 item, there are 2.",
                 "<b>丢更新</b>——两次 put 各涨一次 size，被覆盖掉一次：表里说有 1 个，实际有 2 个。"),
                ("<b>Data lost</b> — two threads add to the same empty bucket; one node overwrites the other.",
                 "<b>丢数据</b>——两个线程同时往同一个空桶放，一个节点把另一个覆盖掉。"),
                ("<b>Broken list / infinite loop</b> — JDK 7 head-insert during resize could make a circle, then <code>get</code> spins forever.",
                 "<b>链坏掉 / 死循环</b>——JDK 7 扩容时头插法可能把链拧成圈，之后 <code>get</code> 永远转不出来。"),
            ]),
            ("note", "Java 8 changed resize to keep the order (no circle), but data loss and wrong size still happen. "
                     "“No circle” is not “thread-safe”.",
             "Java 8 把扩容改成保序（不会再成环），但丢数据和 size 不准依然存在。“不成环”不等于“线程安全”。"),
        ]),
        ("h2", "03", "How to fix it", "怎么解决", [
            ("table", [("Option", "方案"), ("Good for", "适合"), ("Watch out", "注意")],
             [[("ConcurrentHashMap", "ConcurrentHashMap"), ("web apps, shared caches", "Web 应用、共享缓存"),
               ("null keys not allowed", "不允许 null key")],
              [("Collections.synchronizedMap", "Collections.synchronizedMap"), ("rare, small maps", "很少用、很小的表"),
               ("one lock for everything", "整表一把锁，慢")],
              [("ThreadLocal", "ThreadLocal"), ("per-user / per-request data", "每用户、每请求的数据"),
               ("memory leak in thread pools", "线程池里会内存泄漏")],
              [("Local variable", "局部变量"), ("inside one method", "方法内部"), ("nothing", "没有")]]),
        ]),
        ("h2", "04", "One sentence for the interview", "面试用一句话", [
            ("quote", "short", "Say it like this", "可以这样说",
             [("HashMap is not thread-safe because put is a multi-step write: two threads can overwrite each other's size, "
               "lose a node, or in JDK 7 even build a circle and loop forever. In a web application I use ConcurrentHashMap.",
               "HashMap 线程不安全，因为 put 是多步写入：两个线程会互相覆盖 size、丢节点，JDK 7 里甚至会成环死循环。"
               "Web 应用里我用 ConcurrentHashMap。")]),
        ]),
    ],
    "words": [
        ("thread", "/θred/", "One worker inside a program.", "线程：程序里的一个执行单位"),
        ("concurrent", "/kənˈkɜːrənt/", "Happening at the same time.", "并发的：同时发生"),
        ("race condition", "/reɪs kənˈdɪʃn/", "The result depends on who runs first.", "竞态：结果取决于谁先跑"),
        ("lock", "/lɑːk/", "Let only one worker in.", "锁：只让一个线程进"),
        ("synchronized", "/ˈsɪŋkrənaɪzd/", "Java keyword: one thread at a time.", "synchronized：Java 关键字，一次只一个线程"),
        ("volatile", "/ˈvɑːlətl/", "Java keyword: always read the newest value.", "volatile：总是读最新值"),
    ],
    "checks": [
        ("Why can size be wrong after two puts?", "为什么两次 put 之后 size 会不准？"),
        ("What was special about JDK 7 resize?", "JDK 7 的扩容有什么特别之处？"),
        ("What would you use in a Spring service, and why?", "Spring 服务里你会用什么？为什么？"),
    ],
    "next": '<a href="../questions/java-hashmap.html"><span class="in-en">Next: the whole HashMap answer →</span>'
            '<span class="in-zh">下一步：HashMap 整道题 →</span></a>',
}

QUESTION = {
    "path": "questions/java-hashmap.html",
    "title": ("How does HashMap work", "HashMap 是怎么工作的"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Question 1: HashMap</span><span class="in-zh">第 1 题：HashMap</span>',
    "kicker": ("Question 1 · HashMap", "第 1 题 · HashMap"),
    "h1": ("How does HashMap work?", "HashMap 是怎么工作的？"),
    "lede": ("A box of small boxes. Give it a key, get back a value, very fast.",
             "一个装着小盒子的盒子：给它 key，它很快还你 value。"),
    "tags": [("Must know", "必背"), ("HashMap", "HashMap"), ("speak 60s", "60 秒口播"), ("7 lessons", "关联 7 课")],
    "on": "q",
    "blocks": [
        ("h2", "01", "One sentence", "一句话", [
            ("quote", "short", "Say this first", "先说这句",
             [("A HashMap is a box of small boxes. You give it a key, and it gives you back a value very fast. Inside, it uses "
               "an array. Each box in the array is called a bucket. When two keys fall into the same bucket, they stand in a line.",
               "HashMap 是一个装着小盒子的盒子：给它 key，它很快还你 value。底层是一个数组，数组里每一格叫一个桶。"
               "两个 key 落进同一个桶时，就排成一队（链表）。")]),
        ]),
        ("h2", "01b", "The whole thing in nine sentences", "九句话讲清楚（零基础版）", [
            ("ol", [
                ("It is a box: you give it a name (key), it gives back the thing (value) — fast.",
                 "它是个盒子：给它一个名字（key），它很快把对应的东西（value）还给你。"),
                ("Inside is a row of numbered boxes: an array of 16 buckets, numbered 0–15.",
                 "里面是一排带编号的格子，共 16 个，编号 0–15。这排格子就叫数组。"),
                ("When you put something, it computes a number from the key. That number is the hash.",
                 "放东西时，它拿 key 算出一个数字，这个数字叫 hash。"),
                ("The hash picks a bucket. Next time you look up the same key, it picks the same bucket — no searching.",
                 "用 hash 选格子。下次用同样的 key 来拿，还是同一个格子——不用一格格找，所以快。"),
                ("Two different keys can get the same bucket. That is a collision. The fix: put them in a line inside that bucket.",
                 "两个不同的 key 可能选中同一个格子，这叫冲突。办法：在这个格子里挂一条队伍。"),
                ("Looking up a key in a line means comparing names one by one — until the name matches.",
                 "格子里是队伍时，就顺着队伍一个一个比名字，比到为止。"),
                ("When one line reaches 8 items, the line becomes a red-black tree, so a lookup takes only a few steps.",
                 "某一格排到 8 个时，这条队伍变成红黑树——查东西只要几步。"),
                ("At 75% full, the array doubles from 16 to 32, and items are re-split. No hash is recomputed.",
                 "装到 75% 满时，数组从 16 格扩成 32 格，东西重新分一遍；技巧是不用重算 hash。"),
                ("It is not thread-safe: two threads writing at once can overwrite each other. Use ConcurrentHashMap.",
                 "它线程不安全：两个线程同时写会互相覆盖、丢数据。并发里用 ConcurrentHashMap。"),
            ]),
            ("note", "If all nine are clear, you can already answer this question in an interview. The rest is detail.",
             "这九句都清楚，这道题你已经会答了。剩下的都是细节。"),
        ]),

        ("h2", "02", "What is inside", "里面是什么", [
            ("p", "Outside, it looks like a table of names and values:",
             "从外面看，是一张“名字 → 值”的表："),
            ("table", [("key", "键"), ("value", "值")],
             [[('"apple"', '"apple"'), ("5", "5")], [('"pear"', '"pear"'), ("3", "3")]]),
            ("p", "Inside, it is an <b>array of buckets</b>. A bucket has three possible states: empty, a short line, or a tree.",
             "从里面看，是一个<b>桶数组</b>。一个桶只有三种状态：空、短链、树。"),
            ("figure",
             '<div class="arr">'
             '<div class="cell">0</div><div class="cell">1</div><div class="cell">2</div><div class="cell on">3</div>'
             '<div class="cell">4</div><div class="cell">5</div><div class="cell">6</div><div class="cell">7</div>'
             '<div class="cell">8</div><div class="cell on">9</div><div class="cell">10</div><div class="cell">11</div>'
             '<div class="cell on">12</div><div class="cell">13</div><div class="cell">14</div><div class="cell">15</div>'
             '</div>'
             '<div class="chainrow">'
             '<div class="chain"><span class="node">bucket 3: Node</span><span class="nil">→ null</span></div>'
             '<div class="chain"><span class="node">bucket 9: Node</span><span class="arrow">→</span><span class="node">Node</span>'
             '<span class="arrow">→</span><span class="node">Node</span><span class="nil">→ null</span></div>'
             '<div class="chain"><span class="node tree">bucket 12: red-black tree</span></div>'
             '</div>'
             '<figcaption><span class="in-en">An array of 16 buckets. Bucket 9 holds a short line. Bucket 12 has become a tree.</span>'
             '<span class="in-zh">16 个桶的数组：桶 9 是一条短链，桶 12 已经变成了红黑树。</span></figcaption>'),
        ]),
        ("h2", "03", "How put works", "put 的六步", [
            ("ol", [
                ("<b>Make the table</b> — the first put creates the array with 16 buckets.",
                 "<b>建表</b>——第一次 put 才创建 16 格数组。"),
                ("<b>Compute the hash</b> — <code>(h = key.hashCode()) ^ (h &gt;&gt;&gt; 16)</code>, mixing high bits into low bits.",
                 "<b>算 hash</b>——<code>(h = key.hashCode()) ^ (h &gt;&gt;&gt; 16)</code>，把高位混进低位。"),
                ("<b>Find the bucket</b> — <code>index = (n - 1) &amp; hash</code>; because n is a power of two this equals "
                 "<code>hash % n</code>, but faster.",
                 "<b>定位桶</b>——<code>index = (n - 1) &amp; hash</code>；因为 n 是 2 的幂，这等价于 <code>hash % n</code>，但更快。"),
                ("<b>Empty bucket?</b> — put a new node there. Done.", "<b>桶是空的？</b>——放一个新节点，结束。"),
                ("<b>Not empty?</b> — same key → replace the value; different key → go to the end of the line; at 8 items the bucket "
                 "may become a tree.",
                 "<b>不空？</b>——key 相同就覆盖 value；不同就挂到链尾；到 8 个可能树化。"),
                ("<b>Too full?</b> — if <code>size &gt; capacity × 0.75</code>, double the array.", "<b>太满了？</b>——超过 容量 × 0.75 就扩容一倍。"),
            ]),
            ("pre", """if ((tab = table) == null || (n = tab.length) == 0)
    n = (tab = resize()).length;                  // 1. create the array
if ((p = tab[i = (n - 1) & hash]) == null)
    tab[i] = newNode(hash, key, value, null);     // 2. empty bucket
else {
    if (p.hash == hash && (p.key == key || key.equals(p.key)))
        e = p;                                    // 3. same key: replace
    else if (p instanceof TreeNode)
        e = ((TreeNode<K,V>) p).putTreeVal(...);   // 4. bucket is a tree
    else {
        for (int binCount = 0; ; ++binCount) {
            if ((e = p.next) == null) {
                p.next = newNode(hash, key, value, null);  // 5. add at the end
                if (binCount >= TREEIFY_THRESHOLD - 1)
                    treeifyBin(tab, hash);                 //    line too long: tree
                break;
            }
            if (e.hash == hash && (e.key == key || key.equals(e.key))) break;
            p = e;
        }
    }
    if (e != null) { V old = e.value; e.value = value; return old; }
}
++modCount;
if (++size > threshold) resize();                 // 6. too full: grow
return null;"""),
        ]),
        ("h2", "04", "Why resize is cheap", "为什么扩容不贵", [
            ("p", "From 16 to 32, an item has only two possible places: <b>where it is</b>, or <b>where it is + 16</b>. One bit decides:",
             "从 16 扩到 32，每个元素只有两种去处：<b>原位</b>，或者<b>原位 + 16</b>。看一位就够："),
            ("pre", """if ((e.hash & oldCap) == 0)  keep the item at index i
else                          move it to index i + oldCap"""),
            ("p", "So HashMap does not recompute every hash. It splits each bucket into two short lines.", "所以不用重算每个 hash，只是把每个桶拆成两条短链。"),
        ]),
        ("h2", "05", "Two numbers: 0.75 and 8", "两个数字：0.75 和 8", [
            ("table", [("Number", "数字"), ("Means", "含义"), ("Why", "为什么")],
             [[("0.75", "0.75"), ("grow when size > capacity × 0.75", "超过 容量 × 0.75 就扩容"),
               ("balance memory and collisions", "内存和冲突的平衡点")],
              [("8", "8"), ("a bucket with 8 items may treeify", "桶里 8 个可能树化"),
               ("a good hash rarely makes a line of 8", "hash 好时几乎不会有 8 个")],
              [("64", "64"), ("the array must have 64 buckets to treeify", "容量至少 64 才允许树化"),
               ("small array: growing is cheaper", "数组小的时候扩容更划算")],
              [("6", "6"), ("a tree with 6 items turns back to a line", "树里剩 6 个就退回链表"),
               ("a buffer, to avoid flipping", "留缓冲，避免来回变")]]),
        ]),
        ("h2", "06", "Why it is not thread-safe", "为什么线程不安全", [
            ("p", "Two threads call put at the same time: both read size, both write it back — one update is lost. "
                  "In JDK 7, two resizes at once could bend a list into a circle and get would spin forever.",
             "两个线程同时 put：都读到 size、都写回——丢掉一次更新。JDK 7 里两个线程同时扩容，"
             "甚至能把链拧成环，get 就永远转不出来。"),
            ("p", "So in a web application I use <b>ConcurrentHashMap</b>: it locks only the bucket being changed.",
             "所以 Web 应用里我用 <b>ConcurrentHashMap</b>：它只锁正在改的那个桶。"),
            ("note", "Long version: <a href=\"../basics/threads.html\">Lesson 7</a>.",
             "完整版：<a href=\"../basics/threads.html\">第 7 课</a>。"),
        ]),
        ("h2", "07", "Go deeper, one idea at a time", "再往下学，一次一个概念", [
            ("links", [
                ("../basics/array.html", "Lesson 1: What is an array?", "第 1 课：什么是数组"),
                ("../basics/linked-list.html", "Lesson 2: What is a linked list?", "第 2 课：什么是链表"),
                ("../basics/tree.html", "Lesson 3: What is a tree? Red-black tree?", "第 3 课：什么是树、红黑树"),
                ("../basics/hash.html", "Lesson 4: key, hash, collision", "第 4 课：key、hash、冲突"),
                ("../basics/big-o.html", "Lesson 5: O(1), O(n), O(log n)", "第 5 课：O(1)、O(n)、O(log n)"),
                ("../basics/hashmap-methods.html", "Lesson 6: HashMap methods in real code", "第 6 课：HashMap 方法与真实用法"),
                ("../basics/threads.html", "Lesson 7: Why it is not thread-safe", "第 7 课：为什么线程不安全"),
            ]),
        ]),
    ("h2", "08", "Interview script", "面试话术（60 秒）", [
        ("note", "Four steps, always in this order: structure → collision → resize → limits.",
         "四步，顺序固定：结构 → 冲突 → 扩容 → 边界。"),
        ("ol", [
            ("Structure: an array of buckets, O(1) lookup.", "结构：一个数组，每格一个桶，平均 O(1)。"),
            ("Collision: same bucket → list → tree at 8.", "冲突：同一个桶 → 链表；8 个转红黑树。"),
            ("Resize: over 0.75 × capacity → double, no hash recompute.", "扩容：超过容量 0.75 翻倍，不重算 hash。"),
            ("Limits: not thread-safe → ConcurrentHashMap.", "边界：线程不安全 → 用 ConcurrentHashMap。"),
        ]),
        ("quote", "short", "Say this, 60 seconds", "照这段说，60 秒", [
            ("HashMap is an array of buckets. To put a value, it computes the key hash code, uses it to pick a bucket, and stores the entry there, so a lookup is O(1) on average.",
             "HashMap 底层是一个数组，每一格叫一个桶。放数据时先用 key 的 hashCode 算出 hash，用 hash 定位到桶，所以查找平均是 O(1)。"),
            ("If two keys land in the same bucket, that is a collision: the bucket keeps a linked list. When a list reaches 8 entries and the array has at least 64 buckets, the list becomes a red-black tree, and lookup drops from O(n) to O(log n).",
             "如果两个 key 落到同一个桶，就是哈希冲突：桶里挂一条链表。链表到 8 个、并且容量至少 64 时，会转成红黑树，查找从 O(n) 降到 O(log n)。"),
            ("When the number of entries passes capacity times 0.75, the array doubles. Because the capacity is a power of two, every entry either stays where it is or moves by the old capacity, so no hash is recomputed.",
             "元素超过容量 × 0.75 时扩容一倍。因为容量是 2 的幂，每个元素要么留在原位、要么挪到「原位 + 旧容量」，所以不用重算 hash。"),
            ("It is not thread-safe: two threads putting at once can lose data. So for shared mutable state I use ConcurrentHashMap, and I keep plain HashMap for read-only dictionaries and grouping.",
             "它线程不安全，多线程同时 put 会丢数据，所以共享可变状态我用 ConcurrentHashMap；只有只读的字典和分组统计我才用 HashMap。"),
        ]),
        ("p", "Last line, and make it yours — pick one of these from your own projects:",
         "最后一句，换成你自己的项目（选一条你说得出口的）："),
        ("ul", [
            ("Selling machines / satellite stations: <code>ConcurrentHashMap&lt;String, Channel&gt;</code> holds 300+ online devices.",
             "智能售货机 / 卫星地面站：用 ConcurrentHashMap 管 300+ 台在线设备的连接和状态。"),
            ("News ranking: count views in a local ConcurrentHashMap, flush to a Redis sorted set every minute.",
             "热搜榜：本地 ConcurrentHashMap 先计数，每分钟刷进 Redis 有序集合算排名。"),
            ("Order system: index multi-platform orders by platform order id, and cache the status dictionary.",
             "订单系统：按平台单号建索引做去重匹配，状态字典放只读 Map 里缓存。"),
            ("Data reporting: the form engine carries dynamic fields in <code>Map&lt;String, Object&gt;</code>, stats by <code>groupingBy</code>.",
             "数据报送：模板化表单用 Map&lt;String, Object&gt; 承载动态字段，统计用 groupingBy。"),
        ]),
        ("note", "Before you memorise anything: <a href=\"../game/hashmap.html\">play the 5-minute bucket game</a> — you will feel the collision, the resize and the tree.",
         "背之前先手过一遍：<a href=\"../game/hashmap.html\">玩 5 分钟装桶小游戏</a>——冲突、扩容、树化，手上过一遍就记住了。"),
    ]),
    ("h2", "09", "Eight follow-ups", "八个必答追问", [
        ("table", [("Question", "问题"), ("One line", "一句话答")], [
            [("Why must capacity be a power of two?", "为什么容量必须是 2 的幂？"),
             ("(n-1) & hash equals modulo but is faster; on resize one bit decides where it goes.",
              "因为 (n-1) & hash 等价于取模但更快；扩容时只看一位就知道去哪。")],
            [("Why 0.75?", "为什么是 0.75？"),
             ("The trade-off between wasted space and long buckets. Lower wastes memory, higher makes buckets long.",
              "空间和冲突的折中：太低浪费内存，太高桶变长、查询退化。")],
            [("Why 8 for treeify?", "为什么 8 才树化？"),
             ("With a good hash the chance of 8 in a row is about 6 in 10 million, so 8 means the hash is broken.",
              "好的 hash 下链表到 8 的概率约千万分之六，到了说明 hash 有问题。")],
            [("Why 6 to untreeify?", "为什么退化是 6？"),
             ("A buffer, so it does not flip between 7 and 8 again and again.",
              "留缓冲，避免 7、8 之间来回转。")],
            [("Why did JDK 7 loop forever?", "JDK 7 为什么会死循环？"),
             ("Head insertion plus two threads resizing can make a ring in the list; then get never returns.",
              "头插法 + 两个线程同时扩容，可能把链表拧成环，get 就永远转不出来。")],
            [("Why rewrite hashCode with equals?", "为什么 equals 和 hashCode 要一起重写？"),
             ("Or two equal keys land in two buckets and the value is lost.",
              "否则相等的两个 key 会落到两个桶，值就「丢」了。")],
            [("HashMap vs Hashtable vs ConcurrentHashMap?", "和 Hashtable、ConcurrentHashMap 的区别？"),
             ("Hashtable locks the whole table; ConcurrentHashMap locks one bucket and reads without locks.",
              "Hashtable 整表一把锁，早淘汰了；ConcurrentHashMap 桶级锁，读不加锁。")],
            [("Why not use HashMap as a cache?", "为什么不直接用 HashMap 做缓存？"),
             ("No expiry, no size limit, not thread-safe, never collected.",
              "没有过期、没有上限、线程不安全、一直在 GC 里活着。")],
        ]),
    ]),
    ("h2", "10", "Three things not to say", "三句别说", [
        ("ul", [
            ("I read the source code — one question and it shows.", "「我看过源码，我背过 putVal」——一追问就露。"),
            ("I tuned the load factor to 0.5 — they will ask for your benchmark data.",
             "「我把 loadFactor 调成 0.5 优化过」——会问你要压测数据。"),
            ("HashMap is thread-safe — that ends the interview.",
             "「HashMap 是线程安全的」——直接出局。"),
        ]),
        ("note", "When you truly do not know: say what you guess, then say you will check the source. Honest plus a direction beats making it up.",
         "真不会的时候：说你的推测，再说回去查源码确认。诚实 + 有方向，比你硬编好得多。"),
    ]),
    ],
    "words": [
        ("bucket", "/ˈbʌkɪt/", "One box of the array.", "桶：数组的一格"),
        ("capacity", "/kəˈpæsəti/", "How many buckets the array has.", "容量：数组有多少格"),
        ("load factor", "/loʊd ˈfæktər/", "How full before it grows. 0.75.", "负载因子：多满就扩容，默认 0.75"),
        ("threshold", "/ˈθreʃhoʊld/", "capacity × load factor.", "阈值：容量 × 负载因子"),
        ("treeify", "/ˈtriːɪfaɪ/", "Turn a long bucket line into a tree.", "树化：把长链变成树"),
        ("collision", "/kəˈlɪʒn/", "Two keys in the same bucket.", "冲突：两个 key 在一个桶"),
    ],
    "checks": [
        ("Explain the whole thing in 60 seconds, in English.", "用英文把整件事讲 60 秒。"),
        ("Where does the bucket index come from?", "桶的位置是怎么算出来的？"),
        ("Why does resize not recompute the hash?", "为什么扩容不用重算 hash？"),
        ("What would you say if I ask “then why not always use ConcurrentHashMap?”",
         "如果我问“那为什么不干脆一直用 ConcurrentHashMap”，你怎么答？"),
    ],
    "next": '<a href="../glossary.html"><span class="in-en">Next: practice the words →</span>'
            '<span class="in-zh">下一步：把词练熟 →</span></a>',
}

ABOUT = {
    "path": "about.html",
    "title": ("About", "关于"),
    "crumb": '<a href="index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">About</span><span class="in-zh">关于</span>',
    "kicker": ("About", "关于"),
    "h1": ("Learn Java, in English.", "用英文学 Java。"),
    "lede": ("Short sentences, real pronunciation, and a Chinese line whenever you need it.",
             "短句子、真人发音，需要的时候还有一行中文。"),
    "tags": [("English first", "英文优先"), ("no tracking", "无追踪")],
    "on": "",
    "blocks": [
        ("h2", "01", "Why this site exists", "为什么做这个站", [
            ("p", "I am learning Java and English at the same time. If I read Java in Chinese, I learn the idea only. "
                  "If I read it in English, I learn the idea and the words I will hear in an interview.",
             "我在同时学 Java 和英语。用中文读 Java，只学到概念；用英文读，概念和面试里会听到的词一起学到。"),
        ]),
        ("h2", "02", "Three buttons", "三个按钮", [
            ("ul", [
                ("<b>中文</b> — read only Chinese.", "<b>中文</b>——只看中文。"),
                ("<b>中英</b> — English first, Chinese under it. Good for the hard pages.",
                 "<b>中英</b>——先英文，下面跟一行中文。难页用这个。"),
                ("<b>English</b> — the real test.", "<b>English</b>——真正的考试模式。"),
            ]),
        ]),
        ("h2", "03", "How to use it", "怎么用", [
            ("ol", [
                ("Press <b>🔊</b> and follow with your eyes.", "点 <b>🔊</b>，眼睛跟着字走。"),
                ("Say five new words out loud, after YouGlish.", "跟着 YouGlish 把五个新词读出声。"),
                ("Answer the checks out loud, then read the page again if you could not.",
                 "自测题出声回答，答不出来就回去再读。"),
            ]),
            ("note", "Plain HTML, no framework, no tracking. Published by GitHub Pages from <a href=\"https://github.com/TianYuBaBg/offer-camp\">this repository</a>.",
             "纯 HTML，没有框架，没有追踪。由 GitHub Pages 从<a href=\"https://github.com/TianYuBaBg/offer-camp\">这个仓库</a>发布。"),
        ]),
    ],
    "words": [
        ("plain", "/pleɪn/", "Simple, without extra things.", "plain：简单的、不加料的"),
        ("framework", "/ˈfreɪmwɜːrk/", "A set of tools you build on.", "framework：一套打底的工具"),
    ],
    "checks": [
        ("Which mode will you use today?", "今天你打算用哪个模式？"),
        ("Say the three buttons in English.", "用英文说出三个按钮。"),
    ],
    "next": '<a href="index.html"><span class="in-en">Back to the map →</span><span class="in-zh">回目录 →</span></a>',
}

# ---------------- 词表 ----------------
GLOSSARY_GROUPS = [
    ("Data structures", "数据结构", [
        ("array", "/əˈreɪ/", "A row of boxes that touch each other.", "数组：紧挨着的一排盒子"),
        ("index", "/ˈɪndeks/", "The number of a box. Starts at 0.", "下标：盒子编号，从 0 开始"),
        ("element", "/ˈelɪmənt/", "One item inside an array.", "元素：里面的一个东西"),
        ("contiguous", "/kənˈtɪɡjuəs/", "Touching, with no gaps.", "连续的：紧挨着没空隙"),
        ("linked list", "/lɪŋkt lɪst/", "Boxes joined by pointers.", "链表：用指针串起来"),
        ("node", "/noʊd/", "A value plus a pointer.", "节点：值 + 指针"),
        ("pointer", "/ˈpɔɪntər/", "Where the next box is.", "指针：下一个在哪"),
        ("head", "/hed/", "The first node.", "头节点：第一个"),
        ("null", "/nʌl/", "Nothing.", "null：空"),
        ("traverse", "/trəˈvɜːrs/", "Walk through one by one.", "遍历：一个个走"),
        ("tree", "/triː/", "Nodes with children.", "树：带孩子的节点"),
        ("root", "/ruːt/", "The top node.", "根：最上面"),
        ("leaf", "/liːf/", "A node with no children.", "叶子：没有孩子"),
        ("height", "/haɪt/", "How many levels.", "高度：有几层"),
        ("balanced", "/ˈbælənst/", "Left and right are similar.", "平衡：左右差不多"),
        ("rotate", "/ˈroʊteɪt/", "Turn the tree to fix height.", "旋转：转一下调高度"),
        ("red-black tree", "/red blæk triː/", "A tree that colours and rotates itself.", "红黑树：靠颜色和旋转保持平衡"),
    ]),
    ("HashMap", "HashMap", [
        ("HashMap", "/hæʃ mæp/", "Map by key, an array of buckets.", "HashMap：桶数组实现的键值表"),
        ("key", "/kiː/", "The name you look things up by.", "key：用来查的名字"),
        ("value", "/ˈvæljuː/", "The thing stored under a key.", "value：存在 key 下的东西"),
        ("entry", "/ˈentri/", "One key-value pair.", "entry：一个键值对"),
        ("hash", "/hæʃ/", "A number computed from a key.", "hash：由 key 算出的编号"),
        ("hashCode", "/hæʃ koʊd/", "The Java method that gives it.", "hashCode：给出编号的方法"),
        ("bucket", "/ˈbʌkɪt/", "One box of the array.", "桶：数组的一格"),
        ("collision", "/kəˈlɪʒn/", "Two keys in one bucket.", "冲突：两个 key 一个桶"),
        ("capacity", "/kəˈpæsəti/", "How many buckets now.", "容量：现在有多少格"),
        ("load factor", "/loʊd ˈfæktər/", "How full before growing. 0.75.", "负载因子：多满就扩容"),
        ("threshold", "/ˈθreʃhoʊld/", "capacity × load factor.", "阈值：容量 × 负载因子"),
        ("resize", "/ˌriːˈsaɪz/", "Double the array and move items.", "扩容：翻倍并搬数据"),
        ("treeify", "/ˈtriːɪfaɪ/", "Turn a long line into a tree.", "树化：长链变树"),
        ("equals", "/ˈiːkwəlz/", "Says two keys are the same.", "equals：判断 key 相同"),
        ("cache", "/kæʃ/", "A fast copy of slow data.", "缓存：慢数据的快副本"),
    ]),
    ("Complexity", "复杂度", [
        ("time complexity", "/taɪm kəmˈpleksəti/", "How time grows with size.", "时间复杂度"),
        ("Big O", "/bɪɡ oʊ/", "The notation for growth.", "大 O：增长记号"),
        ("constant", "/ˈkɑːnstənt/", "O(1), does not grow.", "常数：O(1)"),
        ("linear", "/ˈlɪniər/", "O(n), grows in a line.", "线性：O(n)"),
        ("logarithmic", "/ˌlɔːɡəˈrɪðmɪk/", "O(log n), grows slowly.", "对数：O(log n)"),
        ("quadratic", "/kwɑːˈdrætɪk/", "O(n²), every pair.", "平方：O(n²)"),
        ("amortized", "/əˈmɔːrtaɪzd/", "Average over many operations.", "均摊：多次操作的平均"),
    ]),
    ("Concurrency", "并发", [
        ("thread", "/θred/", "One worker inside a program.", "线程：一个执行单位"),
        ("concurrent", "/kənˈkɜːrənt/", "At the same time.", "并发的：同时的"),
        ("race condition", "/reɪs kənˈdɪʃn/", "Result depends on order.", "竞态：结果看谁先跑"),
        ("lock", "/lɑːk/", "Only one goes in.", "锁"),
        ("synchronized", "/ˈsɪŋkrənaɪzd/", "One thread at a time.", "synchronized：一次一个"),
        ("volatile", "/ˈvɑːlətl/", "Always read the newest.", "volatile：读最新值"),
        ("thread-safe", "/θred seɪf/", "Safe from many threads.", "线程安全"),
        ("ConcurrentHashMap", "/kənˈkɜːrənt hæʃ mæp/", "Thread-safe HashMap, locks one bucket.", "ConcurrentHashMap：只锁一个桶"),
    ]),
]

GLOSSARY = {
    "path": "glossary.html",
    "title": ("All the words", "所有词"),
    "crumb": '<a href="index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Words</span><span class="in-zh">词表</span>',
    "kicker": ("Glossary", "词表"),
    "h1": ("All the words, in one place.", "所有词，都在这。"),
    "lede": ("Every word from the lessons: how it sounds, and what it means in one line.",
             "课上出现的每个词：怎么读，一句话什么意思。"),
    "tags": [("47 words", "47 个词"), ("read aloud", "都要读出声")],
    "on": "w",
    "blocks": [],
    "words": [],
    "checks": [],
    "next": '<a href="basics/array.html"><span class="in-en">Start with Lesson 1</span>'
            '<span class="in-zh">从第 1 课开始</span></a>',
    "groups": GLOSSARY_GROUPS,
}

