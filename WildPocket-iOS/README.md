# 寻兽记：东非动物图鉴（iOS）

这是一个可用 Xcode 打开并提交 App Store Connect 的 iPhone 工程。所有图鉴文字、图片和声音样本均已打包到应用内；安装后无需网络即可使用。

## 发布前一次性配置

1. 在装有完整 Xcode 的 Mac 上打开 `WildPocket.xcodeproj`。
2. 选择 `WildPocket` target，在 **Signing & Capabilities** 中选择你的 Team，并把 Bundle Identifier 改为你在 Apple Developer 后台登记的唯一值。
3. 在 iPhone 模拟器和真机各检查一次地点筛选、图片、声音和“见过”记录。
4. 选择 **Product → Archive**，在 Organizer 中点击 **Distribute App → App Store Connect** 上传。

## App Store Connect 文案建议

- 名称：寻兽记：东非动物图鉴
- 副标题：离线识别东非野生动物
- 分类：旅游 / 参考资料
- 隐私：应用不收集个人数据；“见过”记录仅保存在设备本地。

## 版本说明

- 最低系统：iOS 16
- 无账号、无网络请求、无分析 SDK
- 外部参考链接仅在用户主动点击后通过系统浏览器打开
