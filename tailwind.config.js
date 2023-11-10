/** @type {import('tailwindcss').Config} */
module.exports = {

  content: ['./**/templates/**/*', './**/static/**/*.js', './**app/**/*.py'],
  daisyui: {
    themes: ["light", "dark", "lofi", "corporate", "retro", "wireframe"],
  },

  theme: {
    fontFamily: {
      sans: ['Inter var', 'Helvetica', 'Arial', 'sans-serif'],
    },
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require('tailwindcss-font-inter'), require('@tailwindcss/forms'), require('@tailwindcss/line-clamp')],
}
