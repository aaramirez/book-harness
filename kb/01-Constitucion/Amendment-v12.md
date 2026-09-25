---
id: amendment-v12
tipo: constitucion
tags: [constitucion, enmienda, durabilidad, conectividad, autoria]
---

# Enmienda v1.2 — Durable Operation, Identity, Connectivity and Authoring

Extiende la constitución y la [[Amendment-v11|Enmienda v1.1]] con cuatro temas:
- **operación durable:** pasos, esperas, continuación, evolución del runtime;
- **identidad:** el principal viaja con el turno;
- **conectividad:** conexiones MCP y OpenAPI, entorno aislado, audiencia;
- **autoría:** el agente como directorio.

Introduce **P-31..P-39** e **INV-E15..INV-E27**. Se ratificó el 2026-09-25 (plan `planes/2026-09-24-amendment-v1-2.md`).

## Nuevos principios (P-31..P-39)

| Principio | Tema | Capítulo que lo materializa |
|-----------|------|-----------------------------|
| P-31 | La identidad viaja con cada turno | CH-31 |
| P-32 | El paso es la unidad de durabilidad y de recuperación | CH-32 |
| P-33 | Esperar es durable y no consume cómputo | CH-33 |
| P-34 | Las conversaciones externas se direccionan, no se infieren | CH-34 |
| P-35 | Los secretos nunca entran al cómputo que controla el modelo | CH-35 |
| P-36 | El runtime evoluciona con sesiones abiertas solo en fronteras inactivas | CH-43 |
| P-37 | La captura de observabilidad está acotada por la audiencia | CH-44 |
| P-38 | Las capabilities externas entran solo por conexiones declaradas | CH-39 |
| P-39 | Un agente se escribe como archivos inspeccionables en ubicaciones convencionales | CH-46 |

## Nuevas invariantes (INV-E15..INV-E27)

| Invariante | Resumen | Capítulo |
|------------|---------|----------|
| INV-E15 | Un arnés sin configurar no admite nada | CH-31 |
| INV-E16 | Un paso comprometido nunca se re-ejecuta al recuperar | CH-32 |
| INV-E17 | Un efecto de resultado desconocido solo se re-ejecuta si su capability es `SAFE` | CH-30 / CH-32 |
| INV-E18 | Una entrega solo reanuda la espera que direcciona, y solo si el respondedor está autorizado | CH-33 |
| INV-E19 | Una dirección de continuación tiene a lo sumo una sesión dueña | CH-34 |
| INV-E20 | Las credenciales nunca se materializan dentro del entorno aislado | CH-35 |
| INV-E21 | El presupuesto de un hijo nunca excede el saldo del padre | CH-41 |
| INV-E22 | El trabajo vivo nunca migra entre versiones del runtime | CH-43 |
| INV-E23 | Ningún destino de trazas captura más que el techo de la sesión | CH-44 |
| INV-E24 | Ningún punto de enganche devuelve una autorización | CH-38 |
| INV-E25 | Ninguna tool externa llega al modelo sin CapabilityRegistry y PolicyEngine | CH-39 |
| INV-E26 | Toda fuente de datos declara su clasificación; sin ella es RESTRICTED | CH-40 |
| INV-E27 | Un diagnóstico de autoría de nivel ERROR impide activar el agente | CH-46 |

Ver también: [[Architecture-Constitution|Constitución]] · [[Amendment-v11|Enmienda v1.1]] · [[Index|Mapa del libro]]
