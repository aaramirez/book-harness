'use strict';

const fs = require('fs');
const path = require('path');
const reg = require('./registries.js');
const { parseChapter } = require('./chapter-parser.js');

/**
 * mindmap.js — lógica PURA (no toca disco salvo para leer las fuentes ya existentes) que calcula
 * los snapshots acumulativos del `BookMindMap` definido en
 * `planes/2026-08-24-mapa-mental-progresivo.md` §3.
 *
 * STRUCT MindMapNode { id, kind, label, introducedInChapter }
 * ENUM NodeKind { CONCEPT, COMPONENT, CONTRACT, CHAPTER }
 *     ^ CHAPTER es una EXTENSIÓN de esta implementación sobre el enum del plan (que solo lista
 *       CONCEPT/COMPONENT/CONTRACT): el propio plan define EdgeKind.INTRODUCES/MODIFIES como
 *       "capítulo → entidad", lo cual exige que el capítulo exista como nodo del grafo (Graphviz
 *       necesita un nodo origen real). Se documenta como decisión de diseño en el Registro de
 *       ejecución del plan §9.
 * STRUCT MindMapEdge { from, to, kind }
 * ENUM EdgeKind { DEPENDS_ON, PRODUCES, CONSUMES, INTRODUCES, MODIFIES }
 *
 * Origen determinista de cada snapshot (plan §3.2):
 *   Glossary (kind: concept)      → nodos CONCEPT   (kind: contract/component del glosario NO
 *                                                      generan nodo propio: ya están representados
 *                                                      por su registry — evita duplicar la entidad)
 *   Component Registry            → nodos COMPONENT
 *   Contract Registry             → nodos CONTRACT
 *   component.dependencies        → aristas DEPENDS_ON  (component -> component)
 *   component.produces            → aristas PRODUCES    (component -> contract)
 *   component.consumes            → aristas CONSUMES    (contract -> component; el contrato
 *                                                         "fluye hacia" quien lo consume)
 *   fm.introduces_contracts/       → aristas INTRODUCES  (chapter -> entidad)
 *   fm.introduces_components/
 *   glossary concept introducido
 *   fm.modifies_contracts          → aristas MODIFIES    (chapter -> entidad YA existente)
 *
 * "No magic entities" aplicado al grafo (plan §4): un componente/capítulo NUNCA puede introducir
 * una arista hacia un nodo que no exista todavía en el snapshot acumulado — si eso ocurre, se
 * lanza una excepción (el CLI `build-mind-map` la convierte en `exit 1`).
 */

