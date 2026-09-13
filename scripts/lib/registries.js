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
  loadConstitutionArticleIds,
};
