# -*- coding: utf-8 -*-
"""生成 question / glossary / about 三页。写完即删。"""
import io, os, urllib.parse

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
    __LISTEN__
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


def tag(t, cls=""):
    c = ' class="tag %s"' % cls if cls else ' class="tag"'
    return '<span%s>%s</span>' % (c, t)


def render(path, title, desc, h1, kicker, lede, tags, crumb, right, body,
           words, checks, nxt, on="", listen=True):
    depth = path.count("/")
    up = "../" * depth
    html = TEMPLATE
    subs = {
        "__TITLE__": title, "__DESC__": desc, "__CSS__": up + "assets/style.css",
        "__JS__": up + "assets/app.js", "__HOME__": up + "index.html",
        "__BASICS__": up + "basics/array.html", "__GLOSS__": up + "glossary.html",
        "__QON__": ' class="on"' if on == "q" else "",
        "__BON__": ' class="on"' if on == "b" else "",
        "__WON__": ' class="on"' if on == "w" else "",
        "__RIGHT__": right, "__CRUMB__": crumb, "__KICKER__": kicker, "__H1__": h1,
        "__LEDE__": lede, "__TAGS__": tags,
        "__LISTEN__": '<button class="listen" data-listen>🔊 Listen to this page</button>' if listen else "",
        "__BODY__": body,
        "__WORDS__": "\n".join(word(*w) for w in words),
        "__CHECKS__": "\n".join("      <li>%s</li>" % c for c in checks),
        "__NEXT__": nxt,
    }
    for k, v in subs.items():
        html = html.replace(k, v)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(html)
    print("wrote", path)


