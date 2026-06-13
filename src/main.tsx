import React from "react";
import ReactDOM from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import { App } from "./app/App";
import "./index.css";

// Auto-update the service worker so users always get the latest build.
registerSW({ immediate: true });

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
