---
name: define-component
description: >-
  Ficha arquitectónica obligatoria (Responsibility / Consumes / Depends on / Produces / Owns /
  Does NOT own) para introducir un componente nuevo en el Component Registry
  (registry/components.yaml). Usar antes de que un componente aparezca en pseudocódigo o en un
  Sequence Diagram.
---

# Skill: define-component

## Cuándo usar esta skill

Antes de que `skills/write-pseudocode/SKILL.md` permita invocar un componente
(`ToolRuntime.execute(...)`, `PolicyEngine.evaluate(...)`, ...) en un bloque de pseudocódigo, y
antes de que ese componente aparezca en un Sequence Diagram como participante activo (no como
mera mención en prosa marcada "Preview").

## Procedimiento

### Paso 1 — Verificar contra la Constitution y el registry

1. Confirmar que el componente corresponde a un dominio real de
   `constitution/ARCHITECTURE_CONSTITUTION.md` Article III (Component Sovereignty) — no inventar
   un dominio de responsabilidad que la Constitution no reconoce, o justificar explícitamente por
   qué se necesita uno nuevo (EVO-07 "Core dependencies require justification").
2. Buscar el nombre en `registry/components.yaml`. Si ya existe, no redefinirlo informalmente:
   añadirlo a `Available Components` del Brief.

### Paso 2 — Escribir la ficha arquitectónica (plantilla obligatoria, REGLAS_LIBRO §6)

```text
COMPONENT: <ComponentName>

Responsibility:
    <responsabilidad primaria, una frase>

Consumes:
    <ContractId o tipos de entrada>

Depends on:
    <ComponentId de los que depende — deben apuntar a contratos/abstracciones, no a
     implementaciones concretas; ver REGLAS_LIBRO §8 "Depend on abstractions, not
     implementations">

Produces:
    <ContractId o tipos de salida>

Owns:
    <decisiones que este componente posee en exclusiva>

Does NOT own:
    <responsabilidades explícitamente excluidas — esto es tan obligatorio como "Owns">
```

`Does NOT own` nunca se omite: es lo que evita que la responsabilidad de un componente se
disuelva silenciosamente en otro (Article IV "Ownership Rule" de la Constitution: "Ningún
componente debe absorber silenciosamente decisiones que pertenecen a otro dominio").

### Paso 3 — Verificar dirección de dependencias

Antes de declarar `Depends on`, confirmar (REGLAS_LIBRO §7-9):

- el componente depende de una `INTERFACE` (contrato de comportamiento), no de una
  `IMPLEMENTATION` concreta;
- la nueva dependencia se agrega al Dependency Map del capítulo (sección 9,
  "Dependency Relationships") y se justifica arquitectónicamente.

### Paso 4 — Registrar

Agregar la entrada a `registry/components.yaml` con el esquema completo:

```text
ID:                       CMP-XXX
Name:                     <ComponentName>
Responsibility:           <texto>
Owns:                     [...]
Does Not Own:             [...]
Dependencies:             [<ComponentId>, ...]
Consumes:                 [<ContractId>, ...]
Produces:                 [<ContractId>, ...]
Introduced In:             CH-XX
Constitutional Articles:   [P-xx, INV-xx, ...]
```

Y declarar el `id` en `introduces_components` del frontmatter del capítulo.

### Paso 5 — Validar

```bash
./scripts/validate-components
```

Falla si: falta algún campo obligatorio (incluido `Does Not Own` aunque esté vacío hay que
declararlo como lista, nunca ausente), alguna `Dependencies` apunta a un `ComponentId`
inexistente, o `Introduced In` no existe en `book/book.yaml`.
