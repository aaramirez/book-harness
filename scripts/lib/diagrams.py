# -*- coding: utf-8 -*-
"""Tres diagramas vectoriales del flujo del harness empresarial.

- IngressDiagram: el ingreso y la aduana (frontera, billete, admision, enrutamiento, activacion).
- LoopDiagram: el ciclo del agente (control, memoria, modelo, decision, capacidades, retorno).
- ParticipationMap: donde participa cada componente del glosario (mapa por tramos).

Usan solo fuentes Helvetica estandar con glifos WinAnsi (sin flechas Unicode, sin
sub/superindices): los conectores se dibujan como vectores.
"""

from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth

INK = HexColor("#1A2233")
NAVY = HexColor("#14324F")
AMBER = HexColor("#B45309")
AMBER_D = HexColor("#92400E")
SAND = HexColor("#FBF6EC")
TEAL = HexColor("#0E7490")
TEAL_L = HexColor("#E7F3F5")
BOX_BG = HexColor("#EEF2F6")
REJECT = HexColor("#B91C1C")
RULE = HexColor("#B9C4D0")
GRAY = HexColor("#4A5568")


class _Kit:
    """Ayudantes de dibujo sobre un canvas ya trasladado al origen del flowable."""

    def __init__(self, c, width):
        self.c = c
        self.W = width

    # ------------------------------------------------------------- primitivas
    def box(self, x, y, w, h, lines, fill=BOX_BG, border=NAVY, size=8.4,
            bold_first=False, bold_all=False, text_color=None):
        c = self.c
        c.setFillColor(fill)
        c.setStrokeColor(border)
        c.setLineWidth(1.05)
        c.roundRect(x, y, w, h, 5, stroke=1, fill=1)
        font = "Helvetica-Bold" if bold_first or bold_all else "Helvetica"
        size = self._fit(lines, font, size, w - 14)
        c.setFont(font, size)
        pitch = size * 1.55
        total = len(lines) * pitch
        top = y + (h + total) / 2.0
        for i, ln in enumerate(lines):
            c.setFillColor(text_color or (INK if i > 0 or not bold_first else NAVY))
            if bold_first and i == 0:
                c.setFont("Helvetica-Bold", size)
            else:
                c.setFont(font, size)
            c.drawCentredString(x + w / 2.0, top - (len(lines) - i) * pitch, ln)

    def _fit(self, lines, font, size, avail):
        if not lines:
            return size
        mx = max(stringWidth(l, font, size) for l in lines)
        if mx > avail and mx > 0:
            size = max(6.2, size * (avail / mx) * 0.985)
        return size

    def v(self, x, y_top, y_bot, color=NAVY, width=1.4):
        """Flecha vertical bajando, cabeza en y_bot."""
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.line(x, y_top - 2, x, y_bot + 2)
        p = c.beginPath()
        p.moveTo(x - 3, y_bot + 5)
        p.lineTo(x + 3, y_bot + 5)
        p.lineTo(x, y_bot - 1)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    def hu(self, x1, x2, y, color=NAVY, width=1.4):
        """Flecha horizontal hacia la derecha, cabeza en x2."""
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.line(x1, y, x2 - 2, y)
        p = c.beginPath()
        p.moveTo(x2 - 6, y - 3)
        p.lineTo(x2 - 6, y + 3)
        p.lineTo(x2 + 1, y)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    def slant(self, cx1, cy1, cx2, cy2, color=NAVY, width=1.4):
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        import math
        ang = math.atan2(cy2 - cy1, cx2 - cx1)
        head = 7
        bx = cx2 - head * math.cos(ang)
        by = cy2 - head * math.sin(ang)
        c.line(cx1, cy1, bx, by)
        p = c.beginPath()
        p.moveTo(bx + head * 0.3 * math.cos(ang - math.pi * 0.3),
                 by + head * 0.3 * math.sin(ang - math.pi * 0.3))
        p.lineTo(cx2, cy2)
        p.lineTo(bx + head * 0.3 * math.cos(ang + math.pi * 0.3),
                 by + head * 0.3 * math.sin(ang + math.pi * 0.3))
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    def dashed_v(self, x, y_bot, y_top, color=TEAL, width=1.0, head=True):
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.setDash(3, 3)
        c.line(x, y_bot, x, y_top)
        c.setDash()
        if head:
            c.setFillColor(color)
            p = c.beginPath()
            p.moveTo(x - 3, y_top - 6)
            p.lineTo(x + 3, y_top - 6)
            p.lineTo(x, y_top)
            p.close()
            c.drawPath(p, stroke=0, fill=1)

    def dashed_h(self, x1, y, x2, color=TEAL, width=1.0, head=True):
        c = self.c
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(width)
        c.setDash(3, 3)
        c.line(x1, y, x2, y)
        c.setDash()
        if head:
            p = c.beginPath()
            p.moveTo(x2 - 6, y - 3)
            p.lineTo(x2 - 6, y + 3)
            p.lineTo(x2, y)
            p.close()
            c.drawPath(p, stroke=0, fill=1)

    def diamond(self, cx, cy, w, h, lines, size=8.2):
        c = self.c
        c.setFillColor(SAND)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.05)
        p = c.beginPath()
        p.moveTo(cx, cy + h / 2.0)
        p.lineTo(cx + w / 2.0, cy)
        p.lineTo(cx, cy - h / 2.0)
        p.lineTo(cx - w / 2.0, cy)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        size = self._fit(lines, "Helvetica", size, w - 18)
        c.setFont("Helvetica", size)
        pitch = size * 1.5
        total = len(lines) * pitch
        top = cy + total / 2.0
        for i, ln in enumerate(lines):
            c.setFillColor(NAVY)
            c.drawCentredString(cx, top - (len(lines) - i) * pitch, ln)

    def tag(self, x, y, text, size=7.6, color=GRAY, bold=False, anchor="l"):
        c = self.c
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.setFillColor(color)
        if anchor == "l":
            c.drawString(x, y, text)
        elif anchor == "r":
            c.drawRightString(x, y, text)
        else:
            c.drawCentredString(x, y, text)

    def tag_v(self, x, y_bot, text, size=7.6, color=GRAY):
        """Texto vertical (de abajo hacia arriba) junto a una flecha punteada."""
        c = self.c
        c.saveState()
        c.translate(x, y_bot)
        c.rotate(90)
        c.setFont("Helvetica-Oblique", size)
        c.setFillColor(color)
        c.drawString(0, 0, text)
        c.restoreState()


