import SwiftUI
import AVFoundation

@main
struct WildPocketApp: App {
    init() {
        // Play animal calls even when the iPhone's silent switch is on.
        try? AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
