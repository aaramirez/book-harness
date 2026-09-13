'use strict';

const yaml = require('./yaml-lite.js');

const REQUIRED_SECTIONS = [
  { n: 1, en: 'Current Architecture' },
  { n: 2, en: 'Problem' },
  { n: 3, en: 'Why the Current Architecture Is Insufficient' },
  { n: 4, en: 'Constitutional Impact' },
  { n: 5, en: 'New Concepts' },
  { n: 6, en: 'New Data Structures' },
  { n: 7, en: 'New Contracts / Interfaces' },
  { n: 8, en: 'Component Responsibilities' },
  { n: 9, en: 'Dependency Relationships' },
  { n: 10, en: 'Sequence Diagram' },
  { n: 11, en: 'Pseudocode' },
  { n: 12, en: 'State Transitions' },
  { n: 13, en: 'Failure Semantics' },
  { n: 14, en: 'Events Produced' },
  { n: 15, en: 'Security / Policy Implications' },
  { n: 16, en: 'Tests' },
  { n: 17, en: 'Architecture After This Chapter' },
  { n: 18, en: 'What We Deliberately Do Not Solve Yet' },
  { n: 19, en: 'Next Increment' },
];

/**
 * Separa un chapter.md en { frontmatter, sections, pseudocodeBlocks }.
 *
 * Convención de encabezado exigida por write-technical-chapter/SKILL.md:
 *   "## <n>. <Título en español> (<Título en inglés>)"
 * El validador ubica cada sección por su número Y su nombre en inglés entre paréntesis, para no
 * depender de la ortografía exacta del título en español.
 */
function parseChapter(raw) {
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!fmMatch) {
    throw new Error('chapter.md no tiene bloque de frontmatter YAML delimitado por "---"');
  }
  const frontmatter = yaml.parse(fmMatch[1]);
  const body = raw.slice(fmMatch[0].length);

  const headingRe = /^##\s+(\d+)\.\s+(.+)$/gm;
  const headings = [];
  let m;
  while ((m = headingRe.exec(body)) !== null) {
    headings.push({ n: parseInt(m[1], 10), title: m[2].trim(), index: m.index, matchLength: m[0].length });
  }

  const sections = [];
  for (let idx = 0; idx < headings.length; idx++) {
    const h = headings[idx];
    const start = h.index + h.matchLength;
    const end = idx + 1 < headings.length ? headings[idx + 1].index : body.length;
    const content = body.slice(start, end);
    const enMatch = h.title.match(/\(([^)]+)\)\s*$/);
    sections.push({
      n: h.n,
      titleRaw: h.title,
      titleEn: enMatch ? enMatch[1].trim() : null,
      content,
    });
  }

  const pseudocodeBlocks = [];
  const fenceRe = /```pseudocode\n([\s\S]*?)```/g;
  let fm2;
  while ((fm2 = fenceRe.exec(body)) !== null) {
    pseudocodeBlocks.push(fm2[1]);
  }

  return { frontmatter, sections, pseudocodeBlocks, body };
}

module.exports = { parseChapter, REQUIRED_SECTIONS };
