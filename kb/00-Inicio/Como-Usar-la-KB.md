---
id: como-usar-kb
tipo: guia
tags: [guia, inicio]
---

# Cómo usar esta KB

Esta es una **Knowledge Base de Obsidian** sobre el libro *¿Cómo construir un arnés?* y el repositorio `book-harness` que lo produce.

## Flujo recomendado

1. **Empieza por el mapa**: [[Index|Index]] es el punto de entrada.
2. **Cimientos primero**: lee [[Architecture-Constitution|la Constitución]] (regla suprema, Artículos I-XII, Enmienda v1.1).
3. **Sigue el libro en orden**: cada capítulo tiene su nota con el resultado esperado y navegación ⬅ ➡ entre capítulos.
4. **Aterriza en contratos y componentes**: cada capítulo introduce contratos (C-XXX) y componentes (CMP-XXX) — navega desde la [[04-Capitulos/00-Índice|índice de capítulos]].
5. **Consulta el vocabulario**: [[05-Glosario/Glosario|Glosario]] con los 134 términos canónicos.

## Convenciones de la KB

| Elemento | Convención |
|----------|-----------|
| Notas de componente | `CMP-XXX-nombre.md` con secciones *responsabilidad / owns / does_not_own / contratos* |
| Notas de contrato | `C-XXX-nombre.md` con *definición canónica* (STRUCT/ENUM) |
| Notas de capítulo | `ch-NN-slug.md` con *resultado esperado* y *qué introduce* |
| Frontmatter | `id`, `tipo`, tags, enlaces a capítulo/contratos/componentes |
| Plantillas | [[Templates/00-Índice|Templates]] para crear notas nuevas |

## Fuentes (en el repo `book-harness`)

| Fuente | Ruta |
|--------|------|
| Constitución | `constitution/ARCHITECTURE_CONSTITUTION.md` |
| Registro de componentes | `registry/components.yaml` |
| Registro de contratos | `registry/contracts.yaml` |
| Registro de glosario | `registry/glossary.yaml` |
| Registro de deuda | `registry/debt.yaml` |
| Manifiesto del libro | `book/book.yaml` |
| Capítulos | `book/chapters/*/chapter.md` |
| Planes de ejecución | `planes/*.md` |
