// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Android/web replacements for the Tauri desktop APIs that Warid's frontend
// imports. The mobile build (vite.mobile.config.ts) aliases every
// `@tauri-apps/*` module to this file, so the desktop code stays untouched.
import { Browser } from "@capacitor/browser";

/* ---------- @tauri-apps/api/core ---------- */
export async function invoke<T = unknown>(cmd: string, args?: Record<string, unknown>): Promise<T> {
  switch (cmd) {
    case "save_pdf": {
      const bytes = new Uint8Array((args?.pdfBytes as number[]) ?? []);
      const name = `${(args?.fileName as string) || "warid"}.pdf`;
      const blob = new Blob([bytes], { type: "application/pdf" });
      const file = new File([blob], name, { type: "application/pdf" });
      const nav = navigator as Navigator & { canShare?: (d: unknown) => boolean };
      if (nav.canShare?.({ files: [file] })) {
        try {
          await navigator.share({ files: [file], title: name });
          return name as T;
        } catch (e) {
          if ((e as Error)?.name === "AbortError") throw "cancelled";
        }
      }
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 10_000);
      return name as T;
    }
    default:
      // update_tray_language, paste_at_cursor, show_overlay ... are desktop-only.
      return undefined as T;
  }
}

/* ---------- @tauri-apps/api/event ---------- */
export async function listen(_event: string, _cb: (e: unknown) => void): Promise<() => void> {
  return () => {};
}
export async function emit(_event: string, _payload?: unknown): Promise<void> {}

/* ---------- @tauri-apps/api/app ---------- */
export async function getVersion(): Promise<string> {
  return (import.meta.env.VITE_APP_VERSION as string) || "1.1.7-android";
}

/* ---------- @tauri-apps/api/window + webviewWindow (floating overlay: desktop only) ---------- */
export class WebviewWindow {}
export async function getAllWebviewWindows(): Promise<WebviewWindow[]> {
  return [];
}
export async function currentMonitor(): Promise<null> {
  return null;
}
export class PhysicalPosition {
  constructor(public x: number, public y: number) {}
}

/* ---------- plugin-process / plugin-updater / plugin-autostart / plugin-global-shortcut ---------- */
export async function relaunch(): Promise<void> {
  location.reload();
}
export interface Update {
  version: string;
  body?: string;
  downloadAndInstall: (cb?: (e: unknown) => void) => Promise<void>;
  download: (cb?: (e: unknown) => void) => Promise<void>;
  install: () => Promise<void>;
}
export async function check(): Promise<Update | null> {
  return null; // updates come from GitHub releases, not the in-app updater
}
export async function enable(): Promise<void> {}
export async function disable(): Promise<void> {}
export async function isEnabled(): Promise<boolean> {
  return false;
}
export async function register(): Promise<void> {}
export async function unregister(): Promise<void> {}
export async function isRegistered(): Promise<boolean> {
  return false;
}

/* ---------- plugin-clipboard-manager ---------- */
export async function writeText(text: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(text);
    return;
  } catch {
    /* fall through to the legacy path (WebView without clipboard permission) */
  }
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.setAttribute("readonly", "");
  ta.style.cssText = "position:fixed;top:-1000px;opacity:0";
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand("copy");
  } finally {
    ta.remove();
  }
}

/* ---------- plugin-opener ---------- */
export async function openUrl(url: string): Promise<void> {
  try {
    await Browser.open({ url });
  } catch {
    window.open(url, "_blank");
  }
}

/* ---------- plugin-store (settings) → localStorage ---------- */
const PREFIX = "warid.store.";
export class Store {
  private constructor(private readonly key: string) {}
  static async load(name: string, _opts?: unknown): Promise<Store> {
    return new Store(PREFIX + name);
  }
  private read(): Record<string, unknown> {
    try {
      return JSON.parse(localStorage.getItem(this.key) ?? "{}");
    } catch {
      return {};
    }
  }
  async get<T>(key: string): Promise<T | null> {
    const v = this.read()[key];
    return (v === undefined ? null : v) as T | null;
  }
  async set(key: string, value: unknown): Promise<void> {
    const all = this.read();
    all[key] = value;
    localStorage.setItem(this.key, JSON.stringify(all));
  }
  async save(): Promise<void> {}
}
