"""Motor de pixel art: arma un personaje por capas sobre un lienzo chico y lo exporta.

Cada personaje es un "muñeco de papel": primero un cuerpo base (cabeza, torso,
brazos, piernas) y luego piezas encima (pelo, ropa, armadura, armas). Todo se
dibuja con primitivas de Pillow sobre un lienzo de 40x56 píxeles.

Para que no se vea plano ("de plástico") el acabado hace cuatro cosas:
  1. Sombreado por zonas con volumen: cada zona de color se aclara arriba a la
     izquierda y se oscurece a la derecha y abajo, con una franja de tramado
     (dithering) en medio, como en los juegos de 16 bits.
  2. Una capa de detalle semitransparente encima (pliegues, mechones, placas
     de armadura) que respeta la sombra que ya hay debajo.
  3. Contorno de color: el borde toma un tono oscuro del color vecino, más
     claro arriba (donde pega la luz) que abajo.
  4. Brillo suave alrededor de los sables de luz.
"""
from collections import deque
from types import SimpleNamespace

from PIL import Image, ImageColor, ImageDraw

ANCHO, ALTO = 40, 56
SUELO = 54                 # fila de los pies; la 55 queda libre para el contorno
CENTRO = 20                # el eje del cuerpo pasa entre las columnas 19 y 20
CONTORNO = (28, 20, 36)
OJOS = "#241c28"
EMPUNADURA = "#b9bcc8"
CAPAS = ("fondo", "cuerpo", "frente", "detalle", "efectos")

# alto de cabeza, torso y piernas según la talla
TALLAS = {
    "adulto": (11, 13, 16),
    "alto": (11, 15, 19),
    "joven": (11, 12, 13),
    "nino": (10, 9, 10),
}
# ancho del torso según la complexión
COMPLEXION = {"delgado": 10, "normal": 12, "fornido": 14, "enorme": 16}

# color del filo y del núcleo de cada sable de luz
SABLES = {
    "azul": ("#3f9bff", "#e2f3ff"),
    "verde": ("#3fe86a", "#e6ffe9"),
    "rojo": ("#ff2b2b", "#ffe2e2"),
    "morado": ("#b45cff", "#f3e6ff"),
}

SOMBRA = (20, 8, 40, 75)       # trazo oscuro semitransparente de la capa de detalle
LUZ = (255, 250, 235, 70)      # trazo claro semitransparente


def rgba(color):
    """Convierte '#rrggbb' o una tupla RGB a una tupla RGBA opaca."""
    if isinstance(color, str):
        color = ImageColor.getrgb(color)
    return tuple(color[:3]) + (255,)


def oscurecer(c, f=0.72):
    """Sombra con un leve giro hacia el morado, como se hace en pixel art."""
    r, g, b, a = c
    return (int(r * f), int(g * f), min(255, int(b * f) + 14), a)


def aclarar(c, f=0.22):
    r, g, b, a = c
    return (r + int((255 - r) * f), g + int((255 - g) * f), b + int((255 - b) * f), a)


def tono(color, f):
    """Versión más oscura (f < 1) o más clara (f > 1) de un color, como '#rrggbb'."""
    c = rgba(color)
    c = oscurecer(c, f) if f < 1 else aclarar(c, f - 1)
    return "#%02x%02x%02x" % c[:3]


