# -*- coding: utf-8 -*-
"""内容 A：首页 + 第 1–4 课。"""

INDEX = {
    "title": ("Learn Java in English", "用英文学生 Java"),
    "crumb": '<a href="index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a>',
    "kicker": ("Java in English · for a complete beginner", "英文 Java · 写给完全零基础"),
    "h1": ("One small page. One idea.",
           "一次只读一页，一次只学一个概念。"),
    "lede": ("I know nothing about Java. I want to learn it in English, not in Chinese. "
             "So every page gives one idea, five new words, and three questions I answer out loud.",
             "我不懂 Java，而且我想用英文学，不是用中文背。所以每一页只讲一个概念、"
             "给五个新词、三道要出声回答的题。"),
    "tags": [("2 questions", "2 道题"), ("7 lessons", "7 节课")],
    "blocks": [
        ("h2", "01", "Two interview questions", "两道面试题",
         [
             ("p", "Only two for now. Each one is a page: a 60-second answer, the mechanism behind it, and the new questions it opens.",
              "现在只有两道。一道一页：60 秒答案、背后的机制、以及它又长出了哪些新问题。"),
             ("html", "__QLIST__"),
             ("note", "A third one gets added when the second one is solid.",
              "第二道读透了再加第三道。"),
         ]),
        ("h2", "02", "The ground: seven lessons", "地基：七节课",
         [
             ("p", "If a word in an answer is missing, the page tells you which lesson to read first. These are the seven pieces.",
              "答案里哪个词不认识，页面会告诉你先补哪一节课。就是这七块。"),
             ("html", "__LESSONS__"),
         ]),
        ("h2", "03", "How to read a page", "怎么读一页",
         [
             ("ol", [
                 ("Press <b>🔊</b> at the top. Follow the words with your eyes. Twice is enough.",
                  "点页面顶部的 <b>🔊</b>，眼睛跟着字走。两遍就够。"),
                 ("Switch to <b>中英</b> if a sentence is too hard. Read the English first, then the Chinese.",
                  "句子太难就切到 <b>中英</b>：先读英文，再看中文。"),
                 ("Read the 60-second answer, then the mechanism. The new questions are at the bottom of the page.",
                  "先读 60 秒答案，再读机制。新问题在同一页的底部。"),
                 ("Answer the three questions at the end <b>out loud</b>, not in your head.",
                  "最后三道自测要<b>出声</b>回答，不要只在心里想。"),
             ]),
             ("note", "Twenty minutes a page. One page a day is enough.",
              "一页二十分钟。一天一页就够。"),
         ]),
        ("h2", "04", "Why English, and why so slow", "为什么要英文、为什么这么慢",
         [
             ("p", "In an interview the words are English: <i>bucket</i>, <i>collision</i>, <i>resize</i>. "
                   "If I only know the Chinese word, I hear a sound I cannot follow.",
              "面试里蹦出来的是英文词：bucket、collision、resize。如果我只知道中文说法，听到的就是一串抓不住的声音。"),
             ("p", "So this site is slow on purpose. One question per page, five words, one picture.",
              "所以这个网站是故意慢的：一页一道题、五个词、一张图。"),
         ]),
    ],
    "words": [
        ("bucket", "/ˈbʌkɪt/", "One box in the array.", "桶：数组里的一格"),
        ("collision", "/kəˈlɪʒn/", "Two keys that land in the same bucket.", "冲突：两个 key 落进同一个桶"),
        ("resize", "/ˌriːˈsaɪz/", "Make the array bigger and move items.", "扩容：把数组变大并搬数据"),
        ("thread", "/θred/", "One worker inside a program.", "线程：程序里的一个干活的"),
        ("complexity", "/kəmˈpleksəti/", "How cost grows with size.", "复杂度：代价随数据量的增长方式"),
    ],
    "checks": [
        ("Say the plan for today in one sentence.", "用一句话说出今天要做的事。"),
        ("Which page are you reading today?", "今天你读哪一页？"),
        ("Say one word you learned, out loud.", "说出一个今天学的词，出声。"),
    ],
    "next": '<a href="basics/array.html"><span class="in-en">Start Lesson 1 →</span><span class="in-zh">开始第 1 课 →</span></a>',
}

