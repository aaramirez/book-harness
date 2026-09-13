'use strict';

const reg = require('./registries.js');
const { parseChapter } = require('./chapter-parser.js');
const fs = require('fs');
const path = require('path');

/**
 * STRUCT BookState (BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md §5), explícito para BH-v0.1.
 *
 * A diferencia de BookIR (book-ir.js), que es renderer-independent y solo lleva lo que Web/PDF
 * necesitan mostrar, BookState es el modelo de autoría/gobierno: qué capítulo introdujo o
 * modificó qué, y en qué estado de validación quedó el último build.
 *
 * STRUCT BookState
 *     bookVersion: Version
 *     chapters: List<ChapterState>
 *     contracts: ContractRegistry
 *     components: ComponentRegistry
 *     adrs: ADRRegistry
 *     glossary: Glossary
 *     dependencies: ArchitectureDependencyGraph
 *     buildStatus: BuildStatus
 * END
 *
 * STRUCT ChapterState
 *     chapterId: ChapterId
 *     title: Text
 *     status: ChapterStatus
 *     introducesComponents: List<ComponentId>
 *     introducesContracts: List<ContractId>
 *     modifiesComponents: List<ComponentId>
 *     modifiesContracts: List<ContractId>
 *     constitutionalArticles: List<ArticleId>
 *     previousChapter: Optional<ChapterId>
 *     nextChapter: Optional<ChapterId>
 * END
 *
 * `dependencies` (ArchitectureDependencyGraph automático) es deuda intencional hacia BH-v0.3
 * (ver plan de ejecución §7 / roadmap §9) — se declara explícitamente aquí como `null` en vez de
 * omitirse, para que quede claro que el campo existe en el modelo pero su cómputo automático
 * todavía no está implementado.
 */
function loadBookState(buildStatus) {
  const { book, chapters } = reg.loadBook();
  const contracts = reg.loadContracts();
  const components = reg.loadComponents();
  const glossary = reg.loadGlossary();

  const chapterStates = chapters.map((chapterEntry) => {
    const full = path.join(reg.ROOT, 'book', chapterEntry.file);
    const raw = fs.readFileSync(full, 'utf8');
    const { frontmatter: fm } = parseChapter(raw);
    return {
      chapterId: fm.id,
      title: fm.title,
      status: buildStatus === 'built' ? 'validated' : 'pending_validation',
      introducesComponents: fm.introduces_components || [],
      introducesContracts: fm.introduces_contracts || [],
      modifiesComponents: [],
      modifiesContracts: fm.modifies_contracts || [],
      constitutionalArticles: fm.constitutional_articles || [],
      previousChapter: fm.previous_chapter || null,
      nextChapter: fm.next_chapter || null,
    };
  });

  return {
    bookVersion: book.version,
    chapters: chapterStates,
    contracts,
    components,
    adrs: [], // ADRRegistry: vacío en BH-v0.1, ver docs/adr/ (deuda intencional hacia BH-v0.2+)
    glossary,
    dependencies: null, // ArchitectureDependencyGraph automático: deuda intencional (BH-v0.3)
    buildStatus,
  };
}

module.exports = { loadBookState };
