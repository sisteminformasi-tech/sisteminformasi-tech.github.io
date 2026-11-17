import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL): 'id' | 'en' {
  const [, lang] = url.pathname.split('/');
  if (lang in ui) return lang as 'id' | 'en';
  return defaultLang;
}

export function useTranslations(lang: 'id' | 'en') {
  return function t(key: keyof typeof ui[typeof defaultLang]): string {
    return ui[lang][key] || ui[defaultLang][key];
  };
}

export function getLocalizedPath(currentPath: string, targetLang: 'id' | 'en'): string {
  // Mapping table between ID and EN paths
  const routeMap: Record<string, string> = {
    '/': '/en/',
    '/profil/': '/en/about/',
    '/akademik/kurikulum/': '/en/academics/curriculum/',
    '/akademik/rps/': '/en/academics/rps/',
    '/civitas/': '/en/faculty/',
    '/riset/kelompok-riset/': '/en/research/groups/',
    '/mahasiswa/': '/en/students/',
    '/alumni/': '/en/alumni/',
    '/tracer-study/': '/en/tracer-study/',
    '/pmb/': '/en/admissions/',
    '/berita/': '/en/news/',
    '/unduhan/': '/en/downloads/',
    '/kontak/': '/en/contact/',
  };

  // Reverse mapping for EN to ID
  const reverseMap: Record<string, string> = {};
  for (const [idRoute, enRoute] of Object.entries(routeMap)) {
    reverseMap[enRoute] = idRoute;
  }

  // Clean trailing slash
  const normPath = currentPath.endsWith('/') ? currentPath : `${currentPath}/`;

  if (targetLang === 'en') {
    if (normPath.startsWith('/en/')) return normPath;
    return routeMap[normPath] || `/en${normPath}`;
  } else {
    // Switching to ID
    if (!normPath.startsWith('/en/')) return normPath;
    return reverseMap[normPath] || normPath.replace(/^\/en/, '') || '/';
  }
}