# ======================================================== question 1
q_body = """
  <section class="sec">
    <h2><span class="num">01</span>One sentence</h2>
    <blockquote class="short">
      <span class="lbl">Say this first</span>
      A HashMap is a box of small boxes. You give it a <b>key</b> (a name), and it gives you back a <b>value</b> (a thing) very fast. Inside, it uses an <b>array</b>. Each box in the array is called a <b>bucket</b>. When two keys fall into the same bucket, they stand in a line.
    </blockquote>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>What is inside</h2>
    <p>On the outside it looks like a table of names and values:</p>
    <table class="ledger">
      <thead><tr><th>key</th><th>value</th></tr></thead>
      <tbody>
        <tr><td>"apple"</td><td>5</td></tr>
        <tr><td>"pear"</td><td>3</td></tr>
      </tbody>
    </table>
    <p>On the inside it is an <b>array of buckets</b>. A bucket can be in one of three states:</p>

    <figure class="figure">
      <div class="arr">
        <div class="cell">0</div><div class="cell">1</div><div class="cell">2</div><div class="cell on">3</div>
        <div class="cell">4</div><div class="cell">5</div><div class="cell">6</div><div class="cell">7</div>
        <div class="cell">8</div><div class="cell on">9</div><div class="cell">10</div><div class="cell">11</div>
        <div class="cell on">12</div><div class="cell">13</div><div class="cell">14</div><div class="cell">15</div>
      </div>
      <div class="chainrow">
        <div class="chain"><span class="node">bucket 3: Node</span><span class="nil">→ null</span></div>
        <div class="chain"><span class="node">bucket 9: Node</span><span class="arrow">→</span><span class="node">Node</span><span class="arrow">→</span><span class="node">Node</span><span class="nil">→ null</span></div>
        <div class="chain"><span class="node tree">bucket 12: red-black tree</span></div>
      </div>
      <figcaption>An array of 16 buckets. Bucket 9 holds a short line. Bucket 12 has become a tree.</figcaption>
    </figure>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>How put works</h2>
    <p>When you call <code>map.put("apple", 5)</code>, six things happen:</p>
    <ol class="steps">
      <li><b>Make the table</b> — the first put creates the array with 16 buckets. (Before that, it is empty.)</li>
      <li><b>Compute the hash</b> — a number from the key: <code>(h = key.hashCode()) ^ (h &gt;&gt;&gt; 16)</code>. The second half mixes the high bits into the low bits, so the number spreads better.</li>
      <li><b>Find the bucket</b> — <code>index = (n - 1) &amp; hash</code>. Because n is a power of two, this is the same as <code>hash % n</code>, but faster.</li>
      <li><b>Empty bucket?</b> — put a new node there. Done.</li>
      <li><b>Not empty?</b> — compare the key: same key → replace the value; different key → go to the end of the line and add a new node. If the line reaches 8 items, the bucket may become a tree.</li>
      <li><b>Too full?</b> — if <code>size &gt; capacity × 0.75</code>, double the array and move the items.</li>
    </ol>

    <pre><code>if ((tab = table) == null || (n = tab.length) == 0)
    n = (tab = resize()).length;                  // 1. create the array
if ((p = tab[i = (n - 1) &amp; hash]) == null)
    tab[i] = newNode(hash, key, value, null);     // 2. empty bucket
else {
    if (p.hash == hash &amp;&amp; (p.key == key || key.equals(p.key)))
        e = p;                                    // 3. same key: replace
    else if (p instanceof TreeNode)
        e = ((TreeNode&lt;K,V&gt;) p).putTreeVal(...);   // 4. bucket is a tree
    else {
        for (int binCount = 0; ; ++binCount) {
            if ((e = p.next) == null) {
                p.next = newNode(hash, key, value, null);  // 5. add at the end
                if (binCount &gt;= TREEIFY_THRESHOLD - 1)
                    treeifyBin(tab, hash);                 //    line is long: tree
                break;
            }
            if (e.hash == hash &amp;&amp; (e.key == key || key.equals(e.key))) break;
            p = e;
        }
    }
    if (e != null) { V old = e.value; e.value = value; return old; }
}
++modCount;
if (++size &gt; threshold) resize();                 // 6. too full: grow
return null;</code></pre>
  </section>

  <section class="sec">
    <h2><span class="num">04</span>Why resize is cheap</h2>
    <p>When the array grows from 16 to 32, an item has only two possible new places: <b>where it is</b>, or <b>where it is + 16</b>. One bit decides:</p>
    <pre><code>if ((e.hash &amp; oldCap) == 0)  keep the item at index i
else                          move it to index i + oldCap</code></pre>
    <p>So HashMap does not recompute the hash or the index for every item. It splits each bucket into two small lines and moves them.</p>
  </section>

  <section class="sec">
    <h2><span class="num">05</span>Two numbers: 0.75 and 8</h2>
    <table class="ledger">
      <thead><tr><th>Number</th><th>What it means</th><th>Why</th></tr></thead>
      <tbody>
        <tr><td>0.75</td><td>load factor: grow when size &gt; capacity × 0.75</td><td>A balance: smaller wastes memory, bigger makes more collisions. 0.75 is the usual middle.</td></tr>
        <tr><td>8</td><td>a bucket with 8 items may become a tree</td><td>With a good hash, a line of 8 is very rare (about 1 in 10,000,000). If it happens, the bucket is unlucky, so a tree makes it fast again.</td></tr>
        <tr><td>64</td><td>the array must have 64 buckets before a tree is allowed</td><td>With a small array it is cheaper to grow the array than to build a tree.</td></tr>
        <tr><td>6</td><td>a tree with 6 items turns back into a line</td><td>A buffer, so the bucket does not flip between tree and line again and again.</td></tr>
      </tbody>
    </table>
  </section>

  <section class="sec">
    <h2><span class="num">06</span>Why it is not thread-safe</h2>
    <p>Two threads can call <code>put</code> at the same time. Both read the same <code>size</code>, both write it back — one increase is lost. In JDK 7, two threads resizing at once could even bend the lines into a circle, and then <code>get</code> would spin forever.</p>
    <p>So in a web application use <b>ConcurrentHashMap</b>. It locks only the bucket that is being changed, not the whole map.</p>
    <p class="note"><b>Want the long version?</b> Read <a href="../basics/threads.html">Lesson 7: Why HashMap is not thread-safe</a>.</p>
  </section>

  <section class="sec">
    <h2><span class="num">07</span>Say it in 60 seconds</h2>
    <blockquote class="script">
      <span class="lbl">Read it out loud · then say it in your own words</span>
      <p>A HashMap is an array of buckets. You give it a key, it computes a hash, and the hash tells it which bucket to use.</p>
      <p>If the bucket is empty, the value goes in. If the bucket already has items with different keys, they stand in a line — a linked list. When one line reaches 8 items and the array has at least 64 buckets, the line becomes a red-black tree, so the worst case is O(log n) instead of O(n).</p>
      <p>When the map is 75 percent full, the array doubles. Because the size is a power of two, each item either stays in its bucket or moves to bucket + old size, so there is no need to recompute the hash.</p>
      <p>HashMap is fast and simple, but it is not thread-safe. In a web application I would use ConcurrentHashMap instead.</p>
    </blockquote>
  </section>

  <section class="sec">
    <h2><span class="num">08</span>The numbers to remember</h2>
    <table class="ledger">
      <thead><tr><th>capacity</th><th>load factor</th><th>tree at</th><th>back to list at</th><th>tree needs capacity</th><th>growth</th></tr></thead>
      <tbody><tr><td>16</td><td>0.75</td><td>8</td><td>6</td><td>64</td><td>×2</td></tr></tbody>
    </table>
  </section>

  <section class="sec">
    <h2><span class="num">09</span>Go deeper</h2>
    <ul>
      <li><a href="../basics/array.html">Lesson 1: What is an array?</a></li>
      <li><a href="../basics/linked-list.html">Lesson 2: What is a linked list?</a></li>
      <li><a href="../basics/tree.html">Lesson 3: What is a tree? And a red-black tree?</a></li>
      <li><a href="../basics/hash.html">Lesson 4: What is a key, a hash, a collision?</a></li>
      <li><a href="../basics/big-o.html">Lesson 5: What is O(1), O(n), O(log n)?</a></li>
      <li><a href="../basics/hashmap-methods.html">Lesson 6: HashMap methods in real life</a></li>
      <li><a href="../basics/threads.html">Lesson 7: Why HashMap is not thread-safe?</a></li>
    </ul>
  </section>
"""

