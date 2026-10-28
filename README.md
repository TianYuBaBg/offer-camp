# 求职自习室 · Offer Camp

一个 **纯静态** 的单页网站：给自己找工作期间用的「学习台账」。

每天三件事打勾（读词 → 刷题 → 写项目），下面挂着学习地图、进度台账、和一行行日记。
没有框架、没有依赖、没有追踪脚本，`git push` 之后 Cloudflare Pages 自动发布。

```
offer-camp/
├─ index.html          # 唯一的页面
├─ assets/style.css    # 排版：纸感 + 账本，宋体标题 / 黑体正文 / 朱红点缀
├─ assets/app.js       # 日期与「第 N 天」、打勾状态（localStorage）、日志渲染
└─ README.md
```

## 本地预览

直接双击 `index.html` 就行（不需要起服务器、不需要 npm）。

## 想改内容时改哪里

| 想改什么 | 改哪 |
|---|---|
| 今日三件事的文案 | `index.html` 里 `<section id="today-block">` |
| 学习地图四张卡 | `index.html` 里 `.cards` |
| 进度台账的数字 | `index.html` 里 `.ledger` |
| 日志（每天一行） | `assets/app.js` 顶部的 `LOGS` 数组 |
| 第 N 天的起始日期 | `assets/app.js` 第一行 `START` |
| 颜色 / 字体 / 间距 | `assets/style.css` 顶部的 `:root` 变量 |

改完提交：

```bash
git add -A && git commit -m "更新日志" && git push
```

## 部署到 Cloudflare Pages（免费）

两条路，选一条即可。

### A. 网页点 5 步（不用命令行）

1. 打开 <https://dash.cloudflare.com> → 左侧 **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. 授权 GitHub，选中仓库 **TianYuBaBg/offer-camp**
3. 设置：
   - Production branch：`main`
   - Framework preset：**None**
   - Build command：**留空**
   - Build output directory：`/`
4. **Save and Deploy**，等 1 分钟
5. 得到地址 `https://offer-camp.pages.dev`，以后每次 push 自动重新发布

### B. 命令行（wrangler）

```bash
npm i -g wrangler
wrangler login
wrangler pages project create offer-camp --production-branch main
wrangler pages deploy . --project-name=offer-camp
```

## 想让别人打不开（可选）

`*.pages.dev` 是公网可访问的。如果不想让任何人随手点开：

- Cloudflare Zero Trust → **Access** → Applications → Add self-hosted → 域名填 `offer-camp.pages.dev` → 策略选 `Emails` 只允许自己的邮箱（免费版够用）
- 或加一个简单口令页（把 `index.html` 改名 `home.html`，用 Worker 转发）

## 说明

- 打勾状态存在浏览器本地（`localStorage`），换设备/清缓存会清空，这是故意的：它只是当日提醒，不是数据中心。
- 页面里的数字（326 个词、179 道题、47 道保命题）来自同目录另外两个仓库的学习材料，手动同步即可。
