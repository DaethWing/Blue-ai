import type { Config } from 'tailwindcss'
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          950: '#081a3b',
          900: '#0b214a',
          800: '#0e2a5a',
          700: '#102a5e', // main brand
          600: '#173a7d',
          500: '#1f4eab'
        }
      },
      borderRadius: {
        '2xl': '1rem'
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0,0,0,.25)'
      }
    }
  },
  plugins: []
} satisfies Config
