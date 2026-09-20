# -*- coding: utf-8 -*-
"""Genera el PDF ejecutivo "El viaje de un mensaje por el harness empresarial".

Renderiza contenido (bloques) con reportlab/Platypus: portada, índice, secciones,
callouts, tablas, glosario y un diagrama de flujo vectorial.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Flowable,
    KeepTogether,
    NextPageTemplate,
)
from reportlab.platypus.tableofcontents import TableOfContents
from lib.diagrams import IngressDiagram, LoopDiagram, ParticipationMap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist", "flujos-harness-empresarial.pdf")

# ---------------------------------------------------------------- paleta
INK = HexColor("#1A2233")
NAVY = HexColor("#14324F")
AMBER = HexColor("#B45309")
AMBER_D = HexColor("#92400E")
SAND = HexColor("#FBF6EC")
TEAL = HexColor("#0E7490")
TEAL_L = HexColor("#E7F3F5")
BOX_BG = HexColor("#EEF2F6")
REJECT = HexColor("#B91C1C")
ALT_ROW = HexColor("#F2F6FA")
RULE = HexColor("#CBD5E1")
GRAY = HexColor("#3A4556")
META = HexColor("#5B6472")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm
DOC_TITLE = "El viaje de un mensaje por el harness empresarial"
TITLE_ABBREV = "El viaje de un mensaje — Harness empresarial"

# --------------------------------------------------------------- estilos
def st(name, **kw):
    base = dict(
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.2,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    base.update(kw)
    return ParagraphStyle(name, **base)


S_COVER_TITLE = st("cov", fontName="Helvetica-Bold", fontSize=25, leading=30,
                   textColor=NAVY, alignment=TA_LEFT)
S_COVER_SUB = st("csub", fontSize=12.5, leading=17, textColor=INK, alignment=TA_LEFT)
S_COVER_META = st("cmeta", fontSize=9, leading=13, textColor=META, alignment=TA_LEFT)
S_H1 = st("h1", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY,
          alignment=TA_LEFT, spaceBefore=14, spaceAfter=8, keepWithNext=1)
S_H2 = st("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY,
          alignment=TA_LEFT, spaceBefore=10, spaceAfter=5, keepWithNext=1)
S_BODY = st("body")
S_BUL = st("bul", leftIndent=12, bulletIndent=2, spaceAfter=3.5)
S_CELL = st("cell", fontSize=8.9, leading=12, alignment=TA_LEFT, spaceAfter=0)
S_CELL_BOLD = st("cellb", fontName="Helvetica-Bold", fontSize=8.9, leading=12,
                 alignment=TA_LEFT, spaceAfter=0)
S_CELL_HEAD = st("cellh", fontName="Helvetica-Bold", fontSize=9.2, leading=12,
                 textColor=white, alignment=TA_LEFT, spaceAfter=0)
S_NOTE = st("note", alignment=TA_LEFT, fontSize=8.6, leading=11.5,
            textColor=META)

# ---------------------------------------------------------------- pies
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 1.45 * cm, PAGE_W - MARGIN, 1.45 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(META)
    canvas.drawString(MARGIN, 1.12 * cm, TITLE_ABBREV)
    canvas.drawRightString(PAGE_W - MARGIN, 1.12 * cm, "Pagina %d" % doc.page)
    canvas.restoreState()


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 1.6 * cm, PAGE_W, 1.6 * cm, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, PAGE_H - 1.72 * cm, PAGE_W, 0.12 * cm, stroke=0, fill=1)
    canvas.restoreState()
    on_page(canvas, doc)


# --------------------------------------------------------- callout
class Callout(Flowable):
    def __init__(self, text, width):
        super().__init__()
        self.text = text
        self.cw = width

    def wrap(self, aw, ah):
        self.width = aw
        self.height = self._h()
        return self.width, self.height

    def _h(self):
        p = Paragraph(self.text, self._style())
        return p.wrap(self.cw - 2.4 * cm, 1000)[1] + 1.1 * cm

    def _style(self):
        return st("idea_c", fontSize=10, leading=14, fontName="Helvetica-Bold",
                  textColor=NAVY, alignment=TA_LEFT, spaceAfter=0)

    def draw(self):
        c = self.canv
        box = self.width - 2.0 * cm
        c.setFillColor(HexColor("#FFFDF7"))
        c.setStrokeColor(RULE)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, box, self.height, 6, stroke=1, fill=1)
        c.setFillColor(AMBER)
        c.rect(0, 0, 0.22 * cm, self.height, stroke=0, fill=1)
        p = Paragraph(self.text, self._style())
        p.wrapOn(c, box - 1.2 * cm, 1000)
        p.drawOn(c, 1.1 * cm, 0.55 * cm)




class _DocWithToc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            if flowable.style.name == "h1":
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = _DocWithToc(
        OUT,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=1.9 * cm, bottomMargin=1.9 * cm,
        title=DOC_TITLE,
        author="Book Harness - Arquitectura de Agentes",
        subject="Flujos del harness empresarial explicados para audiencia no tecnica",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(
        [
            PageTemplate(id="Cover", frames=[frame], onPage=on_cover),
            PageTemplate(id="Body", frames=[frame], onPage=on_page),
        ]
    )

    W = doc.width
    story = []
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t1", fontName="Helvetica-Bold", fontSize=10.5, leading=16,
                       textColor=NAVY, leftIndent=0),
        ParagraphStyle("t2", fontName="Helvetica", fontSize=9.5, leading=14,
                       textColor=INK, leftIndent=14),
    ]

    # ---------------- PORTADA ----------------
    story.append(Spacer(1, 3.6 * cm))
    story.append(Paragraph("El viaje de un mensaje", S_COVER_TITLE))
    story.append(Paragraph("por el harness empresarial", S_COVER_TITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Que ocurre, paso a paso, detras de cada solicitud que recibe un agente, y por que "
        "cada decision sobre la que nadie se pregunta esta ahi a proposito.",
        S_COVER_SUB))
    story.append(Spacer(1, 2.2 * cm))
    story.append(Paragraph(
        "Documento de divulgacion ejecutiva sobre la arquitectura del harness.<br/>"
        "Basado en la Constitucion de Arquitectura y los 28 capitulos del libro "
        "(CH-00 a CH-27, incluyendo la Enmienda v1.1 de Activacion Empresarial).",
        S_COVER_META))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "Dirigido a personas sin perfil tecnico: no hace falta saber programar para "
        "entender lo que describe, pero la descripcion respeta la profundidad real "
        "de cada paso.",
        S_COVER_META))
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # ---------------- INDICE ----------------
    story.append(Paragraph("Contenido", st("toch", fontName="Helvetica-Bold", fontSize=15,
                                           leading=18, textColor=NAVY, alignment=TA_LEFT,
                                           spaceAfter=8)))
    story.append(toc)
    story.append(PageBreak())

    # ---------------- S0 ----------------
    story.append(Paragraph("La idea en una frase", S_H1))
    story.append(Paragraph(
        "Todo lo que el harness hace se puede resumir en dos puertas y una regla. "
        "La primera puerta traduce el mundo exterior: un mensaje de chat, una llamada a una "
        "API, un aviso de un sistema, un disparo de un reloj o una peticion de otro "
        "agente. Todos llegan a un mismo formato interno unico, el “billete” llamado "
        "ActivationRequest.",
        S_BODY))
    story.append(Paragraph(
        "La segunda puerta es la aduana: antes de que cualquier cosa se ponga a trabajar, "
        "el AdmissionController decide si ese mensaje tiene derecho a intentar siquiera "
        "activar un agente. Y la regla: si ninguna regla conocida concede el paso, se "
        "rechaza. Siempre. Por defecto, la puerta esta cerrada.",
        S_BODY))
    story.append(Callout(
        "Los canales por los que llegan los mensajes — app, chat, web, webhook, cola, cron "
        "u otro agente — son cuestiones de la frontera, no del nucleo. El nucleo solo "
        "conoce el billete (ActivationRequest) y la aduana (AdmissionController). Todo lo "
        "demas es traduccion de idiomas en la frontera.", W))
    story.append(Paragraph(
        "Todo lo que describe este documento existe para sostener esa frase: las piezas que "
        "la hacen posible, el orden exacto en que trabajan y las garantias invisibles que "
        "protegen cada mensaje mientras viaja de la puerta a la respuesta.",
        S_BODY))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Una nota para el lector: los terminos en negrita (ActivationRequest, "
        "AdmissionController, AgentCore, PolicyEngine...) son nombres propios de la "
        "arquitectura. Si alguno suena a jerga, la seccion 5, Glosario, lo traduce a una "
        "linea cotidiana.",
        S_NOTE))
    story.append(PageBreak())

    # ---------------- S1 ----------------
    story.append(Paragraph("1. El viaje completo de un mensaje, paso a paso", S_H1))
    story.append(Paragraph(
        "Siga un mensaje generico. Cada paso corresponde a una pieza real del harness: "
        "aqui se explica el por que de cada decision.",
        S_BODY))

    steps = [
        ("Paso 1 - Llega un mensaje, por cualquier medio",
         "Un usuario escribe en una aplicacion o un chat; un sistema corporativo llama a "
         "una API o dispara un webhook; una tarea programada se enciende a su hora; otro "
         "agente envia una peticion. Del lado del mundo exterior no hay un unico puerto: "
         "cada medio tiene el suyo. El harness, sin embargo, no escucha todos esos "
         "idiomas."),
        ("Paso 2 - La frontera lo traduce al billete estandar",
         "En el borde, un traductor (el adaptador de frontera) toma el mensaje tal como "
         "vino y lo normaliza: lo convierte en un ActivationRequest, un documento interno "
         "con los datos esenciales: quien pide, que pide, de donde viene. Aqui no se decide "
         "si la peticion es buena o mala; solo se le da un formato que el nucleo entiende. "
         "Es una regla inquebrantable: ningun medio habla directamente con el nucleo; "
         "siempre pasa por el billete."),
        ("Paso 3 - La aduana decide si el mensaje puede siquiera intentar algo",
         "El AdmissionController ya tiene el billete. Sin saber todavia a que agente va "
         "dirigida la peticion, responde la pregunta mas importante del sistema: tiene "
         "derecho a intentar activar algo? Para responderlo aplica, en orden: identidad de "
         "quien pide, autorizacion, a que tenant (cliente o area) pertenece, capacidad "
         "disponible, velocidad de peticiones permitida, presupuesto, deduplicacion (si ya "
         "se proceso esta peticion) y politica corporativa. El resultado es un veredicto "
         "limpio: ADMIT (puede pasar) o REJECT (se descarta, y nada, absolutamente nada, "
         "se ejecuta). Ante la duda, REJECT."),
        ("Paso 4 - El enrutamiento: el mensaje gana un destino",
         "Aceptada la aduana, la peticion se asocia al agente concreto que le corresponde. "
         "Este paso no decide si la peticion es valida — eso ya lo hizo la aduana — solo "
         "decide hacia donde viaja."),
        ("Paso 5 - La activacion: nace una ejecucion con limite",
         "El AgentCore recibe la peticion enrutada y crea una instancia de ejecucion: un "
         "identificador, una sesion, una traza para seguir todo lo que pase despues y un "
         "presupuesto de uso. A partir de este momento existe un “run” que se puede "
         "observar, interrumpir, reanudar y auditar. Y tiene presupuesto desde el primer "
         "segundo: no es un detalle administrativo, es lo que permite decir “no” mas "
         "tarde."),
        ("Paso 6 - Antes de pensar, se revisan las condiciones",
         "Justo antes de cada ronda de razonamiento, un controlador de ejecucion revisa el "
         "presupuesto gastado y las condiciones de la ejecucion, y decide si la ronda "
         "continua o si hay que detenerse. Asi el agente recuerda su limite antes de cada "
         "paso, no al final."),
        ("Paso 7 - Se construye la memoria que vera el modelo",
         "El agente no ve todo lo que ha pasado ni todo lo que sabe del mundo. El contexto "
         "se empaqueta selectivamente: mensajes previos, informacion pertinente, "
         "observacion del ultimo paso. Decidir que entra en la memoria — y que se deja "
         "fuera — es una capacidad del harness, no del modelo: de ahi dependen tanto la "
         "calidad como la seguridad."),
        ("Paso 8 - El modelo razona: propone, no decide",
         "Con la memoria empaquetada, el modelo de lenguaje razona y produce un resultado "
         "que puede ser de dos tipos: una respuesta final para el usuario, o una propuesta "
         "de usar una capacidad (consultar una base de datos, leer un archivo, llamar a "
         "un servicio). El modelo propone; no ejecuta nada por si mismo."),
        ("Paso 9 - La doble revision: catalogo y politica",
         "Si el modelo propone usar una capacidad, pasan dos filtros. Primero, esa "
         "capacidad debe existir y el agente debe tenerla registrada como disponible. "
         "Segundo, la politica debe permitir ese uso concreto: para que accion, sobre que "
         "destino, con que alcance. La politica responde ALLOW, DENY o REQUIRE_APPROVAL. "
         "Si pide aprobacion humana, aqui es donde interviene una persona (paso 10)."),
        ("Paso 10 - Un humano puede intervenir a mitad de camino",
         "Cuando la politica exige una aprobacion o el agente necesita informacion de una "
         "persona, el harness levanta una consulta y espera. Esa consulta llega a la "
         "persona por su propio medio (la misma aplicacion, un chat, un correo). Cuando "
         "responde, la ejecucion continua exactamente donde estaba. Aprobar desde un chat "
         "o desde una pagina web es, para el harness, exactamente lo mismo."),
        ("Paso 11 - La capacidad se ejecuta, y la observacion es real",
         "Aprobada la politica, la capacidad se ejecuta sobre el mundo (consultar, escribir, "
         "llamar) y el resultado se guarda como observacion real dentro de la memoria. "
         "Nada se da por supuesto: lo que el modelo vera en la siguiente ronda es lo que "
         "realmente devolvio el paso."),
        ("Paso 12 - El ciclo se repite hasta que el trabajo termina",
         "Con la observacion en memoria, el ciclo vuelve a empezar: condiciones, contexto, "
         "razonamiento, capacidades. Cada ronda hace un punto de control (checkpoint), de "
         "modo que si algo se cae el trabajo se reanuda desde el ultimo punto y no se "
         "rehace desde cero. Cuando el modelo ya no necesita capacidades y produce su "
         "respuesta final, la ejecucion se declara completa y la respuesta sale por el "
         "mismo medio por el que entro la peticion."),
    ]
    for title, body in steps:
        story.append(KeepTogether([Paragraph(title, S_H2), Paragraph(body, S_BODY)]))
        story.append(Spacer(1, 2))
    story.append(Paragraph(
        "En ningun momento el mensaje “vuela solo”: cada paso emite un evento que otros "
        "pueden observar (auditoria, trazas, supervisores). El harness no es un copiloto "
        "suelto; es una linea de montaje donde cada estacion deja huella y puede ser "
        "inspeccionada.",
        S_BODY))
    story.append(PageBreak())

    # ---------------- S2 ----------------
    story.append(Paragraph("2. Tres recorridos completos", S_H1))
    story.append(Paragraph(
        "El viaje del generico es el mismo para todos; lo que cambia es la piel del "
        "mensaje. Tres recorridos, el mismo esqueleto.",
        S_BODY))

    journeys = [
        ("2.1  Un usuario humano escribe en la aplicacion (o el chat)",
         "El mensaje entra por el canal humano: la aplicacion, la web, un chat corporativo. "
         "El traductor de ese canal lo convierte en billete. En la aduana se comprueba la "
         "identidad del usuario, a que tenant pertenece, su cuota de peticiones y su "
         "presupuesto. Enrutado al agente adecuado, nace la ejecucion. Si una capacidad "
         "sensible lo pide, la politica elevara la consulta a ese mismo usuario por ese "
         "mismo canal, y su respuesta reanudara el trabajo. La respuesta final vuelve a la "
         "pantalla donde el usuario escribio."),
        ("2.2  Un sistema corporativo llama por webhook o API",
         "Un sistema B (facturacion, inventario, un servicio interno) envia una peticion. "
         "El traductor de frontera la convierte en billete. En la aduana la identidad ya no "
         "es un usuario sino el sistema llamador, con sus credenciales; se aplican las "
         "mismas reglas de tenant, capacidad, presupuesto y deduplicacion (si el webhook se "
         "reenvio por error, la deduplicacion lo detecta). Si el agente necesita leer o "
         "escribir en ese sistema, lo hara por sus capacidades y credenciales intermediadas, "
         "nunca exponiendo secretos al modelo. La respuesta vuelve al mismo origen que "
         "llamo."),
        ("2.3  Otro agente (remoto o independiente) pide cooperacion",
         "Un agente de otra organizacion se comunica bajo un estandar de interoperabilidad. "
         "Su mensaje atraviesa los traductores de protocolo y transporte y entra por una "
         "puerta dedicada a la comunicacion entre agentes. La delegacion es explicita y "
         "limitada: el agente remoto no hereda la autoridad de quien lo invoco; recibe un "
         "alcance, un limite de tiempo y un registro auditable. La participacion de un "
         "agente externo nunca es automatica: es un acto autorizado, con perimetro y "
         "trazabilidad."),
    ]
    for title, body in journeys:
        story.append(Paragraph(title, S_H2))
        story.append(Paragraph(body, S_BODY))
        story.append(Spacer(1, 3))

    story.append(Paragraph("Los tres de un vistazo", S_H2))
    rows = [
        ["", "Entrada", "La aduana comprueba", "Salida"],
        ["Humano", "App, chat o web",
         "Identidad del usuario, tenant, cuota, presupuesto", "Respuesta en la misma app"],
        ["Sistema", "Webhook, API o cola",
         "Credenciales del sistema, dedup de reintentos", "Respuesta por API o webhook"],
        ["Agente externo", "Protocolo estandar (A2A)",
         "Delegacion explicita y limitada, trazable", "Respuesta por el mismo protocolo"],
    ]
    for r, row in enumerate(rows):
        for j, cell in enumerate(row):
            style = S_CELL_HEAD if r == 0 else (S_CELL_BOLD if j == 0 else S_CELL)
            row[j] = Paragraph(cell, style)
    tbl = Table(rows, colWidths=[2.6 * cm, 3.4 * cm, 6.2 * cm, 4.4 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ALT_ROW]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(tbl)
    story.append(PageBreak())

    # ---------------- S3 ----------------
    story.append(Paragraph("3. Las garantias que no se ven", S_H1))
    story.append(Paragraph(
        "Detras del viaje hay decisiones que no aparecen en la superficie pero definen si "
        "el harness es una herramienta responsable o un riesgo. Estas son las garantias "
        "estructurales, cada una con su pieza, su razon y su regla.",
        S_BODY))

    guarantees = [
        ("Una sola puerta, una sola aduana",
         "Como todo entra normalizado y todo pasa la misma admision, no existe un camino "
         "suelto por donde una peticion evite los controles. Si se quiere endurecer una "
         "regla, se endurece en un solo sitio y vale para todos los medios."),
        ("El presupuesto se respeta antes de cada ronda",
         "Ningun agente “piensa por su cuenta” hasta agotar recursos: antes de cada ronda el "
         "controlador de ejecucion revisa presupuesto y condiciones, y puede detener el "
         "trabajo. El limite no es un corte tardio; es parte del latido de cada "
         "ejecucion."),
        ("La memoria se empaqueta, no se vuelca",
         "El modelo recibe exactamente el contexto que el harness decidio darle. Esto "
         "protege la relevancia (solo entra lo pertinente) y la confidencialidad (solo "
         "entra lo que la gobernanza de datos permite). Clasificacion, residencia, "
         "retencion y linaje se gestionan de forma independiente del razonamiento."),
        ("La politica cierra por defecto",
         "Al usar una capacidad o ejecutar una accion, la politica responde ALLOW, DENY o "
         "REQUIRE_APPROVAL. Si no existe una regla que permita, la respuesta es DENY. Lo "
         "que la aduana hace con los mensajes, la politica lo hace con las acciones: ningun "
         "vacio se interpreta como permiso."),
        ("Nada vuelve a empezar desde cero",
         "Cada ronda deja un punto de control y la sesion se persiste. Si el proceso se "
         "cae, se reanuda desde el ultimo punto. El estado durable de la ejecucion — no la "
         "memoria suelta — es la fuente de confianza."),
        ("Una peticion ejecutada dos veces no duplica efectos",
         "Si un webhook se reenvia o una tarea se reintenta, el guardia de idempotencia lo "
         "detecta. Las capacidades con efectos visibles declaran como se comportan ante "
         "reintentos, y los efectos no se disparan en duplicado."),
        ("Todo queda registrado, y la huella es inmutable",
         "Existen dos mundos de registro bien separados: el operativo (logs y trazas, para "
         "diagnosticar) y el de auditoria (evidencia inmutable, para rendir cuentas). No se "
         "confunden. El resultado de negocio se correlaciona con la ejecucion, no solo su "
         "exito tecnico."),
        ("El operador siempre puede frenar",
         "El harness mantiene, fuera del modelo, la capacidad de cancelar una ejecucion, "
         "deshabilitar una capacidad, aislar un tenant, revertir un despliegue o activar "
         "un interruptor de emergencia. Palancas operacionales que no dependen de la "
         "cooperacion del modelo."),
        ("No importa donde corra",
         "El harness se comporta igual si la ejecucion ocurre en un proceso local, un "
         "worker, un cluster o una funcion sin servidor. La topologia de despliegue es "
         "infraestructura, no semantica del agente: se puede mover sin cambiar el "
         "comportamiento."),
        ("Solo se publica lo que fue evaluado",
         "Antes de promoverse a produccion, un candidato (prompt, capacidad, politica) pasa "
         "por un arnes de evaluacion dedicado. La separacion entre evaluacion y produccion "
         "es una garantia de calidad del propio sistema."),
    ]
    for title, body in guarantees:
        story.append(KeepTogether([Paragraph(title, S_H2), Paragraph(body, S_BODY)]))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # ---------------- S4 ----------------
    story.append(Paragraph("4. La frontera: lo que el harness no hace", S_H1))
    story.append(Paragraph(
        "Comprender el perimetro es comprender el sistema. El harness es el sistema "
        "nervioso, no la piel. Hay cuatro cosas que no hace, a proposito:",
        S_BODY))
    story.append(Callout(
        "Ninguno de los traductores del borde (el que ordena un canal humano, el que "
        "recibe un webhook o el que habla con otro agente) vive dentro del nucleo. Si "
        "manana se sustituyera un protocolo, un canal o un transporte, el nucleo no "
        "cambia: esa es la fortaleza de la frontera.", W))
    frontier = [
        ("No decide que canal usar",
         "La interfaz concreta (aplicacion, chat, correo, web) es piel. El nucleo trabaja "
         "con el billete, no con la pantalla. Por eso aprobar desde un canal u otro es "
         "siempre lo mismo para el sistema."),
        ("No habla protocolos directamente",
         "Conectarse con otro agente o con un servicio no se hace desde el nucleo: se hace "
         "a traves de adaptadores que traducen hacia protocolos y transportes concretos "
         "(HTTP, gRPC, websockets, colas). Esos adaptadores son intercambiables uno por "
         "uno, de forma independiente."),
        ("No guarda secretos",
         "Las credenciales se custodian en un intermediario de credenciales. El modelo "
         "nunca toca la clave: solo pide la capacidad, y quien la ejecuta usa la "
         "credencial de forma controlada y auditable."),
        ("No conoce el mundo en bruto",
         "Lo que un agente puede hacer sobre el mundo lo determina el catalogo de "
         "capacidades registradas para el. No hay poderes innatos: si una capacidad no "
         "esta en el catalogo, no existe para el agente."),
    ]
    for title, body in frontier:
        story.append(KeepTogether([Paragraph(title, S_H2), Paragraph(body, S_BODY)]))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # ---------------- S5 ----------------
    story.append(Paragraph("5. Glosario en lenguaje llano", S_H1))
    glossary = [
        ["Termino", "En una frase"],
        ["ActivationRequest",
         "El billete estandar: el mensaje ya traducido al formato interno, sin importar de donde vino."],
        ["AdmissionController",
         "La aduana: decide ADMIT o REJECT antes de que nada se ejecute. Por defecto, siempre REJECT."],
        ["AdmissionDecision",
         "El veredicto de la aduana, basado en identidad, autorizacion, tenant, capacidad, rate, presupuesto, deduplicacion y politica."],
        ["Adaptador de frontera (Ingress Adapter)",
         "El traductor generico que convierte cualquier estimulo externo (webhook, API, cola, cron) en un ActivationRequest. Vive en el borde, no en el nucleo."],
        ["Adaptador de canal (Channel Adapter)",
         "El traductor especializado en humanos: lleva la consulta a la app, chat, web o correo y trae la respuesta. Tambien es borde."],
        ["Adaptadores de protocolo y transporte",
         "Los traductores para hablar con otros agentes: adaptan un formato estandar (como A2A) y su medio de entrega (HTTP, websockets, gRPC). Intercambiables de forma independiente."],
        ["AgentCore",
         "Quien nace la ejecucion: crea el estado del run, su sesion, su traza y su presupuesto cuando el billete ya fue admitido y enrutado."],
        ["ContextEngine",
         "Quien decide que ve el modelo: empaqueta la memoria de forma selectiva; no se vuelca todo ni se filtra nada sin gobernanza."],
        ["ModelGateway",
         "Quien habla con el modelo de lenguaje: envia el contexto y recibe su propuesta (respuesta final o propuesta de usar una capacidad)."],
        ["AgentLoop",
         "El ritmo del agente: orquesta las rondas de razonar, proponer, verificar y observar hasta completar el trabajo."],
        ["CapabilityRegistry",
         "El catalogo: registra que capacidades existen y cual tiene cada agente. Si no esta en el catalogo, no existe."],
        ["PolicyEngine",
         "El juez de acciones: responde ALLOW, DENY o REQUIRE_APPROVAL a cada uso de capacidad. Ante el vacio, DENY."],
        ["ToolRuntime",
         "Quien ejecuta realmente la capacidad aprobada sobre el mundo y devuelve la observacion real, sin suposiciones."],
        ["SessionManager",
         "Quien guarda el punto de control de cada ronda: permite reanudar desde el ultimo punto si algo se cae."],
        ["ExecutionController",
         "Quien revisa presupuesto y condiciones antes de cada ronda y decide si se continua, se detiene o se cancela."],
        ["EventBus",
         "El repartidor de eventos: cada paso emite su huella y el bus la distribuye a quien la observa. Observa, nunca interviene."],
        ["HumanInteractionService",
         "El puente hacia las personas a mitad de trabajo: eleva la consulta de aprobacion, espera la respuesta y reanuda."],
        ["AgentCommunicationGateway",
         "La puerta para hablar con otros agentes: decide a que agente externo va un mensaje, sin acoplarse a un protocolo concreto."],
        ["IdempotencyGuard",
         "El guardian de los reintentos: detecta una peticion ya procesada y evita que un efecto se dispare dos veces."],
        ["CredentialBroker",
         "La caja fuerte de las credenciales: el modelo nunca toca la clave; las capacidades la usan de forma controlada y auditable."],
        ["AuditLedger",
         "La evidencia inmutable: distinta de los logs operativos, sirve para rendir cuentas sin mezclarse con el diagnostico."],
        ["DataGovernanceEngine",
         "El guardian de los datos: clasificacion, residencia, retencion y linaje se deciden fuera del modelo."],
        ["OperationalController",
         "Las palancas del operador: cancelar, deshabilitar, aislar, revertir o frenar todo, sin depender del modelo."],
        ["ExecutionFabricAdapter",
         "El disimulador de topologia: hace que el run se comporte igual en un proceso local, un worker o un cluster."],
        ["EvaluationHarness",
         "El laboratorio previo: los candidatos se evaluan antes de promoverse a produccion."],
        ["Routing",
         "El repartidor de destino: decide a que agente corresponde un billete ya admitido (concepto de la Enmienda v1.1)."],
    ]
    rows = []
    for i, r in enumerate(glossary):
        rows.append([
            Paragraph(r[0], S_CELL_HEAD if i == 0 else S_CELL_BOLD),
            Paragraph(r[1], S_CELL_HEAD if i == 0 else S_CELL),
        ])
    tbl = Table(rows, colWidths=[5.6 * cm, 11.0 * cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ALT_ROW]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Cuatro terminos mas aparecen en el documento y merecen su linea: tenant (cliente, "
        "area o unidad a la que pertenece una peticion), presupuesto (limite de uso "
        "asignado a una ejecucion), checkpoint (punto de control desde el que se puede "
        "reanudar) y deduplicacion (detectar que una peticion ya se proceso, para no "
        "repetirla).",
        S_NOTE))
    story.append(PageBreak())

    # ---------------- ANEXO ----------------
    story.append(Paragraph("Anexo - Los diagramas del flujo", S_H1))
    story.append(Paragraph(
        "Tres vistas complementarias. El Diagrama 1 describe como entra una peticion y "
        "pasa la aduana; el Diagrama 2 muestra el loop del agente y como vuelve la "
        "observacion real; el Diagrama 3 es un mapa de donde participa cada componente "
        "del glosario.",
        S_BODY))

    story.append(Paragraph("Diagrama 1 · El ingreso y la aduana", S_H2))
    story.append(Paragraph(
        "Cualquier medio produce el mismo billete (ActivationRequest) y toda peticion "
        "debe pasar por la aduana (AdmissionController). Por defecto, ante la duda se "
        "rechaza: REJECT significa que nada se ejecuta.",
        S_BODY))
    story.append(Spacer(1, 4))
    story.append(IngressDiagram())
    story.append(PageBreak())

    story.append(Paragraph("Diagrama 2 · El loop del agente", S_H2))
    story.append(Paragraph(
        "Una vez dentro, el agente razona y, cuando propone una capacidad, pasa por "
        "catalogo, politica y ejecucion. La observacion real vuelve a la memoria para "
        "armar el contexto de la siguiente ronda; cada ronda deja checkpoint y evento.",
        S_BODY))
    story.append(Spacer(1, 4))
    story.append(LoopDiagram())
    story.append(PageBreak())

    story.append(Paragraph("Diagrama 3 · Dónde participa cada componente", S_H2))
    story.append(Paragraph(
        "Mapa por tramo: que piezas forman parte del ingreso, cuales trabajan dentro "
        "del loop y cuales acompanan (custodian, observan, controlan y comunican) el "
        "viaje completo.",
        S_BODY))
    story.append(Spacer(1, 4))
    story.append(ParticipationMap())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Leyenda: el billete (ActivationRequest) es la unica entrada al nucleo. La "
        "aduana (AdmissionController) puede descartar la peticion sin que nada se "
        "ejecute. Enrutado y activado el agente, el ciclo de memoria, modelo y "
        "ejecucion de capacidades — con politica y observacion real en cada paso — se "
        "repite hasta completar, dejando un checkpoint en cada ronda.",
        S_NOTE))

    doc.multiBuild(story)


if __name__ == "__main__":
    build()
    print("PDF generado en:", OUT)
