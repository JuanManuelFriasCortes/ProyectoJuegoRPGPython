"""Motor de escenarios en pixel art: piezas para pintar fondos de 320x180 con código.

Cada escenario se pinta de atrás hacia adelante sobre un lienzo de 320x180:
cielo con degradado tramado, capas de montañas o edificios, interiores en
perspectiva, vegetación, efectos de luz y niebla. Todo usa la misma semilla
aleatoria por escenario, así que el resultado es idéntico cada vez que se corre.
"""
import math
import random

from PIL import Image, ImageColor, ImageDraw

ANCHO, ALTO = 320, 180
PASOS = 24      # lo que parpadea (fuego, estrellas, relámpagos) cambia 24 veces por ciclo: 10 por segundo

# matriz de Bayer 4x4: decide qué píxeles cambian de color en un degradado tramado
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def rgb(color):
    if isinstance(color, str):
        return ImageColor.getrgb(color)[:3]
    return tuple(color[:3])


def rgba(color, alfa=255):
    return rgb(color) + (alfa,)


def mezclar(c1, c2, t):
    a, b = rgb(c1), rgb(c2)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def oscuro(color, f=0.72):
    r, g, b = rgb(color)
    return (int(r * f), int(g * f), min(255, int(b * f) + 10))


def claro(color, f=0.25):
    r, g, b = rgb(color)
    return (r + int((255 - r) * f), g + int((255 - g) * f), b + int((255 - b) * f))


