---
id: "C-035"
tipo: contrato
nombre: "SkillDescriptor"
version: "v1"
capitulo: "CH-24"
tags: [contrato, c-035]
used_by: ["CMP-022"]
modified_by: []
articulos_constitucionales: ["P-07", "INV-19"]
---

# SkillDescriptor (C-035)

> Contrato v1 — introducido en [[ch-24-skill-library|CH-24]].

## Definición canónica

```text
STRUCT SkillDescriptor
    skill: SkillId
    name: Text
    version: Text
    procedureRef: Text
    appliesTo: Optional<Text>
END
```

## Usado por

[[CMP-022-skilllibrary|CMP-022]]

## Modificado por

Ninguno

## Impacto constitucional

P-07, INV-19

## Contexto del libro

- Introducido en: [[ch-24-skill-library|CH-24]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
