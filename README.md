# Java Notes

A small website for learning Java in English, written for a complete beginner. **Every page has a 中文 / 中英 / English switch** in the top right corner.
Every page gives one idea, five new words, a picture, and a few questions to check yourself.

Live: **https://tianyubabg.github.io/offer-camp/**

---

## What is on it

| Page | What it teaches |
| --- | --- |
| `index.html` | The map: what to read first |
| `basics/array.html` | What is an array? Why is reading O(1) and inserting O(n)? |
| `basics/linked-list.html` | What is a linked list? Array vs list |
| `basics/tree.html` | What is a tree? What does "red-black" mean? |
| `basics/hash.html` | What is a key, a hash, a collision? |
| `basics/big-o.html` | What is O(1), O(n), O(log n)? |
| `basics/hashmap-methods.html` | HashMap methods, and how they look in real code |
| `basics/threads.html` | Why HashMap is not thread-safe |
| `questions/java-hashmap.html` | The whole HashMap answer, in simple English |
| `glossary.html` | All 47 words, with pronunciation and a Chinese meaning |
| `about.html` | Why the site is in English |

## Language switch (top right)

| Button | What you see |
| --- | --- |
| **中文** | Chinese only. Technical terms stay in English (key, bucket, hash…). |
| **中英** | English first, then a Chinese line under it. Use this on hard pages. |
| **English** | English only. The real test. |

The choice is remembered in the browser (`localStorage`), and the 🔊 button reads whatever language is showing.

## Two things on every page

- **🔊 Listen to this page** — the computer reads the page out loud, in English.
- **▶ hear it** — real people saying a word on [YouGlish](https://youglish.com).
  Every technical word is linked: `https://youglish.com/pronounce/<word>/english`

## How to use it

1. Open the page you are on (start with Lesson 1).
2. Press **Listen to this page**, follow the words with your eyes. Twice is enough.
3. Click **▶ hear it** on five words. Say each word out loud three times.
4. Read *Check yourself* and answer **out loud**, not in your head.
5. Tomorrow: say yesterday's words first, then one new page.

Twenty minutes a day is enough. One page a day is the whole plan.

## Files

```
index.html            the map
basics/*.html         seven short lessons
questions/*.html      interview questions
glossary.html         all words
assets/style.css      the look (paper, serif, one accent colour)
assets/app.js         speak buttons, word links, read-the-page
_build.py             generates every page (bilingual)
_content_a.py         text for home + lessons 1–4
_content_b.py         text for lessons 5–7, the question, words, about
_render.py            layout + CSS/JS
```

Plain HTML, no framework, no tracking, no build step needed to view.
To change the text, edit `_content_a.py` / `_content_b.py` and run `python _build.py`.

## Deploy

The site is published with **GitHub Pages** from the `main` branch, root folder.
Every push to `main` republishes it in about a minute.

Optional: you can also connect the same repo to Cloudflare Pages
(framework preset **None**, build command empty, output directory `/`)
and get a `*.pages.dev` address with better speed in some regions.
