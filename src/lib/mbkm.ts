import curriculum from '../data/curriculum.json';

export type Lang = 'id' | 'en';
export type Course = (typeof curriculum.courses)[number];
export type Scheme = (typeof curriculum.mbkm_structure.schemes)[number];
export type Track = Scheme['tracks'][number];

const courseByCode = new Map<string, Course>(curriculum.courses.map((c) => [c.code, c]));

export function getCourse(code: string): Course {
  const c = courseByCode.get(code);
  if (!c) throw new Error(`MBKM: course ${code} not found in curriculum.json`);
  return c;
}

export function formatPl(pl: string): string {
  return pl.replace(/PL0(\d)/g, 'PL$1').split(',').join(' · ');
}

export type MatrixRow =
  | { kind: 'course'; course: Course }
  | { kind: 'note'; semester: number; text: string }
  | { kind: 'scheme'; semester: number; scheme: Scheme }
  | { kind: 'track'; semester: number; track: Track; label: string };

/**
 * Flattens the course list into table rows, inserting a semester note,
 * a scheme header, and (for multi-track schemes) a track header before
 * each MBKM group so mutually exclusive packages read as distinct blocks.
 */
export function buildMatrixRows(lang: Lang): MatrixRow[] {
  const { schemes, semester_6, semester_7 } = curriculum.mbkm_structure;
  const notes: Record<number, string> = {
    6: lang === 'en' ? semester_6.rule_en : semester_6.rule_id,
    7: lang === 'en' ? semester_7.rule_en : semester_7.rule_id,
  };
  const rows: MatrixRow[] = [];
  const seenSemesters = new Set<number>();
  let lastScheme: string | undefined;
  let lastTrack: string | undefined;

  for (const course of curriculum.courses) {
    if (!course.is_mbkm) {
      rows.push({ kind: 'course', course });
      continue;
    }
    const sem = course.semester;
    if (!seenSemesters.has(sem)) {
      seenSemesters.add(sem);
      rows.push({ kind: 'note', semester: sem, text: notes[sem] ?? '' });
    }
    const scheme = schemes.find((s) => s.category === course.mbkm_category);
    if (!scheme) throw new Error(`MBKM: no scheme for category ${course.mbkm_category}`);
    if (scheme.id !== lastScheme) {
      rows.push({ kind: 'scheme', semester: sem, scheme });
      lastScheme = scheme.id;
      lastTrack = undefined;
    }
    if (scheme.tracks.length > 1 && course.mbkm_track !== lastTrack) {
      const track = scheme.tracks.find((t) => t.label === course.mbkm_track);
      if (!track) throw new Error(`MBKM: no track ${course.mbkm_track}`);
      rows.push({ kind: 'track', semester: sem, track, label: lang === 'en' ? track.label_en : track.label });
      lastTrack = course.mbkm_track;
    }
    rows.push({ kind: 'course', course });
  }
  return rows;
}
