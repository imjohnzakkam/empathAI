/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'emotion-happy': '#10B981',
        'emotion-sad': '#6B7280',
        'emotion-angry': '#EF4444',
        'emotion-disgust': '#8B5CF6',
        'emotion-fear': '#7C3AED',
        'emotion-surprise': '#F59E0B',
        'emotion-neutral': '#4F46E5',
      },
      fontFamily: {
        sans: ['var(--font-inter)'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
} 