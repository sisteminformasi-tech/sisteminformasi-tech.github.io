import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#060E1A',
          900: '#0A192F', // Primary Navy
          800: '#112240',
          700: '#1E3A5F',
          600: '#2A528A',
        },
        gold: {
          950: '#3D050D',
          900: '#5C0A15',
          800: '#75101E',
          700: '#8A172B', // Deep Crimson
          600: '#A31F34', // MIT Cardinal Red (Official)
          500: '#B8233B', // Main interactive red
          400: '#E03E52', // High-visibility bright red on dark backgrounds
          300: '#EE7281',
          200: '#F8B4BD',
          100: '#FDF2F4', // Soft tech rose background
          50: '#FFF5F6',
        },
        mit: {
          red: '#A31F34',
          bright: '#E03E52',
          dark: '#821828',
          tint: '#FDF2F4',
          silver: '#8A8B8C',
        },
        slate: {
          900: '#0F172A',
          800: '#1E293B',
          700: '#334155',
          600: '#475569',
          500: '#64748B',
          400: '#94A3B8',
          200: '#E2E8F0',
          100: '#F1F5F9',
          50: '#F8FAFC',
        },
        canvas: {
          light: '#FAF9F6', // Warm Off-White
          card: '#FFFFFF',
          subtle: '#F4F3EE',
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'Cambria', '"Times New Roman"', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'Menlo', 'Monaco', 'monospace'],
      },
      boxShadow: {
        '2xs': '0 1px 1px 0 rgba(10, 25, 47, 0.05)',
        'subtle': '0 1px 3px 0 rgba(10, 25, 47, 0.05), 0 1px 2px 0 rgba(10, 25, 47, 0.03)',
        'card': '0 4px 6px -1px rgba(10, 25, 47, 0.05), 0 2px 4px -1px rgba(10, 25, 47, 0.03)',
        'elevated': '0 10px 15px -3px rgba(10, 25, 47, 0.08), 0 4px 6px -2px rgba(10, 25, 47, 0.04)',
      }
    },
  },
  plugins: [typography],
};
