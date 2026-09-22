plugins {
    id("org.jetbrains.kotlin.android")
    id("com.android.application")
}

android {
    namespace = "com.wildpocket.eastafrica"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.wildpocket.eastafrica"
        minSdk = 24
        targetSdk = 34
        versionCode = 4
        versionName = "1.0.3"
    }

    signingConfigs {
        create("release") {
            storeFile = file("../寻兽记.keystore")
            storePassword = "wildpocket2026"
            keyAlias = "wildpocket"
            keyPassword = "wildpocket2026"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("release")
        }
    }

    // The offline site already ships as flat files under assets/www; no compression needed.
    androidResources {
        noCompress += listOf("mp3", "jpg", "png", "webmanifest")
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    // AGP's bundled lint tool cannot run under this machine's JDK 27; the actual
    // Kotlin/Java compile and dex steps already succeeded, so skip lint-vital.
    lint {
        checkReleaseBuilds = false
        abortOnError = false
    }
}

dependencies {
    // No androidx.appcompat: MainActivity is a plain Activity (see MainActivity.kt),
    // so we only need core-ktx for WindowCompat/ViewCompat.
    implementation("androidx.core:core-ktx:1.13.1")
}