class Escena:
    """Un fondo en construcción.

    Para animar, el mismo escenario se dibuja una vez por cuadro con `t` = 0, 1, ...,
    `cuadros` - 1. La parte fija sale idéntica en todos los cuadros porque `self.rnd`
    se consume igual cada vez; solo los elementos vivos (fuego, humo, láseres, lluvia,
    partículas, luces) usan `self.fase`, que va de 0 a 1 a lo largo del ciclo. Todo lo
    que se mueve vuelve a su lugar al terminar el ciclo, así el bucle no brinca.

    El ciclo se puede dibujar con más cuadros (144 para 60 fps): lo que se desplaza usa
    `fase` y se ve fluido, y lo que parpadea usa `self.t`, que siempre va de 0 a PASOS - 1
    para que el fuego y las estrellas no titilen seis veces más rápido.
    """

    def __init__(self, semilla, t=0, cuadros=1):
        self.img = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 255))
        self.rnd = random.Random(semilla)
        self.semilla, self.cuadro, self.cuadros = semilla, t, cuadros
        self.t = t * PASOS // cuadros if cuadros > 1 else t     # paso del parpadeo

    # ---------- tiempo ----------
    @property
    def animado(self):
        return self.cuadros > 1

    @property
    def fase(self):
        """Avance del ciclo, de 0 (primer cuadro) a casi 1 (último)."""
        return self.cuadro / self.cuadros

    def onda(self, desfase=0.0, vueltas=1):
        """Seno que da `vueltas` vueltas completas por ciclo (0 si no hay animación)."""
        if not self.animado:
            return 0.0
        return math.sin(2 * math.pi * (self.fase * vueltas + desfase))

    def azar_cuadro(self, *clave):
        """Generador aleatorio propio de este cuadro y este elemento: varía entre cuadros
        sin tocar `self.rnd` (que debe consumirse igual en todos)."""
        return random.Random(hash((self.semilla, self.t) + tuple(int(c) for c in clave)))

    # ---------- primitivas ----------
    @property
    def d(self):
        return ImageDraw.Draw(self.img)

    def rect(self, x0, y0, x1, y1, c):
        if x1 >= x0 and y1 >= y0:
            self.d.rectangle([x0, y0, x1, y1], fill=rgba(c))

    def pix(self, x, y, c):
        if 0 <= x < ANCHO and 0 <= y < ALTO:
            self.img.putpixel((int(x), int(y)), rgba(c))

    def poly(self, puntos, c):
        self.d.polygon(puntos, fill=rgba(c))

    def elipse(self, x0, y0, x1, y1, c):
        self.d.ellipse([x0, y0, x1, y1], fill=rgba(c))

    def linea(self, puntos, c, grosor=1):
        self.d.line(puntos, fill=rgba(c), width=grosor)

    def capa(self, dibujo):
        """Dibuja con transparencia: `dibujo(draw)` pinta sobre una capa que luego se mezcla."""
        capa = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
        dibujo(ImageDraw.Draw(capa))
        self.img.alpha_composite(capa)

    # ---------- degradados y texturas ----------
    def degradado(self, x0, y0, x1, y1, colores):
        """Degradado vertical entre varios colores, con tramado de Bayer en cada transición."""
        px = self.img.load()
        cols = [rgba(c) for c in colores]
        alto = max(1, y1 - y0)
        for y in range(max(0, y0), min(ALTO, y1 + 1)):
            t = (y - y0) / alto * (len(cols) - 1)
            i = min(int(t), len(cols) - 2)
            f = t - i
            for x in range(max(0, x0), min(ANCHO, x1 + 1)):
                px[x, y] = cols[i + 1] if f * 16 > BAYER[y % 4][x % 4] + 0.5 else cols[i]

    def degradado_horizontal(self, x0, y0, x1, y1, colores):
        px = self.img.load()
        cols = [rgba(c) for c in colores]
        ancho = max(1, x1 - x0)
        for x in range(max(0, x0), min(ANCHO, x1 + 1)):
            t = (x - x0) / ancho * (len(cols) - 1)
            i = min(int(t), len(cols) - 2)
            f = t - i
            for y in range(max(0, y0), min(ALTO, y1 + 1)):
                px[x, y] = cols[i + 1] if f * 16 > BAYER[y % 4][x % 4] + 0.5 else cols[i]

    def textura(self, x0, y0, x1, y1, colores, prob=0.08, base=None):
        """Salpica píxeles de otros tonos (piedra, arena, metal gastado).
        Si `base` se da, solo cambia los píxeles que son de ese color."""
        px = self.img.load()
        objetivo = rgba(base) if base else None
        for y in range(max(0, y0), min(ALTO, y1 + 1)):
            for x in range(max(0, x0), min(ANCHO, x1 + 1)):
                if self.rnd.random() < prob and (objetivo is None or px[x, y] == objetivo):
                    px[x, y] = rgba(self.rnd.choice(colores))

    def ruido(self, n, escala, octavas=3):
        """Ruido de valor en 1D (entre 0 y 1), suave, para siluetas de montañas y dunas."""
        valores = [0.0] * n
        amp, total = 1.0, 0.0
        for o in range(octavas):
            paso = max(1, escala >> o)
            puntos = [self.rnd.random() for _ in range(n // paso + 2)]
            for x in range(n):
                i, f = divmod(x, paso)
                f = (1 - math.cos(f / paso * math.pi)) / 2
                valores[x] += amp * (puntos[i] * (1 - f) + puntos[i + 1] * f)
            total += amp
            amp *= 0.5
        return [v / total for v in valores]

    # ---------- cielo y espacio ----------
    def estrellas(self, n, y1=ALTO, colores=("#ffffff", "#c8d4ff", "#ffe8c8", "#8890b0")):
        for i in range(n):
            x, y = self.rnd.randrange(ANCHO), self.rnd.randrange(max(1, y1))
            c = self.rnd.choice(colores)
            if self.animado and (i * 5 + self.t) % PASOS < 2:
                c = oscuro(c, 0.45)          # titila: cada estrella se apaga 2 cuadros por ciclo
            self.pix(x, y, c)
            if self.rnd.random() < 0.06:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    self.pix(x + dx, y + dy, oscuro(c, 0.6))

    def astro(self, x, y, r, color, halo=None, sombra=None, anillos=0):
        """Sol, luna o planeta: halo tramado, disco con terminador de sombra."""
        if halo:
            self.brillo(x, y, r * 2.8, halo, 150)
        self.elipse(x - r, y - r, x + r, y + r, color)
        if sombra:
            px = self.img.load()
            for yy in range(y - r, y + r + 1):
                for xx in range(x - r, x + r + 1):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= r * r and 0 <= xx < ANCHO and 0 <= yy < ALTO:
                        t = (xx - x + r * 0.2) / r
                        if t > 0.35 or (t > 0.1 and BAYER[yy % 4][xx % 4] < 8):
                            px[xx, yy] = rgba(sombra)
            self.elipse(x - r + 2, y - r + 2, x - r // 3, y - r // 3, claro(color, 0.3)) if r > 6 else None
        for i in range(anillos):
            self.d.ellipse([x - r * 2 - i * 2, y - r // 3 - i, x + r * 2 + i * 2, y + r // 3 + i],
                           outline=rgba(oscuro(color, 0.8)))

    def nubes(self, y, alto, color, cantidad=8, ancho=(20, 60), luz=None):
        luz = luz or claro(color, 0.3)
        for _ in range(cantidad):
            cx = self.rnd.randrange(-20, ANCHO + 20)
            w = self.rnd.randint(*ancho)
            cy = y + self.rnd.randint(0, alto)
            for i in range(4):
                bx = cx + self.rnd.randint(-w // 2, w // 2)
                bw = self.rnd.randint(w // 4, w // 2)
                bh = max(3, bw // 3)
                self.elipse(bx - bw, cy - bh, bx + bw, cy + bh, color)
                self.rect(bx - bw // 2, cy - bh, bx + bw // 3, cy - bh, luz)

    # ---------- terreno ----------
    def cordillera(self, y_base, amp, escala, color, luz=None, sombra=None, octavas=3, textura=0.05,
                   picos=1.0):
        """Silueta de montañas o rocas: luz en las laderas que miran a la izquierda,
        sombra en las que miran a la derecha y textura de piedra."""
        luz = luz or claro(color, 0.22)
        sombra = sombra or oscuro(color, 0.72)
        alturas = self.ruido(ANCHO + 1, escala, octavas)
        tops = [int(y_base - amp * (v ** picos)) for v in alturas]
        px = self.img.load()
        for x in range(ANCHO):
            top = tops[x]
            pendiente = tops[x + 1] - top
            banda = 2 + abs(pendiente) * 2
            for y in range(max(0, top), ALTO):
                c = color
                prof = y - top
                if prof == 0:
                    c = luz
                elif prof < banda:
                    c = sombra if pendiente > 0 else (luz if pendiente < 0 else color)
                if self.rnd.random() < textura:
                    c = sombra if self.rnd.random() < 0.6 else luz
                px[x, y] = rgba(c)
        return tops

    def dunas(self, y_base, amp, escala, color, luz, sombra):
        tops = self.cordillera(y_base, amp, escala, color, luz, sombra, octavas=2, textura=0.0)
        for x in range(ANCHO):
            for k in range(6, ALTO - tops[x], 7):
                y = tops[x] + k + int(2 * math.sin((x + k * 3) / 9))
                if y < ALTO and (x + k) % 3:
                    self.pix(x, y, sombra)
        return tops

    def rocas(self, n, y0, y1, color, tam=(3, 10)):
        for _ in range(n):
            x = self.rnd.randrange(ANCHO)
            y = self.rnd.randint(y0, y1)
            w = self.rnd.randint(*tam)
            h = max(2, w * 2 // 3)
            self.elipse(x - w, y - h, x + w, y + 1, color)
            self.elipse(x - w + 1, y - h + 1, x, y - h // 2, claro(color, 0.25))
            self.rect(x - w, y, x + w, y + 1, oscuro(color, 0.6))

    # ---------- arquitectura ----------
    def skyline(self, y_base, color, ventana, prob_luz=0.3, ancho=(8, 22), alto=(20, 70), antenas=True,
                cuerpo_luz=None):
        """Fila de edificios con ventanas encendidas, terrazas y antenas."""
        luz = cuerpo_luz or claro(color, 0.15)
        sombra = oscuro(color, 0.75)
        x = -self.rnd.randint(0, 10)
        while x < ANCHO:
            w = self.rnd.randint(*ancho)
            h = self.rnd.randint(*alto)
            top = y_base - h
            self.rect(x, top, x + w - 1, ALTO - 1, color)
            self.rect(x, top, x, ALTO - 1, luz)
            self.rect(x + w - 1, top, x + w - 1, ALTO - 1, sombra)
            estilo = self.rnd.random()
            if estilo < 0.25:
                self.rect(x + 2, top - 4, x + w - 3, top - 1, color)
                self.rect(x + 2, top - 4, x + w - 3, top - 4, luz)
            elif estilo < 0.4:
                self.poly([(x, top), (x + w - 1, top), (x + w // 2, top - w // 2)], color)
            if antenas and self.rnd.random() < 0.35:
                ax = x + self.rnd.randint(1, max(1, w - 2))
                self.rect(ax, top - self.rnd.randint(4, 12), ax, top, sombra)
            for wy in range(top + 3, ALTO, 3):
                for wx in range(x + 2, x + w - 2, 3):
                    if self.rnd.random() < prob_luz:
                        self.pix(wx, wy, ventana)
                    elif self.rnd.random() < 0.3:
                        self.pix(wx, wy, sombra)
            x += w + self.rnd.randint(0, 3)

    def trafico(self, n, y0, y1, colores=("#ffd28a", "#ff8a6a", "#bfe4ff")):
        """Filas de vehículos voladores: puntos de luz en carriles."""
        for carril in range(3):
            y = y0 + (y1 - y0) * carril // 3
            sentido = 1 if carril % 2 == 0 else -1
            for _ in range(n // 3):
                x = self.rnd.randrange(ANCHO)
                c = self.rnd.choice(colores)
                x = int(x + sentido * self.fase * ANCHO) % ANCHO      # cada vehículo da una vuelta por ciclo
                self.rect(x, y, x + 1, y, c)
                self.pix(x - sentido, y, oscuro(c, 0.5))

    def columna(self, x, y0, y1, w, color, capitel=True):
        luz, sombra = claro(color, 0.25), oscuro(color, 0.7)
        self.rect(x, y0, x + w - 1, y1, color)
        self.rect(x, y0, x + 1, y1, luz)
        self.rect(x + w - 2, y0, x + w - 1, y1, sombra)
        for fx in range(x + 3, x + w - 3, 3):
            self.rect(fx, y0 + 3, fx, y1 - 3, oscuro(color, 0.85))
        if capitel:
            self.rect(x - 2, y0, x + w + 1, y0 + 3, color)
            self.rect(x - 2, y0, x + w + 1, y0, luz)
            self.rect(x - 2, y1 - 3, x + w + 1, y1, color)
            self.rect(x - 2, y1, x + w + 1, y1, sombra)

    def suelo_perspectiva(self, y0, color, linea, fuga_x=ANCHO // 2, radiales=14, color2=None):
        """Piso con líneas que fugan a un punto; si hay color2, en damero."""
        self.rect(0, y0, ANCHO - 1, ALTO - 1, color)
        alto = ALTO - y0
        filas = []
        y, paso = y0, 2.0
        while y < ALTO:
            filas.append(int(y))
            y += paso
            paso *= 1.35
        px = self.img.load()
        if color2:
            for yy in range(y0, ALTO):
                fila = sum(1 for f in filas if f <= yy)
                ancho_baldosa = 4 + (yy - y0) * 1.6
                for xx in range(ANCHO):
                    col = int((xx - fuga_x) / ancho_baldosa + 1000)
                    if (col + fila) % 2:
                        px[xx, yy] = rgba(color2)
        for f in filas:
            self.rect(0, f, ANCHO - 1, f, linea)
        for i in range(-radiales, radiales + 1):
            self.linea([(fuga_x + i * 6, y0), (fuga_x + i * 40, ALTO + alto)], linea)

    def ventanal(self, x0, y0, x1, y1, marco, pintar_fondo, divisiones=3, travesano=True):
        """Ventana grande: pinta el exterior con `pintar_fondo(escena)` recortado al hueco."""
        afuera = Escena(self.rnd.randrange(10 ** 6), self.cuadro, self.cuadros)
        pintar_fondo(afuera)
        self.img.paste(afuera.img.crop((x0, y0, x1 + 1, y1 + 1)), (x0, y0))
        self.rect(x0 - 2, y0 - 2, x1 + 2, y0, marco)
        self.rect(x0 - 2, y1, x1 + 2, y1 + 2, marco)
        self.rect(x0 - 2, y0, x0, y1, marco)
        self.rect(x1, y0, x1 + 2, y1, marco)
        for i in range(1, divisiones):
            x = x0 + (x1 - x0) * i // divisiones
            self.rect(x - 1, y0, x, y1, marco)
        if travesano:
            ym = y0 + (y1 - y0) // 3
            self.rect(x0, ym, x1, ym, marco)
        self.linea([(x0 + 4, y0 + 2), (x0 + 14, y0 + 12)], claro(marco, 0.6))

    # ---------- vegetación ----------
    def arbol(self, x, y_base, alto, tronco, copa, ancho_copa=None):
        ancho_copa = ancho_copa or alto // 2
        self.poly([(x - 2, y_base), (x + 2, y_base), (x + 1, y_base - alto), (x - 1, y_base - alto)], tronco)
        self.rect(x - 1, y_base - alto, x - 1, y_base, claro(tronco, 0.2))
        for i in range(6):
            cx = x + self.rnd.randint(-ancho_copa // 2, ancho_copa // 2)
            cy = y_base - alto + self.rnd.randint(-ancho_copa // 3, ancho_copa // 4)
            r = self.rnd.randint(ancho_copa // 4, ancho_copa // 2)
            self.elipse(cx - r, cy - r * 2 // 3, cx + r, cy + r * 2 // 3, copa)
            self.elipse(cx - r + 1, cy - r * 2 // 3 + 1, cx, cy - 1, claro(copa, 0.2))
            self.elipse(cx, cy, cx + r, cy + r * 2 // 3, oscuro(copa, 0.8))

    def lianas(self, n, color, y_max=60):
        for _ in range(n):
            x = self.rnd.randrange(ANCHO)
            largo = self.rnd.randint(10, y_max)
            for y in range(largo):
                self.pix(x + int(math.sin(y / 6) * 1.5), y, color)
                if y % 5 == 0:
                    self.pix(x + 1 + int(math.sin(y / 6) * 1.5), y, claro(color, 0.3))

    def helechos(self, n, y0, y1, color):
        for _ in range(n):
            x = self.rnd.randrange(ANCHO)
            y = self.rnd.randint(y0, y1)
            for k in range(-4, 5):
                largo = 6 - abs(k)
                self.linea([(x, y), (x + k * 2, y - largo)], color if k % 2 else claro(color, 0.2))

    # ---------- efectos ----------
    def brillo(self, x, y, r, color, alfa=110, pulso=0.0):
        """Halo de luz que se apaga hacia afuera en escalones tramados (estilo pixel art).
        Con `pulso` > 0 late suavemente a lo largo del ciclo (lámparas, fuego, neón)."""
        if pulso:
            alfa = alfa * (1 + pulso * self.onda((x * 7 + y * 3) % 10 / 10))
        px = self.img.load()
        cr, cg, cb = rgb(color)
        escalon = alfa / 4
        for yy in range(max(0, int(y - r)), min(ALTO, int(y + r) + 1)):
            for xx in range(max(0, int(x - r)), min(ANCHO, int(x + r) + 1)):
                dist = math.hypot(xx - x, yy - y) / r
                if dist >= 1:
                    continue
                a = alfa * (1 - dist) ** 1.4
                a = int(a / escalon + BAYER[yy % 4][xx % 4] / 16) * escalon / 255
                if a <= 0:
                    continue
                r0, g0, b0, _ = px[xx, yy]
                px[xx, yy] = (int(r0 + (cr - r0) * a), int(g0 + (cg - g0) * a), int(b0 + (cb - b0) * a), 255)

    def niebla(self, y0, y1, color, alfa=90):
        def dibujar(d):
            for y in range(y0, y1 + 1):
                t = 1 - abs((y - (y0 + y1) / 2) / max(1, (y1 - y0) / 2))
                d.line([(0, y), (ANCHO, y)], fill=rgba(color, int(alfa * t)))
        self.capa(dibujar)

    def rayos(self, x, y, color, n=4, alfa=40, largo=160, abertura=0.5):
        def dibujar(d):
            for i in range(n):
                ang = math.pi / 2 + (i - n / 2) * abertura / n
                x2, y2 = x + math.cos(ang) * largo * 0.6, y + math.sin(ang) * largo
                d.polygon([(x - 2 + i * 3, y), (x + 3 + i * 3, y), (x2 + 10, y2), (x2 - 10, y2)], fill=rgba(color, alfa))
        self.capa(dibujar)

    def lluvia(self, n, color, largo=6, dx=-2, alfa=150):
        def dibujar(d):
            for _ in range(n):
                x, y = self.rnd.randrange(ANCHO), self.rnd.randrange(ALTO)
                y = int(y + self.fase * ALTO * 3) % ALTO          # cada gota cae tres pantallas por ciclo
                d.line([(x, y), (x + dx, y + largo)], fill=rgba(color, alfa))
        self.capa(dibujar)

    def humo(self, x, y, alto, color, ancho=10):
        """Columna de bocanadas que suben y se desvanecen; con animación, cada bocanada
        ocupa al final del ciclo el lugar de la siguiente, así el bucle no brinca."""
        n = max(1, alto // 4)
        for i in range(n):
            k = i + self.fase
            r = int(ancho // 2 + k / 2)
            cx = x + int(math.sin(k / 3) * 4) + int(k / 3)
            cy = int(y - k * 4)
            alfa = int(150 * (1 - k / n) * (min(1.0, k) if self.animado else 1))
            if alfa > 0:
                self.capa(lambda d, cx=cx, cy=cy, r=r, a=alfa: d.ellipse([cx - r, cy - r, cx + r, cy + r],
                                                                         fill=rgba(color, a)))

    def fuego(self, x, y, tam):
        """Llama de tres capas; con animación parpadea, se inclina y suelta brasas."""
        az = self.azar_cuadro(x, y)
        alto = 1 + (az.random() - 0.5) * 0.4 if self.animado else 1
        inclina = az.randint(-1, 1) if self.animado else 0
        for c, k in (("#ff4a1a", 1.0), ("#ff9a2a", 0.7), ("#ffe27a", 0.4)):
            r = max(1, int(tam * k))
            self.poly([(x - r, y), (x + r, y), (x + r // 3 + inclina, y - r * 2 * alto),
                       (x + inclina, y - r * 3 * alto), (x - r // 2, y - r * 2 * alto)], c)
        if self.animado:
            for j in range(3):
                p = (self.fase * 2 + j / 3) % 1
                bx = x + int(math.sin((p + j) * 6) * tam)
                by = int(y - tam * 3 - p * tam * 5)
                if p < 0.85:
                    self.pix(bx, by, "#ffd27a" if p < 0.4 else "#ff7a2a")
        self.brillo(x, y - tam, tam * 4, "#ff8a2a", 70, pulso=0.25)

    def explosion(self, x, y, r):
        r = r * (1 + 0.15 * self.onda(x / 50))
        for c, k in (("#5a3a3a", 1.2), ("#ff4a1a", 1.0), ("#ff9a2a", 0.72), ("#fff2a8", 0.4)):
            rr = int(r * k)
            pts = []
            for i in range(12):
                ang = i * math.pi / 6
                d = rr * (0.75 + self.rnd.random() * 0.4)
                pts.append((x + math.cos(ang) * d, y + math.sin(ang) * d))
            self.poly(pts, c)
        self.brillo(x, y, r * 3, "#ffb04a", 80, pulso=0.3)

    def laser(self, x, y, largo, color, dx=1, dy=0):
        """Disparo de bláster. Con animación recorre toda su trayectoria (una línea que cruza
        la pantalla) una vez por ciclo, con una estela tenue detrás."""
        if self.animado and dx:
            periodo = ANCHO + 40
            nx = (x + 20 + dx * self.fase * periodo) % periodo - 20   # avanza y da la vuelta a la pantalla
            y = y + dy * (nx - x) / dx                                 # sobre su misma línea recta
            x = nx
            estela = rgba(color, 70)
            self.capa(lambda d: d.line([(x - dx * largo * 3, y - dy * largo * 3), (x, y)], fill=estela))
        self.linea([(x, y), (x + dx * largo, y + dy * largo)], claro(color, 0.6))
        self.linea([(x, y + 1), (x + dx * largo, y + dy * largo + 1)], color)

    def motas(self, n, x0, y0, x1, y1, color, amplitud=2):
        """Polvo, polen o ceniza flotando en su lugar (se mecen en círculos pequeños)."""
        for _ in range(n):
            x, y = self.rnd.randint(x0, x1), self.rnd.randint(y0, y1)
            desfase = self.rnd.random()
            self.pix(x + round(amplitud * self.onda(desfase)), y + round(amplitud * self.onda(desfase + 0.25)), color)

    def brasas(self, n, x0, y0, x1, y1, color, vueltas=1):
        """Partículas que suben dentro de una caja y reaparecen abajo (brasas, esporas, chispas)."""
        alto = y1 - y0
        for _ in range(n):
            x, inicio, desfase = self.rnd.randint(x0, x1), self.rnd.random(), self.rnd.random()
            p = (inicio + self.fase * vueltas) % 1
            y = int(y1 - p * alto)
            if p < 0.9:
                self.pix(x + round(1.5 * self.onda(desfase, 2)), y, color if p < 0.6 else oscuro(color, 0.7))

    # ---------- naves ----------
    def venator(self, x, y, escala, color="#c8ccd6", acento="#b03a3a"):
        """Destructor estelar de la República visto de lado: cuña con torres de mando."""
        e = escala
        self.poly([(x, y), (x + 60 * e, y - 6 * e), (x + 64 * e, y + 2 * e), (x + 2 * e, y + 6 * e)], color)
        self.poly([(x, y + 1), (x + 62 * e, y - 1 * e), (x + 64 * e, y + 2 * e), (x + 2 * e, y + 6 * e)], oscuro(color, 0.8))
        self.rect(x + 46 * e, y - 12 * e, x + 50 * e, y - 5 * e, color)
        self.rect(x + 52 * e, y - 12 * e, x + 56 * e, y - 6 * e, color)
        self.rect(x + 46 * e, y - 13 * e, x + 56 * e, y - 12 * e, claro(color, 0.3))
        self.rect(x + 4 * e, y + 1, x + 40 * e, y + 1, acento)
        for i in range(3):
            self.brillo(x + 63 * e, y - 3 * e + i * 2 * e, 2 * e, "#7ad0ff", 120)

    def fragata_separatista(self, x, y, escala, color="#8a7a6a"):
        e = escala
        self.rect(x, y, x + 40 * e, y + 3 * e, color)
        self.elipse(x - 8 * e, y - 5 * e, x + 6 * e, y + 8 * e, color)
        self.rect(x + 10 * e, y - 6 * e, x + 14 * e, y, oscuro(color, 0.8))
        self.rect(x + 10 * e, y + 3 * e, x + 14 * e, y + 9 * e, oscuro(color, 0.8))
        self.rect(x, y, x + 40 * e, y, claro(color, 0.3))
        for i in range(4):
            self.pix(x + (8 + i * 8) * e, y + e, "#ffb04a")

    def caza(self, x, y, color="#c8ccd6", acento="#b03a3a"):
        """Caza estelar pequeño; con animación se mece arriba y abajo y avanza un poco."""
        x = x + round(3 * self.onda(x / 97))
        y = y + round(2 * self.onda(y / 53 + 0.25))
        self.poly([(x, y), (x + 8, y - 2), (x + 8, y + 2)], color)
        self.rect(x + 2, y - 3, x + 5, y - 3, acento)
        self.rect(x + 2, y + 3, x + 5, y + 3, acento)
