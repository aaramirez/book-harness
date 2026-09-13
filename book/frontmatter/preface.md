# Prefacio

Este libro no es una colección de recetas para escribir prompts. Es una guía para construir un
**arnés de agentes** (*Agent Harness*): el runtime determinístico que permite que un modelo de
lenguaje proponga acciones con seguridad, límites explícitos, trazabilidad y evolución
arquitectónica controlada.

La regla que gobierna cada página de este libro es la misma que gobierna su propia producción:

> Los sistemas probabilísticos pueden proponer decisiones. Los sistemas determinísticos deben
> gobernar sus consecuencias.

Este libro mismo fue escrito por un **Book Production Harness** — un sistema editorial gobernado,
no un generador de texto genérico — que aplica sobre sí mismo la misma disciplina que enseña:
registries de contratos y componentes, validadores deterministas que fallan ante errores
estructurales, y una fuente canónica única de la que derivan, sin divergir, la edición Web y la
edición PDF.

Este documento y su arquitectura de producción viven en el repositorio `book-harness`, bajo
`constitution/`, `book/`, `registry/`, `agents/`, `skills/`, `policies/` y `scripts/`.
