# 寻兽记 · 东非动物图鉴

[English version](README.en.md)

面向去坦桑尼亚及东非 Safari 的普通旅行者，一款无网络也能用的动物图鉴。看真实照片、辨识别特征、听动物叫声、读野外故事，并记录自己"见过"的动物。

## 功能

- **筛选与搜索**：按地点、日间/夜间、有助于野外识别的分类筛选，支持按名字或特征搜索。
- **遇见概率**：每种动物标注相对遇见概率，仅用于排序参考，不是实时预报或保护等级。
- **详情页**：每种动物 3 张真实照片（可左右滑动）、认识特征、野外故事、部分动物有叫声。
- **收集册**："我的"页展示已见过的动物、总体进度和按稀有度分组的进度，记录只保存在本机。
- **完全离线**：所有照片、故事和叫声都在首次联网打开时下载到本机（网页版）或直接打包在安装包内（iOS / Android App），之后断网也能正常使用。
- **叫声来源**：38 种动物配有真实录音，来自 Wikimedia Commons、柏林自然博物馆动物声音档案（Tierstimmenarchiv）和 iNaturalist，均为知识共享授权。详细来源见 [CREDITS.md](CREDITS.md)。

## 三种使用方式

| 方式 | 适合 | 需要 |
|---|---|---|
| 网页版（PWA） | 所有平台，最省事 | 一个能打开网页的浏览器 |
| iOS App | iPhone 用户想要原生体验 | Mac、Xcode、你自己的 Apple ID |
| Android App | Android 用户 | 一台 Android 手机 |

---

## 网页版：添加到主屏幕

这是最简单的安装方式，不需要账号，不会过期，安卓和 iPhone 都能用。

1. 用 Safari（iPhone）或 Chrome（Android）打开网站链接。
2. **iPhone**：点底部分享图标，选"添加到主屏幕"。
   **Android**：点右上角菜单，选"安装应用"或"添加到主屏幕"。
3. 首次联网打开时，App 会在后台自动下载全部照片和叫声。
4. 下载完成后即可断网使用，图标会出现在主屏幕上，和原生 App 没有区别。

网页源码在 [`work/safari/dist/`](work/safari/dist/)。想自己搭建，用任意支持 HTTPS 的静态网站托管（如 GitHub Pages、Cloudflare Pages、Netlify）部署这个目录即可。

---

## iOS 安装

iOS 系统只允许安装签过名的 App，必须用你自己的 Apple ID 签名一次。完整步骤、常见问题和更新方法见 [`WildPocket-iOS/安装说明.md`](WildPocket-iOS/安装说明.md)，这里是概览：

**方式一：用 Xcode 直接装（推荐，免费，7 天有效）**

1. 打开 `WildPocket-iOS/WildPocket.xcodeproj`。
2. 在 Signing & Capabilities 里登录你的 Apple ID，Bundle Identifier 改成你自己的唯一值。
3. 手机连接 Mac，开启"设置 → 隐私与安全性 → 开发者模式"。
4. 选中你的手机，按 ⌘R 运行。
5. 首次打开若提示不受信任，去"设置 → 通用 → VPN 与设备管理"信任一次。

**方式二：用 Sideloadly 装未签名的 IPA**

1. 从 [Releases](../../releases) 下载最新的 `WildPocket.ipa`（未签名）。
2. 用 [Sideloadly](https://sideloadly.io) 把 IPA 拖进去，输入你的 Apple ID，点 Start。
3. 同样需要在手机上信任一次开发者。

两种方式都是免费账号的 7 天有效期，到期重装即可，"见过"记录会保留。想长期使用或发给朋友，需要 99 美元一年的 Apple Developer Program，通过 TestFlight 分发。

---

## Android 安装

Android 的 APK 用普通自签名证书即可安装，**不需要付费账号，不会过期**，可以直接发给朋友。

1. 从 [Releases](../../releases) 下载最新的 `WildPocket-Android.apk`。
2. 手机上打开这个文件。如果提示"为保护您的设备，此来源被屏蔽"：
   - 点"设置"，找到对应的浏览器或文件管理器，打开"允许安装未知应用"。
   - 返回重新点开 APK 文件。
3. 点"安装"，完成后在主屏幕能看到"寻兽记"图标。
4. 首次打开会显示已经内置的全部照片、故事和叫声，无需联网即可使用。

想自己编译，进入 `WildPocket-Android/` 目录运行 `./build-apk.sh`。

---

## 项目结构

```
work/safari/dist/          网页版源码，唯一的内容源头（图鉴数据、照片、叫声、离线逻辑）
WildPocket-iOS/             iOS 工程（WKWebView 包装），Resources/Web 由 dist 同步而来
WildPocket-Android/         Android 工程（WebView 包装），assets/www 由 dist 同步而来
CREDITS.md                  全部照片与叫声的作者、许可与来源
```

修改动物数据、照片、叫声或界面，都只改 `work/safari/dist/`，然后：

```bash
# 同步进 iOS 工程并重新打包
cd WildPocket-iOS && ./build-ipa.sh

# 同步进 Android 工程并重新打包
cd WildPocket-Android && ./build-apk.sh
```

## 内容与许可原则

- 图片和叫声均使用知识共享授权的公开来源，详情页底部注明作者、许可与原始链接。
- "相对遇见概率"是按地点、时段和常见程度的粗略估计，不是实时预报，也不代表保护等级。
- 少数动物暂无同种叫声，改用近缘种录音，App 内会明确标注"近缘种"。
- "见过"记录只保存在你自己的设备本地，项目不收集任何个人数据，不含账号、登录或云同步。

## 已知限制

- 17 种动物暂时没有找到开放许可的叫声录音，名单见 [CREDITS.md](CREDITS.md)。
- iOS 免费签名 7 天过期，是苹果的系统限制，不是 Bug。
- 目前只做了 iPhone / Android 手机竖屏，没有适配平板和横屏。
