import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

const base = process.env.ASTRO_BASE || '/';

export default defineConfig({
  site: 'https://sisteminformasi-tech.github.io',
  base: base,
  output: 'static',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
  ],
  i18n: {
    defaultLocale: 'id',
    locales: ['id', 'en'],
    routing: {
      prefixDefaultLocale: false,
      redirectToDefaultLocale: false,
    },
  },
});
