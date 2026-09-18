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

  if (format === 'pdf') {
    normalizePdfForEmbedding(outPath);
  }

  return outPath;
}

/**
 * `dot -Tpdf` emite PDF 1.7 cuyo grafo de objetos internos crece con el tamaño del diagrama (más
 * nodos/aristas por capítulo, per el mapa mental acumulativo, plan
 * `2026-08-24-mapa-mental-progresivo.md`). A partir de cierto tamaño/complejidad (verificado
 * empíricamente al escribir CH-16: `chapter-16.diagram`, 109 nodos/167 aristas, fue el primero en
 * cruzar ese umbral), el xdvipdfmx instalado en este entorno (TeX Live 2022, invocado por xelatex
 * como "driver") falla al incrustar ese PDF con "Error 11 (driver return code)" — sin ningún error
 * de TeX propiamente dicho, solo al ensamblar el PDF final. Reescribir el PDF con Ghostscript
 * (`pdfwrite`, forzando PDF 1.4) normaliza su estructura interna hacia algo que xdvipdfmx sí puede
 * incrustar sin fallar, verificado con el mismo diagrama que antes rompía el build. Best-effort: si
 * `gs` no está disponible en el entorno, se conserva el PDF que `dot` ya produjo (comportamiento
 * previo) en vez de romper el build por una herramienta opcional ausente — build-pdf seguiría
 * expuesto al mismo umbral en ese caso, pero nunca peor que antes de este cambio.
 */
function normalizePdfForEmbedding(pdfPath) {
  const tmpPath = `${pdfPath}.gsclean.tmp`;
  try {
    execFileSync(
      'gs',
      [
        '-q', '-dNOPAUSE', '-dBATCH', '-dSAFER',
        '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        `-sOutputFile=${tmpPath}`, pdfPath,
      ],
      { stdio: 'inherit' }
    );
    fs.renameSync(tmpPath, pdfPath);
  } catch (e) {
    if (fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
    console.warn(
      `render-diagram: no se pudo normalizar "${pdfPath}" con Ghostscript (${e.message}); ` +
      'se conserva el PDF producido directamente por dot -Tpdf.'
    );
  }
}

module.exports = { renderDiagram };