render(
    "questions/java-hashmap.html",
    "How does HashMap work",
    "How HashMap works, explained in simple English: buckets, hash, resize, tree, thread safety.",
    "How does HashMap work?",
    "Question 1 · HashMap",
    "A box of small boxes. Give it a key, get back a value, very fast.",
    tag("Must know", "hot") + tag("HashMap") + tag("speak 60s") + tag("7 lessons"),
    "Question 1: HashMap",
    "Question 1",
    q_body,
    [("bucket", "/ˈbʌkɪt/", "One box in the array that holds items with the same hash."),
     ("hash", "/hæʃ/", "A number computed from the key. Like a fingerprint."),
     ("collision", "/kəˈlɪʒn/", "Two different keys that land in the same bucket."),
     ("resize", "/ˌriːˈsaɪz/", "Make the array bigger and move the items."),
     ("load factor", "/loʊd ˈfæktər/", "How full the table can be before it grows. Default 0.75."),
     ("threshold", "/ˈθreʃhoʊld/", "The size that triggers a resize: capacity × load factor."),
     ("treeify", "/ˈtriːɪfaɪ/", "Turn a long line in a bucket into a tree."),
     ("capacity", "/kəˈpæsəti/", "How many buckets the array has. Default 16."),
     ("thread-safe", "/θred seɪf/", "Safe to use from several threads at the same time.")],
    ["What is a bucket?<small>One box in the array. Items that hash to the same index stand in that box.</small>",
     "How does HashMap find the bucket?<small>index = (n - 1) &amp; hash, where n is the number of buckets.</small>",
     "When does a line become a tree?<small>When one bucket has 8 items and the array has at least 64 buckets.</small>",
     "Why does resize not recompute every hash?<small>Because capacity is a power of two: an item either stays at i or moves to i + oldCap.</small>",
     "Why is HashMap not thread-safe?<small>put is many steps; two threads can overwrite each other, lose updates, or corrupt the lines.</small>"],
    "Next: <a href=\"../index.html\">back to all pages</a> · then try <a href=\"../basics/hash.html\">Lesson 4</a> if “hash” still feels unclear.",
    on="q",
)

# ======================================================== glossary
groups = [
    ("Data structures", [
        ("array", "/əˈreɪ/", "A row of boxes that sit next to each other."),
        ("index", "/ˈɪndeks/", "The number of a box in an array. Starts at 0."),
        ("element", "/ˈelɪmənt/", "One item inside an array."),
        ("contiguous", "/kənˈtɪɡjuəs/", "Touching, with no gaps."),
        ("linked list", "/lɪŋkt lɪst/", "Boxes joined by arrows, one after another."),
        ("node", "/noʊd/", "One box in a list or tree: a value plus pointers."),
        ("pointer", "/ˈpɔɪntər/", "A value that says where the next box is."),
        ("head", "/hed/", "The first node of a list."),
        ("traverse", "/trəˈvɜːrs/", "Walk through items one by one."),
        ("tree", "/triː/", "Nodes with children below them."),
        ("root", "/ruːt/", "The top node of a tree."),
        ("leaf", "/liːf/", "A node with no children."),
        ("height", "/haɪt/", "How many levels a tree has."),
        ("balanced", "/ˈbælənst/", "Left and right sides are about the same size."),
        ("red-black tree", "/red blæk triː/", "A tree that repaints and rotates itself to stay short."),
    ]),
    ("HashMap", [
        ("HashMap", "/hæʃ mæp/", "A map that finds values by key, using an array of buckets."),
        ("key", "/kiː/", "The name you look things up by."),
        ("value", "/ˈvæljuː/", "The thing stored under a key."),
        ("entry", "/ˈentri/", "One key-value pair."),
        ("hash", "/hæʃ/", "A number computed from a key."),
        ("hash function", "/hæʃ ˈfʌŋkʃn/", "The machine that turns a key into a number."),
        ("hashCode", "/hæʃ koʊd/", "Java method that gives an int for an object."),
        ("bucket", "/ˈbʌkɪt/", "One box of the array."),
        ("collision", "/kəˈlɪʒn/", "Two keys with the same bucket."),
        ("capacity", "/kəˈpæsəti/", "How many buckets the array has now."),
        ("load factor", "/loʊd ˈfæktər/", "How full before it grows. Default 0.75."),
        ("threshold", "/ˈθreʃhoʊld/", "capacity × load factor. Crossing it triggers resize."),
        ("resize", "/ˌriːˈsaɪz/", "Double the array and move the items."),
        ("treeify", "/ˈtriːɪfaɪ/", "Turn a long bucket line into a tree."),
        ("equals", "/ˈiːkwəlz/", "Java method that says whether two keys are the same."),
    ]),
    ("Complexity", [
        ("time complexity", "/taɪm kəmˈpleksəti/", "How run time grows with data size."),
        ("Big O", "/bɪɡ oʊ/", "The notation for that growth."),
        ("constant", "/ˈkɑːnstənt/", "Does not grow: O(1)."),
        ("linear", "/ˈlɪniər/", "Grows in a line: O(n)."),
        ("logarithmic", "/ˌlɔːɡəˈrɪðmɪk/", "Grows very slowly: O(log n)."),
        ("quadratic", "/kwɑːˈdrætɪk/", "Grows like n × n: O(n²)."),
        ("amortized", "/əˈmɔːrtaɪzd/", "Average cost over many operations."),
    ]),
    ("Concurrency", [
        ("thread", "/θred/", "One worker running inside a program."),
        ("concurrent", "/kənˈkɜːrənt/", "Happening at the same time."),
        ("race condition", "/reɪs kənˈdɪʃn/", "Result depends on who runs first."),
        ("lock", "/lɑːk/", "Lets only one worker touch something."),
        ("synchronized", "/ˈsɪŋkrənaɪzd/", "Java keyword: one thread at a time here."),
        ("volatile", "/ˈvɑːlətl/", "Java keyword: always read the latest value."),
        ("thread-safe", "/θred seɪf/", "Safe to use from many threads."),
        ("ConcurrentHashMap", "/kənˈkɜːrənt hæʃ mæp/", "Thread-safe HashMap. Locks one bucket at a time."),
    ]),
]

