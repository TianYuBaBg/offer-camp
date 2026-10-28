# -*- coding: utf-8 -*-
"""一次性生成英文站页面。写完即删。"""
import io, os, urllib.parse

ROOT = "."

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · Java Notes</title>
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="__CSS__">
</head>
<body>
<div class="grain" aria-hidden="true"></div>

<header class="masthead">
  <div class="mh-left">
    <span class="mh-mark">Java Notes</span>
    <span class="mh-en">OFFER&nbsp;CAMP</span>
    <nav class="mh-nav">
      <a href="__HOME__"__QON__>Questions</a>
      <a href="__BASICS__"__BON__>Basics</a>
      <a href="__GLOSS__"__WON__>Words</a>
    </nav>
  </div>
  <div class="mh-right"><span>__RIGHT__</span></div>
</header>

<main>
  <p class="crumb"><a href="__HOME__">Home</a> / __CRUMB__</p>

  <div class="qhead">
    <p class="kicker">__KICKER__</p>
    <h1>__H1__</h1>
    <p class="lede">__LEDE__</p>
    __TAGS__
    <button class="listen" data-listen>🔊 Listen to this page</button>
  </div>

__BODY__

  <section class="sec">
    <h2><span class="num">→</span>New words</h2>
    <div class="wordlist">
__WORDS__
    </div>
    <p class="note">Click <b>hear it</b> to listen to real people say the word on YouGlish. Click <b>🔊</b> to hear the computer say it.</p>
  </section>

  <section class="sec">
    <h2><span class="num">✓</span>Check yourself</h2>
    <ol class="checks">
__CHECKS__
    </ol>
  </section>

  <p class="log-tip">__NEXT__</p>
</main>

<footer>
  <div class="f-left"><span>Written for learning English · Wang Tianyu</span></div>
  <div class="f-right"><a href="__HOME__">Home</a><span class="sep">·</span><a href="https://github.com/TianYuBaBg/offer-camp">GitHub</a></div>
