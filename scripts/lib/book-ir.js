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
 *     retrievalSet: RetrievalSet          # NUEVO — plan
 *                                         # 2026-08-23-metodo-aprendizaje-activo-lector.md §3.1
 * END
 *
 * Ver BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md §10. Renderer-independent: build-web y build-pdf
 * consumen exactamente el mismo BookIR (persistido en dist/book-ir.json por build-book-ir) y no
 * tienen permitido derivar contenido semántico por su cuenta.
 *
 * --- Ciclo de Dominio Activo (CDA) — RetrievalSet -------------------------------------------
 *
 * STRUCT RetrievalSet
 *     expectedOutcome: ExpectedOutcome
 *     skeleton: ChapterSkeleton
 *     guidingQuestions: List<GuidingQuestion>
 *     systemsLens: SystemsLensBlock
 *     recallQuestions: List<RecallQuestion>
 *     explainPrompts: List<ExplainPrompt>
 *     interleavedQuestions: List<InterleavedQuestion>
 *     flashcards: List<Flashcard>
 *     calibrationPairs: List<CalibrationPair>
 *     interleavingException: Optional<Text>   # extensión de esta implementación (no está en
 *                                              # §3.1 del plan): documenta por qué un capítulo
 *                                              # sin capítulo anterior (p.ej. CH-00) no produce
 *                                              # interleavedQuestions, en vez de inventar un
 *                                              # capítulo previo falso. Ver Registro de ejecución.
 * END
 *
 * STRUCT ExpectedOutcome { id, text }
 * STRUCT ChapterSkeleton { id, sectionTitles: List<Text>, componentsToBeIntroduced: List<ComponentId>,
 *                          contractsToBeIntroduced: List<ContractId> }
 * STRUCT GuidingQuestion { id, text, answeredBy: RecallQuestionId }
 * STRUCT SystemsLensBlock { icebergVisibleFact, icebergPatterns, icebergStructures,
 *                           icebergMentalModels, reinforcingLoop: Optional<Text>,
 *                           balancingLoop: Optional<Text>, leveragePoint }
 * STRUCT RecallQuestion { id, text }                     # no especificado campo a campo en el
 *                                                          # plan §3.1; diseño de esta ejecución.
 * STRUCT ExplainPrompt { id, text, targetEntity: ContractId | ComponentId | Text }
 *                                                          # targetEntity acepta Text libre para
 *                                                          # cubrir límites constitucionales
 *                                                          # (Article XII) cuando el capítulo aún
 *                                                          # no introduce ningún componente con
 *                                                          # "Owns"/"Does NOT own" — caso de CH-00.
 * STRUCT InterleavedQuestion { id, text, currentChapterEntities: List<Id>,
 *                              priorChapterEntities: List<Id>, priorChapter: ChapterId }
 * STRUCT Flashcard { id, front, back, sourceEntity: ContractId | ComponentId,
 *                    chapterIntroducedIn: ChapterId, reviewStage: ReviewStage }
 * STRUCT CalibrationPair { id, recallQuestion: RecallQuestionId, confidenceLevels: List<Text> }
 * ENUM ReviewStage { DAY_1, DAY_3, DAY_7, DAY_21, MASTERED }
 *
 * Fuente de los datos: bloque `retrieval_set:` en el frontmatter YAML del capítulo (parseado por
 * yaml-lite.js igual que el resto del frontmatter) — mismo principio que contracts/components:
 * el frontmatter/registry es la fuente estructurada; la prosa del capítulo (secciones 0/20/21)
 * es la presentación legible de esos mismos datos, escrita para coincidir, no derivada
 * automáticamente. `scripts/validate-retrieval-set` valida la fuente estructurada.
 */

function normalizeRetrievalSet(rs) {
  rs = rs || {};
  const eo = rs.expected_outcome || {};
  const sk = rs.skeleton || {};
  const sl = rs.systems_lens || {};

  const trim = (s) => (typeof s === 'string' ? s.trim() : s);

  return {
    expectedOutcome: {
      id: eo.id || null,
      text: trim(eo.text) || '',
    },
    skeleton: {
      id: sk.id || null,
      sectionTitles: sk.section_titles || [],
      componentsToBeIntroduced: sk.components_to_be_introduced || [],
      contractsToBeIntroduced: sk.contracts_to_be_introduced || [],
    },
    guidingQuestions: (rs.guiding_questions || []).map((q) => ({
      id: q.id,
      text: trim(q.text) || '',
      answeredBy: q.answered_by || null,
    })),
    systemsLens: {
      icebergVisibleFact: trim(sl.iceberg_visible_fact) || '',
      icebergPatterns: trim(sl.iceberg_patterns) || '',
      icebergStructures: trim(sl.iceberg_structures) || '',
      icebergMentalModels: trim(sl.iceberg_mental_models) || '',
      reinforcingLoop: sl.reinforcing_loop ? trim(sl.reinforcing_loop) : null,
      balancingLoop: sl.balancing_loop ? trim(sl.balancing_loop) : null,
      leveragePoint: trim(sl.leverage_point) || '',
    },
    recallQuestions: (rs.recall_questions || []).map((q) => ({
      id: q.id,
      text: trim(q.text) || '',
    })),
    explainPrompts: (rs.explain_prompts || []).map((p) => ({
      id: p.id,
      text: trim(p.text) || '',
      targetEntity: p.target_entity || null,
    })),
    interleavedQuestions: (rs.interleaved_questions || []).map((q) => ({
      id: q.id,
      text: trim(q.text) || '',
      currentChapterEntities: q.current_chapter_entities || [],
      priorChapterEntities: q.prior_chapter_entities || [],
      priorChapter: q.prior_chapter || null,
    })),
    flashcards: (rs.flashcards || []).map((f) => ({
      id: f.id,
      front: trim(f.front) || '',
      back: trim(f.back) || '',
      sourceEntity: f.source_entity,
      chapterIntroducedIn: f.chapter_introduced_in,
      reviewStage: f.review_stage || 'DAY_1',
    })),
    calibrationPairs: (rs.calibration_pairs || []).map((p) => ({
      id: p.id,
      recallQuestion: p.recall_question,
      confidenceLevels: p.confidence_levels || ['Alta', 'Media', 'Baja'],
    })),
    interleavingException: rs.interleaving_exception ? trim(rs.interleaving_exception) : null,
  };
}

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
    retrievalSet: normalizeRetrievalSet(fm.retrieval_set),
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

module.exports = { buildBookIR, normalizeRetrievalSet };
