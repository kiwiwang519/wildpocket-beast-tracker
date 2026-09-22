# 寻兽记 · 微信小程序

用微信开发者工具打开 `WildPocket-MiniProgram/` 目录即可运行。这是一个完整重写的版本（小程序不能直接跑网页代码），页面结构和玩法与网页版、iOS、Android 版一致：首页筛选与搜索、详情页图集与叫声、"我的"收集进度。

## 图片与音频从哪里来

小程序整包大小有限制（约 20MB），塞不下全部照片和叫声（现在有 30MB 以上）。所以图片和音频不打进包里，而是通过 [jsDelivr](https://www.jsdelivr.com/) 这个全球免费 CDN，直接读取本仓库里已经推送的文件：

```
https://cdn.jsdelivr.net/gh/kiwiwang519/wildpocket-beast-tracker@main/work/safari/dist/assets/
```

首次打开小程序时，会自动把全部照片和叫声下载到本机缓存，之后完全离线可用，逻辑和网页版的 Service Worker 一致（`utils/offline.js`）。

**这意味着：仓库更新了图片或叫声，小程序不用重新打包，直接生效。** 但也意味着必须有网络能连上 GitHub 和 jsDelivr。

## 打开前要做的一步：加白名单

1. 打开 [mp.weixin.qq.com](https://mp.weixin.qq.com)，登录你的小程序账号。
2. 进入"开发管理 → 开发设置 → 服务器域名"。
3. 在 **downloadFile 合法域名** 里加一条：`https://cdn.jsdelivr.net`。
4. 保存。

不做这一步，小程序仍然能联网正常显示图片（`<image>` 标签本身不受这个白名单限制），但没法把文件缓存到本机，也就做不到真正的离线可用。**如果你的目标就是"首次下载好、之后离线用"，这一步不能跳过。**

## 用你自己的 AppID 打开

1. 用微信开发者工具打开这个 `WildPocket-MiniProgram/` 目录。
2. 首次会提示输入 AppID：填你在 mp.weixin.qq.com 注册的小程序 AppID。
3. 也可以手动改 `project.config.json` 里的 `"appid"` 字段（目前是占位的 `"touristappid"`，可以用游客模式在本机预览，但真机扫码预览和正式上传都需要真实 AppID）。

## 本机验证

1. 在开发者工具里点"编译"，模拟器里应该能看到首页动物列表。
2. 点右上角"预览"，用手机微信扫码，在真机上应该能看到同样的界面（这一步会真的联网下载图片，请确保手机联网）。
3. 断开手机网络，重新打开小程序，之前浏览过的动物图片应该还能显示（已经缓存到本机的部分）；完整测试需要先等首页停留几分钟，让全部资料后台下载完，再断网重开。

## 发布给别人用

- **体验版（免审核，人数有限）**：开发者工具里点"上传"，填版本号，然后在 mp.weixin.qq.com 后台"版本管理"里把这个版本设为"体验版"，添加体验成员（微信号或手机号），对方就能通过链接或二维码直接打开，不用等审核。
- **正式发布（所有人可搜索到）**：同样先上传，然后在后台提交审核，通常 1-2 天。审核关注的是内容合规，我们这个 App 没有账号、不收集用户数据，风险较低。

## 项目结构

```
miniprogram/
  app.js / app.json / app.wxss    全局逻辑、页面路由、Tab 栏、全局样式
  data/data.json                  从 work/safari/dist 里的 *.js 数据文件自动导出，纯文本，随包打入
  utils/offline.js                首次启动下载全部图片/音频到本机、本机路径解析
  utils/logic.js                  遇见概率、稀有度等计算逻辑，和网页版 app.js 保持一致
  pages/index/                    首页：筛选、搜索、列表
  pages/detail/                   详情页：图集、特征、叫声、故事、相似动物
  pages/mine/                     我的：收集进度、稀有度分组、离线状态
  images/                         Tab 栏图标
```

## 更新数据

动物数据、照片、叫声改了以后，重新生成 `data.json`：

```bash
cd /Users/rzy/programs/wlx-pro
node -e '
const fs=require("fs"),vm=require("vm");const c={};vm.createContext(c);
const dist="work/safari/dist/";
vm.runInContext(["animals","habitats","stories","sounds","photos"].map(f=>fs.readFileSync(dist+f+".js","utf8")).join(";")+";globalThis.A=ANIMALS;globalThis.L=LOCATIONS;globalThis.S=STORIES;globalThis.C=CALLS;globalThis.G=GALLERY",c);
fs.writeFileSync("WildPocket-MiniProgram/miniprogram/data/data.json",JSON.stringify({animals:c.A,locations:c.L,stories:c.S,calls:c.C,gallery:c.G}));
'
```

改完记得 `git push`，图片改动本身不需要小程序重新上传，只有 `data.json`、页面代码或样式改了才需要在开发者工具里重新上传版本。

## 已知限制

- 小程序端是重写的版本，尽量还原了网页版的功能和视觉，但不是逐像素一致。
- 没有做小程序码分享、转发朋友圈等社交功能。
- 离线缓存依赖小程序自身的文件系统配额，正常够用（约 30MB），个别老旧机型配额较小时可能下载不全。