</footer>
<script src="__JS__"></script>
</body>
</html>
"""


def word(term, ipa, mean):
    q = urllib.parse.quote(term)
    return (
        '      <div class="word">\n'
        '        <span class="w">%s</span>\n'
        '        <span class="ipa">%s</span>\n'
        '        <span class="mean">%s</span>\n'
        '        <span class="links">'
        '<a class="say" href="https://youglish.com/pronounce/%s/english" target="_blank" rel="noopener">▶ hear it</a>'
        '<button class="spk" data-say="%s" aria-label="say %s">🔊</button>'
        '</span>\n'
        '      </div>' % (term, ipa, mean, q, term, term)
    )


def page(path, title, desc, h1, kicker, lede, tags, crumb, right, body, words, checks, nxt,
         on=None):
    depth = path.count("/")
    up = "../" * depth
    html = TEMPLATE
    subs = {
        "__TITLE__": title, "__DESC__": desc, "__CSS__": up + "assets/style.css",
        "__JS__": up + "assets/app.js",
        "__HOME__": up + "index.html",
        "__BASICS__": up + "basics/array.html",
        "__GLOSS__": up + "glossary.html",
        "__QON__": ' class="on"' if on == "q" else "",
        "__BON__": ' class="on"' if on == "b" else "",
        "__WON__": ' class="on"' if on == "w" else "",
        "__RIGHT__": right, "__CRUMB__": crumb, "__KICKER__": kicker,
        "__H1__": h1, "__LEDE__": lede, "__TAGS__": tags, "__BODY__": body,
        "__WORDS__": "\n".join(word(*w) for w in words),
        "__CHECKS__": "\n".join("      <li>%s</li>" % c for c in checks),
        "__NEXT__": nxt,
    }
    for k, v in subs.items():
        html = html.replace(k, v)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    io.open(full, "w", encoding="utf-8").write(html)
    print("wrote", path)


def tag(t, cls=""):
    c = ' class="tag %s"' % cls if cls else ' class="tag"'
    return '<span%s>%s</span>' % (c, t)


def tags(*items):
    return '<div class="qmeta">%s</div>' % "".join(tag(t, c) for t, c in items)


# ---------------------------------------------------------------- index
index_cards = """
  <section class="block">
    <h2><span class="num">01</span>Basics — start here<span class="hint">7 short lessons</span></h2>
    <ul class="qlist">
      <li><a href="basics/array.html">
        <span class="no">01</span>
        <span class="t">What is an array?<small>A row of numbered boxes. Fast to read, slow to insert.</small></span>
        <span class="m">5 min</span></a></li>
      <li><a href="basics/linked-list.html">
        <span class="no">02</span>
        <span class="t">What is a linked list?<small>Notes with arrows. Fast to insert, slow to find.</small></span>
        <span class="m">5 min</span></a></li>
      <li><a href="basics/tree.html">
        <span class="no">03</span>
        <span class="t">What is a tree? And a red-black tree?<small>An upside-down family tree that stays short.</small></span>
        <span class="m">6 min</span></a></li>
      <li><a href="basics/hash.html">
        <span class="no">04</span>
        <span class="t">What is a key? A hash? A collision?<small>The fingerprint idea, in plain words.</small></span>
        <span class="m">6 min</span></a></li>
      <li><a href="basics/big-o.html">
        <span class="no">05</span>
        <span class="t">What is O(1), O(n), O(log n)?<small>How the work grows when the data grows.</small></span>
        <span class="m">6 min</span></a></li>
      <li><a href="basics/hashmap-methods.html">
        <span class="no">06</span>
        <span class="t">HashMap methods in real life<small>put, get, merge, computeIfAbsent — with examples.</small></span>
        <span class="m">7 min</span></a></li>
      <li><a href="basics/threads.html">
        <span class="no">07</span>
        <span class="t">Why is HashMap not thread-safe?<small>Two workers writing the same notebook.</small></span>
        <span class="m">6 min</span></a></li>
    </ul>
  </section>

  <section class="block">
    <h2><span class="num">02</span>Interview questions<span class="hint">one page each</span></h2>
    <ul class="qlist">
      <li><a href="questions/java-hashmap.html">
        <span class="no">Q1</span>
        <span class="t">How does HashMap work?<small>Buckets, hash, resize, tree, thread safety.</small></span>
        <span class="m">12 min</span></a></li>
    </ul>
  </section>

  <section class="block">
    <h2><span class="num">03</span>How to use these pages<span class="hint">3 steps, 10 minutes</span></h2>
    <div class="cards">
      <div class="card"><span class="c-no">1</span><span class="c-title">Read it out loud</span>
        <span class="c-desc">Press Listen. Follow with your eyes and read along. Your mouth learns faster than your eyes.</span>
        <span class="c-meta">3 min</span></div>
      <div class="card"><span class="c-no">2</span><span class="c-title">Say the new words</span>
        <span class="c-desc">Five words per page. Click “hear it” on YouGlish, then say each word three times.</span>
        <span class="c-meta">4 min</span></div>
      <div class="card"><span class="c-no">3</span><span class="c-title">Answer the checks</span>
        <span class="c-desc">Say the answer out loud before you look at the hint. If you cannot say it, read the page again.</span>
        <span class="c-meta">3 min</span></div>
    </div>
  </section>
"""

index_html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Java Notes · learn Java in English</title>
<meta name="description" content="Short English pages about Java: arrays, linked lists, trees, hash, Big O, HashMap.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="grain" aria-hidden="true"></div>

<header class="masthead">
  <div class="mh-left">
    <span class="mh-mark">Java Notes</span>
    <span class="mh-en">OFFER&nbsp;CAMP</span>
    <nav class="mh-nav">
      <a href="index.html" class="on">Questions</a>
      <a href="basics/array.html">Basics</a>
      <a href="glossary.html">Words</a>
    </nav>
  </div>
  <div class="mh-right"><span>7 basics · 1 question</span></div>
</header>

<main>
  <section class="hero">
    <p class="kicker">Java in English · for a complete beginner</p>
    <h1>One small page,<br>one <em>idea</em>.</h1>
    <p class="lede">I know nothing about Java. I want to learn it in English, not in Chinese. So every page gives one idea, five new words, and three questions. Short sentences. No idioms. Read out loud.</p>
  </section>
__CARDS__
</main>

<footer>
  <div class="f-left"><span>Written for learning English · Wang Tianyu · Beijing</span></div>
  <div class="f-right"><a href="https://github.com/TianYuBaBg/offer-camp">GitHub</a><span class="sep">·</span><span>no framework, no tracking</span></div>
</footer>
</body>
</html>
""".replace("__CARDS__", index_cards)

