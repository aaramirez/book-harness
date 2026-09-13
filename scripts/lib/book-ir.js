'use strict';

const fs = require('fs');
const path = require('path');
const reg = require('./registries.js');
const { parseChapter } = require('./chapter-parser.js');

/**
 * STRUCT BookIR
 *     metadata: BookMetadata
 *     chapters: List<ChapterIR>
 *     glossary: Glossary
 *     contracts: ContractRegistry
 *     components: ComponentRegistry
 * END
 *
 * STRUCT ChapterIR
 *     id: ChapterId
 *     sections: List<Section>
 *     diagrams: List<Diagram>
 *     codeBlocks: List<PseudocodeBlock>
 *     references: List<Reference>
 *     contractsIntroduced: List<ContractId>
 *     componentsIntroduced: List<ComponentId>
 * END
 *
 * Ver BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md §10. Renderer-independent: build-web y build-pdf
 * consumen exactamente el mismo BookIR (persistido en dist/book-ir.json por build-book-ir) y no
 * tienen permitido derivar contenido semántico por su cuenta.
 */

function extractDiagrams(body) {
  const diagrams = [];
  const fenceRe = /```(?:text)?\n([\s\S]*?)```/g;
  let m;
  while ((m = fenceRe.exec(body)) !== null) {
    // Ignorar bloques ```pseudocode (ya se capturan aparte como codeBlocks)
    const fullMatch = m[0];
    if (fullMatch.startsWith('```pseudocode')) continue;
    diagrams.push(m[1].trimEnd());
  }
  return diagrams;
}

function buildChapterIR(chapterEntry) {
  const full = path.join(reg.ROOT, 'book', chapterEntry.file);
  const raw = fs.readFileSync(full, 'utf8');
  const parsed = parseChapter(raw);
  const { frontmatter: fm, sections, pseudocodeBlocks, body } = parsed;

  return {
    id: fm.id,
    title: fm.title,
    startingVersion: fm.starting_version,
    endingVersion: fm.ending_version,
    previousChapter: fm.previous_chapter || null,
    nextChapter: fm.next_chapter || null,
    sections: sections.map((s) => ({
      n: s.n,
      title: s.titleRaw,
      titleEn: s.titleEn,
      content: s.content.trim(),
    })),
    diagrams: extractDiagrams(body),
    codeBlocks: pseudocodeBlocks.map((b) => b.trim()),
    references: [],
    contractsIntroduced: fm.introduces_contracts || [],
    componentsIntroduced: fm.introduces_components || [],
  };
}

function buildBookIR() {
  const { book, chapters } = reg.loadBook();
  const contracts = reg.loadContracts();
  const components = reg.loadComponents();
  const glossary = reg.loadGlossary();

  return {
    metadata: {
      id: book.id,
      version: book.version,
      title: book.title,
      language: book.language,
    },
    chapters: chapters.map(buildChapterIR),
    glossary,
    contracts,
    components,
  };
}

module.exports = { buildBookIR };
