// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Android (Capacitor) build: same React app, with every Tauri desktop API
// swapped for a web/Capacitor shim from mobile/shims.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

const tauriShim = path.resolve(__dirname, "mobile/shims/tauri.ts");
const sqlShim = path.resolve(__dirname, "mobile/shims/sql.ts");

export default defineConfig({
  plugins: [react()],
  base: "./",
  define: { "import.meta.env.VITE_MOBILE": JSON.stringify("1") },
  resolve: {
    alias: [
      { find: "@tauri-apps/plugin-sql", replacement: sqlShim },
      { find: /^@tauri-apps\/(api|plugin-[a-z-]+)(\/.*)?$/, replacement: tauriShim },
    ],
  },
  build: { outDir: "www", emptyOutDir: true, target: "es2020", chunkSizeWarningLimit: 2000 },
});