# ================================================================= DIAGRAMA 1
class IngressDiagram(Flowable):
    """El ingreso y la aduana: frontera, billete, admision, enrutamiento, activacion."""

    def wrap(self, aw, ah):
        self.width = aw
        self.height = 630
        return self.width, self.height

    def draw(self):
        k = _Kit(self.canv, self.width)
        c = self.canv
        cx = self.width / 2.0

        k.box(cx - 220, 556, 440, 36,
              ["Cualquier medio: app · chat · web · API · webhook ·",
               "cola · cron · evento · otro agente"],
              fill=white, border=RULE, size=8.8, text_color=INK)
        k.v(cx, 550, 524)

        k.box(cx - 170, 470, 340, 50,
              ["Traductores de frontera",
               "Ingress Adapter · Channel Adapter (humanos)",
               "Protocol Adapter / Transport Adapter (otro agente)"],
              fill=white, border=AMBER, size=8.2, bold_first=True)
        k.v(cx, 464, 438)

        k.box(cx - 150, 404, 300, 30, ["ActivationRequest — el billete estándar"],
              fill=BOX_BG, border=NAVY, size=8.6, bold_all=True)
        k.v(cx, 398, 372)

        k.box(cx - 190, 268, 380, 100,
              ["AdmissionController — la aduana",
               "identidad · autorización · tenant · capacidad ·",
               "rate · presupuesto · deduplicación · política",
               "ADMIT (continúa)        REJECT (se descarta)"],
              fill=SAND, border=AMBER_D, size=8.0, bold_first=True)
        k.tag(cx - 180, 300, "por defecto, ante la duda: REJECT",
              size=7.2, color=REJECT, anchor="l")
        # rama REJECT (salida por la derecha, arriba)
        c.setStrokeColor(REJECT)
        c.setFillColor(REJECT)
        c.setLineWidth(1.2)
        c.setDash(3, 3)
        c.line(cx + 192, 360, cx + 210, 470)
        c.setDash()
        k.tag_v(cx + 216, 300, "REJECT: nada se ejecuta", size=7.6, color=REJECT)

        k.v(cx, 262, 236)
        k.tag(cx + 6, 242, "ADMIT", size=7.4, color=TEAL, bold=True, anchor="l")

        k.box(cx - 150, 190, 300, 30, ["Routing — ¿a qué agente corresponde?"],
              fill=BOX_BG, border=NAVY, size=8.6, bold_all=True)
        k.v(cx, 184, 158)

        k.box(cx - 160, 100, 320, 44, ["AgentCore — nace la ejecución",
                                       "estado · traza · presupuesto (el run empieza)"],
              fill=TEAL_L, border=TEAL, size=8.2, bold_first=True)
        k.tag(cx, 74, "aquí comienza el loop (Diagrama 2)", size=7.6, color=GRAY, anchor="c")


