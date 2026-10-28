# -*- coding: utf-8 -*-
"""每页的“先给答案”和“参考答案”。key = 页面路径。"""

ANSWERS = {
    "index.html": {
        "answer": ("This site teaches Java in English, one idea per page: seven short lessons, then the HashMap interview question.",
                   "这个站用英文教 Java，一页只讲一个概念：先上七节短课，再读 HashMap 那道面试题。"),
        "answers": [
            ("I read one page, learn five words, and answer three questions out loud.",
             "今天要做的事：读一页、学五个词、出声答三道题。"),
            ("Start with Lesson 1, “What is an array?”.",
             "从第 1 课开始：什么是数组。"),
            ("bucket — one box of the array.",
             "bucket：数组里的一格。"),
        ],
    },
    "basics/array.html": {
        "answer": ("An array is a row of numbered boxes that sit next to each other. You reach a box by its number (index), "
                   "which starts at 0. Reading is O(1); inserting in the middle is O(n).",
                   "数组是一排紧挨着、带编号的盒子。用编号（下标，从 0 开始）直接跳到某一格。读是 O(1)，往中间插入是 O(n)。"),
        "answers": [
            ("Because the address is computed, not searched: start + index × size. One step.",
             "因为地址是算出来的，不是找出来的：起始地址 + 下标 × 每格大小，一步到位。"),
            ("Every item after the insert point moves one step to the right: O(n).",
             "插入点后面的每一个元素都要往右挪一步：O(n)。"),
            ("Read O(1); add at the end with room O(1); insert at the front or middle O(n).",
             "读 O(1)；末尾还有空位时加 O(1)；最前面或中间插 O(n)。"),
        ],
    },
    "basics/linked-list.html": {
        "answer": ("A linked list is boxes joined by pointers: each node keeps a value and where the next node is. "
                   "You cannot jump, you walk. Inserting is O(1) once you stand there; finding that place is O(n).",
                   "链表是用指针串起来的盒子：每个节点存一个值和下一个节点的位置。不能跳，只能顺着走。"
                   "已经站在那一点时插入是 O(1)，但找到那一点要 O(n)。"),
        "answers": [
            ("There is no index and no formula. The boxes are not next to each other, so you must follow every pointer.",
             "没有下标也没有公式。盒子不连续，只能一个指针一个指针地走。"),
            ("Linked list: change two pointers, O(1). An array would shift everything after it, O(n).",
             "链表：改两个指针，O(1)。数组要把后面全部挪一遍，O(n)。"),
            ("null — “nothing”. That is how you know the list has ended.",
             "null，表示“没有了”。看到它就说明到头了。"),
        ],
    },
    "basics/tree.html": {
        "answer": ("A tree is a list that forks: each node has up to two children, left smaller and right bigger, so each "
                   "comparison halves what is left — O(log n). A red-black tree is a tree that colours its nodes and rotates "
                   "after inserts so it never becomes a line.",
                   "树是“会分叉的链表”：每个节点最多两个孩子，左小右大，每比较一次就砍掉一半，所以是 O(log n)。"
                   "红黑树是一种靠“涂色 + 插入后旋转”保证自己不会退化成一条线的树。"),
        "answers": [
            ("Each step halves the remaining nodes: 1000 → 500 → 250 → … about 10 steps.",
             "每走一步砍掉一半：1000 → 500 → 250……大约 10 步。"),
            ("It becomes a line again, and lookup falls back to O(n).",
             "它又变成一条线，查找退化回 O(n)。"),
            ("They keep the height near 2 × log n, so the worst case stays O(log n).",
             "颜色规则把高度控制在 2 × log n 左右，最坏情况仍是 O(log n)。"),
        ],
    },
    "basics/hash.html": {
        "answer": ("A key is the name you look things up by. A hash is a number computed from that key. A collision is two "
                   "different keys that get the same number, so they share a bucket. HashMap answers a collision with a short "
                   "list, and with a red-black tree once one bucket holds 8 items.",
                   "key 是你用来查东西的名字；hash 是由这个 key 算出来的一个数字；冲突是两个不同的 key 算出了同一个数字，"
                   "于是挤进同一个桶。HashMap 用一条短链处理冲突，桶里攒到 8 个就换成红黑树。"),
        "answers": [
            ("Key: what you give. Hash: the number computed from it. Bucket: the box that number points to.",
             "key：你给的名字；hash：由它算出的编号；桶：编号指向的那一格。"),
            ("Put the new node at the end of that bucket's short list. When the list reaches 8 and capacity is at least 64, "
             "that bucket becomes a red-black tree.",
             "把新节点挂到该桶短链的末尾。链到 8 个、并且容量至少 64 时，这个桶变成红黑树。"),
            ("Otherwise two keys that are equals() can land in different buckets, and one value looks lost.",
             "否则两个 equals() 相同的 key 会落到不同的桶，其中一个值就像丢了。"),
        ],
    },
    "basics/big-o.html": {
        "answer": ("Big O is not seconds; it is how the number of steps grows when the data grows. "
                   "O(1) one step · O(log n) halve each time · O(n) one by one · O(n²) every pair.",
                   "大 O 说的不是几秒，而是“数据变多时步数怎么长”：O(1) 一步；O(log n) 每次砍一半；O(n) 一个一个来；"
                   "O(n²) 两两配对。"),
        "answers": [
            ("Steps grow in a straight line with n: double the data, double the steps.",
             "步数和 n 成正比：数据翻倍，步数也翻倍。"),
            ("One multiplication and one addition give the address. No loop, no search.",
             "一次乘法加一次加法就算出地址，没有循环、没有查找。"),
            ("If the bucket has treeified: about 3 comparisons (log₂8). If it is still a list: at most 8.",
             "已经树化：约 3 次比较（log₂8）；还是链表：最多 8 次。"),
        ],
    },
    "basics/hashmap-methods.html": {
        "answer": ("Six methods cover almost everything: put (add or replace), get (read), getOrDefault (read with a default), "
                   "computeIfAbsent (compute and store only if missing), merge (combine old and new), remove (delete).",
                   "六个方法基本够用：put 存或覆盖；get 读；getOrDefault 读不到给默认值；computeIfAbsent 没有才算并存入；"
                   "merge 合并新旧值；remove 删除。"),
        "answers": [
            ("get returns null when the key is missing; getOrDefault returns the default you pass.",
             "get 没有这个 key 就返回 null；getOrDefault 返回你给的默认值。"),
            ("`cache.computeIfAbsent(id, k -> db.selectById(k))` — one line, no null check.",
             "`cache.computeIfAbsent(id, k -> db.selectById(k))`——一行，不用判空。"),
            ("`count.merge(status, 1, Integer::sum)` — old + 1, or 1 the first time.",
             "`count.merge(status, 1, Integer::sum)`——老值 +1，第一次出现就给 1。"),
        ],
    },
    "basics/threads.html": {
        "answer": ("HashMap is not thread-safe because put is a multi-step write: two threads can overwrite each other's size, "
                   "lose a node, and in JDK 7 even bend a list into a circle so get loops forever. In a web app use "
                   "ConcurrentHashMap, which locks only one bucket.",
                   "HashMap 线程不安全，因为 put 是多步写入：两个线程会互相覆盖 size、丢掉节点；在 JDK 7 里甚至能把链拧成环，"
                   "让 get 永远转不出来。Web 应用里用 ConcurrentHashMap，它只锁一个桶。"),
        "answers": [
            ("Both threads read 10 and write 11. Two nodes were added, but the number went up by one.",
             "两个线程都读到 10、都写 11。实际加了两个节点，数字只涨了 1。"),
            ("It used head insertion, so the list was reversed during resize. Two threads could make a node point back — a circle.",
             "扩容用头插法，链表会被倒置；两个线程同时做，就可能让某个节点指回去，形成环。"),
            ("ConcurrentHashMap: one bucket is locked at a time, so reads stay fast and writes stay safe.",
             "ConcurrentHashMap：一次只锁一个桶，读照样快，写也安全。"),
        ],
    },
    "questions/java-hashmap.html": {
        "answer": ("HashMap is an array of buckets. The hash of the key picks the bucket; each bucket holds a short list, "
                   "which becomes a red-black tree at 8 items (capacity ≥ 64). At 75% full the array doubles, and each item "
                   "moves by one bit. It is fast (O(1) average) but not thread-safe.",
                   "HashMap 是一个桶数组：用 key 的 hash 选桶；每个桶里挂一条短链，攒到 8 个（且容量 ≥ 64）就变红黑树；"
                   "装到 75% 扩容一倍，每个元素只看一位就知道原位还是搬走。它平均 O(1)，但线程不安全。"),
        "answers": [
            ("A HashMap is an array of buckets. The hash picks a bucket; a short list or a tree handles keys that collide. "
             "It grows at 75% by doubling, and it is not thread-safe, so I use ConcurrentHashMap in a web app.",
             "HashMap 是桶数组：hash 选桶，冲突用短链或红黑树。装到 75% 扩容一倍；线程不安全，Web 应用里我用 ConcurrentHashMap。"),
            ("(n - 1) & hash, where n is a power of two — the same as hash % n but faster. The hash is also mixed with "
             "^ (h >>> 16) so high bits take part.",
             "用 (n-1) & hash：n 是 2 的幂，等价于 hash % n 但更快；hash 还会 ^ (h>>>16) 把高位混下来。"),
            ("Because capacity doubles, the old index bits do not change. One new bit says: stay, or + old capacity.",
             "因为容量翻倍，原来的下标位全都不变，只是多了一位：这一位是 0 就原位，是 1 就搬到 原位 + 旧容量。"),
            ("It is safer but costs more: more memory per node, and CAS/lock overhead. A local map inside one method, or a "
             "map used by only one thread, does not need it.",
             "它更安全但更贵：每个节点多占内存，还有 CAS/加锁开销。方法内部的局部 map、只被一个线程用的 map 就不必用它。"),
        ],
    },
    "about.html": {
        "answer": ("A plain HTML site with a language switch: seven short lessons, one interview question and a word list. "
                   "English first; Chinese when a sentence is too hard.",
                   "一个纯 HTML 小站，带语言切换：七节短课、一道面试题、一份词表。英文优先，句子太难时看中文。"),
        "answers": [
            ("中文 to understand, 中英 to connect words with meaning, English to test myself.",
             "中文用来读懂，中英用来把词和意思对上，English 用来考试。"),
            ("Chinese / Bilingual / English.",
             "中文 / 中英 / English。"),
        ],
    },
}