L1 = {
    "path": "basics/array.html",
    "title": ("What is an array", "什么是数组"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 1: Array</span><span class="in-zh">第 1 课：数组</span>',
    "kicker": ("Lesson 1 · Data structure", "第 1 课 · 数据结构"),
    "h1": ("What is an array?", "什么是数组？"),
    "lede": ("A row of boxes with numbers. If you know the number, you jump straight to the box.",
             "一排带编号的盒子。知道编号，就能一步走到那一格。"),
    "tags": [("Basics", "基础"), ("data structure", "数据结构"), ("O(1) read", "读 O(1)")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The idea", "先有一个画面", [
            ("analogy", "Think of it like this", "先这样想",
             "Ten lockers in a row. They touch each other. Each locker has a number: 0, 1, 2 … 9. "
             "If you know the number, you walk straight to that locker. You do not open the other nine first.",
             "十个储物柜排成一排，紧挨着。每个柜子有编号：0、1、2……9。知道编号，你就直接走到那个柜子，"
             "不用先把另外九个都打开。"),
            ("p", "An <b>array</b> is that row of boxes. It has two facts:",
             "<b>数组</b>就是这一排盒子。它只有两个事实："),
            ("ul", [
                ("The boxes are <b>next to each other</b> in memory.", "这些盒子在内存里<b>紧挨着</b>。"),
                ("Each box has a <b>number</b>, called an <b>index</b>. The first index is <b>0</b>, not 1.",
                 "每个盒子有个<b>编号</b>，叫 <b>index</b>（下标）。第一个是 <b>0</b>，不是 1。"),
            ]),
            ("table", [("index", "下标"), ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")],
             [[("value", "值"), ("apple", "苹果"), ("banana", "香蕉"), ("cherry", "樱桃"), ("date", "枣"), ("fig", "无花果")]]),
        ]),
        ("h2", "02", "Why reading is fast", "为什么“读”很快", [
            ("p", "Because the boxes touch each other, the computer can <b>compute</b> the address:",
             "因为盒子紧挨着，电脑可以直接<b>算出</b>地址："),
            ("pre", "address = start + index × size_of_one_box"),
            ("p", "So reading box 500 costs the same as reading box 0. One step. In Big O words, this is "
                  "<b>O(1)</b> — constant time.",
             "所以读第 500 格和读第 0 格一样快：都是一步。用大 O 的说法，这叫 <b>O(1)</b>，常数时间。"),
        ]),
        ("h2", "03", "Why inserting is slow", "为什么“插入”很慢", [
            ("p", "The boxes are full and touching. If you insert an item in the middle, every item after it must "
                  "<b>move one step</b> to the right. With one thousand items, that is one thousand moves. "
                  "This is <b>O(n)</b> — linear time.",
             "盒子是满的、紧挨着的。在中间插入一个东西，后面的每一个都得<b>往右挪一步</b>。"
             "一千个元素就是一千次挪动。这叫 <b>O(n)</b>，线性时间。"),
            ("note", "When you add to the <b>end</b> and there is still room, it is O(1). Only inserting in the middle "
                     "or at the front is expensive.",
             "往<b>末尾</b>加、并且还有空位，是 O(1)。只有往中间或最前面插才贵。"),
        ]),
        ("h2", "04", "Where you meet it", "你会在哪里遇到它", [
            ("ul", [
                ("A list of orders for today: you know the position, you want it fast.",
                 "今天的订单列表：知道位置，要快。"),
                ("A HashMap is built on an array — that is why lesson 4 exists.",
                 "HashMap 底层就是一个数组，所以后面要学第 4 课。"),
            ]),
        ]),
    ],
    "words": [
        ("array", "/əˈreɪ/", "A row of boxes that touch each other.", "数组：紧挨着的一排盒子"),
        ("index", "/ˈɪndeks/", "The number of a box. Starts at 0.", "下标：盒子的编号，从 0 开始"),
        ("element", "/ˈelɪmənt/", "One item inside an array.", "元素：数组里的一个东西"),
        ("contiguous", "/kənˈtɪɡjuəs/", "Touching, with no gaps.", "连续的：紧挨着没有空隙"),
        ("traverse", "/trəˈvɜːrs/", "Walk through the items one by one.", "遍历：一个个走过去"),
    ],
    "checks": [
        ("Why is reading index 500 as fast as index 0?", "为什么读第 500 格和读第 0 格一样快？"),
        ("What has to happen when you insert in the middle?", "往中间插入时，发生了什么？"),
        ("Which is O(1) and which is O(n): read, insert at the end, insert at the front?",
         "哪个是 O(1)、哪个是 O(n)：读、末尾加、最前面插？"),
    ],
    "next": '<a href="linked-list.html"><span class="in-en">Next: Lesson 2, linked list →</span>'
            '<span class="in-zh">下一课：第 2 课，链表 →</span></a>',
}

