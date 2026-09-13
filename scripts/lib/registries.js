'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('./yaml-lite.js');

const ROOT = path.resolve(__dirname, '..', '..');

function readYaml(relPath) {
  const full = path.join(ROOT, relPath);
  return yaml.parse(fs.readFileSync(full, 'utf8'));
}

function loadBook() {
  const data = readYaml('book/book.yaml');
  const chapters = data.chapters || [];
  const order = chapters.map((c) => c.id);
  return { book: data.book, chapters, order };
}

function chapterIndex(order, chapterId) {
  return order.indexOf(chapterId);
}

function loadContracts() {
  const data = readYaml('registry/contracts.yaml');
  return data.contracts || [];
}

function loadComponents() {
  const data = readYaml('registry/components.yaml');
  return data.components || [];
}

function loadGlossary() {
  const data = readYaml('registry/glossary.yaml');
  return data.terms || [];
}

/**
 * Carga book/frontmatter/*.md — Prefacio e Introducción, en el orden editorial fijo (preface
 * antes que introduction). Son páginas de texto libre, sin frontmatter YAML propio (a diferencia
 * de book/chapters/*.md): no pasan por validate-chapter ni entran a los registries, así que se
 * modela cada una simplemente como { id, title, body } — id = nombre de archivo sin extensión,
 * title = primer encabezado `# ...`, body = el resto del Markdown.
 *
 * Se listan explícitamente (no se hace glob de la carpeta) para que el orden editorial sea una
 * decisión declarada, no un accidente del orden alfabético del filesystem.
 */
const FRONTMATTER_ORDER = ['preface.md', 'introduction.md'];

function loadFrontmatter() {
  const dir = path.join(ROOT, 'book', 'frontmatter');
  const pages = [];
  for (const file of FRONTMATTER_ORDER) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) continue; // opcional: no todo libro tiene los 2 documentos
    const raw = fs.readFileSync(full, 'utf8');
    const m = raw.match(/^#\s+(.+?)\s*\n([\s\S]*)$/);
    const id = path.basename(file, '.md');
    pages.push({
      id,
      title: m ? m[1].trim() : id,
      body: (m ? m[2] : raw).trim(),
    });
  }
  return pages;
}

/**
 * Extrae los ids de artículos constitucionales realmente definidos en
 * constitution/ARCHITECTURE_CONSTITUTION.md (P-01..P-30, INV-01..INV-20, INV-E01..INV-E14),
 * para que analyze-constitutional-impact / validate-chapter puedan rechazar referencias a
 * artículos inventados.
 */
function loadConstitutionArticleIds() {
  const full = path.join(ROOT, 'constitution', 'ARCHITECTURE_CONSTITUTION.md');
  const text = fs.readFileSync(full, 'utf8');
  const ids = new Set();
  const re = /\b(P-\d{2}|INV-E\d{2}|INV-\d{2})\b/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    ids.add(m[1]);
  }
  return ids;
}

module.exports = {
  ROOT,
  readYaml,
  loadBook,
  chapterIndex,
  loadContracts,
  loadComponents,
  loadGlossary,
  loadFrontmatter,
  loadConstitutionArticleIds,
};