io.open("index.html", "w", encoding="utf-8").write(index_html)
print("wrote index.html")

# ---------------------------------------------------------------- lessons
def lesson(path, title, desc, kicker, h1, lede, right, crumb, body, words, checks, nxt, tagline):
    page(path, title, desc, h1, kicker, lede, tags(("Basics", ""), (tagline, "")),
         crumb, right, body, words, checks, nxt, on="b")

# --- 1 array
body = """
  <section class="sec">
    <h2><span class="num">01</span>The idea</h2>
    <div class="analogy"><b>Think of it like this</b>Ten lockers in a row. They touch each other. Each locker has a number: 0, 1, 2 … 9. If you know the number, you walk straight to that locker. You do not open the other nine first.</div>
    <p>An <b>array</b> is that row of boxes. It has two facts:</p>
    <ul>
      <li>The boxes are <b>next to each other</b> in memory.</li>
      <li>Each box has a <b>number</b>, called an <b>index</b>. The first index is <b>0</b>, not 1.</li>
    </ul>

    <table class="ledger">
      <thead><tr><th>index</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead>
      <tbody><tr><td>value</td><td>apple</td><td>banana</td><td>cherry</td><td>date</td><td>fig</td></tr></tbody>
    </table>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Why reading is fast</h2>
    <p>Because the boxes touch each other, the computer can <b>compute</b> the address:</p>
    <pre><code>address = start + index × size_of_one_box</code></pre>
    <p>So reading box 500 costs the same as reading box 0. One step. In Big O words, this is <b>O(1)</b> — constant time.</p>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>Why inserting is slow</h2>
    <p>The boxes are full and touching. If you insert an item in the middle, every item after it must <b>move one step</b> to the right. With one thousand items, that is one thousand moves. This is <b>O(n)</b> — linear time.</p>
    <div class="analogy"><b>Remember</b>An array is like a bookshelf where every book must stand next to the next one. Adding a book in the middle means pushing all the books after it.</div>
  </section>

  <section class="sec">
    <h2><span class="num">04</span>In Java</h2>
    <pre><code>int[] scores = new int[10];   // 10 boxes, all 0
scores[0] = 90;               // put 90 in box 0
int first = scores[0];        // read box 0

String[] names = {"Ann", "Bob", "Cid"};   // 3 boxes, already filled</code></pre>
    <p>You already met arrays today, even if you did not know it: <b>ArrayList</b> uses an array inside, and <b>HashMap</b> uses an <b>array of buckets</b>. The array is the most common box in Java.</p>
  </section>
"""
lesson("basics/array.html", "What is an array", "Array: a row of numbered boxes. Fast to read, slow to insert.",
       "Lesson 1 · Data structure", "What is an array?",
       "A row of boxes with numbers. If you know the number, you jump straight to the box.",
       "Lesson 1", "Lesson 1: Array", body,
       [("array", "/əˈreɪ/", "A row of boxes that sit next to each other."),
        ("index", "/ˈɪndeks/", "The number of a box. The first number is 0."),
        ("element", "/ˈelɪmənt/", "One item inside the array."),
        ("memory", "/ˈmeməri/", "The place in the computer where data lives."),
        ("contiguous", "/kənˈtɪɡjuəs/", "Touching, next to each other, with no gap."),
        ("constant time", "/ˈkɑːnstənt taɪm/", "The work does not change when the data grows.")],
       ["In an array of 10 boxes, what is the last index?<small>9. Indexes start at 0, so 0 to 9.</small>",
        "Why can the computer jump to box 7 so fast?<small>Because the boxes touch: address = start + 7 × size.</small>",
        "Why is inserting in the middle slow?<small>All items after the hole must move one step. That is O(n).</small>"],
       "Next: <a href=\"linked-list.html\">What is a linked list?</a>", "data structure")

