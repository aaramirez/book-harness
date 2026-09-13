'use strict';

/**
 * yaml-lite.js
 *
 * Parser YAML de un SUBCONJUNTO deliberadamente mínimo, escrito a mano sin dependencias de npm
 * (decisión de runtime, ver scripts/README.md). Soporta exactamente lo que usan los registries y
 * el frontmatter de capítulos de este repositorio:
 *
 *   - mappings anidados por indentación ("key: value")
 *   - secuencias ("- item" / "- key: value")
 *   - listas en línea ("[a, b, c]", "[]")
 *   - escalares con o sin comillas simples/dobles, enteros, booleanos, null
 *   - block scalars literales ("|") y plegados (">")
 *   - comentarios de línea completa ("# ...") y líneas en blanco (ignoradas)
 *
 * NO soporta: anchors/aliases, tags, multi-documento, claves complejas, flow maps ("{a: 1}"),
 * ni tabs como indentación. Si algo de esto aparece en un archivo de este repo, es un error de
 * autoría, no una limitación a "arreglar" silenciosamente.
 */

function tokenize(text) {
  const rawLines = text.replace(/\r\n/g, '\n').split('\n');
  const tokens = [];
  for (const raw of rawLines) {
    if (raw.trim() === '') continue;
    if (raw.trim().startsWith('#')) continue;
    if (raw.includes('\t')) {
      throw new Error('yaml-lite: tabs no soportados como indentación: ' + JSON.stringify(raw));
    }
    const indent = raw.length - raw.trimStart().length;
    tokens.push({ indent, text: raw.trim(), raw });
  }
  return tokens;
}

function stripQuotes(s) {
  if (s.length >= 2) {
    if (s[0] === '"' && s[s.length - 1] === '"') return s.slice(1, -1);
    if (s[0] === "'" && s[s.length - 1] === "'") return s.slice(1, -1);
  }
  return s;
}

function parseFlowList(s) {
  const inner = s.slice(1, -1).trim();
  if (inner === '') return [];
  return inner.split(',').map((part) => parseScalar(part.trim()));
}

function parseScalar(s) {
  if (s === '' ) return null;
  if (s === '[]') return [];
  if (s[0] === '[' && s[s.length - 1] === ']') return parseFlowList(s);
  if (s === 'null' || s === '~') return null;
  if (s === 'true') return true;
  if (s === 'false') return false;
  if (/^-?\d+$/.test(s)) return parseInt(s, 10);
  if (/^-?\d+\.\d+$/.test(s)) return parseFloat(s);
  return stripQuotes(s);
}

function splitKeyValue(line) {
  // busca el primer ": " (key: value) o un ':' final (key:  con valor vacío)
  let idx = line.indexOf(': ');
  if (idx === -1) {
    if (line.endsWith(':')) {
      idx = line.length - 1;
    } else {
      throw new Error('yaml-lite: línea de mapping inválida (falta ": "): ' + JSON.stringify(line));
    }
  }
  const key = line.slice(0, idx).trim();
  const value = line.slice(idx + 1).trim();
  return { key, value };
}

function looksLikeMapLine(text) {
  return /^[A-Za-z0-9_.-]+:(\s|$)/.test(text);
}

class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.i = 0;
  }

  peek() {
    return this.tokens[this.i];
  }

  parseBlockScalar(indicator, keyIndent) {
    const lines = [];
    let baseIndent = null;
    while (this.i < this.tokens.length && this.tokens[this.i].indent > keyIndent) {
      const tok = this.tokens[this.i];
      if (baseIndent === null) baseIndent = tok.indent;
      const relative = tok.indent - baseIndent;
      lines.push(' '.repeat(Math.max(relative, 0)) + tok.text);
      this.i++;
    }
    if (indicator[0] === '|') {
      return lines.join('\n');
    }
    // ">" folded: unir con espacios, colapsar
    return lines.join(' ').trim();
  }

  // Parsea el nodo (map o sequence) que empieza en la posición actual, a un indent dado.
  parseNodeAt(indent) {
    const tok = this.peek();
    if (!tok || tok.indent !== indent) {
      throw new Error('yaml-lite: indentación inesperada en ' + JSON.stringify(tok));
    }
    if (tok.text.startsWith('- ') || tok.text === '-') {
      return this.parseSequence(indent);
    }
    return this.parseMapping(indent);
  }

  parseSequence(indent) {
    const result = [];
    while (this.i < this.tokens.length) {
      const tok = this.tokens[this.i];
      if (tok.indent !== indent) break;
      if (!(tok.text.startsWith('- ') || tok.text === '-')) break;
      const rest = tok.text === '-' ? '' : tok.text.slice(2).trim();
      this.i++;
      if (rest === '') {
        const next = this.peek();
        if (next && next.indent > indent) {
          result.push(this.parseNodeAt(next.indent));
        } else {
          result.push(null);
        }
      } else if (looksLikeMapLine(rest)) {
        result.push(this.parseMapping(indent + 2, rest));
      } else {
        result.push(parseScalar(rest));
      }
    }
    return result;
  }

  // Parsea un mapping cuyas claves están a `indent`. Si `firstLine` viene dado (caso
  // "- key: value"), se procesa como la primera clave sin consumir un token nuevo para ella.
  parseMapping(indent, firstLine) {
    const result = {};

    const consumeKeyLine = (lineText) => {
      const { key, value } = splitKeyValue(lineText);
      if (value === '') {
        const next = this.peek();
        if (next && next.indent > indent) {
          result[key] = this.parseNodeAt(next.indent);
        } else {
          result[key] = null;
        }
      } else if (value === '|' || value === '>' || value === '|-' || value === '>-') {
        result[key] = this.parseBlockScalar(value, indent);
      } else {
        result[key] = parseScalar(value);
      }
    };

    if (firstLine !== undefined) {
      consumeKeyLine(firstLine);
    }

    while (this.i < this.tokens.length) {
      const tok = this.tokens[this.i];
      if (tok.indent !== indent) break;
      if (tok.text.startsWith('- ') || tok.text === '-') break;
      this.i++;
      consumeKeyLine(tok.text);
    }

    return result;
  }
}

function parse(text) {
  const tokens = tokenize(text);
  if (tokens.length === 0) return {};
  const parser = new Parser(tokens);
  return parser.parseNodeAt(tokens[0].indent);
}

module.exports = { parse };
