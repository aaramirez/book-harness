---
id: "CH-35"
tipo: capitulo
titulo: "El Entorno Aislado y las Credenciales que Solo Existen en el Egress"
tags: [capitulo, ch35, tramo-4]
introduces_components: ["CMP-026"]
introduces_contracts: ["C-047", "C-048"]
modifies_contracts: []
articulos_constitucionales: ["P-27", "P-35", "INV-05", "INV-E07", "INV-E08", "INV-E20"]
---

# CH-35 — El Entorno Aislado y las Credenciales que Solo Existen en el Egress

## Navegación

⬅ [[ch-34-canales-continuacion|CH-34]] · **CH-35** · [[ch-36-integracion-turno-durable|CH-36]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir dónde corre el código que el modelo pide ejecutar, qué puede alcanzar por la red, y cómo ese código usa un servicio autenticado sin que ninguna credencial llegue nunca a estar dentro de su entorno.

## Qué introduce este capítulo

### Componentes

- [[CMP-026-isolatedexecutionenvironment|CMP-026 IsolatedExecutionEnvironment]], dueño de "sandboxing" (Article XII). [[CMP-014-credentialbroker|CredentialBroker]] gana `resolveEgressCredential` dentro de su `owns`.

### Contratos

- [[C-047-sandboxsession|C-047 SandboxSession]]
- [[C-048-networkpolicy|C-048 NetworkPolicy]]

## Artículos constitucionales relevantes

P-27, P-35, INV-05, INV-E07, INV-E08, INV-E20

## Localización en el repo

`book/chapters/35-entorno-aislado/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
