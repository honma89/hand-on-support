import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/app/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "1rem",
        lg: "4rem",
      },
      screens: { "2xl": "1400px" },
    },
    extend: {
      colors: {
        background: "rgb(249 249 249)",
        foreground: "rgb(26 28 28)",
        card: "rgb(255 255 255)",
        "card-foreground": "rgb(26 28 28)",
        primary: "rgb(116 91 0)",
        "primary-foreground": "rgb(255 255 255)",
        "primary-container": "rgb(255 204 0)",
        "primary-fixed": "rgb(255 224 139)",
        "primary-fixed-dim": "rgb(241 193 0)",
        secondary: "rgb(163 62 0)",
        "secondary-foreground": "rgb(255 255 255)",
        "secondary-container": "rgb(254 101 0)",
        tertiary: "rgb(0 104 116)",
        "tertiary-foreground": "rgb(255 255 255)",
        "tertiary-container": "rgb(0 231 254)",
        surface: "rgb(249 249 249)",
        "surface-variant": "rgb(226 226 226)",
        border: "rgb(128 118 95)",
        input: "rgb(226 226 226)",
        ring: "rgb(116 91 0)",
      },
      fontFamily: {
        sans: ["var(--font-body)", "Inter", "sans-serif"],
        display: ["var(--font-display)", "Montserrat", "sans-serif"],
      },
      borderRadius: {
        sm: "0.25rem",
        DEFAULT: "0.5rem",
        md: "0.75rem",
        lg: "1rem",
        xl: "1.5rem",
        full: "9999px",
      },
      spacing: {
        base: "8px",
        xs: "4px",
        sm: "12px",
        md: "24px",
        lg: "48px",
        xl: "80px",
        gutter: "24px",
        "margin-mobile": "16px",
        "margin-desktop": "64px",
      },
      boxShadow: {
        ambient: "0px 4px 20px rgba(0, 0, 0, 0.05)",
        "ambient-hover": "0px 8px 30px rgba(0, 0, 0, 0.08)",
      },
      fontSize: {
        "display-lg": ["48px", { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "700" }],
        "headline-lg": ["32px", { lineHeight: "1.2", fontWeight: "700" }],
        "headline-lg-mobile": ["28px", { lineHeight: "1.2", fontWeight: "700" }],
        "headline-md": ["24px", { lineHeight: "1.3", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "1.6", fontWeight: "400" }],
        "body-md": ["16px", { lineHeight: "1.5", fontWeight: "400" }],
        "label-md": ["14px", { lineHeight: "1.2", fontWeight: "600" }],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