# ================================================================= DIAGRAMA 2
class LoopDiagram(Flowable):
    """El ciclo del agente con sus componentes y la vuelta de la observacion."""

    def wrap(self, aw, ah):
        self.width = aw
        self.height = 624
        return self.width, self.height

    def draw(self):
        k = _Kit(self.canv, self.width)
        c = self.canv
        cx = self.width / 2.0

        # ---- espina central
        k.box(cx - 150, 580, 300, 40,
              ["1 · Antes de razonar: presupuesto y condiciones",
               "ExecutionController: CONTINUE / STOP / CANCEL"],
              size=8.3, bold_first=True)
        k.v(cx, 576, 562)

        k.box(cx - 150, 520, 300, 40,
              ["2 · Memoria: ContextEngine arma el contexto",
               "no se vuelca todo: se empaqueta lo pertinente"],
              size=8.3, bold_first=True)
        k.v(cx, 516, 502)

        k.box(cx - 150, 460, 300, 40,
              ["3 · Modelo: ModelGateway lleva el contexto",
               "el modelo razona y propone"],
              size=8.3, bold_first=True)
        k.v(cx, 494, 440)

        k.diamond(cx, 407, 280, 54, ["¿Respuesta final", "o propone una capacidad?"])

        # ---- rama izquierda: cadena de capacidad
        k.slant(cx - 4, 375, cx - 105, 328)                # decision -> catalogo
        k.box(cx - 210, 288, 210, 40, ["Catálogo: CapabilityRegistry",
                                       "¿existe y la tiene el agente?"],
              size=8.0, bold_first=True)
        k.v(cx - 105, 284, 268)
        k.box(cx - 210, 228, 210, 40, ["Política: PolicyEngine",
                                       "ALLOW · DENY · REQUIRE_APPROVAL"],
              size=8.0, bold_first=True)
        k.v(cx - 105, 224, 208)
        k.box(cx - 210, 168, 210, 40, ["Ejecución: ToolRuntime",
                                       "se ejecuta · observación real"],
              size=8.0, bold_first=True)

        # nota humana por encima de la rama derecha
        k.tag(cx + 60, 348, "REQUIRE_APPROVAL: la persona aprueba", size=7.6, color=GRAY)
        k.tag(cx + 60, 338, "(HumanInteractionService) y el run se reanuda", size=7.6, color=GRAY)

        # ---- rama derecha: respuesta final
        k.slant(cx + 4, 378, cx + 105, 328)                # decision -> respuesta
        k.box(cx + 10, 288, 190, 40, ["Respuesta final", "el run llega a COMPLETED"],
              fill=TEAL_L, border=TEAL, size=8.0, bold_first=True)
        k.v(cx + 105, 284, 268)
        k.box(cx + 10, 228, 190, 40, ["Respuesta al canal original", "por donde entró la petición"],
              fill=TEAL_L, border=TEAL, size=8.0, bold_first=True)

        # ---- vuelta del loop: observacion real a la memoria
        k.dashed_v(16, 174, 554, color=TEAL)
        k.tag_v(22, 194, "la observación real vuelve a la memoria: se arma el contexto de la siguiente ronda",
                size=7.6, color=TEAL)

        # ---- franja inferior: checkpoint y eventos
        k.box(24, 44, 214, 36, ["SessionManager", "checkpoint por ronda (reanudable)"],
              size=8.0, bold_first=True)
        k.box(248, 44, 200, 36, ["EventBus", "cada paso emite su evento"],
              size=8.0, bold_first=True)