# 首页：九个问题 → 一句话答案 → 对应的课
INDEX_QA_HEAD = [("Question", "问题"), ("One-line answer", "一句话答案"), ("Where", "在哪")]
INDEX_QA = [
    ("What are an array, a linked list and a red-black tree? How are they different?",
     "数组、链表、红黑树分别是什么？区别在哪？",
     "Array: numbered boxes that touch each other — read fast, insert slow. Linked list: boxes joined by pointers — insert fast, find slow. "
     "Red-black tree: a search tree that stays short, so find is O(log n).",
     "数组：紧挨着的带编号盒子，读快、中间插慢；链表：用指针串起来的盒子，插快、找慢；"
     "红黑树：会自己保持矮的查找树，查找 O(log n)。",
     "1–3", "basics/array.html"),
    ("Why do we have to handle hash collisions?",
     "为什么必须处理哈希冲突？",
     "If we do nothing, 1000 keys can sit in one bucket and lookup falls from O(1) to O(n).",
     "不处理的话，一千个 key 可能挤在同一个桶里，查找就从 O(1) 掉到 O(n)。",
     "4", "basics/hash.html"),
    ("What is a linked list, in one line?",
     "链表是什么？一句话。",
     "A node holds a value and where the next node is. You walk, you cannot jump.",
     "一个节点存“值 + 下一个节点在哪”。只能顺着走，不能跳。",
     "2", "basics/linked-list.html"),
    ("Which HashMap methods do I use every day?",
     "HashMap 平时用哪些方法？",
     "put, get, getOrDefault, computeIfAbsent, merge, remove.",
     "put、get、getOrDefault、computeIfAbsent、merge、remove。",
     "6", "basics/hashmap-methods.html"),
    ("What do O(1), O(n) and O(log n) mean?",
     "O(1)、O(n)、O(log n) 是什么意思？",
     "O(1): one step. O(n): one by one, follows the data. O(log n): halve the range every step.",
     "O(1)：一步；O(n)：一个一个来，跟着数据翻倍；O(log n)：每步砍掉一半。",
     "5", "basics/big-o.html"),
    ("What is a key? What is a hash?",
     "什么是 key？什么是 hash？",
     "Key: the name you look up by. Hash: a number computed from that key, used to pick the bucket.",
     "key：你用来查的名字；hash：由 key 算出的编号，用来选桶。",
     "4", "basics/hash.html"),
    ("Why is HashMap not thread-safe?",
     "为什么 HashMap 线程不安全？",
     "put is a multi-step write: two threads overwrite each other's size or lose a node; JDK 7 could even build a circle and loop forever.",
     "put 是多步写入：两个线程会互相覆盖 size、丢节点；JDK 7 里甚至会成环死循环。",
     "7", "basics/threads.html"),
    ("How does HashMap work as a whole?",
     "HashMap 整体是怎么工作的？",
     "Array of buckets + hash picks the bucket + short list or red-black tree inside + doubles at 75% full + not thread-safe.",
     "桶数组 + 用 hash 选桶 + 桶里短链或红黑树 + 75% 时翻倍扩容 + 线程不安全。",
     "题", "questions/java-hashmap.html"),
    ("How should I learn this in English?",
     "我该怎么用英文学这些？",
     "Read in 中文, switch to 中英 to connect words, finish in English and answer out loud.",
     "先用中文读懂，切“中英”把词和意思对上，最后用 English 出声答出来。",
     "法", "about.html"),
]

ANSWERS["glossary.html"] = {
    "answer": ("47 words, five a day: click ▶ hear it twice, say it three times, then cover the meaning and say it from memory.",
               "47 个词，一天五个：点 ▶ hear it 听两遍，跟读三遍，然后盖住意思凭记忆说一遍。"),
}