# --- 2 linked list
body = """
  <section class="sec">
    <h2><span class="num">01</span>The idea</h2>
    <div class="analogy"><b>Think of it like this</b>A treasure hunt. Each note says one thing: the next place. You cannot jump to the end. You follow the arrows, one note at a time.</div>
    <p>A <b>linked list</b> is made of small boxes called <b>nodes</b>. Each node has two parts:</p>
    <ul>
      <li>a <b>value</b> (the thing you want to keep),</li>
      <li>a <b>pointer</b> to the <b>next</b> node.</li>
    </ul>
    <p>The first node is called the <b>head</b>. The last node points to <b>null</b> — nothing. That means “this is the end”.</p>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Difference from an array</h2>
    <table class="ledger">
      <thead><tr><th></th><th>Array</th><th>Linked list</th></tr></thead>
      <tbody>
        <tr><td>Where it lives</td><td>boxes next to each other</td><td>boxes anywhere in memory</td></tr>
        <tr><td>Read item 500</td><td>jump straight there — O(1)</td><td>walk 500 steps — O(n)</td></tr>
        <tr><td>Insert in the middle</td><td>move everything after — O(n)</td><td>change two arrows — O(1)</td></tr>
        <tr><td>Extra cost</td><td>none</td><td>each node stores one extra pointer</td></tr>
      </tbody>
    </table>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>In Java</h2>
    <pre><code>LinkedList&lt;String&gt; list = new LinkedList&lt;&gt;();
list.add("Ann");
list.add("Bob");
list.get(1);        // "Bob" — but it walks from the head</code></pre>
    <p>You will meet this shape again in HashMap: when two keys land in the same bucket, they form a <b>linked list</b> — each <code>Node</code> has a <code>next</code> pointer. That is exactly the treasure hunt.</p>
  </section>
"""
lesson("basics/linked-list.html", "What is a linked list", "Linked list: nodes with arrows. Fast to insert, slow to find.",
       "Lesson 2 · Data structure", "What is a linked list?",
       "Notes with arrows. You cannot jump; you follow the next pointer.",
       "Lesson 2", "Lesson 2: Linked list", body,
       [("linked list", "/lɪŋkt lɪst/", "Boxes connected by arrows, one after another."),
        ("node", "/noʊd/", "One small box: a value plus a pointer."),
        ("pointer", "/ˈpɔɪntər/", "A value that says where the next box is."),
        ("head", "/hed/", "The first node of the list."),
        ("traverse", "/trəˈvɜːrs/", "Walk through all the nodes, one by one."),
        ("null", "/nʌl/", "Nothing. It marks the end of the list.")],
       ["What two things does a node keep?<small>A value and a pointer to the next node.</small>",
        "Why is finding item 500 slow?<small>You must walk from the head, one node at a time. That is O(n).</small>",
        "Why is inserting fast if you already stand at that place?<small>You only change two pointers. No boxes move.</small>"],
       "Next: <a href=\"tree.html\">What is a tree?</a>", "data structure")

