import type { Config } from "tailwindcss";
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          900: "#0a1633",
          800: "#0f2150",
          700: "#153066",
          600: "#1b3e86"
        }
      }
    }
  },
  plugins: []
} satisfies Config;