L2 = {
    "path": "basics/linked-list.html",
    "title": ("What is a linked list", "什么是链表"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 2: Linked list</span><span class="in-zh">第 2 课：链表</span>',
    "kicker": ("Lesson 2 · Data structure", "第 2 课 · 数据结构"),
    "h1": ("What is a linked list?", "什么是链表？"),
    "lede": ("Boxes that hold hands. Each one knows only where the next one is.",
             "手拉手的一串盒子，每个只知道自己右边是谁。"),
    "tags": [("Basics", "基础"), ("data structure", "数据结构"), ("O(1) insert", "插 O(1)")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The idea", "先有一个画面", [
            ("analogy", "Think of it like this", "先这样想",
             "A treasure hunt. The first note says “the next note is under the tree”. The second says “the next note is "
             "in the kitchen”. To get to the third note, you must read the first and the second. There is no number to jump to.",
             "寻宝游戏：第一张纸条写“下一张在树下”，第二张写“下一张在厨房”。"
             "想到第三张，必须先读第一张、再读第二张。没有编号可以直接跳。"),
            ("p", "A <b>linked list</b> is that chain of notes. Each box is a <b>node</b>. A node holds:",
             "<b>链表</b>就是这一串纸条。每个盒子叫 <b>node</b>（节点），里面装两样东西："),
            ("ul", [
                ("the <b>value</b>", "<b>值</b>（要存的东西）"),
                ("the <b>pointer</b> to the next node", "指向下一个节点的<b>指针</b>"),
            ]),
            ("figure", '<div class="chainrow" style="margin:0"><div class="chain">'
                       '<span class="node">10</span><span class="arrow">→</span><span class="node">20</span>'
                       '<span class="arrow">→</span><span class="node">30</span><span class="nil">→ null</span></div></div>'
                       '<figcaption><span class="in-en">Three nodes. The last one points to null — “nothing”.</span>'
                       '<span class="in-zh">三个节点，最后一个指向 null，意思是“没有了”。</span></figcaption>'),
        ]),
        ("h2", "02", "Array vs linked list", "数组和链表差在哪", [
            ("table", [("", ""), ("Array", "数组"), ("Linked list", "链表")],
             [
                 [("Where the boxes are", "盒子在哪"), ("next to each other", "紧挨着"),
                  ("anywhere, joined by pointers", "随便放，用指针连起来")],
                 [("Read number 500", "读第 500 个"), ("O(1) one step", "O(1)，一步"),
                  ("O(n) walk 500 nodes", "O(n)，要走 500 个")],
                 [("Insert in the middle", "中间插入"), ("O(n) move everything after", "O(n)，后面全要挪"),
                  ("O(1) change two pointers", "O(1)，改两个指针")],
                 [("Memory", "内存"), ("needs one full block", "要一整块连续内存"),
                  ("any small blocks", "小块内存就行")],
             ]),
        ]),
        ("h2", "03", "Why it is used in HashMap", "为什么 HashMap 里要用它", [
            ("p", "Two different keys can land in the same bucket. The simplest fix is to keep them in a short linked list: "
                  "put the new one at the end, and when you look up a key, walk the list and compare keys.",
             "两个不同的 key 可能落进同一个桶。最简单的办法就是把它们串成一条短链表：新的放末尾，"
             "查找时顺着链走、逐个比 key。"),
            ("note", "That is why the array inside a HashMap is called an “array of buckets”: each cell holds the <b>head</b> "
                     "of a small list.",
             "所以 HashMap 里的数组叫“桶数组”：每一格存的是那条短链的<b>头</b>。"),
        ]),
        ("h2", "04", "Where you meet it", "你会在哪里遇到它", [
            ("ul", [
                ("HashMap: one bucket = one short list (lesson 4).",
                 "HashMap：一个桶就是一条短链（第 4 课会讲）。"),
                ("A queue of tasks with a pointer to the next: a linked list.",
                 "任务队列：每个任务指向下一个，本质就是链表。"),
            ]),
        ]),
    ],
    "words": [
        ("linked list", "/lɪŋkt lɪst/", "Boxes joined by pointers.", "链表：用指针串起来的盒子"),
        ("node", "/noʊd/", "One box: a value plus a pointer.", "节点：一个值加一个指针"),
        ("pointer", "/ˈpɔɪntər/", "A value that says where the next box is.", "指针：记录下一个盒子在哪"),
        ("head", "/hed/", "The first node of the list.", "头节点：链表的第一个"),
        ("null", "/nʌl/", "Nothing. The end of a list.", "空；链表的结尾"),
    ],
    "checks": [
        ("Why can I not jump to the 500th item?", "为什么不能直接跳到第 500 个？"),
        ("Insert in the middle: array or linked list? Why?", "中间插入：数组还是链表？为什么？"),
        ("What does the last pointer hold?", "最后一个节点的指针指向什么？"),
    ],
    "next": '<a href="tree.html"><span class="in-en">Next: Lesson 3, tree →</span>'
            '<span class="in-zh">下一课：第 3 课，树 →</span></a>',
}