# --- 3 tree
body = """
  <section class="sec">
    <h2><span class="num">01</span>The idea</h2>
    <div class="analogy"><b>Think of it like this</b>A family tree, upside down. One person at the top (the root). Their children below. Each child has children below. To find a person, you go down level by level.</div>
    <p>A <b>tree</b> is made of nodes, like a linked list, but each node can point to <b>two</b> children: a left child and a right child. A tree like that is called a <b>binary tree</b>.</p>
    <ul>
      <li><b>root</b> — the top node.</li>
      <li><b>leaf</b> — a node with no children.</li>
      <li><b>height</b> — how many levels the tree has.</li>
    </ul>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Why height matters</h2>
    <p>If the tree is <b>balanced</b> (left and right are about the same size), the height grows like <b>log n</b>. With 1,000,000 nodes the height is about 20. So finding a value takes about 20 steps, not 1,000,000.</p>
    <p>If the tree is <b>not</b> balanced, it becomes a line — and then it is just a slow linked list again.</p>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>What is a red-black tree</h2>
    <p>A <b>red-black tree</b> is a tree that <b>fixes itself</b> after every insert and delete. It paints each node red or black and rotates the branches, so the height can never grow too much. The rule of thumb: the height stays around 2 × log(n). That is why lookup is <b>O(log n)</b> and never falls back to O(n).</p>
    <div class="analogy"><b>Remember</b>Linked list = a line. Tree = a short, wide shape. Red-black tree = a tree that keeps itself short.</div>
  </section>

  <section class="sec">
    <h2><span class="num">04</span>Where HashMap uses it</h2>
    <p>Inside HashMap, one bucket is usually empty or holds a short linked list. But if one bucket collects <b>8 items or more</b> (and the table has at least 64 buckets), that bucket is turned into a <b>red-black tree</b>. So a very bad bucket goes from O(n) back to O(log n).</p>
    <p>That is the whole reason the tree appears in the HashMap story: <b>a safety net for bad luck</b>.</p>
  </section>
"""
lesson("basics/tree.html", "What is a tree", "Tree and red-black tree in plain English, and why HashMap uses one.",
       "Lesson 3 · Data structure", "What is a tree? And a red-black tree?",
       "An upside-down family tree. A red-black tree is one that keeps itself short.",
       "Lesson 3", "Lesson 3: Tree", body,
       [("tree", "/triː/", "Nodes with children below them."),
        ("root", "/ruːt/", "The top node of the tree."),
        ("leaf", "/liːf/", "A node with no children."),
        ("height", "/haɪt/", "How many levels the tree has."),
        ("balanced", "/ˈbælənst/", "Left and right sides are about the same size."),
        ("red-black tree", "/red blæk triː/", "A tree that repaints and rotates itself to stay short.")],
       ["What does balanced mean?<small>The left and right sides have about the same number of nodes, so the tree stays short.</small>",
        "Why is a balanced tree fast?<small>Its height is about log n, so you take about log n steps to find something.</small>",
        "When does HashMap turn a bucket into a tree?<small>When one bucket has 8 or more items and the table has at least 64 buckets.</small>"],
       "Next: <a href=\"hash.html\">What is a key, a hash, a collision?</a>", "data structure")

# --- 4 hash
body = """
  <section class="sec">
    <h2><span class="num">01</span>Three words: key, hash, bucket</h2>
    <div class="analogy"><b>Think of it like this</b>Your name is the <b>key</b>. The school gives you a <b>student number</b> computed from your name — that is the <b>hash</b>. The classroom with that number is the <b>bucket</b>.</div>
    <ul>
      <li><b>key</b> — the thing you look up by. For example <code>"apple"</code>.</li>
      <li><b>hash</b> — a number computed from the key. Same key, same number, every time.</li>
      <li><b>hash function</b> — the machine that turns a key into a number.</li>
      <li><b>bucket</b> — one box in the array, chosen by the hash.</li>
    </ul>
    <p>In HashMap the bucket number is computed like this:</p>
    <pre><code>index = (n - 1) &amp; hash</code></pre>
    <p><code>n</code> is the number of buckets (16 by default). The result is always between 0 and n-1, so it always points at a real box.</p>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>What is a collision</h2>
    <p>Two different keys can produce the <b>same</b> bucket number. That is a <b>collision</b>.</p>
    <pre><code>key "apple"  → hash 97  → index 1
key "grape"  → hash 97  → index 1   ← same box: collision</code></pre>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>Why we must deal with collisions</h2>
    <p>Because a bucket holds items in a <b>line</b> (a linked list). If ten keys land in one bucket, finding one of them takes up to ten steps — <b>O(n)</b> instead of O(1). One bad bucket can make the whole map slow.</p>
    <p>So HashMap does three things:</p>
    <ol class="steps">
      <li><b>Spreads the keys</b> with a good hash function, so collisions are rare.</li>
      <li><b>Keeps a short line</b> in the bucket, and grows the array (resize) when it gets crowded.</li>
      <li><b>Grows a tree</b> when one bucket gets 8 items — the worst case becomes O(log n).</li>
    </ol>
    <div class="analogy"><b>Remember</b>A collision is not an error. It is normal. HashMap does not prevent it; it keeps it small.</div>
  </section>
"""
lesson("basics/hash.html", "What is a key, hash and collision", "Key, hash, bucket, collision — in plain English.",
       "Lesson 4 · Hash", "What is a key? A hash? A collision?",
       "A key is the name you search by. A hash is a number computed from it. A collision is two keys with the same number.",
       "Lesson 4", "Lesson 4: Key and hash", body,
       [("key", "/kiː/", "The name you look things up by, like \"apple\"."),
        ("hash", "/hæʃ/", "A number computed from a key. Like a fingerprint."),
        ("hash function", "/hæʃ ˈfʌŋkʃn/", "The machine that turns a key into a number."),
        ("collision", "/kəˈlɪʒn/", "Two different keys that get the same bucket."),
        ("bucket", "/ˈbʌkɪt/", "One box in the array that holds items with the same hash.")],
       ["Is the hash the same thing as the key?<small>No. The key is the name; the hash is a number computed from that name.</small>",
        "What is a collision?<small>Two different keys land in the same bucket.</small>",
        "Does a collision break HashMap?<small>No. It only makes that bucket slower. HashMap keeps the line short and turns long lines into a tree.</small>"],
       "Next: <a href=\"big-o.html\">What is O(1), O(n), O(log n)?</a>", "hash")

