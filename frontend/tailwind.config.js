/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        "body-text": "var(--body-text-font-family)",
        subheading: "var(--subheading-font-family)",
        'pretendard': ['Pretendard', 'sans-serif'],
      },
      boxShadow: {
        "button-shadow": "var(--button-shadow)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};