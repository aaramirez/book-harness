---
id: "CH-03"
tipo: capitulo
titulo: "ModelGateway y la Invocación Real del Modelo"
tags: [capitulo, ch03]
introduces_components: ["CMP-003"]
introduces_contracts: ["C-006", "C-007"]
articulos_constitucionales: ["P-01", "P-02", "P-10", "P-12", "P-13", "INV-01", "INV-02", "INV-03"]
---

# CH-03 — ModelGateway y la Invocación Real del Modelo

## Navegación

⬅ [[ch-02-tool-runtime|CH-02]] · **CH-03** · [[ch-04-context-engine|CH-04]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro de la invocación real de un modelo de lenguaje, qué tramo le pertenece en exclusiva al componente que adapta mensajes e invoca al proveedor y qué tramos pertenecen a dominios distintos (continuación cognitiva, ejecución de una tool call, selección de contexto) que ya tienen o todavía no tienen componente propio — y podrás diseñar, para cualquier respuesta cruda de un proveedor, una representación normalizada que distinga texto final de una propuesta de acción sin resolver esa propuesta prematuramente.

## Qué introduce este capítulo

### Componentes

- [[CMP-003-modelgateway|CMP-003]] — Seleccionar el provider de modelo correspondiente, adaptar los AgentMessage de un turno (más los límites de generación relevantes) hacia el ModelRequest que ese provider espera, invocar al modelo, soportar streaming y normalizar la respuesta cruda del provider hacia un ModelResponse — sin decidir si otro turno de razonamiento debe ocurrir, sin ejecutar ninguna tool call y sin resolver ninguna propuesta de acción hacia un ToolCall validado.

### Contratos

- [[C-006-modelrequest|C-006]] — ModelRequest (impacto: P-01, P-02, INV-02)
- [[C-007-modelresponse|C-007]] — ModelResponse (impacto: P-10, P-13, INV-03)


## Artículos constitucionales relevantes

P-01, P-02, P-10, P-12, P-13, INV-01, INV-02, INV-03

## Localización en el repo

`book/chapters/03-model-gateway/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