# --- 5 big o
body = """
  <section class="sec">
    <h2><span class="num">01</span>The idea</h2>
    <div class="analogy"><b>Think of it like this</b>Guess a number from 1 to 100. Each guess halves the range. 50? lower. 25? higher. You find it in about 7 guesses. That is what log n feels like.</div>
    <p><b>Big O</b> answers one question: <b>when the data grows, how much more work do I do?</b> It ignores small details and keeps only the shape of the growth.</p>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Four shapes</h2>
    <table class="ledger">
      <thead><tr><th>Big O</th><th>Name</th><th>Work when n = 1,000,000</th><th>Example</th></tr></thead>
      <tbody>
        <tr><td>O(1)</td><td>constant</td><td>1 step</td><td>read array[500]</td></tr>
        <tr><td>O(log n)</td><td>logarithmic</td><td>about 20 steps</td><td>binary search, balanced tree</td></tr>
        <tr><td>O(n)</td><td>linear</td><td>1,000,000 steps</td><td>walk a linked list</td></tr>
        <tr><td>O(n²)</td><td>quadratic</td><td>1,000,000,000,000 steps</td><td>two nested loops</td></tr>
      </tbody>
    </table>
    <p>HashMap is O(1) on average because it computes the bucket directly — no walking. When a bucket is a line, the worst case is O(n); after the tree, it is O(log n).</p>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>How to read the notation</h2>
    <ul>
      <li><b>n</b> — how many items you have.</li>
      <li><b>O(1)</b> — the time does not change with n.</li>
      <li><b>O(n)</b> — twice the items, twice the time.</li>
      <li><b>O(log n)</b> — double the items, add one step.</li>
    </ul>
    <div class="analogy"><b>Remember</b>Big O is not about seconds on your laptop. It is about the <b>shape</b> of the cost when the data grows.</div>
  </section>
"""
lesson("basics/big-o.html", "What is O(1), O(n), O(log n)", "Big O in plain English with a table of the four common shapes.",
       "Lesson 5 · Complexity", "What is O(1), O(n), O(log n)?",
       "Big O tells you how the work grows when the data grows. That is all it is.",
       "Lesson 5", "Lesson 5: Big O", body,
       [("time complexity", "/taɪm kəmˈpleksəti/", "How the running time grows with the data size."),
        ("constant", "/ˈkɑːnstənt/", "Does not change: O(1)."),
        ("linear", "/ˈlɪniər/", "Grows in a straight line: O(n)."),
        ("logarithmic", "/ˌlɔːɡəˈrɪðmɪk/", "Grows very slowly: O(log n)."),
        ("quadratic", "/kwɑːˈdrætɪk/", "Grows like n × n: O(n²)."),
        ("growth", "/ɡroʊθ/", "How fast the cost goes up.")],
       ["If n doubles, what happens to O(n)?<small>The work doubles too.</small>",
        "If n doubles, what happens to O(log n)?<small>It adds about one step. Doubling 1,000,000 to 2,000,000 adds one step to the 20.</small>",
        "Why is HashMap usually O(1)?<small>Because it computes the bucket number directly, without walking through items.</small>"],
       "Next: <a href=\"hashmap-methods.html\">HashMap methods in real life</a>", "complexity")