function slugify(text) {
  return String(text)
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // quitar diacríticos (acentos) tras normalize('NFD')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * Sintetiza un id estable para un término de glosario (kind: concept), que no tiene id propio en
 * registry/glossary.yaml (solo `term`) — decisión §"IDs de nodo" del plan (Paso 2.3 del encargo):
 * "CONCEPT-<slug-del-término>", p.ej. "Architecture Constitution" → "CONCEPT-architecture-constitution".
 */
function conceptNodeId(term) {
  return `CONCEPT-${slugify(term)}`;
}

function loadChapterFrontmatter(chapterEntry) {
  const full = path.join(reg.ROOT, 'book', chapterEntry.file);
  const raw = fs.readFileSync(full, 'utf8');
  return parseChapter(raw).frontmatter;
}

function buildMindMapSnapshots() {
  const { chapters } = reg.loadBook();
  const contracts = reg.loadContracts();
  const components = reg.loadComponents();
  const glossary = reg.loadGlossary();

  const contractsById = new Map(contracts.map((c) => [c.id, c]));
  const componentsById = new Map(components.map((c) => [c.id, c]));

  const conceptsByChapter = new Map(); // chapterId -> [{id,label}]
  for (const term of glossary) {
    if (term.kind !== 'concept') continue; // ver nota arriba: solo "concept" genera nodo propio
    const list = conceptsByChapter.get(term.introduced_in) || [];
    list.push({ id: conceptNodeId(term.term), label: term.term });
    conceptsByChapter.set(term.introduced_in, list);
  }

  const componentsByChapter = new Map();
  for (const c of components) {
    const list = componentsByChapter.get(c.introduced_in) || [];
    list.push(c);
    componentsByChapter.set(c.introduced_in, list);
  }

  const nodesMap = new Map(); // acumulado a través de todos los capítulos procesados hasta ahora
  const edgesAcc = []; // acumulado igual que nodesMap
  const chapterSnapshots = [];

  function addNode(node) {
    if (!nodesMap.has(node.id)) nodesMap.set(node.id, node);
    return nodesMap.get(node.id);
  }

  chapters.forEach((entry, chapterIndex) => {
    const fm = loadChapterFrontmatter(entry);
    const chapterId = fm.id;
    const newNodeIds = [];

    // Nodo CHAPTER (extensión de esta implementación, ver comentario de cabecera)
    addNode({ id: chapterId, kind: 'CHAPTER', label: fm.title, introducedInChapter: chapterId });
    newNodeIds.push(chapterId);

    for (const cid of fm.introduces_contracts || []) {
      const c = contractsById.get(cid);
      if (!c) {
        throw new Error(
          `capítulo "${chapterId}" declara introduces_contracts "${cid}", que no existe en ` +
          'registry/contracts.yaml — no magic entities'
        );
      }
      addNode({ id: c.id, kind: 'CONTRACT', label: c.name, introducedInChapter: chapterId });
      newNodeIds.push(c.id);
      edgesAcc.push({ from: chapterId, to: c.id, kind: 'INTRODUCES' });
    }

    for (const cid of fm.introduces_components || []) {
      const c = componentsById.get(cid);
      if (!c) {
        throw new Error(
          `capítulo "${chapterId}" declara introduces_components "${cid}", que no existe en ` +
          'registry/components.yaml — no magic entities'
        );
      }
      addNode({ id: c.id, kind: 'COMPONENT', label: c.name, introducedInChapter: chapterId });
      newNodeIds.push(c.id);
      edgesAcc.push({ from: chapterId, to: c.id, kind: 'INTRODUCES' });
    }

    for (const concept of conceptsByChapter.get(chapterId) || []) {
      addNode({ id: concept.id, kind: 'CONCEPT', label: concept.label, introducedInChapter: chapterId });
      newNodeIds.push(concept.id);
      edgesAcc.push({ from: chapterId, to: concept.id, kind: 'INTRODUCES' });
    }

    for (const cid of fm.modifies_contracts || []) {
      if (!nodesMap.has(cid)) {
        throw new Error(
          `capítulo "${chapterId}" declara modifies_contracts "${cid}", que todavía no existe en ` +
          'el mapa mental acumulado — no magic entities'
        );
      }
      edgesAcc.push({ from: chapterId, to: cid, kind: 'MODIFIES' });
    }

    // DEPENDS_ON / PRODUCES / CONSUMES: derivados de la ficha completa del componente en el
    // MISMO capítulo en que se introduce (su ficha arquitectónica ya está completa al introducirse).
    for (const c of componentsByChapter.get(chapterId) || []) {
      for (const dep of c.dependencies || []) {
        if (!nodesMap.has(dep)) {
          throw new Error(
            `componente "${c.id}" (capítulo "${chapterId}") declara dependencies -> "${dep}", que ` +
            'no existe todavía en el mapa mental acumulado — no magic entities'
          );
        }
        edgesAcc.push({ from: c.id, to: dep, kind: 'DEPENDS_ON' });
      }
      for (const ref of c.produces || []) {
        if (!nodesMap.has(ref)) {
          throw new Error(
            `componente "${c.id}" (capítulo "${chapterId}") declara produces -> "${ref}", que no ` +
            'existe todavía en el mapa mental acumulado — no magic entities'
          );
        }
        edgesAcc.push({ from: c.id, to: ref, kind: 'PRODUCES' });
      }
      for (const ref of c.consumes || []) {
        if (!nodesMap.has(ref)) {
          throw new Error(
            `componente "${c.id}" (capítulo "${chapterId}") declara consumes -> "${ref}", que no ` +
            'existe todavía en el mapa mental acumulado — no magic entities'
          );
        }
        edgesAcc.push({ from: ref, to: c.id, kind: 'CONSUMES' });
      }
    }

    chapterSnapshots.push({
      chapterIndex,
      chapterId,
      nodes: Array.from(nodesMap.values()).map((n) => ({ ...n })),
      edges: edgesAcc.map((e) => ({ ...e })),
      newNodeIds, // extensión de esta implementación: ids de nodos nuevos EN ESTE capítulo, para
                  // que dot-writer.js pueda resaltarlos visualmente distinto (plan §5)
    });
  });

  const lastSnapshot = chapterSnapshots[chapterSnapshots.length - 1];
  const fullBook = lastSnapshot
    ? { nodes: lastSnapshot.nodes, edges: lastSnapshot.edges }
    : { nodes: [], edges: [] };

  return { chapterSnapshots, fullBook };
}

module.exports = { buildMindMapSnapshots, slugify, conceptNodeId };
