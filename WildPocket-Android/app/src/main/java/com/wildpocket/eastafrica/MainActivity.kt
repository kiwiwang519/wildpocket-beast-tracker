package com.wildpocket.eastafrica

import android.annotation.SuppressLint
import android.app.Activity
import android.media.AudioManager
import android.os.Bundle
import android.view.WindowManager
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.core.view.WindowCompat

// Plain Activity, not AppCompatActivity: AppCompatActivity requires the app to use
// a Theme.AppCompat (or MaterialComponents) theme and throws IllegalStateException
// at launch otherwise. Our manifest uses the plain framework Theme.Material — we
// don't need any AppCompat widgets here (no action bar, no fragments), so a plain
// Activity is enough and avoids that crash.
class MainActivity : Activity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Deliberately NOT edge-to-edge: an earlier version called
        // WindowCompat.setDecorFitsSystemWindows(window, false) plus a WindowInsets
        // listener to pad the WebView by the status/nav bar size, so our own CSS could
        // draw behind them for an iOS-style immersive look. On this device (a Huawei
        // phone on a heavily customized Android build) that WindowInsets callback either
        // didn't fire or fired with stale/zero values, so the WebView's content — including
        // the detail page's back button — rendered underneath the status bar, in an area
        // the status bar's own window still intercepts touches for. The button was visibly
        // there but physically untappable, which read as "no back button".
        //
        // Leaving decorFitsSystemWindows at its default `true` makes Android reserve
        // status/nav bar space the old, unconditional way: it resizes our content view
        // itself, no callback involved, so it cannot silently fail to fire. We lose the
        // cosmetic behind-the-bars look; we gain a back button you can actually press on
        // every device.
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        // Explicit, not just "don't call the edge-to-edge API": on this device (Huawei
        // EMUI 11) the window still rendered full-bleed behind the status/nav bars even
        // after removing our own setDecorFitsSystemWindows(false) call, so something in
        // the OEM's systemUI defaults for this targetSdk was still forcing it. Ask
        // explicitly for the non-edge-to-edge behavior and clear any legacy
        // fullscreen/layout-stable flags the theme or OS might have preset.
        WindowCompat.setDecorFitsSystemWindows(window, true)
        @Suppress("DEPRECATION")
        window.decorView.systemUiVisibility = 0
        // Let animal calls play through the media stream even if the ringer is silenced.
        volumeControlStream = AudioManager.STREAM_MUSIC

        webView = WebView(this)
        setContentView(webView)

        // Belt and braces: on this device the window keeps rendering edge-to-edge no
        // matter what the Window APIs above ask for (confirmed via `dumpsys window` —
        // the surface stays the full display size regardless), so don't rely on the
        // system resizing our content at all. Look up the status/navigation bar heights
        // the old, pre-WindowInsets way — a resource lookup that's been stable across
        // Android versions and OEM skins for over a decade — and pad the WebView with
        // them directly. This can't silently fail to fire the way a WindowInsets
        // callback can.
        fun systemDimen(name: String): Int {
            val id = resources.getIdentifier(name, "dimen", "android")
            return if (id > 0) resources.getDimensionPixelSize(id) else 0
        }
        webView.setPadding(0, systemDimen("status_bar_height"), 0, systemDimen("navigation_bar_height"))

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            allowFileAccess = true
            mediaPlaybackRequiresUserGesture = false
            cacheMode = android.webkit.WebSettings.LOAD_DEFAULT
        }
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        webView.loadUrl("file:///android_asset/www/index.html")
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) webView.goBack() else super.onBackPressed()
    }
}
