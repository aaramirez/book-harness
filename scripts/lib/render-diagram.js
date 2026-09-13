'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

/**
 * render-diagram.js — helper compartido (decisión §"Un helper compartido" del plan) que invoca el
 * binario `dot` (Graphviz, confirmado instalado: v12.2.1 en /usr/local/bin) para convertir un
 * archivo `.diagram` (texto DOT) a SVG (Web) o PDF (libro PDF). Usado tanto por `build-web` como
 * por `build-pdf`, para no duplicar la llamada a `dot` en dos scripts distintos.
 *
 * Los `.diagram` en `diagrams/mindmap/` son FUENTE (se comitean). Los `.svg`/`.pdf` que produce
 * esta función son artefactos de build (van a `dist/`, ya gitignorado) — nunca se escriben junto
 * a la fuente.
 */
function renderDiagram(diagramPath, outPath, format) {
  if (format !== 'svg' && format !== 'pdf') {
    throw new Error(`render-diagram: formato no soportado "${format}" (usar "svg" o "pdf")`);
  }
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  execFileSync('dot', [`-T${format}`, diagramPath, '-o', outPath], { stdio: 'inherit' });
  return outPath;
}

module.exports = { renderDiagram };
