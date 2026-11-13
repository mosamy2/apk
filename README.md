# Warid for Android (وارِد)

Android port of [Warid](https://github.com/MohamedMaslooh/Warid) — voice → Gemini → text (transcription, translation, custom prompts).
Forked from the desktop app, licensed **AGPL-3.0-or-later** (see `LICENSE`, `NOTICE`).

## What changed vs. desktop
- Wrapped with **Capacitor** (WebView) instead of Tauri; every Tauri API is replaced by a shim in `mobile/shims/`
  (settings → localStorage, SQLite → sql.js persisted in IndexedDB, clipboard/opener/share → web & Capacitor).
- New mobile UI layer (`src/styles/mobile.css`, `src/components/layout/MobileNav.tsx`): bottom tab bar, glossy 3D record orb, raised cards, pressable buttons.
- Desktop-only features hidden on mobile: global hotkeys, tray, floating overlay, launch-on-startup, auto-updater.

## Install
Download `warid.apk` from the **warid-latest** release (or Actions → latest run → Artifacts), allow "install unknown apps", open it, then paste your free Gemini key from <https://aistudio.google.com> in Settings.

## Build
`npm ci && npm run build:mobile && npx cap add android && npx cap sync android && cd android && ./gradlew assembleDebug`
(CI does this on every push to `warid-android`.)
