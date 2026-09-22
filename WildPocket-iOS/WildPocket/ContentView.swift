import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            // Paint the status-bar region white so it matches the web app's navigation bar in dark mode too.
            Color.white.ignoresSafeArea()
            WildPocketWebView()
                .ignoresSafeArea(edges: .bottom)
        }
        .preferredColorScheme(.light)
    }
}
