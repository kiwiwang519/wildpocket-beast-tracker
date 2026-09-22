#!/bin/bash
# 生成已签名的 寻兽记.apk（自签名证书，可直接安装，不需要 Google Play 账号）
# 用法：在本目录运行  ./build-apk.sh
set -euo pipefail
cd "$(dirname "$0")"

export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home}"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/android-sdk}"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:/opt/homebrew/bin:$PATH"

if [ ! -x "$JAVA_HOME/bin/java" ]; then
  echo "❌ 没找到 Java。请先运行：brew install openjdk"
  exit 1
fi
if [ ! -d "$ANDROID_HOME/platforms/android-34" ]; then
  echo "❌ 没找到 Android SDK。请先安装 Android SDK 命令行工具，并运行："
  echo "   sdkmanager \"platform-tools\" \"platforms;android-34\" \"build-tools;34.0.0\""
  exit 1
fi
if [ ! -f "寻兽记.keystore" ]; then
  echo "首次运行，生成签名密钥…"
  keytool -genkeypair -v -keystore 寻兽记.keystore -alias wildpocket -keyalg RSA \
    -keysize 2048 -validity 10000 -storepass wildpocket2026 -keypass wildpocket2026 \
    -dname "CN=WildPocket, OU=WildPocket, O=WildPocket, L=Unknown, ST=Unknown, C=CN"
fi

echo "1/2 同步最新网页到 App 工程…"
rsync -a --delete --delete-excluded --exclude app-preview.html --exclude sw.js \
  ../work/safari/dist/ app/src/main/assets/www/

echo "2/2 编译并签名…"
echo "sdk.dir=$ANDROID_HOME" > local.properties
gradle assembleRelease --console=plain

APK=app/build/outputs/apk/release/app-release.apk
[ -f "$APK" ] || { echo "❌ 没找到 $APK"; exit 1; }
cp "$APK" "寻兽记.apk"
echo "✅ 完成：$PWD/寻兽记.apk（$(du -h 寻兽记.apk | cut -f1)）"
echo "   可以直接把这个文件发给朋友，在 Android 手机上打开安装即可。"
