/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Etched-board palette: near-black substrate, phosphor-green traces.
        // Single accent hue by design — only danger departs from it.
        cairn: {
          void: "#05070a", // page substrate
          panel: "#0b1210", // raised surface (cards, nav, inputs)
          "panel-alt": "#0e1a15", // pressed / hovered surface
          trace: "#14532d", // hairline borders, etched traces
          "trace-dim": "#0f2419", // resting rails, dividers
          ink: "#b8f5cf", // body text
          dim: "#5f8f74", // secondary text
          neon: "#2ee06a", // primary accent
          "neon-soft": "#1c7f45", // accent at rest
          solder: "#7dffb0", // pad highlights
          danger: "#b91c1c",
          "danger-ink": "#fca5a5",
        },
      },
      fontFamily: {
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "SF Mono",
          "Menlo",
          "Consolas",
          "Liberation Mono",
          "monospace",
        ],
      },
      boxShadow: {
        // Emission, not elevation: the board glows rather than casting shadow.
        trace: "0 0 0 1px rgba(46, 224, 106, 0.08)",
        emit: "0 0 12px -2px rgba(46, 224, 106, 0.45)",
        "emit-strong": "0 0 18px -1px rgba(46, 224, 106, 0.7)",
      },
      keyframes: {
        padPulse: {
          "0%, 100%": { opacity: "0.55", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.35)" },
        },
      },
      animation: {
        "pad-pulse": "padPulse 2.4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
