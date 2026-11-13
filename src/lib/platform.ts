// SPDX-License-Identifier: AGPL-3.0-or-later

/** True in the Android (Capacitor) build, produced by `vite.mobile.config.ts`. */
export const IS_MOBILE = import.meta.env.VITE_MOBILE === "1";

if (IS_MOBILE && typeof document !== "undefined") {
  document.documentElement.classList.add("is-mobile");
}