# --- 6 methods
body = """
  <section class="sec">
    <h2><span class="num">01</span>The six methods you will use every day</h2>
    <table class="ledger">
      <thead><tr><th>Method</th><th>What it does</th></tr></thead>
      <tbody>
        <tr><td><code>put(k, v)</code></td><td>Add or replace a value. Returns the old value, or null.</td></tr>
        <tr><td><code>get(k)</code></td><td>Read the value. Returns null if the key is missing.</td></tr>
        <tr><td><code>getOrDefault(k, d)</code></td><td>Read, or give a default when the key is missing.</td></tr>
        <tr><td><code>containsKey(k)</code></td><td>True if the key exists. Use it when null is a real value.</td></tr>
        <tr><td><code>remove(k)</code></td><td>Delete the key and return its value.</td></tr>
        <tr><td><code>size()</code></td><td>How many pairs are inside.</td></tr>
      </tbody>
    </table>
    <pre><code>Map&lt;String, Integer&gt; price = new HashMap&lt;&gt;();
price.put("apple", 5);
price.put("apple", 6);              // replaces 5, returns 5
int p = price.get("apple");         // 6
int q = price.getOrDefault("pear", 0);   // 0, no exception
boolean has = price.containsKey("pear"); // false</code></pre>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Three real patterns</h2>

    <h3>1. Count things</h3>
    <pre><code>Map&lt;String, Integer&gt; count = new HashMap&lt;&gt;();
for (String word : words) {
    count.merge(word, 1, Integer::sum);   // add 1, or create with 1
}</code></pre>
    <p><code>merge</code> is the shortest way to count. Old style was <code>get</code>, plus one, then <code>put</code>.</p>

    <h3>2. Group things</h3>
    <pre><code>Map&lt;Character, List&lt;String&gt;&gt; byLetter = new HashMap&lt;&gt;();
for (String name : names) {
    byLetter.computeIfAbsent(name.charAt(0), k -&gt; new ArrayList&lt;&gt;()).add(name);
}</code></pre>
    <p><code>computeIfAbsent</code> creates the list only when needed. Without it you would write an <code>if (list == null)</code> every time.</p>

    <h3>3. A small cache</h3>
    <pre><code>Map&lt;Long, User&gt; cache = new HashMap&lt;&gt;();
User u = cache.computeIfAbsent(id, this::loadFromDb);</code></pre>
    <p>Read from the map; if the key is missing, load it and remember it. Note: this is not thread-safe, so use <code>ConcurrentHashMap</code> in a web application.</p>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>Two traps</h2>
    <ul>
      <li><b>get returns null</b> when the key is missing. If a real value can also be null, use <code>containsKey</code> to tell the two apart.</li>
      <li><b>Mutable keys are dangerous.</b> If you change a key object after <code>put</code>, its hash changes and <code>get</code> cannot find it any more. Use immutable keys like String or Long.</li>
    </ul>
  </section>
"""
lesson("basics/hashmap-methods.html", "HashMap methods in real life", "put, get, getOrDefault, merge, computeIfAbsent with three real examples.",
       "Lesson 6 · Practice", "HashMap methods, and how to use them",
       "Six methods you use every day, and three patterns that solve most problems.",
       "Lesson 6", "Lesson 6: Methods", body,
       [("method", "/ˈmeθəd/", "A function that belongs to a class."),
        ("parameter", "/pəˈræmɪtər/", "The value you pass into a method."),
        ("return", "/rɪˈtɜːrn/", "The value a method gives back."),
        ("entry", "/ˈentri/", "One key-value pair inside the map."),
        ("frequency", "/ˈfriːkwənsi/", "How many times something appears."),
        ("cache", "/kæʃ/", "A small store of things you already computed.")],
       ["Which method reads a value with a default?<small>getOrDefault(key, defaultValue).</small>",
        "Why is merge good for counting?<small>It adds one in a single call, with no null check.</small>",
        "What happens if you change a key after put?<small>Its hash changes, so get cannot find it any more. Use immutable keys.</small>"],
       "Next: <a href=\"threads.html\">Why is HashMap not thread-safe?</a>", "practice")

