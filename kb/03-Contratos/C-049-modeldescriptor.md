---
id: "C-049"
tipo: contrato
nombre: "ModelDescriptor"
version: "v1"
capitulo: "CH-39"
tags: [contrato, c-049]
used_by: ["CMP-003"]
modified_by: []
articulos_constitucionales: ["P-02", "INV-E10"]
---

# ModelDescriptor (C-049)

> Contrato v1 — introducido en [[ch-39-modelo-como-dato|CH-39]].

## Definición canónica

```text
STRUCT ModelDescriptor
    modelId: Text
    provider: Text
    descriptorVersion: Text
    contextWindow: Integer
    maxOutputTokens: Integer
    pricing: ModelPricing
    capabilities: List<ModelCapability>
END
```

## Usado por

[[CMP-003-modelgateway|CMP-003]]

## Modificado por

Ninguno

## Impacto constitucional

P-02, INV-E10

## Contexto del libro

- Introducido en: [[ch-39-modelo-como-dato|CH-39]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
