# 求职自习室 · 面试题本

一个**纯静态**的面试题本：一题一页，每页固定五块——30 秒版、原理拆解、追问、照念稿、常见答错。

线上：<https://offer-camp-4no.pages.dev>

## 目录

```
index.html                    题目列表（首页）
about.html                    这个站是干什么的
questions/java-hashmap.html   第 1 题：HashMap 的原理
assets/style.css              全部样式（纸感账本，无框架无依赖）
```

## 加一道新题的步骤

1. 复制 `questions/java-hashmap.html`，改名成新题（如 `questions/java-concurrenthashmap.html`）
2. 改四块内容：题目、30 秒版、拆解、追问、照念稿
3. 在 `index.html` 的 `.qlist` 里加一行链接，把顶部的「共 N 题」和 `mh-right` 里的更新日期改掉
4. 提交：

```bash
git add -A && git commit -m "加题：ConcurrentHashMap" && git push
```

推上去约 40 秒，Cloudflare Pages 自动发布。

## 写题时的几条约定

- **30 秒版先给结论**，能用嘴念顺；细节放后面。
- 每个设计选择都要写「为什么是它」，而不是只写「是什么」。
- 追问至少 5 个，都是面试官真的会接着问的。
- 照念稿控制在 250～320 字（约 60 秒），念起来要像人说话，不像论文。
- 常见答错写「别人踩过的坑」，一条一行。

## 部署

已接好：GitHub `main` 分支 → Cloudflare Pages（项目 `offer-camp`，框架 None，构建命令空，输出目录 `/`）。
`git push` 即自动部署，无需再点按钮。

本地预览：直接双击 `index.html`，或 `python -m http.server 8000`。

## 注意

仓库是 public，线上也是公开可访问的。别往里放私人信息（电话、住址、公司内部资料）。需要限制访问时，去 Cloudflare Zero Trust → Access 给这个域名加邮箱白名单。
