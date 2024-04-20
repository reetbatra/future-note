/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#123C69',
        'custom-pink': '#AC3B61',
        'custom-beige': '#EDC7B7',
        'custom-light': '#EEE2DC',
        'custom-gray': '#BAB2B5',
      },
    },
  },
  plugins: [],
}

