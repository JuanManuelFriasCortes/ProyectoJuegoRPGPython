"""Genera los escenarios (fondos) del juego en pixel art.

Uso:  python generar_escenarios.py               (todos, fijos y animados)
      python generar_escenarios.py mustafar ...   (solo los que se nombren)
      python generar_escenarios.py --sin-animar   (solo los fondos fijos, mucho más rápido)
      python generar_escenarios.py --60fps        (además, el ciclo a 60 fps; tarda varios minutos)

Salida, junto a este archivo:
  fondos/<clave>.png     fondo escalado x4 (1280x720)
  fondos_1x/<clave>.png  fondo original de 320x180
  animados/<clave>.gif   fondo animado x4 (1280x720), 24 cuadros de 100 ms que se repiten
  animados_1x/<clave>.png  los 24 cuadros de 320x180 uno junto a otro (7680x180), para el juego
  animados_60/<clave>.png  el mismo ciclo en 144 cuadros (60 fps), en cuadrícula de 12x12 (3840x2160)
  galeria.png            todos juntos con su nombre, para revisarlos
  escenarios.json        clave -> nombre, archivo y fichas del guion que lo usan
  fichas.json            ficha del guion (D001...) -> clave del escenario
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from motor_escenarios import ALTO, ANCHO, Escena, claro, mezclar, oscuro, rgba

ESCALA = 4
CARPETA = Path(__file__).resolve().parent
ESCENARIOS = {}   # clave -> (nombre, semilla, función)


def escenario(clave, nombre, semilla):
    def registrar(funcion):
        ESCENARIOS[clave] = (nombre, semilla, funcion)
        return funcion
    return registrar


# ---------- piezas propias de varios escenarios ----------
def cristal(e, x, base, w, h, color):
    """Prisma de cristal con una cara iluminada y otra en sombra."""
    medio = x + w // 2
    punta = base - h
    e.poly([(x, base), (medio, base), (medio, punta)], claro(color, 0.25))
    e.poly([(medio, base), (x + w, base), (medio, punta)], oscuro(color, 0.75))
    e.linea([(medio, base), (medio, punta)], claro(color, 0.6))
    if h > 30:
        for y in range(punta + 8, base, 7):
            e.pix(medio - 2, y, claro(color, 0.7))


def ciudad_coruscant(e, atardecer=False, noche=False):
    """Skyline de Coruscant: cielo, tres capas de torres y tráfico aéreo."""
    if noche:
        e.degradado(0, 0, ANCHO - 1, 120, ["#0a0a1e", "#1a1a3a", "#3a2a5a", "#6a3a6a"])
        e.estrellas(40, 60)
        capas = [("#2a2a4a", "#ffd88a", 0.35), ("#1e1e36", "#ffcf7a", 0.4), ("#121224", "#ffe0a0", 0.45)]
    elif atardecer:
        e.degradado(0, 0, ANCHO - 1, 120, ["#3a2a5a", "#8a4a6a", "#e07a4a", "#f8c070"])
        e.astro(250, 95, 14, "#fff0c0", halo="#ffb070")
        capas = [("#8a5a6a", "#ffe0a0", 0.15), ("#5a3a4e", "#ffd08a", 0.25), ("#3a2434", "#ffc070", 0.3)]
    else:
        e.degradado(0, 0, ANCHO - 1, 120, ["#5a8ac8", "#8ab4e0", "#c8dcf0", "#e8e4d8"])
        e.nubes(20, 30, "#f0f4fa", 6)
        capas = [("#9aa6c0", "#e8eef8", 0.08), ("#6a7896", "#ffe8b0", 0.12), ("#465068", "#ffe0a0", 0.18)]
    for i, (color, ventana, prob) in enumerate(capas):
        e.skyline(90 + i * 22, color, ventana, prob, ancho=(6 + i * 3, 14 + i * 6), alto=(25 + i * 5, 70 - i * 8))
        if i == 0:
            e.trafico(30, 50, 80)
    e.trafico(24, 95, 125)


# ======================================================================
# Escenarios
# ======================================================================
@escenario("christophsis", "Christophsis — ciudad de cristal en ruinas", 1)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 130, ["#16224a", "#2a447e", "#5478b0", "#a8c4e4"])
    e.degradado(0, 120, ANCHO - 1, ALTO - 1, ["#8aa4c8", "#4a5a80", "#2c3656"])
    e.nubes(30, 25, "#c8d8ee", 5, (30, 70))
    for i in range(16):
        x = i * 21 + e.rnd.randint(-6, 6)
        cristal(e, x, 125, e.rnd.randint(10, 18), e.rnd.randint(30, 70), "#8ac0dc")
    e.niebla(95, 130, "#c8dcf0", 80)
    for x, h in ((20, 95), (70, 120), (190, 110), (250, 85), (290, 130)):
        cristal(e, x, 150, 26, h, "#3f86b8")
    for x in (60, 210, 300):
        e.humo(x, 120, 60, "#4a5068", 12)
        e.fuego(x, 128, 4)
    e.cordillera(160, 14, 30, "#344264", textura=0.12)
    e.rocas(25, 158, 178, "#4a5a7a", (3, 9))
    e.brasas(16, 40, 95, 310, 132, "#ffb060")
    for x in (30, 150, 270):
        cristal(e, x, 179, 14, 26, "#5ab0e0")
    e.laser(40, 70, 30, "#ff3a3a", 1, 0.3)
    e.laser(230, 60, 26, "#3a8aff", -1, 0.4)


@escenario("dunas_tatooine", "Tatooine — mar de dunas", 2)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 115, ["#4f8fcc", "#86b8e0", "#c4dcec", "#f0e2c4"])
    e.astro(232, 38, 9, "#fff8dc", halo="#ffe6a0")
    e.astro(258, 52, 6, "#ffe2a4", halo="#ffcf80")
    e.cordillera(108, 28, 70, "#c49a6a", "#e2c08c", "#9a7248", octavas=2, textura=0.03, picos=0.5)
    e.niebla(95, 112, "#f2e2c0", 70)
    e.dunas(128, 16, 90, "#e2b874", "#f4d49a", "#c08e54")
    e.dunas(152, 20, 70, "#d8a862", "#eec88a", "#ac7c44")
    # vaporizador de humedad
    for y in range(118, 150):
        e.rect(56, y, 59, y, "#b8b4a8" if y % 6 else "#7a766c")
    e.rect(54, 116, 61, 118, "#d8d4c8")
    e.rect(52, 149, 63, 151, "#8a8478")
    e.rocas(10, 160, 178, "#a87a4c", (4, 12))
    e.motas(36, 0, 118, ANCHO - 1, 176, "#f4dcaa", 3)


@escenario("oficina_canciller", "Oficina del Canciller", 3)
def _(e):
    pared = "#5e1820"
    e.rect(0, 0, ANCHO - 1, ALTO - 1, pared)
    e.textura(0, 0, ANCHO - 1, 130, ["#541418", "#6a1e26"], 0.05)
    for x in range(10, ANCHO, 40):
        e.rect(x, 10, x + 1, 130, "#4a1016")
        e.rect(x + 2, 10, x + 2, 130, "#7a2a32")
    e.ventanal(90, 22, 230, 118, "#2a0c10", lambda f: ciudad_coruscant(f, atardecer=True), divisiones=4)
    e.brillo(160, 70, 90, "#ff9a5a", 60)
    e.motas(26, 96, 26, 224, 114, "#ffe0b0", 2)
    e.rect(0, 130, ANCHO - 1, ALTO - 1, "#3a0c12")
    e.degradado(0, 131, ANCHO - 1, ALTO - 1, ["#4a1018", "#2a080c"])
    e.rect(110, 128, 210, 131, "#2a1210")
    # escritorio y sillón
    e.rect(118, 116, 202, 140, "#3a2218")
    e.rect(118, 116, 202, 117, "#6a4630")
    e.rect(150, 96, 170, 118, "#1e0e0c")
    e.rect(152, 98, 168, 99, "#4a2a22")
    # estatuas a los lados del ventanal
    for x in (54, 254):
        e.rect(x, 40, x + 10, 128, "#5a4430")
        e.rect(x, 40, x + 1, 128, "#8a6a48")
        e.elipse(x - 2, 30, x + 12, 44, "#5a4430")
        e.rect(x - 4, 124, x + 14, 130, "#3a2a1e")
    for x in range(30, ANCHO, 60):
        e.brillo(x, 6, 10, "#ffd0a0", 90, pulso=0.25)
        e.rect(x - 3, 4, x + 3, 6, "#ffe8c8")


@escenario("jungla", "Selva (Wasskah, Onderon, Kaller, Devaron)", 4)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#b8e0c8", "#7ab89a", "#3e7a62", "#244a3a"])
    e.cordillera(80, 30, 12, "#2f6650", octavas=2, textura=0.05)
    e.niebla(60, 100, "#c8ecd8", 70)
    for x in range(0, ANCHO, 26):
        e.arbol(x + e.rnd.randint(-6, 6), 130, e.rnd.randint(50, 80), "#3a2e22", "#2e6a3a", 34)
    e.rayos(120, -10, "#f0ffd8", 5, 30, 200, 0.6)
    e.motas(40, 70, 20, 250, 140, "#f4ffd0", 3)
    e.cordillera(150, 10, 20, "#1e3a22", octavas=2, textura=0.1)
    for x in (12, 290):
        e.rect(x, 0, x + 14, ALTO - 1, "#2a2018")
        e.rect(x, 0, x + 2, ALTO - 1, "#4a3a2a")
        e.textura(x, 0, x + 14, ALTO - 1, ["#1e1610", "#3a2c1e"], 0.15)
    e.lianas(18, "#3a7a3a", 90)
    e.helechos(40, 150, 178, "#3a8a3a")


@escenario("mustafar", "Mustafar — ríos de lava", 5)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#140808", "#3a0e0c", "#8a2210", "#e05a1a"])
    for _ in range(80):
        e.pix(e.rnd.randrange(ANCHO), e.rnd.randrange(120), e.rnd.choice(["#ff8a3a", "#5a2a20", "#ffb060"]))
    e.cordillera(100, 40, 50, "#24140f", "#a0381a", "#140a08", textura=0.04)
    for x, y in ((60, 62), (230, 55)):
        e.poly([(x - 18, y + 40), (x + 18, y + 40), (x + 4, y), (x - 4, y)], "#2e1a12")
        e.fuego(x, y + 2, 4)
    # colector separatista
    e.rect(150, 70, 158, 128, "#1a1414")
    e.poly([(140, 70), (170, 70), (176, 60), (134, 60)], "#1a1414")
    e.rect(158, 90, 200, 94, "#1a1414")
    e.brillo(154, 75, 6, "#ffb060", 140, pulso=0.5)
    # río de lava
    for y in range(128, 150):
        anchura = 30 + (y - 128) * 6
        x0 = 120 + int(math.sin(y / 5 - e.fase * 2 * math.pi) * 8) - anchura // 2
        e.rect(x0, y, x0 + anchura, y, "#ff5a14")
        nucleo = x0 + anchura // 3 + round(4 * e.onda(y / 22))
        e.rect(nucleo, y, nucleo + 3 + (y % 3), y, "#ffd060")
    e.brillo(150, 140, 70, "#ff6a1a", 90, pulso=0.2)
    e.brasas(34, 60, 80, 260, 150, "#ffb060", 2)
    e.cordillera(150, 18, 30, "#1a110e", "#c0461a", "#0e0806", textura=0.06)
    e.rect(0, 170, ANCHO - 1, ALTO - 1, "#0e0806")
    for _ in range(40):
        e.pix(e.rnd.randrange(ANCHO), e.rnd.randrange(ALTO), "#ffa050")


@escenario("consejo_jedi", "Cámara del Consejo Jedi", 6)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#a88a68")
    e.ventanal(20, 14, 300, 112, "#5a4430", lambda f: ciudad_coruscant(f, atardecer=True), divisiones=7, travesano=False)
    e.brillo(160, 80, 120, "#ffb070", 50)
    e.motas(30, 30, 20, 290, 108, "#ffe8c0", 2)
    e.suelo_perspectiva(112, "#8a6e52", "#6e5640", 160, 18)
    for r, c in ((150, "#9a7c5c"), (110, "#7a6048"), (70, "#9a7c5c")):
        e.d.ellipse([160 - r, 150 - r // 4, 160 + r, 150 + r // 4], outline=rgba(c), width=2)
    e.elipse(130, 140, 190, 160, "#b8946a")
    e.elipse(134, 142, 186, 158, "#8a6a48")
    # sillones del Consejo en arco
    for i in range(7):
        ang = math.pi * (0.1 + 0.8 * i / 6)
        x = int(160 - math.cos(ang) * 130)
        y = int(130 - math.sin(ang) * 14)
        e.rect(x - 7, y - 16, x + 7, y + 6, "#c8ab84")
        e.rect(x - 7, y - 16, x - 6, y + 6, "#e2c8a2")
        e.rect(x + 6, y - 16, x + 7, y + 6, "#8e7254")
        e.rect(x - 9, y - 2, x + 9, y + 8, "#b0916c")
        e.rect(x - 9, y + 8, x + 9, y + 9, "#6e5640")


def arco(e, x0, y0, x1, y1, color):
    """Hueco o ventana con remate en medio punto."""
    r = (x1 - x0) // 2
    e.elipse(x0, y0, x1, y0 + 2 * r, color)
    e.rect(x0, y0 + r, x1, y1, color)


def espacio(f, planeta=True):
    """Exterior espacial para ventanas: estrellas, nebulosa, planeta y naves."""
    f.rect(0, 0, ANCHO - 1, ALTO - 1, "#04050c")
    f.brillo(90, 40, 80, "#4a2a7a", 70)
    f.estrellas(180)
    if planeta:
        f.astro(250, 150, 70, "#3c6aa8", sombra="#12284a")
    f.venator(40, 60, 1.2)
    f.fragata_separatista(200, 45, 1)


def pasillo(e, pared, techo, suelo, puerta, luz, acento, emblema=None):
    """Pasillo de nave en perspectiva con paneles, franjas de luz y una compuerta al fondo."""
    fx0, fy0, fx1, fy1 = 128, 52, 192, 112
    e.poly([(0, 0), (fx0, fy0), (fx0, fy1), (0, ALTO)], pared)
    e.poly([(ANCHO, 0), (fx1, fy0), (fx1, fy1), (ANCHO, ALTO)], oscuro(pared, 0.85))
    e.poly([(0, 0), (ANCHO, 0), (fx1, fy0), (fx0, fy0)], techo)
    e.poly([(0, ALTO), (fx0, fy1), (fx1, fy1), (ANCHO, ALTO)], suelo)
    for k, t in enumerate((0.15, 0.32, 0.5, 0.66, 0.8, 0.9)):
        xi = int(fx0 * t)
        yi0, yi1 = int(fy0 * t), int(ALTO - (ALTO - fy1) * t)
        xd = int(ANCHO - (ANCHO - fx1) * t)
        e.linea([(xi, yi0), (xi, yi1)], oscuro(pared, 0.7))
        e.linea([(xd, yi0), (xd, yi1)], oscuro(pared, 0.6))
        if not (e.animado and (k + e.t // 2) % 6 == 0):
            e.rect(xi + 2, (yi0 + yi1) // 2 - 2, xi + 4, (yi0 + yi1) // 2, acento)
        e.linea([(xi, yi1), (xd, yi1)], oscuro(suelo, 0.75))
    for x in (110, 210):
        e.linea([(x, 0), (fx0 + (x - 110) * 0.64, fy0)], luz, 2)
    e.brillo(160, 30, 70, luz, 60, pulso=0.25)
    e.linea([(160, ALTO), (160, fy1)], acento)
    e.rect(fx0, fy0, fx1, fy1, puerta)
    e.rect(159, fy0, 160, fy1, oscuro(puerta, 0.6))
    for y in range(fy0 + 4, fy1, 8):
        e.rect(fx0 + 3, y, fx1 - 3, y, oscuro(puerta, 0.8))
    e.rect(fx0, fy0, fx1, fy0 + 2, acento)
    if emblema:
        e.poly([(160, 72), (170, 78), (170, 88), (160, 94), (150, 88), (150, 78)], emblema)
        e.poly([(160, 76), (166, 80), (166, 86), (160, 90), (154, 86), (154, 80)], oscuro(emblema, 0.6))


@escenario("monasterio_teth", "Teth — monasterio B'omarr en el acantilado", 7)
def _(e):
    e.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#f2daa2", "#d8b878", "#9aa070", "#3e5a3e"])
    e.astro(70, 38, 10, "#fff4d0", halo="#ffe0a0")
    e.cordillera(112, 50, 60, "#7a8a6a", octavas=3, textura=0.04)
    e.niebla(85, 125, "#f0e0b0", 90)
    roca = "#5e5a4a"
    e.poly([(168, ALTO), (252, ALTO), (238, 70), (184, 66)], roca)
    e.textura(168, 66, 252, ALTO - 1, ["#4a463a", "#6e6a58", "#3e3a30"], 0.2, base=roca)
    e.linea([(184, 66), (168, ALTO)], "#7e7a66", 2)
    e.linea([(238, 70), (252, ALTO)], "#3a362c", 2)
    e.rect(184, 58, 240, 70, "#7e7662")
    for x, w, h in ((188, 14, 30), (205, 18, 42), (226, 12, 26)):
        e.rect(x, 64 - h, x + w - 1, 64, "#8e8672")
        e.rect(x, 64 - h, x + 1, 64, "#b0a890")
        e.rect(x + w - 2, 64 - h, x + w - 1, 64, "#6a6452")
        e.elipse(x - 1, 64 - h - w // 2, x + w, 64 - h + w // 2, "#a09880")
        for y in range(64 - h + 6, 62, 8):
            e.rect(x + w // 2 - 1, y, x + w // 2, y + 3, "#2a2620")
    for x in range(176, 246, 9):
        largo = e.rnd.randint(20, 70)
        e.linea([(x, 70), (x + 2, 70 + largo)], "#4a6a3a")
    e.cordillera(150, 34, 14, "#34552e", octavas=2, textura=0.1)
    for x in (20, 60, 110, 280, 305):
        e.arbol(x, 178, e.rnd.randint(40, 60), "#3a2e22", "#3a6a34", 30)
    e.helechos(30, 160, 178, "#4a7a3a")
    e.motas(30, 0, 60, ANCHO - 1, 170, "#f8f0c0", 3)


@escenario("palacio_hutt", "Palacio de los Hutt (Jabba y Ziro)", 8)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#3e2e22")
    e.textura(0, 0, ANCHO - 1, 130, ["#33261c", "#4a3828", "#2a2018"], 0.12)
    for y in range(0, 130, 10):
        e.rect(0, y, ANCHO - 1, y, "#30241a")
    for x in range(22, ANCHO, 62):
        arco(e, x, 30, x + 30, 112, "#160f0a")
        arco(e, x + 3, 34, x + 27, 112, "#241810")
        e.brillo(x + 15, 90, 26, "#ff9a4a", 50, pulso=0.3)
    for x in range(8, ANCHO, 62):
        e.rect(x, 62, x + 3, 74, "#2a2018")
        e.fuego(x + 2, 62, 3)
    for x0, x1 in ((0, 36), (284, ANCHO - 1)):
        e.rect(x0, 0, x1, 140, "#6a1a1a")
        for x in range(x0 + 3, x1, 6):
            e.rect(x, 0, x + 1, 140, "#4a1010")
        e.rect(x0, 0, x1, 8, "#8a2a22")
    e.suelo_perspectiva(132, "#3a2c20", "#2a2016", 160, 10)
    e.rect(90, 112, 230, 134, "#5a4430")
    for y in (118, 124, 130):
        e.rect(90, y, 230, y, "#3a2c1e")
    e.rect(90, 112, 230, 113, "#7a6046")
    e.elipse(118, 96, 202, 120, "#7a5a3a")
    e.elipse(124, 98, 196, 114, "#9a3a2a")
    e.elipse(132, 100, 160, 106, "#ba5a42")
    e.elipse(126, 150, 194, 172, "#1a140e")
    for x in range(130, 194, 6):
        e.linea([(x, 152), (x, 170)], "#4a3a2a")
    for y in range(152, 172, 5):
        e.linea([(128, y), (192, y)], "#4a3a2a")
    for x in (70, 160, 250):
        e.linea([(x, 0), (x, 30)], "#2a2018")
        e.rect(x - 4, 30, x + 4, 36, "#8a6a3a")
        e.brillo(x, 34, 14, "#ffb060", 90, pulso=0.3)
    e.niebla(60, 140, "#ff9a4a", 30)
    e.motas(30, 40, 20, 280, 130, "#ffd8a0", 2)


@escenario("cabina", "Cabina de nave (viajes y hiperespacio)", 9)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#060a24")
    for _ in range(170):
        ang = e.rnd.random() * math.tau
        r0 = e.rnd.randint(4, 30)
        r1 = r0 + e.rnd.randint(25, 120)
        avance = (e.fase * 60 + r0 * 7) % 60 if e.animado else 0
        r0, r1 = r0 + avance, r1 + avance
        c = e.rnd.choice(["#c8e4ff", "#7aa8ff", "#ffffff", "#4a6ad8"])
        e.linea([(160 + math.cos(ang) * r0, 68 + math.sin(ang) * r0 * 0.6),
                 (160 + math.cos(ang) * r1, 68 + math.sin(ang) * r1 * 0.6)], c)
    e.brillo(160, 68, 60, "#bcd8ff", 150)
    marco = "#2a2e3a"
    e.rect(0, 0, ANCHO - 1, 16, marco)
    e.poly([(0, 0), (46, 0), (74, 124), (0, 150)], marco)
    e.poly([(ANCHO, 0), (274, 0), (246, 124), (ANCHO, 150)], marco)
    e.linea([(46, 0), (74, 124)], "#4a5062", 2)
    e.linea([(274, 0), (246, 124)], "#4a5062", 2)
    e.rect(0, 120, ANCHO - 1, ALTO - 1, "#22262e")
    e.rect(0, 120, ANCHO - 1, 122, "#3a4050")
    e.textura(0, 123, ANCHO - 1, ALTO - 1, ["#1a1e26", "#2a2e38"], 0.1)
    for i, x in enumerate(range(20, 300, 14)):
        for j in range(3):
            c = ["#ff4a4a", "#4aff7a", "#ffd04a", "#4ab0ff"][(i + j) % 4]
            if e.rnd.random() < 0.7 and not (e.animado and (i * 3 + j + e.t) % 8 == 0):
                e.rect(x, 130 + j * 6, x + 3, 131 + j * 6, c)
    for x0 in (90, 200):
        e.rect(x0, 128, x0 + 30, 150, "#0e2a1e")
        for y in range(131, 149, 3):
            e.rect(x0 + 2, y, x0 + 2 + e.rnd.randint(6, 26), y, "#4ad07a")
    for x in (140, 180):
        e.rect(x - 1, 150, x + 1, 170, "#4a4e5a")
        e.rect(x - 8, 146, x + 8, 150, "#5a5e6a")


@escenario("puente_crucero", "Puente de mando de un crucero de la República", 10)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#5c606c")
    e.textura(0, 0, ANCHO - 1, 100, ["#545864", "#666a76"], 0.05)
    e.ventanal(26, 16, 294, 92, "#3a3e48", espacio, divisiones=6)
    e.suelo_perspectiva(100, "#6a6e7a", "#545862", 160, 12)
    for x0, x1 in ((24, 128), (192, 296)):
        e.rect(x0, 118, x1, 152, "#262a32")
        e.rect(x0, 118, x1, 119, "#7a7e8a")
        for x in range(x0 + 6, x1 - 6, 12):
            e.rect(x, 124, x + 7, 130, "#123a5a")
            e.rect(x + 1, 125, x + 6, 125, "#4ab0ff")
            e.pix(x + 2, 128, "#ffd04a" if (x // 12 + e.t // 3) % 3 else "#5a4a2a")
    e.rect(138, 100, 182, ALTO - 1, "#7a7e8a")
    e.rect(138, 100, 139, ALTO - 1, "#9a9eaa")
    e.elipse(142, 150, 178, 160, "#1a3a6a")
    e.brillo(160, 148, 26, "#4aa8ff", 150, pulso=0.3)
    for x in (152, 160, 168):
        if not (e.animado and (x + e.t) % 6 == 0):
            e.linea([(x, 152), (x + (x - 160) // 2, 136)], "#7ac8ff")


@escenario("espacio_batalla", "Batalla en el espacio", 11)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#04050c")
    e.brillo(80, 40, 90, "#5a2a7a", 90)
    e.brillo(250, 120, 110, "#1a4a7a", 80)
    e.estrellas(240)
    e.astro(30, 175, 75, "#4a7ac8", sombra="#16284a")
    e.brillo(30, 175, 85, "#8ac0ff", 60)
    e.venator(20, 66, 2)
    e.venator(150, 112, 1.3)
    e.venator(232, 38, 0.7)
    e.fragata_separatista(200, 82, 1.5)
    e.fragata_separatista(262, 140, 1)
    for _ in range(14):
        e.caza(e.rnd.randrange(ANCHO), e.rnd.randrange(20, 160),
               *e.rnd.choice([("#c8ccd6", "#b03a3a"), ("#8a7a6a", "#3a3a4a")]))
    for _ in range(26):
        c = e.rnd.choice(["#ff3a3a", "#3a9aff", "#4aff7a"])
        e.laser(e.rnd.randrange(ANCHO), e.rnd.randrange(ALTO), e.rnd.randint(6, 16), c,
                e.rnd.choice([-1, 1]), e.rnd.uniform(-0.4, 0.4))
    for x, y, r in ((190, 76, 8), (120, 40, 5), (280, 110, 6)):
        e.explosion(x, y, r)


@escenario("pasillo_republica", "Pasillo de nave o base de la República", 12)
def _(e):
    pasillo(e, "#aeb2be", "#7e828e", "#686c78", "#8e929e", "#f4f8ff", "#d84a3a")


@escenario("pasillo_separatista", "Pasillo de nave separatista", 13)
def _(e):
    pasillo(e, "#3e4050", "#2a2c38", "#26262e", "#4a4c5c", "#ff5a4a", "#ff3a3a", emblema="#6a5ac8")


@escenario("hangar_republica", "Hangar de la República", 14)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#5a5e68")
    e.ventanal(40, 34, 280, 108, "#3a3e48", lambda f: espacio(f, planeta=False), divisiones=1, travesano=False)
    e.capa(lambda d: d.rectangle([40, 34, 280, 108], fill=rgba("#4a8aff", int(40 + 14 * e.onda()))))
    e.rect(0, 0, ANCHO - 1, 26, "#363a44")
    for x in range(0, ANCHO, 24):
        e.rect(x, 0, x + 3, 26, "#2a2e36")
        e.linea([(x + 12, 26), (x + 12, 32)], "#2a2e36")
        e.brillo(x + 12, 28, 12, "#f0f4ff", 90, pulso=0.2)
    e.suelo_perspectiva(110, "#6e727c", "#5a5e68", 160, 12)
    e.linea([(60, ALTO), (140, 110)], "#e8c040", 2)
    e.linea([(260, ALTO), (180, 110)], "#e8c040", 2)
    for x, y, s in ((70, 132, 1.0), (236, 140, 1.2)):
        e.poly([(x - 30 * s, y), (x + 30 * s, y), (x + 8 * s, y - 10 * s), (x - 8 * s, y - 10 * s)], "#c8ccd6")
        e.rect(x - 6 * s, y - 16 * s, x + 6 * s, y - 6 * s, "#d8dce4")
        e.rect(x - 3 * s, y - 14 * s, x + 3 * s, y - 10 * s, "#2a3a5a")
        e.rect(x - 30 * s, y, x + 30 * s, y + 2, "#8a8e9a")
        e.rect(x - 24 * s, y - 3, x - 14 * s, y - 2, "#b03a3a")
        e.rect(x + 14 * s, y - 3, x + 24 * s, y - 2, "#b03a3a")
    for x, y in ((140, 150), (150, 150), (145, 142), (300, 128)):
        e.rect(x, y, x + 9, y + 8, "#6a5a3a")
        e.rect(x, y, x + 9, y, "#8a7a52")
        e.rect(x + 4, y, x + 5, y + 8, "#4a3e28")


@escenario("senado", "Rotonda del Senado Galáctico", 15)
def _(e):
    e.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#0c1222", "#18223c", "#283856"])
    for k in range(9):
        rx, ry = 50 + k * 28, 18 + k * 12
        for i in range(0, 60):
            ang = math.pi * (1.05 + 0.9 * i / 59)
            x = int(160 + math.cos(ang) * rx)
            y = int(150 + math.sin(ang) * ry)
            if 0 <= x < ANCHO:
                e.rect(x - 2, y - 1, x + 2, y + 1, "#6a7690")
                e.pix(x - 2, y - 1, "#a8b4cc")
                if e.rnd.random() < 0.2 and not (e.animado and (i + k + e.t) % 9 == 0):
                    e.pix(x, y, "#ffe8a8")
    e.rayos(160, 0, "#c8dcff", 3, 28, 190, 0.18)
    e.rect(150, 110, 170, ALTO - 1, "#7a86a0")
    e.rect(150, 110, 152, ALTO - 1, "#a8b4cc")
    e.elipse(128, 102, 192, 116, "#a8b4cc")
    e.elipse(132, 104, 188, 112, "#c8d4ea")
    e.brillo(160, 108, 34, "#bcd4ff", 110, pulso=0.25)
    e.motas(30, 132, 0, 188, 104, "#e0ecff", 2)
    e.niebla(100, 170, "#5a7aa8", 50)


@escenario("departamento_padme", "Departamento de Padmé (noche)", 16)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#c4b4a4")
    e.ventanal(72, 14, 304, 122, "#3a3640", lambda f: ciudad_coruscant(f, noche=True), divisiones=3, travesano=False)
    e.rect(72, 104, 304, 106, "#2a2832")
    for x in range(74, 304, 8):
        e.rect(x, 106, x, 122, "#2a2832")
    e.textura(0, 0, 70, 124, ["#b8a898", "#d0c0b0"], 0.06)
    e.rect(0, 0, ANCHO - 1, 8, "#a89888")
    e.degradado(0, 124, ANCHO - 1, ALTO - 1, ["#4a3e3a", "#2e2624"])
    for x in range(90, 290, 30):
        e.linea([(x, 126), (x - 6, ALTO)], "#6a5a6a")
    e.rect(96, 134, 206, 152, "#a8988a")
    e.rect(96, 126, 206, 136, "#b8a89a")
    e.rect(96, 126, 206, 127, "#d4c4b6")
    for x in (130, 166):
        e.rect(x, 128, x, 150, "#8a7a6e")
    e.rect(30, 138, 44, 156, "#6a5a4a")
    for k in range(-5, 6):
        e.linea([(37, 138), (37 + k * 3, 112 + abs(k) * 3)], "#3a7a4a" if k % 2 else "#5a9a5a")
    e.rect(52, 40, 54, 120, "#8a7a68")
    e.rect(46, 34, 60, 40, "#f0e0c0")
    e.brillo(53, 38, 30, "#ffd8a0", 110, pulso=0.15)


@escenario("plataforma_coruscant", "Plataforma de aterrizaje en Coruscant", 17)
def _(e):
    ciudad_coruscant(e)
    e.poly([(0, 136), (ANCHO, 148), (ANCHO, ALTO), (0, ALTO)], "#7a7e88")
    e.textura(0, 136, ANCHO - 1, ALTO - 1, ["#6a6e78", "#8a8e98"], 0.06, base="#7a7e88")
    for x in range(0, ANCHO, 16):
        y = 136 + x * 12 // ANCHO
        e.rect(x, y, x + 7, y + 1, "#e8c040")
        e.rect(x + 8, y, x + 15, y + 1, "#2a2a30")
    for x in (40, 120, 200, 280):
        y = 140 + x * 12 // ANCHO
        e.rect(x, y, x + 2, y + 1, "#ff5a4a")
        e.brillo(x + 1, y, 8, "#ff5a4a", 100, pulso=0.9)
    for y in range(152, ALTO, 7):
        e.linea([(0, y), (ANCHO, y + 4)], "#6a6e78")
    # lanzadera
    e.poly([(190, 150), (290, 150), (270, 128), (214, 126)], "#c8ccd6")
    e.poly([(214, 126), (270, 128), (258, 116), (226, 116)], "#dfe2ea")
    e.rect(234, 118, 252, 124, "#2a3a5a")
    e.rect(196, 148, 284, 150, "#8a8e9a")
    e.linea([(214, 126), (270, 128)], "#f4f6fa")
    for x in (206, 274):
        e.rect(x, 150, x + 2, 156, "#5a5e6a")


@escenario("niveles_bajos", "Niveles bajos de Coruscant", 18)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#121018")
    e.degradado(90, 0, 230, 70, ["#2a2440", "#3a2a4a", "#1a1624"])
    e.skyline(70, "#1e1a2a", "#ff6aa8", 0.15, ancho=(8, 14), alto=(20, 50), antenas=False)
    for x0, x1, c in ((0, 90, "#1e1a24"), (230, ANCHO - 1, "#1a1620")):
        e.rect(x0, 0, x1, 150, c)
        e.textura(x0, 0, x1, 150, ["#2a2430", "#141018"], 0.12)
        for y in range(10, 150, 14):
            for x in range(x0 + 6, x1 - 6, 12):
                e.rect(x, y, x + 5, y + 6, "#0c0a10")
                if e.rnd.random() < 0.35:
                    e.rect(x + 1, y + 1, x + 4, y + 5, e.rnd.choice(["#ffb86a", "#6ad8ff", "#ff8ad0"]))
    for x, y, w, c in ((20, 40, 40, "#ff4aa8"), (250, 30, 50, "#4ae8ff"), (34, 96, 28, "#ffe04a"),
                       (246, 90, 34, "#ff6a3a")):
        e.rect(x, y, x + w, y + 8, "#1a1018")
        if e.animado and x == 250 and e.t in (5, 6, 17):
            continue            # este letrero falla de vez en cuando
        e.rect(x + 2, y + 2, x + w - 2, y + 6, c)
        e.rect(x + 4, y + 3, x + w - 4, y + 5, claro(c, 0.5))
        e.brillo(x + w // 2, y + 4, w, c, 90, pulso=0.2)
    for y in (20, 34):
        e.linea([(0, y), (80, y + 10), (160, y + 14), (240, y + 10), (ANCHO, y)], "#0a080e")
    for x in (95, 104, 214, 222):
        e.rect(x, 0, x + 3, 150, "#3a3a48")
        e.rect(x, 0, x, 150, "#5a5a6a")
    e.rect(0, 150, ANCHO - 1, ALTO - 1, "#18161e")
    for _ in range(50):
        x = e.rnd.randrange(ANCHO)
        c = e.rnd.choice(["#ff4aa8", "#4ae8ff", "#ffe04a", "#ff6a3a"])
        x += round(e.onda(x / 40))
        e.rect(x, e.rnd.randint(152, 178), x, e.rnd.randint(152, 178), oscuro(c, 0.6))
    e.humo(150, 170, 50, "#6a6478", 10)
    e.humo(190, 172, 40, "#5a5468", 8)
    e.lluvia(160, "#8a9ab8", 5, -1, 110)


@escenario("templo_exterior", "Templo Jedi — fachada y escalinata", 19)
def _(e):
    ciudad_coruscant(e, atardecer=True)
    piedra = "#c8b48e"
    e.poly([(56, 74), (264, 74), (292, 134), (28, 134)], piedra)
    e.textura(28, 74, 292, 134, ["#b8a47e", "#d8c49e"], 0.08, base=piedra)
    for y in range(80, 134, 6):
        e.linea([(56 - (y - 74) * 28 // 60, y), (264 + (y - 74) * 28 // 60, y)], "#a8946e")
    e.linea([(56, 74), (28, 134)], "#e8d8b4", 2)
    e.linea([(264, 74), (292, 134)], "#8a7654", 2)
    for x, h, w in ((156, 70, 8), (106, 44, 6), (208, 44, 6), (74, 30, 5), (240, 30, 5)):
        e.poly([(x - w, 74), (x + w, 74), (x + 2, 74 - h), (x - 2, 74 - h)], piedra)
        e.linea([(x - w, 74), (x - 2, 74 - h)], "#e8d8b4")
        e.linea([(x + w, 74), (x + 2, 74 - h)], "#8a7654")
        e.rect(x - 1, 74 - h - 4, x + 1, 74 - h, "#e8d8b4")
    for x in range(70, 252, 12):
        e.rect(x, 84, x + 4, 100, "#3a2e22")
    e.rect(142, 104, 178, 134, "#2a2018")
    e.brillo(160, 120, 20, "#ffd090", 70, pulso=0.3)
    e.motas(20, 60, 130, 260, 178, "#f0e0c0", 2)
    e.poly([(112, 134), (208, 134), (262, ALTO), (58, ALTO)], "#b8a47e")
    for y in range(136, ALTO, 4):
        ancho = 48 + (y - 134) * 54 // 46
        e.rect(160 - ancho, y, 160 + ancho, y, "#94805e")
    for k in range(4):
        y = 140 + k * 10
        ancho = 52 + (y - 134) * 54 // 46
        for x in (160 - ancho - 4, 160 + ancho + 2):
            e.rect(x, y - 8, x + 2, y, "#e2d2ae")
            e.elipse(x - 1, y - 11, x + 3, y - 7, "#e2d2ae")
    e.rect(0, 134, 58, ALTO - 1, "#8a7e6a")
    e.rect(262, 134, ANCHO - 1, ALTO - 1, "#8a7e6a")


@escenario("templo_pasillo", "Templo Jedi — gran salón y archivo", 20)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#6e5e4a", "#9a8a70", "#b8a68a"])
    for x in (136, 152, 168):
        e.rect(x, 30, x + 8, 96, "#fff0cc")
    e.brillo(160, 60, 50, "#ffe8b0", 110)
    e.rect(130, 96, 190, 100, "#8a7a62")
    e.suelo_perspectiva(100, "#b8a88e", "#9a8a72", 160, 12)
    e.capa(lambda d: d.polygon([(136, 100), (176, 100), (230, ALTO), (90, ALTO)], fill=rgba("#fff0cc", 40)))
    e.rayos(160, 30, "#fff4d8", 5, 26, 170, 0.5)
    e.motas(44, 96, 30, 224, 172, "#fff0c8", 2)
    for k in range(5):
        s = 1 - k * 0.17
        w = max(4, int(18 * s))
        y0, y1 = int(4 + k * 12), int(176 - k * 15)
        xl = int(14 + k * 26)
        xr = ANCHO - xl - w
        for x in (xl, xr):
            e.columna(x, y0, y1, w, "#cbbb9e")
        if k < 4:
            for x in (xl + w + 4, xr - 14):
                for y in range(y0 + 20, y1 - 10, 6):
                    for dx in range(0, 10, 3):
                        if e.rnd.random() < 0.6:
                            c = e.rnd.choice(["#6ac8ff", "#4a8ad8", "#a8e4ff"])
                            e.pix(x + dx, y, "#ffffff" if e.animado and (x + dx + y + e.t) % 17 == 0 else c)
    e.rect(154, 70, 166, 96, "#a8987c")
    e.elipse(153, 62, 167, 74, "#a8987c")


@escenario("ciudadela", "Prisión (Ciudadela, Kadavo, celdas)", 21)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#26262e")
    for y in range(0, 130, 8):
        e.rect(0, y, ANCHO - 1, y, "#1a1a20")
        for x in range((y // 8) % 2 * 12, ANCHO, 24):
            e.rect(x, y, x, y + 7, "#1a1a20")
    e.textura(0, 0, ANCHO - 1, 128, ["#30303a", "#1e1e26"], 0.1)
    for x in (20, 100, 180, 260):
        e.rect(x, 50, x + 44, 126, "#0c0c12")
        e.rect(x - 3, 46, x + 47, 50, "#3a3a46")
        e.rect(x - 3, 46, x - 1, 126, "#3a3a46")
        e.rect(x + 45, 46, x + 47, 126, "#3a3a46")
        for bx in range(x + 4, x + 42, 6):
            e.rect(bx, 52, bx, 124, "#ff8a8a" if e.animado and (bx + e.t) % 7 == 0 else "#ff3a3a")
        e.brillo(x + 22, 88, 30, "#ff3a3a", 70, pulso=0.3)
    e.rect(0, 128, ANCHO - 1, 134, "#4a4a56")
    e.rect(0, 128, ANCHO - 1, 128, "#6a6a78")
    for x in range(0, ANCHO, 20):
        e.rect(x, 116, x + 1, 128, "#5a5a68")
    e.rect(0, 116, ANCHO - 1, 117, "#5a5a68")
    e.degradado(0, 135, ANCHO - 1, ALTO - 1, ["#1a1a22", "#08080c"])
    e.rayos(10, 0, "#e8f0ff", 2, 30, 180, 0.3)
    e.rayos(310, 0, "#e8f0ff", 2, 30, 180, 0.3)
    for x in (70, 240):
        for y in range(0, 40, 3):
            e.rect(x, y, x + 1, y + 1, "#5a5a66")


@escenario("fabrica_droides", "Fábrica e instalación separatista", 22)
def _(e):
    e.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#22160f", "#3e2416", "#5e3418"])
    e.skyline(110, "#2a2018", "#ff9a3a", 0.12, ancho=(14, 30), alto=(30, 80), antenas=False)
    for x in (30, 90, 250, 300):
        e.rect(x, 0, x + 5, 120, "#3a2a20")
        e.rect(x, 0, x, 120, "#5a4030")
    e.rect(10, 60, 60, 110, "#1a1008")
    e.rect(14, 64, 56, 106, "#ff7a1a")
    e.rect(20, 70, 50, 100, "#ffc04a")
    e.brillo(35, 85, 50, "#ff8a2a", 110, pulso=0.2)
    e.rect(100, 0, 104, 50, "#4a3a30")
    e.poly([(90, 50), (116, 50), (110, 62), (96, 62)], "#5a4a3a")
    e.rect(102, 62, 104, 104, "#ffb040")
    e.brillo(103, 90, 16, "#ff9a3a", 100, pulso=0.4)
    e.elipse(88, 100, 118, 112, "#3a2a20")
    for y in (118, 148):
        e.rect(0, y, ANCHO - 1, y + 8, "#2a2420")
        e.rect(0, y, ANCHO - 1, y, "#5a4a3e")
        for x in range(4, ANCHO, 10):
            e.elipse(x, y + 5, x + 5, y + 10, "#4a3e34")
        for x in range(10 - 26 + int(e.fase * 26), ANCHO, 26):
            e.elipse(x, y - 7, x + 9, y, "#d8c8a0")
            e.rect(x + 2, y - 5, x + 3, y - 4, "#2a2018")
            e.rect(x + 6, y - 5, x + 7, y - 4, "#2a2018")
    for x in (160, 220):
        e.linea([(x, 0), (x, 70), (x + 10, 90)], "#6a5a4a", 2)
        e.linea([(x + 10, 90), (x + 4, 98)], "#8a7a6a", 2)
    chispas = e.azar_cuadro(22)
    for _ in range(30):
        x, y = chispas.randrange(ANCHO), chispas.randrange(60, 160)
        e.pix(x, y, "#ffd060")
    e.rect(0, 166, ANCHO - 1, ALTO - 1, "#1e1610")


@escenario("geonosis", "Geonosis — agujas de roca", 23)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 130, ["#f4c080", "#e8945a", "#c06a40", "#9a4a30"])
    e.astro(70, 30, 7, "#fff2c8", halo="#ffc890")
    e.cordillera(118, 30, 50, "#a85a3a", octavas=2, textura=0.06)
    for _ in range(9):
        x = e.rnd.randrange(10, ANCHO - 10)
        h = e.rnd.randint(40, 90)
        w = e.rnd.randint(6, 12)
        e.poly([(x - w, 125), (x + w, 125), (x + 2, 125 - h), (x - 3, 125 - h + 4)], "#8e4a30")
        e.linea([(x - w, 125), (x - 3, 125 - h + 4)], "#c47452")
        for y in range(125 - h + 10, 120, 9):
            e.rect(x - 1, y, x, y + 2, "#3a1a10")
    e.niebla(95, 135, "#f0a070", 80)
    e.humo(230, 120, 70, "#5a3a30", 12)
    e.humo(60, 125, 50, "#6a4a3a", 10)
    for x, y in ((180, 50), (210, 40), (250, 60)):
        x, y = x + round(4 * e.onda(x / 61)), y + round(2 * e.onda(x / 37 + 0.25))
        e.poly([(x, y), (x + 12, y - 2), (x + 14, y + 2), (x, y + 3)], "#c8ccd6")
        e.laser(x - 10, y + 4, 10, "#3a9aff", -1, 0.6)
    e.cordillera(150, 16, 40, "#8a4228", "#b8664a", "#5a2a18", textura=0.1)
    e.rocas(18, 158, 178, "#7a3a24", (4, 11))
    e.motas(36, 0, 90, ANCHO - 1, 176, "#f4b88a", 3)


@escenario("palacio_elegante", "Palacio elegante (Cato Neimoidia, Alderaan, Raxus, Zygerria, Serenno, ópera)", 24)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#e6dac6")
    e.textura(0, 0, ANCHO - 1, 120, ["#dccfb8", "#efe4d2", "#d2c4aa"], 0.08)
    for x in (40, 130, 220):
        arco(e, x, 18, x + 60, 112, "#7aa0c8")
        e.degradado(x + 2, 20, x + 58, 112, ["#5a86c0", "#a8c4e4", "#f0e4c8"])
        e.nubes(50, 20, "#ffffff", 2, (10, 20))
        e.rect(x + 29, 20, x + 31, 112, "#c8a050")
        e.rect(x, 64, x + 60, 66, "#c8a050")
        e.rect(x - 6, 14, x + 4, 116, "#8a1e24")
        e.rect(x + 56, 14, x + 66, 116, "#8a1e24")
        for fx in (x - 4, x + 0, x + 58, x + 62):
            e.rect(fx, 14, fx, 116, "#6a1418")
    for x in (24, 112, 200, 288):
        e.columna(x, 6, 120, 12, "#c8a050")
    e.suelo_perspectiva(120, "#e0d4c0", "#c4b49a", 160, 14, color2="#cfc2aa")
    e.motas(30, 40, 20, 280, 112, "#fff4d8", 2)
    e.poly([(140, 120), (180, 120), (226, ALTO), (94, ALTO)], "#9a2a2a")
    e.linea([(140, 120), (94, ALTO)], "#d8b050", 2)
    e.linea([(180, 120), (226, ALTO)], "#d8b050", 2)
    e.linea([(160, 0), (160, 20)], "#8a7040")
    e.elipse(140, 18, 180, 30, "#c8a050")
    for x in range(144, 178, 5):
        e.pix(x, 31, "#fff4c0")
        e.brillo(x, 32, 5, "#fff0b0", 120, pulso=0.5)


@escenario("palacio_mandalore", "Mandalore — palacio de Sundari", 25)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#d8dce4")

    def sundari(f):
        """Sundari: ciudad de cubos blancos bajo una cúpula, en un desierto pálido."""
        f.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#9ab4cc", "#c8d8e4", "#e8e0cc", "#d4c8a8"])
        f.d.arc([50, 30, 270, 200], 180, 360, fill=rgba("#7a94ac"), width=2)
        f.capa(lambda d: d.pieslice([50, 30, 270, 200], 180, 360, fill=rgba("#bcd4e8", 50)))
        for capa, (base, color, sombra) in enumerate(((100, "#d8dee6", "#a8b2c0"), (114, "#eef2f6", "#b8c2ce"))):
            for _ in range(45):
                x = f.rnd.randrange(60, 260)
                w = f.rnd.randint(6, 14)
                h = f.rnd.randint(8, 34 - capa * 10)
                f.rect(x, base - h, x + w, base, color)
                f.rect(x + w - 1, base - h, x + w, base, sombra)
                f.rect(x, base - h, x + w, base - h, "#ffffff")
                for wy in range(base - h + 3, base - 1, 4):
                    for wx in range(x + 2, x + w - 2, 3):
                        encendida = f.rnd.random() >= 0.7
                        if f.animado and (wx + wy * 3 + f.t) % 29 == 0:
                            encendida = not encendida
                        f.pix(wx, wy, "#ffe8a0" if encendida else "#4a6a8a")
        f.rect(0, 114, ANCHO - 1, ALTO - 1, "#c8bc9c")
    e.ventanal(70, 20, 250, 116, "#a8b4c4", sundari, divisiones=3)
    for x0 in (0, 260):
        for y in range(10, 120, 14):
            for x in range(x0 + 6, x0 + 56, 14):
                c = e.rnd.choice(["#3a8a9a", "#2a5a7a", "#7ab8c4", "#d8dce4"])
                e.rect(x, y, x + 11, y + 11, c)
                e.rect(x, y, x + 11, y, claro(c, 0.3))
    e.rect(0, 116, ANCHO - 1, 120, "#a8b0bc")
    e.suelo_perspectiva(120, "#e4e8ee", "#c4ccd6", 160, 12)
    e.rect(120, 128, 200, 140, "#c8d0dc")
    e.rect(120, 128, 200, 129, "#f4f6fa")
    e.rect(132, 104, 188, 128, "#3a6a8a")
    e.rect(136, 108, 184, 124, "#2a5a7a")
    e.poly([(160, 110), (168, 116), (160, 122), (152, 116)], "#d8e4ec")


@escenario("kamino", "Kamino — instalaciones de clonación", 26)
def _(e):
    e.rect(0, 0, ANCHO - 1, ALTO - 1, "#e2e8ee")
    afuera = Escena(e.rnd.randrange(10 ** 6), e.cuadro, e.cuadros)
    afuera.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#2a3442", "#4a5868", "#6a7a8a", "#3a4a5a"])
    afuera.nubes(10, 30, "#5a6878", 8, (30, 60))
    if not e.animado or e.t in (2, 3, 15):
        afuera.linea([(200, 20), (194, 40), (204, 44), (196, 70)], "#ffffff", 2)
        afuera.brillo(198, 44, 60 if e.t == 2 else 30, "#c8dcff", 120)
    for y in range(95, 130, 4):
        for x in range(0, ANCHO, 12):
            ox = x + (y // 4) % 3 * 4 + int(e.fase * 12)
            afuera.rect(ox, y, ox + 6, y, "#8a9aaa")
    afuera.lluvia(220, "#b8c8d8", 7, -2, 140)
    mascara = Image.new("L", (ANCHO, ALTO), 0)
    ImageDraw.Draw(mascara).ellipse([96, 16, 224, 120], fill=255)
    e.img.paste(afuera.img, (0, 0), mascara)
    e.d.ellipse([94, 14, 226, 122], outline=rgba("#9aa4b0"), width=3)
    e.rect(158, 16, 161, 120, "#9aa4b0")
    for x in (24, 54, 252, 282):
        e.rect(x, 30, x + 16, 120, "#bcdcec")
        e.rect(x, 30, x + 2, 120, "#e8f6ff")
        e.rect(x + 6, 60, x + 10, 72, "#e8c8b0")
        e.elipse(x + 5, 52, x + 11, 60, "#e8c8b0")
        e.rect(x - 2, 24, x + 18, 30, "#9aa4b0")
        e.rect(x - 2, 120, x + 18, 126, "#9aa4b0")
        e.brillo(x + 8, 75, 20, "#7ad0ff", 60, pulso=0.35)
    e.suelo_perspectiva(130, "#d0d8e0", "#b8c4d0", 160, 12)
    for x in range(0, ANCHO, 40):
        e.rect(x, 128, x + 20, 129, "#4ab0ff")


def arbol_retorcido(e, x, y_base, alto, tronco, hojas=None):
    """Árbol de ramas torcidas (Dathomir, Dagobah)."""
    puntos_i, puntos_d = [], []
    for k in range(alto):
        dx = int(math.sin(k / 9) * 4)
        ancho = max(2, 6 - k // 8)
        puntos_i.append((x + dx - ancho, y_base - k))
        puntos_d.append((x + dx + ancho, y_base - k))
    e.poly(puntos_i + puntos_d[::-1], tronco)
    e.linea(puntos_i, claro(tronco, 0.2))
    for k in range(3):
        y = y_base - alto + k * 8
        lado = 1 if k % 2 else -1
        rx, ry = x + lado * (14 + k * 3), y - 10
        e.linea([(x, y + 6), (x + lado * 8, y), (rx, ry)], tronco, 2)
        if hojas:
            e.elipse(rx - 8, ry - 5, rx + 8, ry + 4, hojas)
            e.elipse(rx - 6, ry - 4, rx, ry, claro(hojas, 0.2))
    for lado in (-1, 1):
        e.linea([(x + lado * 3, y_base - 6), (x + lado * 10, y_base + 1)], tronco, 2)


@escenario("dathomir", "Dathomir — selva roja con niebla", 27)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 130, ["#24080e", "#5e1220", "#a42a34", "#d8685a"])
    e.astro(250, 40, 13, "#ead2c8", sombra="#9a6a6a")
    e.astro(280, 62, 5, "#d8b8b0")
    e.cordillera(112, 44, 40, "#36121a", octavas=3, textura=0.05)
    for x, h in ((70, 30), (80, 44), (90, 26)):
        e.poly([(x - 4, 80), (x + 4, 80), (x, 80 - h)], "#1e080c")
    e.brillo(80, 64, 10, "#7aff8a", 120, pulso=0.5)
    e.niebla(90, 135, "#e8a0a0", 90)
    for x in range(10, ANCHO, 46):
        arbol_retorcido(e, x + e.rnd.randint(-8, 8), 150, e.rnd.randint(50, 80), "#2a0e12", "#8a1c26")
    e.niebla(130, 165, "#d88888", 70)
    e.cordillera(166, 12, 30, "#1e0a0e", textura=0.08)
    e.rocas(12, 168, 178, "#3a141a", (4, 10))
    e.brasas(26, 0, 70, ANCHO - 1, 170, "#ffa0a0")


@escenario("mortis", "Mortis — el mundo de la Fuerza", 28)
def _(e):
    e.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#141036", "#3a2e7a", "#9a6ab8", "#f2c88a"])
    e.estrellas(60, 70)
    for k, c in enumerate(("#7affc8", "#a8a0ff", "#ff9ae0")):
        pts = [(x, 30 + k * 14 + int(math.sin(x / 30 + k + e.fase * 2 * math.pi) * 10))
               for x in range(0, ANCHO + 10, 10)]
        e.capa(lambda d, pts=pts, c=c: d.line(pts, fill=rgba(c, 70), width=4))
    e.poly([(110, 92), (210, 92), (196, 106), (170, 136), (150, 128), (124, 106)], "#4a3e5a")
    e.textura(110, 92, 210, 136, ["#3a2e4a", "#5a4e6e"], 0.15, base="#4a3e5a")
    e.rect(110, 90, 210, 92, "#8a7aa8")
    e.rect(152, 30, 168, 90, "#d8c8e8")
    e.rect(152, 30, 154, 90, "#f4ecff")
    e.poly([(148, 30), (172, 30), (160, 12)], "#d8c8e8")
    for x in (128, 186):
        e.rect(x, 56, x + 8, 90, "#b8a8d0")
        e.poly([(x - 2, 56), (x + 10, 56), (x + 4, 46)], "#b8a8d0")
    e.brillo(160, 20, 30, "#fff4c8", 140, pulso=0.3)
    for x, y, s in ((40, 70, 10), (270, 60, 14), (90, 40, 6), (240, 110, 8)):
        y += round(2 * e.onda(x / 90))
        e.poly([(x - s, y), (x + s, y), (x + s // 2, y + s), (x - s // 3, y + s // 2)], "#3a2e4a")
        e.rect(x - s, y - 1, x + s, y, "#7a6a98")
    e.cordillera(160, 26, 50, "#2a2240", "#8a7ab8", "#1a142a", textura=0.06)
    for x in (30, 80, 250, 300):
        e.poly([(x - 4, 170), (x + 4, 170), (x + 1, 140), (x - 1, 140)], "#a8f0ff")
        e.brillo(x, 150, 14, "#a8f0ff", 90, pulso=0.4)


@escenario("umbara", "Umbara — mundo de sombras", 29)
def _(e):
    e.degradado(0, 0, ANCHO - 1, ALTO - 1, ["#04050c", "#0a1022", "#141c34", "#0a0e1a"])
    e.cordillera(100, 30, 40, "#0e1424", octavas=3, textura=0.03)
    e.niebla(80, 120, "#2a3a5a", 60)
    for _ in range(26):
        x = e.rnd.randrange(ANCHO)
        base = e.rnd.randint(110, 175)
        alto = e.rnd.randint(30, 90)
        c = e.rnd.choice(["#4af0ff", "#c060ff", "#6affb0"])
        e.linea([(x, base), (x + e.rnd.randint(-6, 6), base - alto)], "#1a2236", 2)
        for k in range(3):
            y = base - alto + k * 10
            e.elipse(x - 3, y - 3, x + 3, y + 3, c)
            e.pix(x - 1, y - 1, "#ffffff")
            e.brillo(x, y, 12, c, 70, pulso=0.5)
    e.cordillera(160, 14, 20, "#0a0e18", textura=0.04)
    for _ in range(60):
        x, y = e.rnd.randrange(ANCHO), e.rnd.randint(160, 178)
        e.pix(x, y, e.rnd.choice(["#4af0ff", "#c060ff"]))
    e.niebla(130, 175, "#1a2a4a", 70)
    e.brasas(30, 0, 60, ANCHO - 1, 172, "#7af0e0")


@escenario("pueblo_colonia", "Pueblo o colonia (Ryloth, Kiros, Raydonia, Batuu)", 30)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#5e98d4", "#9ec4e2", "#ecdcc0"])
    e.nubes(15, 25, "#f8f8f4", 5)
    e.cordillera(100, 40, 60, "#b08a68", "#d4ae88", "#8a6a4c", textura=0.05)
    e.rect(0, 120, ANCHO - 1, ALTO - 1, "#c8a880")
    e.textura(0, 120, ANCHO - 1, ALTO - 1, ["#b8986e", "#d8b890", "#a88860"], 0.1)
    casas = [(10, 104, 40, 30), (60, 110, 36, 24), (230, 106, 44, 30), (280, 112, 36, 22), (110, 96, 28, 30)]
    for x, y, w, h in casas:
        e.rect(x, y, x + w, y + h, "#d8b890")
        e.elipse(x, y - h // 2, x + w, y + h // 2, "#d8b890")
        e.elipse(x + 2, y - h // 2 + 1, x + w // 2, y, "#ead0a8")
        e.rect(x + w - 2, y, x + w, y + h, "#b8986e")
        arco(e, x + w // 2 - 4, y + h - 14, x + w // 2 + 4, y + h, "#4a3424")
        e.rect(x + 4, y + 4, x + 8, y + 8, "#4a3424")
    for x, c in ((150, "#c84a3a"), (190, "#3a8ac8")):
        e.rect(x, 128, x + 2, 150, "#6a4a30")
        e.rect(x + 30, 128, x + 32, 150, "#6a4a30")
        e.poly([(x - 4, 128), (x + 36, 128), (x + 32, 120), (x, 120)], c)
        e.rect(x + 2, 140, x + 30, 150, "#8a6a48")
        for k in range(5):
            e.elipse(x + 4 + k * 5, 136, x + 8 + k * 5, 140, e.rnd.choice(["#e8c04a", "#e86a3a", "#8ad04a"]))
    e.rocas(10, 160, 178, "#a88860", (3, 8))
    e.motas(24, 0, 110, ANCHO - 1, 176, "#f0dcb8", 3)


@escenario("puesto_avanzado", "Puesto avanzado en luna rocosa (Rishi, Florrum, Vanqor)", 31)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#04060e", "#0e1428", "#1e2840"])
    e.estrellas(140, 110)
    e.astro(70, 60, 34, "#c87a4a", sombra="#4a2418", anillos=2)
    e.cordillera(116, 34, 50, "#3a4050", "#5a6278", "#262a36", textura=0.06)
    e.rect(150, 86, 250, 128, "#6a7080")
    e.poly([(146, 86), (254, 86), (240, 74), (160, 74)], "#7a8090")
    e.rect(150, 86, 152, 128, "#8a90a0")
    for x in range(160, 244, 14):
        e.rect(x, 98, x + 8, 104, "#2a3040")
        e.rect(x + 1, 99, x + 7, 103, "#ffd88a")
    e.rect(192, 112, 208, 128, "#2a2e3a")
    for k in range(10):
        y = 74 - k * 6
        e.linea([(270 - k, 128 - k * 6), (270 - k, y)], "#5a6070")
    e.linea([(262, 30), (278, 128)], "#5a6070")
    e.linea([(278, 30), (262, 128)], "#5a6070")
    e.rect(268, 24, 272, 30, "#5a6070")
    e.brillo(270, 24, 8, "#ff3a3a", 140, pulso=0.9)
    e.elipse(110, 66, 138, 82, "#a8aeb8")
    e.elipse(114, 68, 134, 78, "#6a707e")
    e.linea([(124, 82), (128, 128)], "#5a6070", 2)
    e.brillo(200, 100, 40, "#ffd88a", 50, pulso=0.15)
    e.cordillera(150, 16, 30, "#2e323e", "#4a5062", "#1e2028", textura=0.1)
    e.rocas(16, 156, 178, "#3a3e4c", (4, 10))
    for x in (60, 74, 88):
        e.rect(x, 138, x + 10, 146, "#5a5040")
        e.rect(x, 138, x + 10, 138, "#7a6e58")


@escenario("moraband", "Moraband — valle de los señores Sith", 32)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 120, ["#160404", "#4a0c0c", "#9a2a1a", "#d8603a"])
    e.degradado(0, 108, ANCHO - 1, ALTO - 1, ["#7a2a18", "#4a1410", "#1e0606"])
    e.textura(0, 108, ANCHO - 1, ALTO - 1, ["#5a1a10", "#8a3a22"], 0.08)
    e.poly([(130, 110), (190, 110), (166, 70), (154, 70)], "#2a0a08")
    e.brillo(160, 104, 16, "#ff6a3a", 100, pulso=0.4)
    e.poly([(0, 0), (70, 0), (112, ALTO), (0, ALTO)], "#4a1210")
    e.poly([(250, 0), (ANCHO, 0), (ANCHO, ALTO), (208, ALTO)], "#4a1210")
    e.textura(0, 0, ANCHO - 1, ALTO - 1, ["#3a0c0a", "#5e1a14"], 0.15, base="#4a1210")
    e.linea([(70, 0), (112, ALTO)], "#8a2a1a", 2)
    e.linea([(250, 0), (208, ALTO)], "#2a0806", 2)
    for y in range(10, ALTO, 16):
        e.linea([(0, y), (60 + y * 42 // ALTO, y + 4)], "#3a0c0a")
        e.linea([(ANCHO, y), (260 - y * 42 // ALTO, y + 4)], "#3a0c0a")
    for x, signo in ((40, 1), (276, -1)):
        e.poly([(x - 14, 150), (x + 14, 150), (x + 10, 70), (x - 10, 70)], "#2e0a08")
        e.poly([(x - 10, 70), (x + 10, 70), (x, 46)], "#2e0a08")
        e.elipse(x - 6, 56, x + 6, 70, "#1a0604")
        e.linea([(x - signo * 14, 150), (x - signo * 10, 70)], "#8a2a1a")
        e.rect(x - 2, 62, x - 1, 63, "#ff4a2a")
        e.rect(x + 1, 62, x + 2, 63, "#ff4a2a")
    e.niebla(100, 150, "#c84a2a", 60)
    e.cordillera(160, 12, 30, "#3a0e0c", "#7a2418", "#1e0606", textura=0.08)
    e.brasas(40, 0, 0, ANCHO - 1, ALTO - 1, "#ff8a5a")


@escenario("dagobah", "Dagobah — pantano", 33)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 130, ["#4a5a3a", "#6a7a58", "#8a9a76"])
    e.niebla(30, 110, "#b8c8a0", 100)
    for x in range(20, ANCHO, 60):
        arbol_retorcido(e, x + e.rnd.randint(-10, 10), 130, e.rnd.randint(60, 100), "#3a3a28", "#4a5a30")
    e.lianas(20, "#5a6a3a", 70)
    e.rect(0, 130, ANCHO - 1, ALTO - 1, "#2a3a2a")
    reflejo = e.img.crop((0, 70, ANCHO, 130)).transpose(Image.FLIP_TOP_BOTTOM)
    capa_reflejo = Image.new("RGBA", reflejo.size, (0, 0, 0, 0))
    capa_reflejo.paste(reflejo, (0, 0))
    capa_reflejo.putalpha(70)
    e.img.alpha_composite(capa_reflejo, (0, 130))
    for y in range(134, ALTO, 6):
        for x in range(e.rnd.randint(0, 20) - 30 + int(e.fase * 30), ANCHO, 30):
            e.rect(x, y, x + 8, y, "#5a6a4a")
    e.poly([(40, 150), (150, 142), (152, 148), (42, 156)], "#4a3a26")
    e.rect(40, 150, 150, 150, "#6a5a3a")
    e.niebla(120, 165, "#a8b890", 80)
    e.motas(18, 0, 60, ANCHO - 1, 150, "#e0ff8a", 4)


@escenario("utapau", "Utapau — ciudad en los sumideros", 34)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 60, ["#b8b8a8", "#dcd8c4"])
    e.degradado(0, 60, ANCHO - 1, ALTO - 1, ["#8a7e64", "#4a4232", "#1e1a12"])
    for x0, x1 in ((0, 110), (210, ANCHO - 1)):
        e.rect(x0, 0, x1, ALTO - 1, "#b4a284")
        for y in range(0, ALTO, 12):
            e.rect(x0, y, x1, y + 1, "#94845e")
        e.textura(x0, 0, x1, ALTO - 1, ["#a4926e", "#c8b694"], 0.1, base="#b4a284")
    e.linea([(110, 0), (110, ALTO)], "#e0d0ae", 2)
    e.linea([(210, 0), (210, ALTO)], "#6a5a40", 2)
    for x, y in ((40, 40), (80, 90), (30, 140), (250, 60), (290, 110), (240, 150)):
        e.elipse(x - 14, y - 10, x + 14, y + 6, "#d8c8a4")
        e.rect(x - 14, y - 2, x + 14, y + 6, "#c8b894")
        for k in range(-10, 12, 6):
            e.rect(x + k, y, x + k + 2, y + 2, "#ffd88a")
        e.brillo(x, y + 2, 16, "#ffd88a", 50, pulso=0.3)
    for y in (70, 120):
        e.rect(110, y, 210, y + 3, "#6a5e46")
        e.rect(110, y, 210, y, "#a8987a")
        for x in range(112, 210, 8):
            e.rect(x, y + 3, x, y + 6, "#5a4e38")
    e.niebla(130, 179, "#2a2418", 90)
    e.motas(30, 110, 20, 210, 170, "#e8d8b0", 3)


@escenario("naboo", "Naboo — Theed y el lago", 35)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 110, ["#4a8ad4", "#8ab8e8", "#d8e8f4"])
    e.nubes(15, 30, "#ffffff", 7)
    e.cordillera(100, 46, 50, "#6a8a5a", "#8aaa72", "#4a6a40", textura=0.05)
    for x in (40, 70, 250):
        for y in range(54, 120):
            e.rect(x + (y % 3) - 1, y, x + 3 + (y % 2), y, "#e8f4ff" if (y - e.t) % 4 else "#b8d4ec")
        e.brillo(x + 1, 118, 10, "#ffffff", 120, pulso=0.3)
    for x, y, w, h in ((110, 80, 30, 34), (150, 70, 40, 44), (196, 84, 26, 30)):
        e.rect(x, y, x + w, y + h, "#e0d0a8")
        e.rect(x, y, x + 1, y + h, "#f4e8c8")
        e.rect(x + w - 1, y, x + w, y + h, "#b8a880")
        for cx in range(x + 3, x + w - 2, 5):
            e.rect(cx, y + 8, cx + 1, y + h, "#c4b48c")
        e.elipse(x - 2, y - w // 2, x + w + 2, y + w // 2, "#4a8a6a")
        e.elipse(x + 2, y - w // 2 + 2, x + w // 2, y - 2, "#6aaa8a")
        e.rect(x - 2, y, x + w + 2, y + 1, "#c8b88c")
    e.rect(0, 118, ANCHO - 1, ALTO - 1, "#4a8ab8")
    for y in range(120, ALTO, 5):
        for x in range(e.rnd.randint(0, 16) - 24 + int(e.fase * 24), ANCHO, 24):
            e.rect(x, y, x + 9, y, "#8ac0e0")
    e.cordillera(170, 20, 30, "#4a7a3a", "#6a9a52", "#2e5a26", textura=0.08)
    for x in (16, 300):
        e.arbol(x, 172, 36, "#4a3a2a", "#4a8a3a", 26)


@escenario("campo_batalla", "Campo de batalla en ruinas (Anaxes, Ringo Vinda, asedio de Mandalore)", 36)
def _(e):
    e.degradado(0, 0, ANCHO - 1, 130, ["#2e2e36", "#5a5450", "#8a7660", "#b08a62"])
    e.skyline(110, "#2a2a30", "#ff9a4a", 0.05, ancho=(12, 28), alto=(30, 70), antenas=False)
    for _ in range(14):
        x = e.rnd.randrange(ANCHO)
        e.poly([(x, 60), (x + 6, 40 + e.rnd.randint(0, 20)), (x + 10, 70)], "#2a2a30")
    for x in (40, 130, 220, 290):
        e.humo(x, 110, 90, "#3a3634", 14)
        e.fuego(x, 112, 5)
    e.cordillera(140, 16, 30, "#3e3a36", "#5a5450", "#26221e", textura=0.1)
    for x, y in ((80, 152), (230, 160)):
        e.elipse(x - 22, y - 5, x + 22, y + 5, "#26221e")
        e.elipse(x - 18, y - 4, x + 18, y + 2, "#1a1612")
    e.rect(150, 132, 200, 146, "#5a5e66")
    e.rect(156, 124, 190, 132, "#6a6e76")
    e.rect(150, 132, 200, 132, "#8a8e96")
    e.linea([(190, 128), (214, 120)], "#4a4e56", 2)
    for x in (152, 166, 182, 196):
        e.elipse(x - 4, 144, x + 4, 152, "#2a2a30")
    e.fuego(176, 124, 4)
    for _ in range(12):
        c = e.rnd.choice(["#ff3a3a", "#3a9aff"])
        e.laser(e.rnd.randrange(ANCHO), e.rnd.randint(60, 140), 12, c, e.rnd.choice([-1, 1]), 0.1)
    e.rocas(20, 158, 178, "#4a4440", (3, 9))
    e.brasas(24, 20, 70, 300, 125, "#ffa050")


# ===== fin de los escenarios =====




# ======================================================================
# Qué escenario usa cada ficha del guion
# ======================================================================
FICHAS = [   # (desde, hasta, clave): rangos de fichas de Historia.md
    # Acto I
    (1, 8, "christophsis"), (9, 14, "monasterio_teth"), (15, 15, "cabina"), (16, 18, "dunas_tatooine"),
    (19, 23, "palacio_hutt"), (24, 24, "dunas_tatooine"), (25, 25, "puente_crucero"), (26, 26, "espacio_batalla"),
    (27, 27, "pasillo_republica"), (28, 28, "espacio_batalla"), (29, 29, "cabina"), (30, 31, "pasillo_separatista"),
    (32, 32, "oficina_canciller"), (33, 33, "espacio_batalla"), (34, 35, "fabrica_droides"),
    (36, 36, "puente_crucero"), (37, 37, "hangar_republica"), (38, 40, "puesto_avanzado"),
    (41, 41, "hangar_republica"), (42, 42, "puente_crucero"), (43, 43, "espacio_batalla"),
    (44, 44, "pasillo_republica"), (45, 45, "puente_crucero"), (46, 49, "pueblo_colonia"),
    (50, 50, "oficina_canciller"), (51, 51, "departamento_padme"), (52, 55, "senado"),
    (56, 56, "plataforma_coruscant"), (57, 58, "templo_pasillo"),
    # Acto II
    (59, 59, "templo_pasillo"), (60, 61, "pasillo_separatista"), (62, 62, "ciudadela"), (63, 64, "mustafar"),
    (65, 65, "consejo_jedi"), (66, 66, "oficina_canciller"), (67, 67, "consejo_jedi"), (68, 70, "palacio_elegante"),
    (71, 71, "departamento_padme"), (72, 72, "geonosis"), (73, 73, "fabrica_droides"), (74, 75, "geonosis"),
    (76, 77, "pasillo_republica"), (78, 78, "hangar_republica"), (79, 79, "geonosis"),
    (80, 80, "palacio_mandalore"), (81, 82, "palacio_elegante"), (83, 83, "niveles_bajos"),
    (84, 84, "templo_pasillo"), (85, 85, "puesto_avanzado"), (86, 86, "consejo_jedi"),
    (87, 87, "puesto_avanzado"), (88, 88, "templo_pasillo"), (89, 93, "kamino"), (94, 95, "templo_pasillo"),
    (96, 96, "palacio_elegante"), (97, 97, "templo_pasillo"), (98, 98, "palacio_elegante"), (99, 100, "senado"),
    (101, 101, "departamento_padme"), (102, 102, "dathomir"), (103, 104, "jungla"), (105, 105, "templo_pasillo"),
    (106, 117, "mortis"), (118, 118, "puente_crucero"), (119, 122, "ciudadela"), (123, 123, "consejo_jedi"),
    (124, 125, "jungla"), (126, 126, "puente_crucero"),
    # Acto III
    (127, 136, "umbara"), (137, 137, "pueblo_colonia"), (138, 140, "palacio_elegante"), (141, 141, "ciudadela"),
    (142, 142, "palacio_elegante"), (143, 143, "ciudadela"), (144, 144, "pasillo_republica"),
    (145, 145, "consejo_jedi"), (146, 146, "plataforma_coruscant"), (147, 147, "templo_pasillo"),
    (148, 148, "ciudadela"), (149, 149, "niveles_bajos"), (150, 150, "palacio_elegante"), (151, 154, "naboo"),
    (155, 155, "templo_pasillo"), (156, 156, "consejo_jedi"), (157, 157, "puesto_avanzado"),
    (158, 158, "dathomir"), (159, 161, "pueblo_colonia"), (162, 162, "templo_pasillo"),
    (163, 163, "oficina_canciller"), (164, 164, "departamento_padme"),
    # Acto IV
    (165, 165, "consejo_jedi"), (166, 168, "jungla"), (169, 169, "consejo_jedi"), (170, 172, "jungla"),
    (173, 173, "niveles_bajos"), (174, 174, "palacio_mandalore"), (175, 175, "consejo_jedi"),
    (176, 180, "palacio_mandalore"), (181, 181, "ciudadela"), (182, 182, "dathomir"),
    (183, 183, "palacio_elegante"), (184, 184, "hangar_republica"), (185, 186, "ciudadela"),
    (187, 190, "niveles_bajos"), (191, 191, "consejo_jedi"), (192, 195, "senado"),
    (196, 197, "templo_exterior"), (198, 198, "templo_pasillo"),
    # Acto V
    (199, 199, "campo_batalla"), (200, 203, "kamino"), (204, 204, "oficina_canciller"),
    (205, 205, "niveles_bajos"), (206, 206, "hangar_republica"), (207, 208, "niveles_bajos"),
    (209, 209, "departamento_padme"), (210, 211, "senado"), (212, 212, "oficina_canciller"),
    (213, 214, "palacio_elegante"), (215, 215, "senado"), (216, 216, "niveles_bajos"),
    (217, 218, "consejo_jedi"), (219, 219, "templo_pasillo"), (220, 220, "consejo_jedi"), (221, 221, "dagobah"),
    (222, 222, "mortis"), (223, 224, "moraband"), (225, 225, "templo_pasillo"), (226, 226, "oficina_canciller"),
    (227, 227, "senado"), (228, 228, "consejo_jedi"), (229, 230, "pueblo_colonia"),
    (231, 232, "palacio_elegante"), (233, 233, "templo_pasillo"), (234, 236, "utapau"),
    (237, 237, "templo_pasillo"), (238, 239, "pueblo_colonia"), (240, 240, "fabrica_droides"),
    (241, 241, "campo_batalla"), (242, 244, "fabrica_droides"), (245, 245, "hangar_republica"),
    (246, 248, "niveles_bajos"),
    # Acto VI
    (249, 249, "campo_batalla"), (250, 250, "espacio_batalla"), (251, 254, "pasillo_separatista"),
    (255, 255, "senado"), (256, 256, "departamento_padme"), (257, 257, "templo_pasillo"),
    (258, 258, "departamento_padme"), (259, 259, "templo_pasillo"), (260, 260, "oficina_canciller"),
    (261, 261, "consejo_jedi"), (262, 262, "templo_pasillo"), (263, 263, "palacio_elegante"),
    (264, 264, "consejo_jedi"), (265, 265, "plataforma_coruscant"), (266, 266, "senado"),
    (267, 268, "campo_batalla"), (269, 270, "pasillo_republica"), (271, 272, "utapau"),
    (273, 273, "oficina_canciller"), (274, 274, "templo_pasillo"), (275, 275, "consejo_jedi"),
    (276, 276, "departamento_padme"), (277, 280, "oficina_canciller"), (281, 283, "pasillo_republica"),
    (284, 284, "jungla"), (285, 285, "consejo_jedi"), (286, 286, "departamento_padme"), (287, 287, "mustafar"),
    (288, 288, "departamento_padme"), (289, 289, "templo_pasillo"), (290, 290, "departamento_padme"),
    (291, 293, "mustafar"), (294, 294, "oficina_canciller"), (295, 295, "kamino"),
    # líneas de la luz, el emperador y el exilio
    (296, 297, "senado"), (298, 298, "oficina_canciller"), (299, 299, "templo_pasillo"),
    (300, 300, "pasillo_republica"), (301, 301, "utapau"), (302, 302, "senado"), (303, 303, "consejo_jedi"),
    (304, 304, "naboo"), (305, 306, "oficina_canciller"), (307, 307, "departamento_padme"), (308, 308, "senado"),
    (309, 309, "plataforma_coruscant"), (310, 310, "cabina"), (311, 312, "naboo"),
]
TOTAL_FICHAS = 312


def mapa_fichas():
    """Convierte los rangos en {"D001": clave, ...} y comprueba que no falte ni sobre nada."""
    mapa = {}
    for desde, hasta, clave in FICHAS:
        assert clave in ESCENARIOS, f"escenario desconocido: {clave}"
        for n in range(desde, hasta + 1):
            ficha = f"D{n:03d}"
            assert ficha not in mapa, f"{ficha} está en dos rangos"
            mapa[ficha] = clave
    faltan = [f"D{n:03d}" for n in range(1, TOTAL_FICHAS + 1) if f"D{n:03d}" not in mapa]
    assert not faltan, f"fichas sin escenario: {faltan}"
    sin_uso = set(ESCENARIOS) - set(mapa.values())
    assert not sin_uso, f"escenarios que ninguna ficha usa: {sin_uso}"
    return mapa


CUADROS = 24             # cuadros por ciclo de animación
DURACION = 100           # milisegundos por cuadro: el ciclo dura 2.4 s y se repite
CUADROS_60 = 144         # el mismo ciclo de 2.4 s a 60 cuadros por segundo
COLUMNAS_60 = 12         # los 144 cuadros van en una cuadrícula de 12x12 (3840x2160)


def dibujar(clave, t=0, cuadros=1):
    e = Escena(ESCENARIOS[clave][1], t, cuadros)
    ESCENARIOS[clave][2](e)
    return e.img


def animar(clave):
    """Dibuja los cuadros del ciclo y los guarda como GIF (x4, para verlo) y como tira PNG
    (x1, todos los cuadros uno junto a otro, para que el juego los cargue)."""
    cuadros = [dibujar(clave, t, CUADROS).convert("RGB") for t in range(CUADROS)]
    tira = Image.new("RGB", (ANCHO * CUADROS, ALTO))
    for t, c in enumerate(cuadros):
        tira.paste(c, (t * ANCHO, 0))
    tira.save(CARPETA / "animados_1x" / f"{clave}.png")
    # una sola paleta para todos los cuadros: así los colores no parpadean entre cuadro y cuadro
    paleta = tira.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    gif = [c.quantize(palette=paleta, dither=Image.Dither.NONE).resize((ANCHO * ESCALA, ALTO * ESCALA), Image.NEAREST)
           for c in cuadros]
    gif[0].save(CARPETA / "animados" / f"{clave}.gif", save_all=True, append_images=gif[1:],
                duration=DURACION, loop=0, disposal=1)


def animar_60(clave):
    """El ciclo a 60 fps: 144 cuadros de 320x180 en una cuadrícula de 12x12. El cuadro t está en
    x = (t % 12) * 320, y = (t // 12) * 180. No hay GIF: un GIF no puede ir a 60 fps."""
    hoja = Image.new("RGB", (ANCHO * COLUMNAS_60, ALTO * (CUADROS_60 // COLUMNAS_60)))
    for t in range(CUADROS_60):
        hoja.paste(dibujar(clave, t, CUADROS_60).convert("RGB"), ((t % COLUMNAS_60) * ANCHO, (t // COLUMNAS_60) * ALTO))
    hoja.save(CARPETA / "animados_60" / f"{clave}.png")


def galeria(imagenes, columnas=4, escala=2):
    try:
        fuente = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        fuente = ImageFont.load_default()
    cw, ch = ANCHO * escala, ALTO * escala + 26
    filas = (len(imagenes) + columnas - 1) // columnas
    hoja = Image.new("RGBA", (columnas * cw, filas * ch), "#24202e")
    d = ImageDraw.Draw(hoja)
    for i, (clave, img) in enumerate(imagenes):
        x, y = (i % columnas) * cw, (i // columnas) * ch
        hoja.alpha_composite(img.resize((ANCHO * escala, ALTO * escala), Image.NEAREST), (x, y))
        d.text((x + 6, y + ALTO * escala + 4), ESCENARIOS[clave][0], fill="#f0ecf8", font=fuente)
    return hoja


def main(claves, animados=True, a_60=False):
    for carpeta in ("fondos", "fondos_1x", "animados", "animados_1x", "animados_60"):
        (CARPETA / carpeta).mkdir(exist_ok=True)
    hechas = []
    for clave in claves:
        img = dibujar(clave)
        img.save(CARPETA / "fondos_1x" / f"{clave}.png")
        img.resize((ANCHO * ESCALA, ALTO * ESCALA), Image.NEAREST).save(CARPETA / "fondos" / f"{clave}.png")
        hechas.append((clave, img))
        if animados:
            animar(clave)
        if a_60:
            animar_60(clave)
    galeria(hechas).save(CARPETA / "galeria.png")
    mapa = mapa_fichas()
    (CARPETA / "fichas.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    indice = {c: {"nombre": ESCENARIOS[c][0], "fondo": f"fondos/{c}.png", "fondo_1x": f"fondos_1x/{c}.png",
                  "fichas": [f for f, e in mapa.items() if e == c]} for c in ESCENARIOS}
    (CARPETA / "escenarios.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(hechas)} escenarios generados en {CARPETA}; {len(mapa)} fichas con fondo asignado")


if __name__ == "__main__":
    pedidas = [a for a in sys.argv[1:] if not a.startswith("--")]
    main([c for c in ESCENARIOS if not pedidas or any(p in c for p in pedidas)], "--sin-animar" not in sys.argv,
         "--60fps" in sys.argv)
