import React from "react";
import ReactDOM from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import { App } from "./app/App";
import { startAppUpdates } from "./app/appUpdate";
import "./index.css";

// registerType "prompt" (vite.config.ts): a new build waits for his tap on the
// Update banner. The registration goes to the update logic, which shows the
// banner, sends SKIP_WAITING on the tap, reloads once, and asks for a new build
// on start, on return to the foreground and every 30 minutes.
registerSW({
  immediate: true,
  onRegisteredSW(_url, registration) {
    if (registration) {
      startAppUpdates({
        container: navigator.serviceWorker,
        registration,
        reload: () => window.location.reload(),
      });
    }
  },
});

// Mid-session deploy safety: if a dynamic import fails because the precache was
// swapped under us, reload to pick up the new build (auto-save makes this safe).
window.addEventListener("vite:preloadError", (e) => {
  e.preventDefault();
  window.location.reload();
});

// Ask the browser to keep our IndexedDB store from being evicted under pressure.
if (navigator.storage?.persist) {
  void navigator.storage.persist();
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
