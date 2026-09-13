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

## Cómo leer este libro

Leer un capítulo entero no es lo mismo que aprenderlo. Este libro está construido para el
**Ciclo de Dominio Activo** (CDA): cada capítulo abre con una Sección 0 ("Preguntas Guía") que
fija qué vas a poder *hacer* al terminar — no solo qué vas a leer — y cierra con una Sección 21
("Practica lo que aprendiste") que te obliga a recordar, explicar en voz alta, conectar con
capítulos anteriores y espaciar el repaso en el tiempo, antes de pasar al siguiente.

Para que ese ciclo funcione, léelo así:

- **Rendimiento profundo.** Reserva un bloque de **~90 minutos sin distracciones** por
  capítulo — inspirado en los *Think Weeks* de Bill Gates. El foco durante ese bloque importa
  más que las horas acumuladas: es mejor un bloque intenso de 90 minutos que tres horas
  distraídas.
- **Antes de leer** (Sección 0): fija el resultado esperado y mira el esqueleto del capítulo
  antes de leer el detalle — el 20% esencial primero.
- **Durante la lectura**: al llegar a la Sección 20 ("Lente de Sistemas"), detente y relee la
  arquitectura recién enseñada bajo el marco Iceberg / Bucles de retroalimentación / Punto de
  apalancamiento (Dinámica de Sistemas, Forrester/Meadows) — no es contenido nuevo, es una
  relectura con otra lente.
- **Después de leer** (Sección 21): cierra el libro y responde de memoria antes de mirar atrás.
  Repasa las tarjetas de cada capítulo al día 1, al día 3, al día 7 y al día 21 (curva del
  olvido de Ebbinghaus) — no las dejes para "después", el olvido no espera.

Este método (ver `planes/2026-08-23-metodo-aprendizaje-activo-lector.md` para las fuentes
completas y el modelo de datos) se aplica, en esta primera versión (BH-v0.1), como bloques
estáticos de lectura — la vista `/repaso` interactiva con calendario de repaso persistido por
lector queda para una versión posterior del harness.
