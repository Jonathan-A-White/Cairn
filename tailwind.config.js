/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        cairn: {
          bg: "#f8f9fa",
          ink: "#1f2937",
        },
      },
    },
  },
  plugins: [],
};
