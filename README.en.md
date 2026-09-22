# WildPocket Beast Tracker (寻兽记)

[中文版](README.md)

An offline field guide to East African wildlife, built for ordinary travellers heading out on safari in Tanzania. Real photos, identification tips, animal calls, and field stories — plus a personal "seen it" collection — all of it usable without a network connection.

## Features

- **Filters and search** — by location, day/night, and identification-friendly categories (not strict taxonomy); free-text search by name or trait.
- **Encounter likelihood** — a rough relative estimate per animal, for sorting only; not a live forecast or a conservation status.
- **Detail pages** — 3 real photos per animal (swipeable), key identification traits, a field story, and audio calls for some species.
- **Collection** — the "Mine" tab shows everything you've marked as seen, overall progress, and progress by rarity tier. Records stay on your device only.
- **Fully offline** — every photo, story and sound is downloaded to the device the first time you open it online (web version) or bundled directly into the install package (iOS/Android apps). After that it works with no connection at all.
- **Animal calls** — 38 species have real recordings sourced from Wikimedia Commons, the Berlin Natural History Museum's Tierstimmenarchiv (animal sound archive), and iNaturalist, all under Creative Commons licences. Full attribution in [CREDITS.md](CREDITS.md).

## Four ways to use it

| Method | Best for | You need |
|---|---|---|
| Web app (PWA) | Everyone, the easiest path | Any browser |
| iOS app | iPhone users who want a native app | A Mac, Xcode, your own Apple ID |
| Android app | Android users | An Android phone |
| WeChat Mini Program | Opening it straight inside WeChat | WeChat, a Mini Program developer account |

---

## Web app: add to home screen

The simplest option. No account, never expires, works on both iPhone and Android.

1. Open the site link in Safari (iPhone) or Chrome (Android).
2. **iPhone**: tap the share icon, choose "Add to Home Screen".
   **Android**: tap the menu, choose "Install app" or "Add to Home screen".
3. On first launch while online, the app quietly downloads every photo and sound in the background.
4. Once that finishes, it works fully offline — the home-screen icon looks and behaves just like a native app.

Source lives in [`work/safari/dist/`](work/safari/dist/). To self-host, deploy that folder to any HTTPS static host (GitHub Pages, Cloudflare Pages, Netlify, etc.).

---

## iOS install

iOS only runs signed apps, so it must be signed once with your own Apple ID. Full steps, troubleshooting and update instructions live in [`WildPocket-iOS/安装说明.md`](WildPocket-iOS/安装说明.md) (Chinese only for now); here's the overview:

**Option A: install directly from Xcode (recommended, free, lasts 7 days)**

1. Open `WildPocket-iOS/WildPocket.xcodeproj`.
2. In Signing & Capabilities, sign in with your Apple ID and change the Bundle Identifier to something unique.
3. Connect your iPhone to the Mac and enable Settings → Privacy & Security → Developer Mode.
4. Select your phone as the run destination and press ⌘R.
5. If iOS says the developer isn't trusted, go to Settings → General → VPN & Device Management and trust it once.

**Option B: sideload the unsigned IPA with Sideloadly**

1. Download the latest `WildPocket.ipa` (unsigned) from [Releases](../../releases).
2. Drag it into [Sideloadly](https://sideloadly.io), enter your Apple ID, click Start.
3. Trust the developer certificate on the phone as above.

Both options use a free account, so the app expires after 7 days — just reinstall the same way; your "seen it" records are kept. For a longer-lived install, or to share with friends, you need a paid Apple Developer Program membership ($99/year) and TestFlight distribution.

---

## Android install

Android APKs only need an ordinary self-signed certificate — **no paid account, no expiry**, and you can hand the file straight to a friend.

1. Download the latest `WildPocket-Android.apk` from [Releases](../../releases).
2. Open the file on the phone. If it warns "installation blocked for your protection":
   - Tap Settings, find the relevant browser or file manager, and allow "Install unknown apps" for it.
   - Go back and open the APK again.
3. Tap Install. The "寻兽记" (Beast Tracker) icon appears on the home screen when it's done.
4. On first launch everything — photos, stories, sounds — is already bundled in, so no network is needed.

To build it yourself, run `./build-apk.sh` from the `WildPocket-Android/` directory.

---

## WeChat Mini Program

The Mini Program is a full rewrite (Mini Programs can't run regular web code), matching the features of the other three. Photos and sounds are fetched from a CDN on first launch and cached locally for offline use afterwards. Full setup, domain whitelisting and publishing steps are in [`WildPocket-MiniProgram/README.md`](WildPocket-MiniProgram/README.md) (Chinese only, since Mini Program publishing is a Chinese-platform workflow).

1. Open `WildPocket-MiniProgram/` in WeChat DevTools.
2. In the Mini Program admin console (mp.weixin.qq.com), add `https://cdn.jsdelivr.net` to the downloadFile domain whitelist.
3. Set your own Mini Program AppID in `project.config.json`.
4. Compile and preview, or upload a trial/review version.

---

## Project layout

```
work/safari/dist/          The web app source — the single source of truth (animal data, photos, sounds, offline logic)
WildPocket-iOS/             iOS project (WKWebView wrapper); Resources/Web is synced from dist
WildPocket-Android/         Android project (WebView wrapper); assets/www is synced from dist
WildPocket-MiniProgram/     WeChat Mini Program project; photos and sounds are fetched via CDN from work/safari/dist
CREDITS.md                  Every photo and audio clip's author, licence and source link
```

To change animal data, photos, sounds or the UI, edit only `work/safari/dist/`, then:

```bash
# sync into the iOS project and rebuild
cd WildPocket-iOS && ./build-ipa.sh

# sync into the Android project and rebuild
cd WildPocket-Android && ./build-apk.sh
```

## Content and licensing

- All photos and sounds come from openly licensed sources (Creative Commons); every detail page credits the author, licence and original link.
- "Relative encounter likelihood" is a rough estimate from location, time of day and how common a species is — not a real-time forecast and not a conservation status.
- A few animals lack a same-species recording, so a close relative's call is used instead; the app clearly labels these as "近缘种" (related species).
- "Seen it" records live only on your own device. The project collects no personal data and has no accounts, login or cloud sync.

## Known limitations

- 17 species still lack an openly licensed call recording; see [CREDITS.md](CREDITS.md) for the list.
- The iOS free-signing 7-day expiry is an Apple platform limit, not a bug.
- Only phone-sized portrait layouts are designed for; no tablet or landscape support yet.
