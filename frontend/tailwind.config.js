/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    screens: {
      'phone': { min: '0px' },
      'tablet': { min: '641px' },
      'full': { min: '1025px' },
    }
  },
  plugins: [],
}