L3 = {
    "path": "basics/tree.html",
    "title": ("What is a tree", "什么是树"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 3: Tree</span><span class="in-zh">第 3 课：树</span>',
    "kicker": ("Lesson 3 · Data structure", "第 3 课 · 数据结构"),
    "h1": ("What is a tree? And what is a red-black tree?", "什么是树？什么是红黑树？"),
    "lede": ("A list that forks. Each node can have two children, so a search goes left or right.",
             "会分叉的链表：每个节点有两个孩子，查找时往左或往右。"),
    "tags": [("Basics", "基础"), ("data structure", "数据结构"), ("O(log n)", "O(log n)")],
    "on": "b",
    "blocks": [
        ("h2", "01", "The idea", "先有一个画面", [
            ("analogy", "Think of it like this", "先这样想",
             "Guess a number from 1 to 1000, and I count your guesses. If you say 500 and I say “higher”, you do not go 501, "
             "502, 503 — you say 750. Each guess cuts the range in half. Ten guesses are enough for a thousand numbers.",
             "1 到 1000 猜一个数，我数你用几次。你说 500，我说“小了”，你不会接着猜 501、502，你会猜 750。"
             "每次砍掉一半，一千个数十次就猜到。"),
            ("p", "A <b>tree</b> is that guessing game. Each <b>node</b> can have two children: left (smaller) and right (bigger). "
                  "Finding a thing is: go left or go right, again and again.",
             "<b>树</b>就是这个猜数游戏：每个节点最多两个孩子——左孩子更小、右孩子更大。"
             "查找就是反复地“往左还是往右”。"),
        ]),
        ("h2", "02", "Why a line is too slow", "为什么“链”太慢", [
            ("p", "A linked list of 8 items needs up to 8 steps to find one — O(n). A balanced tree of 8 items needs about 3 — "
                  "<b>O(log n)</b>. Each time the data doubles, the tree needs one more step; the list needs double.",
             "8 个元素的链表最多要走 8 步，O(n)；8 个元素的平衡树大约 3 步，<b>O(log n)</b>。"
             "数据翻一倍，树只多一步，链表要多一倍。"),
        ]),
        ("h2", "03", "Why “balanced”", "为什么要“平衡”", [
            ("p", "If the tree grows only on one side, it becomes a line again — and a line is O(n). A <b>balanced</b> tree "
                  "keeps left and right about the same height, so the number of steps stays small.",
             "如果树只往一边长，它就又变成一条链，又回到 O(n)。<b>平衡</b>的意思是左右高度差不多，"
             "步数一直很小。"),
            ("p", "A <b>red-black tree</b> is a balanced tree with a cheap trick: each node is coloured red or black, and a few "
                  "colour rules keep it short. When an insert makes it too deep, it repaints and rotates a little.",
             "<b>红黑树</b>是一种平衡树，用的是很省的技巧：每个节点涂红或涂黑，几条颜色规则保证它不会太高。"
             "插入后如果太深了，就重新涂色、再转一转（旋转）。"),
            ("quote", "short", "Say it like this", "可以这样说",
             [("A red-black tree is a binary tree that colours its nodes red or black and rotates itself after inserts, "
               "so the height stays about 2 × log n.", "红黑树是给节点涂红或黑的二叉树，插入后会自己旋转，保证高度大约是 2 × log n。")]),
        ]),
        ("h2", "04", "Where you meet it", "你会在哪里遇到它", [
            ("ul", [
                ("HashMap: when one bucket holds 8 items, that bucket becomes a red-black tree — lookup stays O(log n).",
                 "HashMap：一个桶里攒够 8 个，就把这个桶变成红黑树，查找仍是 O(log n)。"),
                ("TreeMap in Java is a red-black tree. It keeps keys in order.",
                 "Java 的 TreeMap 就是红黑树，key 是有序的。"),
            ]),
        ]),
    ],
    "words": [
        ("tree", "/triː/", "Nodes with children below them.", "树：下面挂着孩子的节点"),
        ("root", "/ruːt/", "The top node.", "根：最上面那个节点"),
        ("leaf", "/liːf/", "A node with no children.", "叶子：没有孩子的节点"),
        ("balanced", "/ˈbælənst/", "Left and right are about the same height.", "平衡：左右高度差不多"),
        ("rotate", "/ˈroʊteɪt/", "Turn the tree a little to fix the height.", "旋转：转一下把高度调回来"),
    ],
    "checks": [
        ("Why is a balanced tree O(log n)?", "为什么平衡树是 O(log n)？"),
        ("What happens if the tree grows only on one side?", "树只往一边长会怎样？"),
        ("What do the colours in a red-black tree do for us?", "红黑树里的颜色有什么用？"),
    ],
    "next": '<a href="hash.html"><span class="in-en">Next: Lesson 4, hash →</span>'
            '<span class="in-zh">下一课：第 4 课，哈希 →</span></a>',
}

L4 = {
    "path": "basics/hash.html",
    "title": ("What is a key, a hash, a collision", "什么是 key、hash、冲突"),
    "crumb": '<a href="../index.html"><span class="in-en">Home</span><span class="in-zh">首页</span></a> / '
             '<span class="in-en">Lesson 4: Hash</span><span class="in-zh">第 4 课：哈希</span>',
    "kicker": ("Lesson 4 · HashMap", "第 4 课 · HashMap"),
    "h1": ("What is a key? A hash? A collision?", "什么是 key？什么是 hash？什么是冲突？"),
    "lede": ("A key is a name. A hash is a number made from it. A collision is two names with the same number.",
             "key 是名字；hash 是由它算出来的编号；冲突是两个名字算出了同一个编号。"),
    "tags": [("Basics", "基础"), ("HashMap", "HashMap"), ("must know", "必背")],
    "on": "b",
    "blocks": [
        ("h2", "01", "Key: the name", "key：名字", [
            ("p", "A <b>key</b> is what you look things up by. <code>map.put(\"apple\", 5)</code> — here the key is "
                  "<code>\"apple\"</code>, the value is <code>5</code>.",
             "<b>key</b> 是你用来查东西的名字。<code>map.put(\"apple\", 5)</code> 里，key 是 <code>\"apple\"</code>，"
             "value 是 <code>5</code>。"),
            ("p", "In Java, a key must have two methods that agree with each other: <code>hashCode()</code> and "
                  "<code>equals()</code>.",
             "Java 里 key 必须有两个互相配合的方法：<code>hashCode()</code> 和 <code>equals()</code>。"),
        ]),
        ("h2", "02", "Hash: the number", "hash：编号", [
            ("analogy", "Think of it like this", "先这样想",
             "A cloakroom. You give a coat, you get a ticket with a number. The number tells the staff which shelf to use. "
             "The coat is the key, the number is the hash, the shelf is the bucket.",
             "寄存处：你交出外套，拿到一张带编号的票，编号告诉工作人员去哪个架子。"
             "外套＝key，编号＝hash，架子＝桶（bucket）。"),
            ("pre", "hash = key.hashCode()          //  a number, like -1894770\nindex = (n - 1) & hash          //  which bucket: 0 .. n-1"),
            ("p", "The hash is <b>not</b> the memory address and <b>not</b> the value. It is only a number used to pick a bucket.",
             "hash <b>不是</b>内存地址，<b>不是</b> value，只是一个用来选桶的编号。"),
            ("note", "Java 8 also mixes the high bits into the low bits: <code>(h = key.hashCode()) ^ (h &gt;&gt;&gt; 16)</code>. "
                     "If the high bits are all the same, some buckets would be overused.",
             "Java 8 还做了高低位混合 — <code>(h = key.hashCode()) ^ (h &gt;&gt;&gt; 16)</code>。"
             "如果不混合，高位相同的 key 会挤在同一批桶里。"),
        ]),
        ("h2", "03", "Collision: the same number", "冲突：编号撞了", [
            ("p", "There are about four billion possible ints, but a HashMap has only 16 buckets at the start. Two different keys "
                  "can easily get the same bucket. That is a <b>collision</b>.",
             "int 有四十亿种可能，但 HashMap 一开始只有 16 个桶，两个不同的 key 很容易落到同一个桶。这就是<b>冲突</b>。"),
            ("p", "A collision is not a bug. There are only three ways to handle it, and HashMap uses the first two:",
             "冲突不是 bug。处理冲突只有三种办法，HashMap 用了前两种："),
            ("ul", [
                ("<b>Separate chaining</b> — keep a short list in the bucket (what HashMap does for small counts).",
                 "<b>拉链法</b>——桶里挂一条短链（HashMap 数量少时就这么做）"),
                ("<b>Treeify</b> — when one bucket has 8 items, turn that list into a red-black tree (HashMap, Java 8+).",
                 "<b>树化</b>——一个桶攒到 8 个，就把短链变成红黑树（Java 8+ 的 HashMap）"),
                ("<b>Open addressing</b> — move to the next free bucket (ThreadLocalMap, not HashMap).",
                 "<b>开放寻址</b>——往下一个空桶放（ThreadLocalMap 用这种，HashMap 不用）"),
            ]),
        ]),
        ("h2", "04", "Why we must handle it", "为什么必须处理冲突", [
            ("p", "If every key landed in its own bucket, looking up would be one step: O(1). When many keys share one bucket, "
                  "you must walk the list inside it: O(n) in the worst case.",
             "如果每个 key 都落在自己的桶里，查找就是一步 O(1)。当很多 key 挤在一个桶，就得在桶里顺着链走，"
             "最坏是 O(n)。"),
            ("note", "That is the whole reason for the 0.75 load factor and the 8-item treeify rule: keep buckets short.",
             "负载因子 0.75 和“8 个树化”这两条规则，目的都只有一个：让每个桶都很短。"),
        ]),
        ("h2", "05", "equals and hashCode must agree", "equals 和 hashCode 必须一致", [
            ("p", "If two keys are <code>equals()</code>, they <b>must</b> have the same <code>hashCode()</code>. Otherwise the map "
                  "puts the same key into two different buckets, and you will “lose” a value.",
             "如果两个 key <code>equals()</code> 为真，它们的 <code>hashCode()</code> <b>必须</b>相同。"
             "否则同一个 key 会被放进两个不同的桶，你就会“丢”数据。"),
            ("p", "So when you write <code>equals()</code>, always write <code>hashCode()</code> too — use your IDE, it generates both.",
             "所以重写 <code>equals()</code> 时一定同时重写 <code>hashCode()</code>——让 IDE 一次生成两个就行。"),
        ]),
    ],
    "words": [
        ("key", "/kiː/", "The name you look things up by.", "key：用来查东西的名字"),
        ("hash", "/hæʃ/", "A number computed from a key.", "hash：由 key 算出的编号"),
        ("hashCode", "/hæʃ koʊd/", "The Java method that gives that number.", "hashCode：给出这个编号的 Java 方法"),
        ("bucket", "/ˈbʌkɪt/", "One box of the array.", "桶：数组里的一格"),
        ("collision", "/kəˈlɪʒn/", "Two keys with the same bucket.", "冲突：两个 key 落进同一个桶"),
        ("equals", "/ˈiːkwəlz/", "The method that says two keys are the same.", "equals：判断两个 key 是否相同"),
    ],
    "checks": [
        ("What is the difference between a key, a hash and a bucket?", "key、hash、桶，三者有什么区别？"),
        ("Two keys collide — what does HashMap do?", "两个 key 冲突了，HashMap 怎么处理？"),
        ("Why must equals and hashCode agree?", "为什么 equals 和 hashCode 必须一致？"),
    ],
    "next": '<a href="big-o.html"><span class="in-en">Next: Lesson 5, Big O →</span>'
            '<span class="in-zh">下一课：第 5 课，复杂度 →</span></a>',
}


# 主线（首页那条线）：从一个问题长出去
SPINE = [
    dict(n="01", q_en="What is a HashMap, really?",
         q_zh="HashMap 到底是个什么东西？",
         a_en="An array of buckets; each bucket holds a short list.",
         a_zh="一个桶数组，每个桶挂一条短链。",
         href="questions/java-hashmap.html",
         tag_en="Question 1 · live", tag_zh="第 1 题 · 已上线"),
    dict(n="02", q_en="How does a key end up in one bucket?",
         q_zh="一个 key 怎么就跑到某个桶里？",
         a_en="hash it, then <code>h &amp; (n - 1)</code>.",
         a_zh="先算 hash，再 <code>h &amp; (n-1)</code> 取下标。",
         href="basics/hash.html",
         tag_en="Lesson 4", tag_zh="第 4 课"),
    dict(n="03", q_en="Two keys, one bucket. Now what?",
         q_zh="两个 key 撞进同一个桶，怎么办？",
         a_en="Stand in a line — a linked list; after 8, a tree.",
         a_zh="排队——挂成链表；到 8 个就转成红黑树。",
         href="basics/tree.html",
         tag_en="Lessons 2–3", tag_zh="第 2–3 课"),
    dict(n="04", q_en="The buckets are getting full. Then?",
         q_zh="桶快满了呢？",
         a_en="At 75% the array doubles; each key stays or moves +n.",
         a_zh="装到 75% 翻倍；每个 key 要么原位、要么 +n。",
         href="basics/big-o.html",
         tag_en="Lesson 5", tag_zh="第 5 课"),
    dict(n="05", q_en="Two threads put at the same time?",
         q_zh="两个线程同时 put 会怎样？",
         a_en="Lost data, or a loop in JDK 7. Use ConcurrentHashMap.",
         a_zh="丢数据，JDK 7 还会成环。换 ConcurrentHashMap。",
         href="basics/threads.html",
         tag_en="Lesson 7", tag_zh="第 7 课"),
    dict(n="06", q_en="So how is it used as a cache at work?",
         q_zh="那工作中怎么拿它当缓存用？",
         a_en="Redis in front of the DB — and three ways the cache bites back.",
         a_zh="Redis 挡在数据库前面——以及缓存咬你的三种方式。",
         href="", href_en="", href_zh="",
         tag_en="Not written yet", tag_zh="待写"),
    dict(n="07", q_en="WeChat sends the same callback three times. Then?",
         q_zh="微信同时回调三条，怎么办？",
         a_en="Idempotent table, then status CAS, then a lock.",
         a_zh="幂等表 → 状态 CAS → 再上锁。",
         href="questions/pay-callback.html",
         tag_en="Question 2 · live", tag_zh="第 2 题 · 已上线"),
    dict(n="08", q_en="Ten thousand people, one thousand items. No oversell?",
         q_zh="一万人抢一千件，怎么不超卖？",
         a_en="Pre-deduct in Redis, then let the DB be the last check.",
         a_zh="先在 Redis 预扣，数据库做最后一道闸。",
         href="", href_en="", href_zh="",
         tag_en="Not written yet", tag_zh="待写"),
]