gl_body = ""
for title, items in groups:
    rows = "\n".join(word(*w) for w in items)
    gl_body += """
  <section class="sec">
    <h2><span class="num">%s</span>%s</h2>
    <div class="wordlist">
%s
    </div>
  </section>
""" % ("•", title, rows)

gl_body += """
  <section class="sec">
    <p class="note"><b>How to use this page.</b> Pick five words a day. Click “hear it”, listen twice, then say the word three times while looking at the meaning. Tomorrow, say them again before you open the page.</p>
  </section>
"""

render("glossary.html", "All the words", "Every word used on this site, with pronunciation and a one-line meaning.",
       "All the words, in one place.",
       "Glossary", "Every word from the lessons, with a pronunciation link and one simple meaning.",
       tag("45 words") + tag("read aloud"), "Words", "Glossary", gl_body,
       [], [], "Next: <a href=\"basics/array.html\">start with Lesson 1</a>.", on="w")

# ======================================================== about
about_body = """
  <section class="sec">
    <h2><span class="num">01</span>Why this site is in English</h2>
    <p>I am learning Java, and I am learning English at the same time. If I read Java in Chinese, I only learn the idea. If I read it in English, I learn the idea <b>and</b> the words I will hear in an interview.</p>
    <p>So every page here is in English, with short sentences and no idioms. Every technical word has a real pronunciation link.</p>
  </section>

  <section class="sec">
    <h2><span class="num">02</span>How to use it</h2>
    <ul>
      <li><b>Listen first.</b> Press “Listen to this page” and follow with your eyes.</li>
      <li><b>Say the new words.</b> Five words a page. YouGlish gives real people saying them.</li>
      <li><b>Answer the checks out loud.</b> If you cannot say it, read the page again.</li>
      <li><b>Come back tomorrow.</b> Yesterday's words, then one new page.</li>
    </ul>
  </section>

  <section class="sec">
    <h2><span class="num">03</span>What is on it</h2>
    <ul>
      <li><b>Basics</b> — seven short lessons: array, linked list, tree, hash, Big O, HashMap methods, threads.</li>
      <li><b>Questions</b> — one page per interview question, starting with HashMap.</li>
      <li><b>Words</b> — every word in one list, with pronunciation.</li>
    </ul>
    <p class="note">The site is plain HTML with no framework and no tracking. It is published from <a href="https://github.com/TianYuBaBg/offer-camp">GitHub</a> by Cloudflare Pages.</p>
  </section>
"""

render("about.html", "About", "Why this site is in English, and how to use it.",
       "Learn Java, in English.",
       "About", "Short sentences, real pronunciation, no Chinese in the learning path.",
       tag("English first") + tag("no tracking"), "About", "About", about_body,
       [], [], "Next: <a href=\"basics/array.html\">start Lesson 1</a>.")
print("done")
