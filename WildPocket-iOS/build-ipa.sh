#!/bin/bash
# 生成未签名的 WildPocket-unsigned.ipa（供 Sideloadly / AltStore 用你自己的 Apple ID 重新签名后安装）
# 用法：在本目录运行  ./build-ipa.sh
set -euo pipefail
cd "$(dirname "$0")"

if ! xcrun --sdk iphoneos --show-sdk-path >/dev/null 2>&1; then
  echo "❌ Xcode 还不能使用。请先在终端运行一次：sudo xcodebuild -license accept"
  exit 1
fi

echo "1/3 同步最新网页到 App 工程…"
rsync -a --delete --delete-excluded --exclude app-preview.html --exclude sw.js ../work/safari/dist/ WildPocket/Resources/Web/

echo "2/3 编译 iPhone 真机版本（不签名）…"
rm -rf build
xcodebuild -project WildPocket.xcodeproj -target WildPocket -configuration Release -sdk iphoneos \
  SYMROOT="$PWD/build" CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" build

echo "3/3 打包 IPA…"
APP="build/Release-iphoneos/WildPocket.app"
[ -d "$APP" ] || { echo "❌ 没找到 $APP"; exit 1; }
rm -rf Payload WildPocket-unsigned.ipa
mkdir Payload && cp -R "$APP" Payload/
zip -qry WildPocket-unsigned.ipa Payload
rm -rf Payload
echo "✅ 完成：$PWD/WildPocket-unsigned.ipa（$(du -h WildPocket-unsigned.ipa | cut -f1)）"
