---
id: architecture-constitution
tipo: moc
tags: [constitucion, moc]
---

# Architecture Constitution (v1.0 + Enmienda v1.1)

> Documento rector del arnés. Define los **principios (P-xx)**, **invariantes (INV-xx)** y **fronteras de titularidad** que gobiernan el diseño, implementación, evolución y operación del harness.
>
> **Regla suprema:** *Probabilistic systems may propose decisions. Deterministic systems must govern consequences.*
>
> Fuente: `constitution/ARCHITECTURE_CONSTITUTION.md`

## Principio rector

```text
Probabilistic Intelligence  →  propone  →  Deterministic Runtime  →  gobierna  →  External World
```

El **modelo** decide *qué intentar*. El **harness** decide *qué puede ocurrir, cómo, bajo qué límites y con qué trazabilidad*.

## Artículos

| Artículo | Tema | Contenido |
|----------|------|-----------|
| [[Article-I-Principios|I]] | Principios fundamentales | P-01..P-15 |
| [[Article-II-Invariantes|II]] | Invariantes | INV-01..INV-20 |
| [[Article-III-Soberania|III]] | Soberanía de componentes | 11 componentes del runtime |
| [[Article-IV-Decision-Ownership|IV]] | Titularidad de decisiones | quién decide qué |
| [[Article-V-Lifecycle|V]] | Ciclo de vida | estados de un AgentRun |
| [[Article-VI-Execution|VI]] | Ejecución | reglas de ejecución |
| [[Article-VII-Failure|VII]] | Semántica de fallos | categorías de fallo |
| [[Article-VIII-Human-Interaction|VIII]] | Interacción humana | aprobaciones y reanudación |
| [[Article-IX-Resources|IX]] | Recursos y presupuestos | ExecutionBudget |
| [[Article-X-Observability|X]] | Observabilidad | eventos, logs, traces |
| [[Article-XI-Evolution|XI]] | Evolución | EVO-01..EVO-10 |
| [[Article-XII-Boundary|XII]] | Frontera determinística vs. agéntica | decisión suprema |
| [[Amendment-v11|Enmienda v1.1]] | Enterprise | P-16..P-30 · INV-E01..INV-E14 · 8 planes |
| [[Amendment-v12|Enmienda v1.2]] | Durabilidad, identidad, conectividad y autoría | P-31..P-39 · INV-E15..INV-E27 |

## Cómo se usa

La constitución es criterio obligatorio para: diseño de componentes, architecture reviews, pull requests, nuevas capacidades, extensiones, integraciones, seguridad, gobierno, trade-offs, breaking changes y evolución del runtime.

Ver también: [[Index|Mapa del libro]]
