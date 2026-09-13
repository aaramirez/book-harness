---
name: define-contract
description: >-
  Plantilla y reglas PC-01..PC-10 para definir un contrato (STRUCT/ENUM con nombre canónico)
  antes de usarlo en pseudocódigo. Usar cada vez que un capítulo introduzca o modifique una
  entrada del Contract Registry (registry/contracts.yaml).
---

# Skill: define-contract

## Cuándo usar esta skill

Antes de que `skills/write-pseudocode/SKILL.md` permita usar una nueva entidad de datos con
nombre propio (`ToolCall`, `AgentMessage`, `HarnessError`, ...) en un bloque de pseudocódigo. Un
contrato SIEMPRE se define antes de aparecer en comportamiento (REGLAS_LIBRO §5 "Data structures
before behavior").

## Procedimiento

### Paso 1 — Verificar que no exista ya

Buscar el nombre candidato en `registry/contracts.yaml`. Si ya existe:

- si el capítulo actual solo lo **usa**, añadir su `id` a `Available Contracts` del Brief, no
  redefinirlo;
- si el capítulo actual necesita **cambiarlo**, es un breaking/non-breaking change de contrato:
  seguir la regla de §10 de REGLAS_LIBRO (declarar qué cambió, por qué, qué componentes afecta,
  compatibilidad y migration impact) y actualizar `modified_by` en el registry — no crear un id
  nuevo para el mismo concepto.

### Paso 2 — Definir el STRUCT/ENUM canónico

Usando exclusivamente la gramática de `skills/write-pseudocode/SKILL.md`:

```text
STRUCT <Name>
    <field>: <Type>
    ...
END
```

Reglas PC aplicables aquí (REGLAS_LIBRO §23):

- **PC-02**: toda entidad relevante tiene tipo explícito (nunca un campo sin tipo).
- **PC-05**: el nombre es canónico; no se le cambia informalmente en capítulos posteriores.
- **PC-07**: si el contrato representa un resultado o puede fallar, modelar explícitamente éxito
  y error (no un campo `Any`/`Value` genérico para todo).

### Paso 3 — Escribir la ficha de Contract Registry

Esta ficha es la que se agrega a `registry/contracts.yaml` (y se muestra en la sección "New
Contracts / Interfaces" del capítulo):

```text
ID:                     C-XXX
Name:                   <Name>
Version:                v1
Introduced In:          CH-XX
Current Definition:     <bloque STRUCT/ENUM del Paso 2>
Used By:                [<ComponentId>, ...]     (puede estar vacío si aún no hay componentes)
Modified By:            []                       (vacío al introducirlo)
Constitutional Impact:  [P-xx, INV-xx, ...]
```

Los 8 campos son obligatorios; ninguno se omite aunque su valor sea una lista vacía.

### Paso 4 — Registrar

Agregar la entrada a `registry/contracts.yaml` (mismo esquema, ver comentario de cabecera de ese
archivo) y declarar el `id` en `introduces_contracts` del frontmatter del capítulo.

### Paso 5 — Validar

```bash
./scripts/validate-contracts
```

Falla si: falta algún campo obligatorio, `Introduced In` no existe en `book/book.yaml`, o el
`id` no sigue el formato `C-NNN`.
