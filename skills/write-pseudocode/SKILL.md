---
name: write-pseudocode
description: >-
  Gramática canónica de pseudocódigo del libro (STRUCT, ENUM, INTERFACE, IMPLEMENTATION,
  FUNCTION, COMMAND, EVENT, control de flujo) y la regla "no magic entities". Usar cada vez que
  se escriba un bloque de código en un capítulo, siempre después de define-contract /
  define-component para cualquier entidad nueva.
---

# Skill: write-pseudocode

## Regla no negociable: no magic entities

> Ningún pseudocódigo puede utilizar una entidad que no haya sido definida previamente mediante
> `STRUCT`, `INTERFACE`, `ENUM`, `EVENT`, `COMMAND` o error type — en este capítulo o en un
> capítulo anterior ya registrado. (REGLAS_LIBRO_AGENT_HARNESS(1).md §2)

Secuencia obligatoria por concepto:

```text
Concept → Contract → Pseudocode → Interaction
```

## Cuándo usar esta skill

Cada vez que se escriba cualquier bloque ` ```pseudocode ` dentro de un `chapter.md` — en las
secciones "New Data Structures", "New Contracts / Interfaces", "Pseudocode", "State Transitions"
o "Failure Semantics".

## Gramática canónica (palabras reservadas)

```text
STRUCT
ENUM
INTERFACE
IMPLEMENTATION
FUNCTION
COMMAND
EVENT

IF
ELSE
END

FOR EACH
WHILE

RETURN
THROW

EMIT
AWAIT

OPTIONAL
LIST
MAP
```

No usar sintaxis de un lenguaje real (TypeScript, Python, Java, ...) — el pseudocódigo debe ser
independiente de lenguaje pero suficientemente preciso para implementarse (PC-10).

## Procedimiento

### Paso 1 — Data structures before behavior (§5)

Definir siempre `STRUCT`/`ENUM` antes de cualquier función o método que los use:

```text
STRUCT ToolCall
    id: ToolCallId
    capability: CapabilityId
    arguments: Map<Text, Value>
END

ENUM ToolExecutionStatus
    SUCCESS
    FAILED
    DENIED
    CANCELLED
    TIMED_OUT
END
```

### Paso 2 — Interfaces before implementations (§7)

```text
INTERFACE ToolRuntime
    execute(
        call: ToolCall,
        execution: ExecutionContext
    ) -> ToolResult
END
```

Las implementaciones concretas (si el capítulo las necesita) van después y declaran
`IMPLEMENTS`:

```text
IMPLEMENTATION LocalToolRuntime IMPLEMENTS ToolRuntime
```

### Paso 3 — Reglas de tipado (PC-01, PC-02, PC-09)

- Toda `FUNCTION` declara sus inputs, su output y sus errores relevantes.
- Preferir:

  ```text
  result: ToolResult =
      ToolRuntime.execute(call, execution)
  ```

  sobre `result = doSomething()`.
- Todo `branching` importante muestra la condición o el estado explícito (nunca un `IF` sin
  variable de estado nombrada).

### Paso 4 — Checklist antes de insertar el bloque en el capítulo (PC-01..PC-10)

```text
[ ] PC-01 Toda función declara parámetros y retorno.
[ ] PC-02 Toda entidad relevante tiene tipo.
[ ] PC-03 Todo componente utilizado existe en registry/components.yaml.
[ ] PC-04 Todo contrato utilizado existe en registry/contracts.yaml.
[ ] PC-05 Los nombres son canónicos (coinciden exactamente con el registry).
[ ] PC-06 Las llamadas entre componentes respetan el Dependency Map del capítulo.
[ ] PC-07 Resultados y errores están modelados explícitamente (no un THROW Error genérico).
[ ] PC-08 No hay side effects escondidos dentro de helpers genéricos.
[ ] PC-09 Todo branching importante muestra condición o estado explícito.
[ ] PC-10 El pseudocódigo es abstracto pero implementable.
```

### Paso 5 — Errores (nunca genéricos)

```text
THROW HarnessError(
    category = TOOL,
    code = "TOOL_TIMEOUT",
    recoverable = TRUE,
    retryable = TRUE
)
```

Nunca `THROW Error` a secas — todo error usa el contrato `HarnessError` (C-011) con
`ErrorCategory` explícito.

### Paso 6 — Validar

```bash
./scripts/validate-chapter <ruta-del-capitulo>
```

`validate-chapter` extrae cada entidad referenciada dentro de los bloques ` ```pseudocode ` del
capítulo y falla si alguna no está definida en ese mismo capítulo ni registrada en
`registry/contracts.yaml` / `registry/components.yaml` con un `introduced_in` igual o anterior.
