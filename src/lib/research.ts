/** Split a focus string into chips: top-level commas and "dan"/"and" only (commas inside parentheses are kept). */
export function splitFocus(focus: string): string[] {
  const parts: string[] = [];
  let depth = 0;
  let buf = '';
  for (const ch of focus.replace(/\.\s*$/, '')) {
    if (ch === '(') depth++;
    if (ch === ')') depth = Math.max(0, depth - 1);
    if (ch === ',' && depth === 0) {
      parts.push(buf);
      buf = '';
    } else buf += ch;
  }
  parts.push(buf);
  return parts
    .map((p) => p.trim().replace(/^(dan|and)\s+/i, ''))
    .filter(Boolean);
}

export function initials(name: string): string {
  const words = name
    .replace(/\(.*?\)/g, '')
    .split(',')[0]
    .split(/\s+/)
    .filter((w) => w && !/^(dr|prof|ir)\.?$/i.test(w));
  return words.slice(0, 2).map((w) => w[0].toUpperCase()).join('');
}

export function isCoordinatorEntry(m: string): boolean {
  return /\((Koordinator|Coordinator)\)/i.test(m);
}

export function cleanMember(m: string): string {
  return m.replace(/\s*\((Koordinator|Coordinator)\)\s*/i, '').trim();
}