# --- 7 threads
body = """
  <section class="sec">
    <h2><span class="num">01</span>The idea</h2>
    <div class="analogy"><b>Think of it like this</b>Two people writing on the same line of a notebook at the same time. Person A writes “5”, person B writes “7”. The last hand wins, and nobody knows what the first hand wrote.</div>
    <p>A <b>thread</b> is one worker inside your program. Two threads can run at the same time. A <b>race condition</b> happens when two workers use the same data and the result depends on who is faster.</p>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>Why HashMap is not safe</h2>
    <p>Look at what <code>put</code> really does. It is not one step:</p>
    <ol class="steps">
      <li>compute the hash,</li>
      <li>find the bucket,</li>
      <li>insert the node at the end of the line,</li>
      <li>increase <code>size</code>, and maybe resize the array.</li>
    </ol>
    <p>Between any two steps, the other thread can change things. Real results:</p>
    <ul>
      <li><b>Lost update</b> — both threads write a new value, one is silently gone.</li>
      <li><b>Wrong size</b> — both increase <code>size</code> from the same old value.</li>
      <li><b>Broken line</b> — two threads insert at the same place, a pointer is overwritten, items disappear.</li>
      <li><b>Infinite loop (JDK 7)</b> — two threads resize at the same time and the links form a circle; then <code>get</code> spins forever and the CPU is at 100%.</li>
    </ul>
    <p>JDK 8 changed the resize to keep the order, so the circle is gone. The data loss is <b>not</b> gone: JDK 8 is still not thread-safe.</p>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>What to use instead</h2>
    <table class="ledger">
      <thead><tr><th>Option</th><th>When</th></tr></thead>
      <tbody>
        <tr><td><code>ConcurrentHashMap</code></td><td>Many threads read and write. Locks only the bucket head, so it is fast.</td></tr>
        <tr><td><code>Collections.synchronizedMap</code></td><td>One big lock. Simple, but slow when many threads write.</td></tr>
        <tr><td>Plain <code>HashMap</code></td><td>One thread only, or read-only after it is built.</td></tr>
      </tbody>
    </table>
    <div class="analogy"><b>Remember</b>HashMap is a fast bicycle. ConcurrentHashMap is a bicycle with training wheels and a lock. Use the second one when two people ride.</div>
  </section>
"""
lesson("basics/threads.html", "Why HashMap is not thread-safe", "Threads, race conditions, and why HashMap breaks under concurrent writes.",
       "Lesson 7 · Concurrency", "Why is HashMap not thread-safe?",
       "Because put is many steps, and two threads can step on each other between them.",
       "Lesson 7", "Lesson 7: Threads", body,
       [("thread", "/θred/", "One worker running inside your program."),
        ("concurrent", "/kənˈkɜːrənt/", "Happening at the same time."),
        ("race condition", "/reɪs kənˈdɪʃn/", "A bug where the result depends on who runs first."),
        ("lock", "/lɑːk/", "A way to let only one worker touch something."),
        ("synchronized", "/ˈsɪŋkrənaɪzd/", "Java's keyword for “only one thread at a time here”."),
        ("thread-safe", "/θred seɪf/", "Safe to use from many threads at the same time.")],
       ["What is a race condition?<small>Two threads use the same data, and the result depends on the order they run in.</small>",
        "Name one thing that breaks when two threads put at once.<small>Lost update, wrong size, broken line, or (in JDK 7) an infinite loop.</small>",
        "What should you use in a web application instead of HashMap?<small>ConcurrentHashMap. It locks only the bucket head, so it stays fast.</small>"],
       "Back to: <a href=\"../questions/java-hashmap.html\">Question 1: How does HashMap work?</a>", "concurrency")

print("lessons done")
