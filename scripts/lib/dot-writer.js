'use strict';

/**
 * dot-writer.js — serializa un snapshot { nodes, edges } (ver scripts/lib/mindmap.js) a texto
 * Graphviz DOT válido. Formato de `.diagram` decidido para este plan: Graphviz DOT (ver Paso 2.1
 * del encargo de ejecución) — `dot -Tsvg` / `dot -Tpdf` son el "Diagram Renderer" que exige
 * `reference/md/BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md` §13 ("Diagrams as Source").
 *
 * Diferenciación visual por `kind` (Paso 2.4 del encargo): CONCEPT, COMPONENT, CONTRACT (y la
 * extensión CHAPTER, ver mindmap.js) usan `shape`/`fillcolor` distintos. Los nodos nuevos de ESTE
 * capítulo (pasados en `options.newNodeIds`) se resaltan con `penwidth`/`color` de borde más
 * intensos — solo se usa para los snapshots por capítulo, nunca para `full-book.diagram` (ahí
 * todos los nodos son "ya conocidos").
 *
 * Enlaces "a la definición canónica" (Paso 2.5 del encargo — simplificación documentada): cada
 * nodo lleva un atributo `URL`, que Graphviz traduce a un `<a xlink:href>` real en el SVG, apuntando
 * a `chapters/<ChapterId>.html#<entity-id>` — un anchor nuevo agregado por build-web al inicio del
 * cuerpo de la página del capítulo que introduce esa entidad. No existen páginas de definición
 * dedicadas por entidad (glosario navegable) en este alcance v0.1; el link "canónico" es, por
 * ahora, la sección del capítulo que la introdujo. El nodo CHAPTER enlaza a la página del propio
 * capítulo (sin anchor).
 */

const NODE_STYLE = {
  CHAPTER: { shape: 'folder', fillcolor: '#e2e2e2', extraStyle: 'bold' },
  CONCEPT: { shape: 'ellipse', fillcolor: '#fff3a3' },
  COMPONENT: { shape: 'box', fillcolor: '#bfe0ff', extraStyle: 'rounded' },
  CONTRACT: { shape: 'note', fillcolor: '#c9f2cf' },
};

const EDGE_STYLE = {
  INTRODUCES: { color: '#2a5fa5', style: 'bold' },
  MODIFIES: { color: '#c77c00', style: 'dashed' },
  DEPENDS_ON: { color: '#666666', style: 'solid' },
  PRODUCES: { color: '#2a8f4b', style: 'solid' },
  CONSUMES: { color: '#7a3fa0', style: 'solid' },
};

function escapeDot(s) {
  return String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

/**
 * URL del nodo, relativa a dist/web/ (mismo criterio que usa dist/web/mapa.html — ver Paso 2.5 y
 * el rewrite documentado en build-web para cuando el mismo SVG se incrusta dentro de
 * dist/web/chapters/*.html).
 */
function nodeUrl(node) {
  if (node.kind === 'CHAPTER') return `chapters/${node.id}.html`;
  return `chapters/${node.introducedInChapter}.html#${node.id}`;
}

function writeDot(snapshot, options = {}) {
  const { title, newNodeIds } = options;
  const newSet = new Set(newNodeIds || []);
  const lines = [];

  lines.push('digraph BookMindMap {');
  lines.push('  rankdir=LR;');
  lines.push('  size="6.5,9"; ratio=compress;');
  lines.push('  node [fontname="Helvetica", fontsize=11, style=filled, target="_top"];');
  lines.push('  edge [fontname="Helvetica", fontsize=9];');
  if (title) {
    lines.push(`  labelloc="t"; fontsize=14; fontname="Helvetica-Bold"; label="${escapeDot(title)}";`);
  }

  for (const node of snapshot.nodes) {
    const style = NODE_STYLE[node.kind] || { shape: 'box', fillcolor: '#eeeeee' };
    const attrs = [
      `label="${escapeDot(node.label)}"`,
      `shape=${style.shape}`,
      `fillcolor="${style.fillcolor}"`,
      `URL="${escapeDot(nodeUrl(node))}"`,
    ];
    const styleParts = new Set(['filled']);
    if (style.extraStyle) styleParts.add(style.extraStyle);
    if (newSet.has(node.id)) styleParts.add('bold');
    attrs.push(`style="${Array.from(styleParts).join(',')}"`);
    if (newSet.has(node.id)) {
      attrs.push('penwidth=3');
      attrs.push('color="#d62728"');
    }
    lines.push(`  "${escapeDot(node.id)}" [${attrs.join(', ')}];`);
  }

  for (const edge of snapshot.edges) {
    const style = EDGE_STYLE[edge.kind] || {};
    const attrs = [`label="${escapeDot(edge.kind)}"`];
    if (style.color) attrs.push(`color="${style.color}"`);
    if (style.style) attrs.push(`style="${style.style}"`);
    lines.push(`  "${escapeDot(edge.from)}" -> "${escapeDot(edge.to)}" [${attrs.join(', ')}];`);
  }

  lines.push('}');
  return lines.join('\n') + '\n';
}

module.exports = { writeDot };