# ================================================================= DIAGRAMA 3
class ParticipationMap(Flowable):
    """Mapa: donde participa cada componente del glosario, por tramo del viaje."""

    BANDS = [
        ("ENTRADA — quién traduce el exterior y quién admite",
         "El mundo de la frontera y la aduana.",
         ["Ingress Adapter", "Channel Adapter", "Protocol Adapter", "Transport Adapter",
          "AdmissionController", "Routing"],
         NAVY),
        ("EL LOOP — quién trabaja en cada ronda",
         "Las piezas que hacen que el agente piense y actue.",
         ["ExecutionController", "ContextEngine", "ModelGateway", "AgentLoop",
          "CapabilityRegistry", "PolicyEngine", "ToolRuntime", "SessionManager"],
         TEAL),
        ("ACOMPAÑAN — quiénes custodian, observan y conectan",
         "Lo que sostiene, vigila, controla y comunica todo lo anterior.",
         ["EventBus", "AuditLedger", "IdempotencyGuard", "DataGovernanceEngine",
          "OperationalController", "CredentialBroker", "HumanInteractionService",
          "AgentCommunicationGateway", "ExecutionFabricAdapter", "EvaluationHarness"],
         AMBER_D),
    ]

    def _rows_for(self, pills, size, avail):
        rows = []
        cur, curw = [], 0
        for p in pills:
            w = stringWidth(p, "Helvetica", size) + 14
            if cur and curw + w > avail:
                rows.append(cur)
                cur, curw = [], 0
            cur.append((p, w))
            curw += w
        if cur:
            rows.append(cur)
        return rows

    def wrap(self, aw, ah):
        self.width = aw
        avail = aw - 24
        total = 0
        for _, _, pills, _ in self.BANDS:
            nrows = len(self._rows_for(pills, 7.8, avail))
            total += 34 + nrows * 24 + 16
        self.height = total + 6
        return self.width, self.height

    def draw(self):
        k = _Kit(self.canv, self.width)
        c = self.canv
        avail = self.width - 24
        y = self.height - 6

        for header, sub, pills, color in self.BANDS:
            nrows = len(self._rows_for(pills, 7.8, avail))
            band_h = 34 + nrows * 24 + 16
            y -= 34
            # cabecera
            c.setFillColor(color)
            c.setStrokeColor(color)
            c.setLineWidth(1.0)
            c.roundRect(8, y, self.width - 16, 30, 4, stroke=1, fill=1)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 8.8)
            c.drawString(18, y + 18 - 3, header)
            c.setFont("Helvetica-Oblique", 7.6)
            c.drawString(18, y + 6, sub)
            # pills
            yy = y - 24 + 4
            for row in self._rows_for(pills, 7.8, avail):
                x = 14
                for text, w in row:
                    k.box(x, yy - 4, w, 18, [text], fill=BOX_BG, border=RULE,
                          size=7.8, text_color=INK)
                    x += w + 6
                yy -= 24
            y -= nrows * 24 + 16
            # flecha hacia el siguiente tramo (salvo el ultimo)
            if self.BANDS.index((header, sub, pills, color)) < len(self.BANDS) - 1:
                k.v(self.width / 2.0, y + 12, y - 2, color=RULE, width=1.1)
                y -= 12