class Sprite:
    """Un personaje en construcción: capas de dibujo más la geometría de su cuerpo."""

    def __init__(self):
        self.capas = {n: Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0)) for n in CAPAS}
        self.fijos = {rgba(OJOS)}   # colores que no se sombrean (ojos, tatuajes finos)
        self.g = None
        self.piel = None

    # ---------- primitivas ----------
    def _d(self, capa):
        return ImageDraw.Draw(self.capas[capa])

    def rect(self, x0, y0, x1, y1, color, capa="cuerpo"):
        if x1 >= x0 and y1 >= y0:
            relleno = color if isinstance(color, tuple) and len(color) == 4 else rgba(color)
            self._d(capa).rectangle([x0, y0, x1, y1], fill=relleno)

    def pix(self, x, y, color, capa="cuerpo"):
        if 0 <= x < ANCHO and 0 <= y < ALTO:
            relleno = color if isinstance(color, tuple) and len(color) == 4 else rgba(color)
            self.capas[capa].putpixel((x, y), relleno)

    def pixs(self, puntos, color, capa="cuerpo"):
        for x, y in puntos:
            self.pix(x, y, color, capa)

    def poly(self, puntos, color, capa="cuerpo"):
        self._d(capa).polygon(puntos, fill=rgba(color))

    def elipse(self, x0, y0, x1, y1, color, capa="cuerpo"):
        self._d(capa).ellipse([x0, y0, x1, y1], fill=rgba(color))

    def linea(self, puntos, color, capa="cuerpo"):
        self._d(capa).line(puntos, fill=rgba(color), width=1)

    def quitar(self, x, y, capa="cuerpo"):
        if 0 <= x < ANCHO and 0 <= y < ALTO:
            self.capas[capa].putpixel((x, y), (0, 0, 0, 0))

    def fijo(self, color):
        """Registra un color de detalle para que el sombreado no lo toque."""
        self.fijos.add(rgba(color))
        return color

    def es(self, x, y, color, capa="cuerpo"):
        """¿El píxel (x, y) de la capa es de ese color?"""
        return 0 <= x < ANCHO and 0 <= y < ALTO and self.capas[capa].getpixel((x, y)) == rgba(color)

    def pliegues(self, x0, y0, x1, y1, color, cada=3, capa="cuerpo"):
        """Líneas verticales de pliegue, solo sobre los píxeles de ese color."""
        for x in range(x0 + 1, x1, cada):
            for y in range(y0 + 1, y1 + 1):
                if self.es(x, y, color, capa):
                    self.pix(x, y, SOMBRA, "detalle")

    # ---------- cuerpo base ----------
    def cuerpo(self, talla="adulto", complexion="normal", piel="#f0c8a0", torso="#888888",
               piernas="#555555", botas="#2e2624", brazos=None, manos=None, cabeza_ancho=10):
        """Dibuja el cuerpo de frente y guarda su geometría en self.g.

        Las cajas son (x0, y0, x1, y1) inclusivas. "i" y "d" son los lados
        izquierdo y derecho **de quien mira** la imagen.
        """
        alto_cab, alto_torso, alto_piernas = TALLAS[talla]
        ancho_torso = COMPLEXION[complexion]
        ancho_brazo = 4 if ancho_torso >= 14 else 3
        total = alto_cab + 1 + alto_torso + alto_piernas
        y0 = SUELO - total + 1

        cx0 = CENTRO - cabeza_ancho // 2
        cab = (cx0, y0, cx0 + cabeza_ancho - 1, y0 + alto_cab - 1)
        cuello = cab[3] + 1
        tx0 = CENTRO - ancho_torso // 2
        tor = (tx0, cuello + 1, tx0 + ancho_torso - 1, cuello + alto_torso)
        bi = (tor[0] - ancho_brazo, tor[1], tor[0] - 1, tor[3] + 1)
        bd = (tor[2] + 1, tor[1], tor[2] + ancho_brazo, tor[3] + 1)
        mi = (bi[0], bi[3] + 1, bi[2], bi[3] + 2)
        md = (bd[0], bd[3] + 1, bd[2], bd[3] + 2)
        pi = (tor[0] + 1, tor[3] + 1, CENTRO - 2, SUELO)
        pd = (CENTRO + 1, tor[3] + 1, tor[2] - 1, SUELO)
        self.g = SimpleNamespace(cab=cab, tor=tor, bi=bi, bd=bd, mi=mi, md=md, pi=pi, pd=pd,
                                 cin=tor[3] - 1, ojo_y=cab[1] + alto_cab // 2 + 1, cx=CENTRO,
                                 talla=talla, ancho_brazo=ancho_brazo)
        self.piel = piel

        brazos = brazos or torso
        manos = manos or piel
        for p in (pi, pd):
            self.rect(*p, piernas)
            self.rect(p[0], p[3] - 2, p[2], p[3], botas)
            self.rect(p[0], p[3], p[2], p[3], tono(botas, 0.6))          # suela
            self.pix(p[0], p[3] - 2, tono(botas, 1.35))                     # brillo de la bota
            self.pix(p[0] + 1, p[1] + (p[3] - p[1]) // 2 - 1, SOMBRA, "detalle")   # rodilla
        self.rect(*tor, torso)
        for b in (bi, bd):
            self.rect(*b, brazos)
            self.pix(b[0] + 1, b[1] + (b[3] - b[1]) // 2, SOMBRA, "detalle")     # codo
        for m in (mi, md):
            self.rect(*m, manos)
        self.quitar(bi[0], bi[1])
        self.quitar(bd[2], bd[1])
        self.rect(CENTRO - 2, cuello, CENTRO + 1, cuello, piel)
        self.rect(CENTRO - 2, tor[1], CENTRO + 1, tor[1], SOMBRA, "detalle")     # sombra de la barbilla
        self.rect(*cab, piel)
        for x, y in ((cab[0], cab[1]), (cab[2], cab[1]), (cab[0], cab[3]), (cab[2], cab[3])):
            self.quitar(x, y)
        return self.g

    # ---------- cara y pelo ----------
    def cara(self, ojos=OJOS, boca=None, alto_ojo=2, cejas=None):
        """Ojos, cejas, nariz y boca. Las cejas, la nariz y la boca solo se
        pintan donde se ve piel (no encima de un casco, máscara o barba)."""
        g = self.g
        self.fijo(ojos)
        for x in (CENTRO - 3, CENTRO + 2):
            self.rect(x, g.ojo_y, x, g.ojo_y + alto_ojo - 1, ojos)
        if self.piel is None:
            return
        ceja = self.fijo(cejas or tono(self.piel, 0.62))
        for x in (CENTRO - 4, CENTRO - 3, CENTRO + 2, CENTRO + 3):
            if self.es(x, g.ojo_y - 2, self.piel):
                self.pix(x, g.ojo_y - 2, ceja)
        nariz = self.fijo(tono(self.piel, 0.8))
        if self.es(CENTRO, g.ojo_y + 2, self.piel):
            self.pix(CENTRO, g.ojo_y + 2, nariz)
        y_boca = g.cab[3] - 1
        color_boca = self.fijo(boca or tono(self.piel, 0.66))
        if boca or self.es(CENTRO - 1, y_boca, self.piel):
            self.rect(CENTRO - 1, y_boca, CENTRO, y_boca, color_boca)

    def ojos_brillantes(self, color):
        """Ojos que brillan (Sith, droides): van en la capa de efectos, sin contorno."""
        g = self.g
        for x in (CENTRO - 3, CENTRO + 2):
            self.rect(x, g.ojo_y, x, g.ojo_y + 1, color, "efectos")

    def _mechones(self, x0, y0, x1, y1):
        """Mechones oscuros y un brillo arriba a la izquierda sobre el pelo."""
        for x in range(x0 + 2, x1, 3):
            self.pix(x, y0 + 1, SOMBRA, "detalle")
            self.pix(x, y0 + 2, SOMBRA, "detalle")
        self.rect(x0 + 2, y0, x0 + 3, y0, LUZ, "detalle")
        self.pix(x0 + 1, y0 + 1, LUZ, "detalle")

    def pelo(self, estilo, color):
        x0, y0, x1, y1 = self.g.cab
        c = color
        if estilo == "rapado":
            self.rect(x0 + 1, y0, x1 - 1, y0 + 1, c)
            self.pixs([(x0, y0 + 2), (x1, y0 + 2)], c)
            self.rect(x0 + 2, y0, x0 + 3, y0, LUZ, "detalle")
        elif estilo in ("corto", "ondulado", "largo", "chongo", "coleta", "trenza"):
            self.rect(x0 + 1, y0 - 1, x1 - 1, y0 - 1, c)
            self.rect(x0, y0, x1, y0 + 2, c)
            self.rect(x0, y0 + 3, x0, y0 + 5, c)
            self.rect(x1, y0 + 3, x1, y0 + 5, c)
            self.pix(x0 + 1, y0 + 3, c)
            if estilo == "ondulado":
                self.rect(x0 - 1, y0 + 1, x0 - 1, y1 - 1, c)
                self.rect(x1 + 1, y0 + 1, x1 + 1, y1 - 1, c)
                self.rect(x0, y0 + 6, x0, y1 - 2, c)
                self.rect(x1, y0 + 6, x1, y1 - 2, c)
                self.pixs([(x0 + 2, y0 + 3), (x1 - 1, y0 + 3)], c)
            elif estilo == "largo":
                self.rect(x0 - 1, y0 + 1, x0, y1 + 4, c)
                self.rect(x1, y0 + 1, x1 + 1, y1 + 4, c)
                for x in (x0 - 1, x1 + 1):
                    self.pixs([(x, y0 + 5), (x, y0 + 9)], SOMBRA, "detalle")
            elif estilo == "chongo":
                self.rect(CENTRO - 2, y0 - 4, CENTRO + 1, y0 - 1, c)
                self.rect(CENTRO - 3, y0 - 3, CENTRO + 2, y0 - 2, c)
                self.pix(CENTRO - 2, y0 - 3, LUZ, "detalle")
            elif estilo == "coleta":
                self.rect(x1 + 1, y0 + 2, x1 + 1, y1 + 6, c)
                self.rect(x1, y1 + 1, x1 + 1, y1 + 2, c)
            elif estilo == "trenza":
                self.rect(x1 + 1, y0 + 3, x1 + 1, y1 + 5, c)
                for y in range(y0 + 4, y1 + 5, 2):
                    self.pix(x1 + 1, y, SOMBRA, "detalle")
            self._mechones(x0, y0 - 1, x1, y0 + 2)
        elif estilo == "rastas":
            self.rect(x0, y0 - 1, x1, y0 + 2, c)
            for i, x in enumerate((x0 - 2, x0 - 1, x0, x1, x1 + 1, x1 + 2)):
                largo = y1 + (6 if i in (0, 5) else 4)
                self.rect(x, y0 + 1, x, largo, c)
                for y in range(y0 + 2 + i % 2, largo, 3):
                    self.pix(x, y, SOMBRA, "detalle")
            self._mechones(x0, y0 - 1, x1, y0 + 2)
        elif estilo == "receso":
            self.rect(x0, y0 + 1, x0, y0 + 5, c)
            self.rect(x1, y0 + 1, x1, y0 + 5, c)
            self.rect(x0 + 1, y0, x0 + 2, y0, c)
            self.rect(x1 - 2, y0, x1 - 1, y0, c)

    def barba(self, estilo, color):
        x0, y0, x1, y1 = self.g.cab
        if estilo == "corta":
            self.rect(x0, y1 - 3, x0, y1, color)
            self.rect(x1, y1 - 3, x1, y1, color)
            self.rect(x0 + 1, y1 - 1, x1 - 1, y1 + 1, color)
            self.rect(CENTRO - 2, y1 - 2, CENTRO + 1, y1 - 2, color)
            self.pixs([(x0 + 2, y1), (x0 + 5, y1 + 1), (x1 - 2, y1)], SOMBRA, "detalle")
        elif estilo == "larga":
            self.rect(x0, y1 - 3, x0, y1, color)
            self.rect(x1, y1 - 3, x1, y1, color)
            self.rect(x0 + 1, y1 - 1, x1 - 1, y1, color)
            self.rect(x0 + 1, y1 + 1, x1 - 1, y1 + 4, color)
            self.rect(x0 + 3, y1 + 5, x1 - 3, y1 + 7, color)
            self.rect(CENTRO - 1, y1 - 2, CENTRO, y1 - 2, "#7a4a3a")
            for x in range(x0 + 2, x1 - 1, 2):
                self.pix(x, y1 + 2 + x % 3, SOMBRA, "detalle")
        elif estilo == "bigote":
            self.rect(CENTRO - 2, y1 - 2, CENTRO + 1, y1 - 2, self.fijo(color))
        elif estilo == "candado":
            self.rect(CENTRO - 2, y1 - 1, CENTRO + 1, y1 + 1, color)

    # ---------- ropa ----------
    def cinturon(self, color, hebilla=None):
        g = self.g
        self.rect(g.tor[0], g.cin, g.tor[2], g.cin + 1, color)
        bolsa = tono(color, 0.7)
        for x in (g.tor[0] + 1, g.tor[2] - 2):
            self.rect(x, g.cin, x + 1, g.cin + 2, bolsa)
        self.rect(g.tor[0], g.cin + 2, g.tor[2], g.cin + 2, SOMBRA, "detalle")
        if hebilla:
            self.rect(CENTRO - 1, g.cin, CENTRO, g.cin + 1, hebilla)

    def tabardo(self, color, largo=5):
        g = self.g
        for x in (g.tor[0] + 2, g.tor[2] - 3):
            self.rect(x, g.tor[1], x + 1, g.cin + largo, color)
        # cruce de la túnica Jedi a la altura del pecho
        self.pixs([(CENTRO - 2, g.tor[1] + 2), (CENTRO - 1, g.tor[1] + 3), (CENTRO + 1, g.tor[1] + 2),
                   (CENTRO, g.tor[1] + 3)], SOMBRA, "detalle")

    def escote(self, color):
        g = self.g
        self.rect(CENTRO - 1, g.tor[1], CENTRO, g.tor[1] + 1, color)

    def faldon(self, color, largo=5):
        """Parte baja de la túnica que cae sobre los muslos."""
        g = self.g
        self.rect(g.tor[0], g.cin + 2, g.tor[2], g.cin + 1 + largo, color)
        self.pliegues(g.tor[0], g.cin + 2, g.tor[2], g.cin + 1 + largo, color)

    def tunica_larga(self, color, desde=None, abierta=None):
        """Túnica, vestido o abrigo hasta el suelo (tapa las piernas)."""
        g = self.g
        y = desde if desde is not None else g.cin
        self.poly([(g.tor[0], y), (g.tor[2], y), (g.tor[2] + 2, SUELO), (g.tor[0] - 2, SUELO)], color)
        if abierta:
            self.poly([(CENTRO - 1, y + 2), (CENTRO, y + 2), (CENTRO + 2, SUELO), (CENTRO - 3, SUELO)], abierta)
        self.pliegues(g.tor[0] - 2, y + 2, g.tor[2] + 2, SUELO - 1, color, cada=3)
        self.rect(CENTRO - 4, SUELO, CENTRO - 2, SUELO, "#2e2624")
        self.rect(CENTRO + 1, SUELO, CENTRO + 3, SUELO, "#2e2624")

    def capa(self, color):
        g = self.g
        self.poly([(g.bi[0], g.tor[1]), (g.bd[2], g.tor[1]), (g.bd[2] + 4, SUELO), (g.bi[0] - 4, SUELO)],
                  color, "fondo")
        pliegue = self.fijo(tono(color, 0.74))
        for x in (g.bi[0] - 2, g.bd[2] + 2):
            for y in range(g.tor[3], SUELO):
                if self.es(x, y, color, "fondo"):
                    self.pix(x, y, pliegue, "fondo")

    def capucha(self, color, cara_sombra=None):
        x0, y0, x1, y1 = self.g.cab
        self.rect(x0 - 1, y0 - 2, x1 + 1, y0 + 1, color)
        self.rect(x0 - 2, y0 + 1, x0, y1 + 2, color)
        self.rect(x1, y0 + 1, x1 + 2, y1 + 2, color)
        self.rect(x0 + 1, y0 - 3, x1 - 1, y0 - 3, color)
        self.rect(x0 + 1, y0 + 2, x1 - 1, y0 + 2, SOMBRA, "detalle")
        if cara_sombra:
            self.rect(x0 + 1, y0 + 2, x1 - 1, y1 - 2, self.fijo(cara_sombra))

    def hombreras(self, color, alto=3):
        g = self.g
        for b in (g.bi, g.bd):
            self.rect(b[0], b[1], b[2], b[1] + alto - 1, color)
            self.rect(b[0], b[1] + alto - 1, b[2], b[1] + alto - 1, SOMBRA, "detalle")

    def armadura_clon(self, marca, kama=None, marcas_piernas=True):
        """Marcas de la legión y placas sobre la armadura blanca del cuerpo base."""
        g = self.g
        traje = "#2c2c36"
        self.hombreras(marca)
        for b in (g.bi, g.bd):
            self.rect(b[0], b[1] + 6, b[2], b[1] + 6, traje)
        self.rect(CENTRO - 1, g.tor[1] + 1, CENTRO, g.tor[1] + 5, marca)
        self.rect(g.tor[0], g.cin - 1, g.tor[2], g.cin - 1, traje)
        self.cinturon("#4a4a55")
        # placas: pecho, abdomen y muslos
        self.rect(g.tor[0] + 1, g.tor[1] + 6, g.tor[2] - 1, g.tor[1] + 6, SOMBRA, "detalle")
        self.rect(CENTRO - 3, g.tor[1] + 8, CENTRO + 2, g.tor[1] + 8, SOMBRA, "detalle")
        self.pixs([(g.tor[0] + 1, g.tor[1] + 1), (g.tor[0] + 2, g.tor[1] + 1), (g.tor[0] + 1, g.tor[1] + 2)],
                  LUZ, "detalle")
        for p in (g.pi, g.pd):
            self.rect(p[0], p[1] + 5, p[2], p[1] + 5, traje)
            self.rect(p[0], p[1] + 2, p[2], p[1] + 2, SOMBRA, "detalle")
            if marcas_piernas:
                self.rect(p[0], p[1] + 7, p[2], p[1] + 8, marca)
        if kama:
            for x0, x1 in ((g.tor[0] - 2, g.tor[0]), (g.tor[2], g.tor[2] + 2)):
                self.rect(x0, g.cin + 2, x1, g.cin + 10, kama, "frente")
                self.rect(x0, g.cin + 10, x1, g.cin + 10, marca, "frente")

    # ---------- cabezas especiales ----------
    def montrales(self, base, raya, lekku=True):
        x0, y0, x1, y1 = self.g.cab
        # cuerno de la izquierda, de abajo hacia arriba: (dy, desde, hasta) relativo a x0
        forma = [(1, -1, 2), (0, -1, 2), (-1, -1, 1), (-2, -1, 1), (-3, 0, 1), (-4, 0, 1), (-5, 1, 2), (-6, 2, 2)]
        for dy, a, b in forma:
            col = raya if dy in (-1, -4) else base
            self.rect(x0 + a, y0 + dy, x0 + b, y0 + dy, col)
            self.rect(x1 - b, y0 + dy, x1 - a, y0 + dy, col)
        if lekku:
            tor = self.g.tor
            for xa in (x0 - 1, x1):
                for y in range(y0 + 4, tor[1] + 9):
                    col = raya if (y - y0) % 4 in (0, 1) else base
                    self.rect(xa, y, xa + 1, y, col, "frente")

    def lekku(self, color, raya=None):
        x0, y0, x1, y1 = self.g.cab
        tor = self.g.tor
        for xa in (x0 - 2, x1 + 1):
            self.rect(xa, y0 + 2, xa + 1, tor[1] + 8, color)
            self.pix(xa + (1 if xa < x0 else 0), tor[1] + 9, color)
            for y in range(y0 + 5, tor[1] + 8, 4):
                self.pix(xa, y, SOMBRA, "detalle")
            if raya:
                self.rect(xa, tor[1] + 3, xa + 1, tor[1] + 3, raya)
        self.rect(x0, y0 - 1, x1, y0 + 1, color)

    def tentaculos(self, color, oscuro):
        x0, y0, x1, y1 = self.g.cab
        tor = self.g.tor
        self.rect(x0 + 1, y0 - 1, x1 - 1, y0, color)
        for i, xa in enumerate((x0 - 3, x0 - 2, x0 - 1, x1 + 1, x1 + 2, x1 + 3)):
            largo = tor[1] + (2 if i in (0, 5) else 7)
            self.rect(xa, y0 + 1 + (i in (0, 5)) * 3, xa, largo, oscuro if i in (1, 4) else color)

    def cuernos(self, color, puntos):
        x0, y0, _, _ = self.g.cab
        for dx, alto in puntos:
            self.rect(x0 + dx, y0 - alto, x0 + dx, y0 - 1, color)

    def orejas(self, color, largo=4, y=None, hacia_arriba=False):
        x0, y0, x1, y1 = self.g.cab
        yo = y if y is not None else self.g.ojo_y - 1
        alza = -2 if hacia_arriba else 0
        self.poly([(x0, yo), (x0 - largo, yo + alza - 1), (x0, yo + 3)], color)
        self.poly([(x1, yo), (x1 + largo, yo + alza - 1), (x1, yo + 3)], color)

    def sombrero(self, color, banda=None):
        x0, y0, x1, y1 = self.g.cab
        self.rect(x0 - 4, y0 + 1, x1 + 4, y0 + 2, color)
        self.rect(x0, y0 - 4, x1, y0 + 1, color)
        self.rect(x0 - 4, y0 + 3, x1 + 4, y0 + 3, SOMBRA, "detalle")
        if banda:
            self.rect(x0, y0, x1, y0, banda)

    def gafas(self, marco, lente, y=None):
        x0, y0, x1, y1 = self.g.cab
        yy = y if y is not None else self.g.ojo_y
        self.rect(x0, yy, x1, yy + 1, marco)
        self.rect(CENTRO - 4, yy, CENTRO - 2, yy + 1, self.fijo(lente))
        self.rect(CENTRO + 1, yy, CENTRO + 3, yy + 1, lente)
        self.pixs([(CENTRO - 4, yy), (CENTRO + 1, yy)], LUZ, "detalle")

    def casco_completo(self, base, visor, marca=None):
        """Casco de clon puesto: tapa la cabeza entera con el visor en T."""
        x0, y0, x1, y1 = self.g.cab
        self.rect(x0, y0 - 1, x1, y1, base)
        self.rect(x0 - 1, y0 + 2, x1 + 1, y1, base)
        self.rect(x0 + 1, self.g.ojo_y - 1, x1 - 1, self.g.ojo_y, self.fijo(visor))
        self.rect(CENTRO - 1, self.g.ojo_y, CENTRO, y1 - 2, visor)
        self.pixs([(x0 + 1, y0), (x0 + 2, y0), (x0 + 1, y0 + 1)], LUZ, "detalle")
        if marca:
            self.rect(CENTRO - 1, y0 - 1, CENTRO, self.g.ojo_y - 2, marca)

    # ---------- objetos ----------
    def _mano(self, lado):
        return self.g.mi if lado == "i" else self.g.md

    def sable(self, color, lado="i", largo=13, doble=False):
        m = self._mano(lado)
        x = m[0] + 1
        self.rect(x, m[1] - 2, x, m[3], EMPUNADURA, "frente")
        self.pix(x, m[1] - 1, "#4a4a55", "frente")
        filo, nucleo = SABLES[color]
        halo = rgba(filo)[:3] + (80,)
        tope = m[1] - 3
        tramos = [(tope - largo + 1, tope)]
        if doble:
            tramos.append((m[3] + 1, SUELO))
        for a, b in tramos:
            self.rect(x - 2, a + 1, x + 2, b, halo, "efectos")
            self.rect(x - 1, a + 1, x + 1, b, filo, "efectos")
            self.rect(x, a, x, b, nucleo, "efectos")

    def pistola(self, lado="d", color="#3a3a44"):
        m = self._mano(lado)
        if lado == "d":
            self.rect(m[2], m[1], m[2] + 3, m[1] + 1, color, "frente")
            self.pix(m[2] + 1, m[1] + 2, color, "frente")
            self.pix(m[2] + 3, m[1], "#8a8a96", "frente")
        else:
            self.rect(m[0] - 3, m[1], m[0], m[1] + 1, color, "frente")
            self.pix(m[0] - 1, m[1] + 2, color, "frente")
            self.pix(m[0] - 3, m[1], "#8a8a96", "frente")

    def funda(self, lado="d", color="#3a3a44"):
        p = self.g.pi if lado == "i" else self.g.pd
        x = p[0] - 1 if lado == "i" else p[2] + 1
        self.rect(x, p[1] + 1, x, p[1] + 4, color, "frente")

    def rifle(self, lado="d", color="#3a3a44", largo=16):
        m = self._mano(lado)
        x = m[2] + 1 if lado == "d" else m[0] - 2
        self.rect(x, m[1] - largo + 4, x + 1, m[3] + 2, color, "frente")
        self.rect(x, m[1] - largo + 6, x + 1, m[1] - largo + 7, "#6a6a78", "frente")
        self.rect(x, m[1] - largo + 4, x, m[3] + 2, LUZ, "detalle")

    def arma_pesada(self, color="#4a4a55"):
        m = self.g.md
        self.rect(m[0] - 6, m[1] - 3, m[2] + 3, m[1] - 1, color, "frente")
        self.rect(m[2] + 1, m[1] - 4, m[2] + 3, m[1] + 1, color, "frente")
        self.rect(m[0] - 6, m[1] - 3, m[2] + 3, m[1] - 3, LUZ, "detalle")

    def baston(self, lado="d", color="#7a5a3a", alto=None, punta=None):
        m = self._mano(lado)
        x = m[2] + 1 if lado == "d" else m[0] - 1
        tope = alto if alto is not None else self.g.cab[1] + 2
        self.rect(x, tope, x, SUELO, color, "frente")
        if punta:
            self.rect(x - 1, tope - 2, x + 1, tope, punta, "frente")

    def casco_bajo_brazo(self, marca, base="#e8e8ee", visor="#22222a", antena=False):
        m = self.g.mi
        hx1 = m[0] + 1
        hx0 = hx1 - 7
        hy1 = m[3] + 1
        hy0 = hy1 - 7
        self.rect(hx0, hy0 + 1, hx1, hy1, base, "frente")
        self.rect(hx0 + 1, hy0, hx1 - 1, hy0, base, "frente")
        self.rect(hx0 + 3, hy0, hx0 + 4, hy0 + 2, marca, "frente")
        self.fijo(visor)
        self.rect(hx0 + 1, hy0 + 3, hx1 - 1, hy0 + 3, visor, "frente")
        self.rect(hx0 + 3, hy0 + 4, hx0 + 4, hy1 - 1, visor, "frente")
        self.rect(hx0, hy1, hx1, hy1, marca, "frente")
        self.pixs([(hx0 + 1, hy0 + 1), (hx0 + 2, hy0 + 1)], LUZ, "detalle")
        if antena:
            self.rect(hx0, hy0 - 3, hx0, hy0, "#c0c0c8", "frente")

    def mochila(self, color, alto=10):
        g = self.g
        self.rect(g.tor[0] - 2, g.tor[1] - 2, g.tor[2] + 2, g.tor[1] + alto, color, "fondo")

    # ---------- acabado ----------
    def _sombrear(self, img):
        """Volumen por zonas: luz arriba a la izquierda, sombra a la derecha y abajo,
        con una franja de tramado entre la luz y la sombra."""
        src = img.load()
        out = img.copy()
        dst = out.load()
        visto = set()

        def distinto(x, y, c):
            return not (0 <= x < ANCHO and 0 <= y < ALTO) or src[x, y] != c

        for sy in range(ALTO):
            for sx in range(ANCHO):
                c = src[sx, sy]
                if (sx, sy) in visto or c[3] == 0 or c in self.fijos:
                    continue
                zona, cola = [], deque([(sx, sy)])
                visto.add((sx, sy))
                while cola:
                    x, y = cola.popleft()
                    zona.append((x, y))
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if (nx, ny) not in visto and not distinto(nx, ny, c):
                            visto.add((nx, ny))
                            cola.append((nx, ny))
                xs = [p[0] for p in zona]
                ys = [p[1] for p in zona]
                x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
                w, h = x1 - x0 + 1, y1 - y0 + 1
                es_piel = self.piel is not None and c == rgba(self.piel)
                for x, y in zona:
                    nivel = 0
                    if w >= 6:
                        rel = (x - x0) / (w - 1)
                        if rel >= (0.8 if es_piel else 0.74):
                            nivel = 1
                        elif not es_piel and rel >= 0.56 and (x + y) % 2 == 0:
                            nivel = 1
                        elif rel <= 0.16:
                            nivel = -1
                    if h >= 10 and (y - y0) / (h - 1) >= 0.82:
                        nivel = max(nivel, 1)
                    borde_osc = (distinto(x + 1, y, c) and not distinto(x - 1, y, c)) or \
                                (distinto(x, y + 1, c) and not distinto(x, y - 1, c))
                    borde_luz = (distinto(x - 1, y, c) and not distinto(x + 1, y, c)) or \
                                (distinto(x, y - 1, c) and not distinto(x, y + 1, c))
                    if borde_osc:
                        nivel = 2 if nivel == 1 else 1
                    elif borde_luz and nivel <= 0:
                        nivel = -1
                    if nivel == -1:
                        dst[x, y] = aclarar(c, 0.24)
                    elif nivel == 1:
                        dst[x, y] = oscurecer(c, 0.8)
                    elif nivel == 2:
                        dst[x, y] = oscurecer(c, 0.64)
        return out

    def _contornear(self, img):
        """Contorno de color: un tono muy oscuro del vecino; más claro arriba."""
        src = img.load()
        out = img.copy()
        dst = out.load()
        for y in range(ALTO):
            for x in range(ANCHO):
                if src[x, y][3]:
                    continue
                # el vecino de abajo primero: si el borde está ENCIMA de la figura, le pega la luz
                for nx, ny, f in ((x, y + 1, 0.42), (x + 1, y, 0.32), (x - 1, y, 0.32), (x, y - 1, 0.24)):
                    if 0 <= nx < ANCHO and 0 <= ny < ALTO and src[nx, ny][3]:
                        r, g, b, _ = src[nx, ny]
                        dst[x, y] = (int(r * f * 0.6 + CONTORNO[0] * 0.4),
                                     int(g * f * 0.6 + CONTORNO[1] * 0.4),
                                     int(b * f * 0.6 + CONTORNO[2] * 0.4), 255)
                        break
        return out

    def terminar(self):
        """Une las capas, sombrea, pone el detalle, el contorno y encima los efectos."""
        img = self.capas["fondo"].copy()
        img.alpha_composite(self.capas["cuerpo"])
        img.alpha_composite(self.capas["frente"])
        img = self._sombrear(img)
        img.alpha_composite(self.capas["detalle"])
        img = self._contornear(img)
        img.alpha_composite(self.capas["efectos"])
        return img
