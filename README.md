# offer-camp

一个**空白**的静态项目。放东西用的。

## 现状

仓库里只有一个空的 `index.html`（打开是白页）。没有框架、没有依赖、没有构建步骤。

## 已经接好的部署

| 项 | 值 |
|---|---|
| GitHub | <https://github.com/TianYuBaBg/offer-camp>（public） |
| Cloudflare Pages 项目 | `offer-camp` |
| 线上地址 | <https://offer-camp-4no.pages.dev> |
| 生产分支 | `main` |
| 框架预设 | 无 ／ 构建命令 空 ／ 输出目录 `/` |

`main` 每次 push，Cloudflare 约 40 秒后自动重新发布，不需要再点任何按钮。

## 以后往里放东西

直接往仓库根目录丢文件即可：

```
index.html          首页（现在空白）
子页面.html         想再加页面就加文件
files/xxx.pdf       图片/文档放在子目录里，用相对路径引用
```

推上去就生效：

```bash
git add -A && git commit -m "放了一份 xx" && git push
```

本地预览：双击 `index.html`，或

```bash
python -m http.server 8000   # 然后开 http://127.0.0.1:8000
```

## 想用命令行部署（可选）

```bash
npm i -g wrangler
wrangler login
wrangler pages deploy . --project-name=offer-camp
```

## 两点注意

- 仓库是 **public**，`*.pages.dev` 也是公网可访问的。要放私人文件就别放这里，或者去 Cloudflare Zero Trust → Access 给这个域名加邮箱白名单。
- 加了新页面后，`index.html` 里记得放个链接，否则只能靠猜地址访问。
