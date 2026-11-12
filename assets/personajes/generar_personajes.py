"""Genera los sprites de cuerpo completo de todos los personajes del guion.

Uso:  python generar_personajes.py            (todos)
      python generar_personajes.py anakin ...  (solo los que se nombren)

Salida, junto a este archivo:
  sprites/<clave>.png      sprite escalado x8 (320x448), fondo transparente
  sprites_1x/<clave>.png   sprite original de 40x56, para escalar en el juego
  galeria.png              todos juntos con su nombre, para revisarlos
  personajes.json          clave -> nombre y archivo, para la interfaz
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageDraw, ImageFont

from motor_pixel import ALTO, ANCHO, CENTRO, SUELO, Sprite

ESCALA = 8           # cada píxel del sprite se vuelve un bloque de 8x8
CARPETA = Path(__file__).resolve().parent
PERSONAJES = {}   # clave -> (nombre, función que lo dibuja)

# ---------- paleta ----------
PIEL_CLARA, PIEL_MEDIA, PIEL_MORENA, PIEL_OSCURA = "#f2c9a0", "#dca47a", "#b9805a", "#6e4430"
PIEL_PALIDA, PIEL_CLON = "#f3e3d8", "#c98e62"
NEGRO_PELO, CASTANO, CASTANO_CLARO, PELIRROJO, RUBIO, CANOSO = (
    "#2a2120", "#5e3a22", "#8a5a30", "#b5652c", "#e9cd6c", "#cfcac2")
BLANCO_ARMADURA, TRAJE_NEGRO = "#e9e9ef", "#2c2c36"
LEGION_501, LEGION_212, GUARDIA, REMESA = "#3a6ed8", "#e8892c", "#c0302a", "#7c808c"
TUNICA_CLARA, TUNICA_MEDIA, MARRON, MARRON_OSC, NEGRO_CALIDO = (
    "#dcc7a0", "#a87e54", "#6e4a30", "#4a3426", "#2e2624")
CUERO, BOTAS = "#7a5232", "#2e2624"


def personaje(clave, nombre):
    def registrar(funcion):
        PERSONAJES[clave] = (nombre, funcion)
        return funcion
    return registrar


# ---------- piezas que se repiten ----------
def jedi(s, piel, pelo=None, tunica=TUNICA_CLARA, tabardo=TUNICA_MEDIA, pantalon=MARRON, talla="adulto",
         complexion="normal", larga=False, capa=None):
    """Jedi con túnica, tabardo y cinturón de cuero."""
    s.cuerpo(talla, complexion, piel=piel, torso=tunica, piernas=pantalon, botas=BOTAS)
    if capa:
        s.capa(capa)
    if larga:
        s.tunica_larga(tabardo)
    else:
        s.faldon(tunica, 4)
    s.tabardo(tabardo)
    s.cinturon(CUERO, "#c9a24a")
    s.escote(piel)
    if pelo:
        s.pelo(*pelo)


def clon(s, marca, pelo=("rapado", NEGRO_PELO), complexion="normal", kama=None, casco=True, antena=False,
         piel=PIEL_CLON):
    """Soldado clon con la armadura blanca y las marcas de su legión."""
    s.cuerpo("adulto", complexion, piel=piel, torso=BLANCO_ARMADURA, piernas=BLANCO_ARMADURA,
             botas=BLANCO_ARMADURA, manos=TRAJE_NEGRO)
    s.armadura_clon(marca, kama=kama)
    if pelo:
        s.pelo(*pelo)
    s.cara()
    if casco:
        s.casco_bajo_brazo(marca, antena=antena)


# ======================================================================
# Protagonistas
# ======================================================================
@personaje("anakin_skywalker", "Anakin Skywalker")
def _(s):
    s.cuerpo(piel=PIEL_CLARA, torso="#5a3a28", piernas="#3e2c22", botas="#1e1a1a")
    s.faldon("#5a3a28", 4)
    s.tabardo("#2a2020")
    s.cinturon(CUERO, "#b0b0b8")
    s.escote(PIEL_CLARA)
    s.rect(*s.g.mi, "#1e1a1a")                      # guante de la mano mecánica
    s.pelo("ondulado", CASTANO)
    s.cara()
    s.pix(CENTRO - 3, s.g.ojo_y - 2, s.fijo("#b0605a"))   # cicatriz sobre el ojo
    s.pix(CENTRO - 3, s.g.ojo_y + 2, "#b0605a")
    s.sable("azul", "i")


@personaje("ahsoka_tano", "Ahsoka Tano")
def _(s):
    s.cuerpo("joven", piel="#e07b39", torso="#7a3428", piernas="#8a8a98", botas=MARRON)
    s.cinturon(MARRON_OSC, "#c9a24a")
    s.faldon("#7a3428", 3)
    marcas = s.fijo("#f6f2ea")
    x0, y0, x1, y1 = s.g.cab
    s.pixs([(CENTRO - 1, y0 + 1), (CENTRO, y0 + 1), (CENTRO - 1, y0 + 2), (CENTRO, y0 + 2),
            (CENTRO - 4, s.g.ojo_y - 2), (CENTRO - 3, s.g.ojo_y - 2), (CENTRO + 2, s.g.ojo_y - 2),
            (CENTRO + 3, s.g.ojo_y - 2), (CENTRO - 4, s.g.ojo_y + 2), (CENTRO + 3, s.g.ojo_y + 2),
            (CENTRO - 1, y1 - 1), (CENTRO, y1 - 1)], marcas)
    s.montrales("#f6f2ea", "#3a6ed8")
    s.cara()
    s.sable("verde", "i")
    s.sable("verde", "d", largo=8)


@personaje("obi_wan_kenobi", "Obi-Wan Kenobi")
def _(s):
    jedi(s, PIEL_CLARA, ("corto", PELIRROJO))
    s.hombreras("#f2f2f4", 3)
    s.rect(s.g.tor[0] + 1, s.g.tor[1] + 2, s.g.tor[2] - 1, s.g.tor[1] + 4, "#f2f2f4")
    s.escote(PIEL_CLARA)
    s.barba("corta", PELIRROJO)
    s.cara()
    s.sable("azul", "i")


@personaje("padme_amidala", "Padmé Amidala")
def _(s):
    s.cuerpo(piel=PIEL_CLARA, torso="#2c3c70", piernas="#2c3c70", botas="#1c2240", complexion="delgado")
    s.cinturon("#c8ccd8")
    s.rect(s.g.tor[0], s.g.tor[1], s.g.tor[2], s.g.tor[1] + 1, "#c8ccd8")
    s.pelo("chongo", "#4a2c1c")
    s.cara(boca="#c0605a")
    s.pistola("d", "#d0d4dc")


@personaje("capitan_rex", "Capitán Rex")
def _(s):
    clon(s, LEGION_501, pelo=("rapado", "#e8e0c8"), kama="#2c2c36")
    s.funda("i")
    s.funda("d")
    s.pistola("d")


@personaje("yoda", "Maestro Yoda")
def _(s):
    verde, tunica = "#95b860", "#a07a50"
    s.poly([(15, 45), (24, 45), (26, SUELO), (13, SUELO)], tunica)
    s.pliegues(13, 45, 26, SUELO - 1, tunica)
    s.rect(12, 46, 14, 49, tunica)
    s.rect(12, 50, 14, 51, verde)
    s.rect(25, 46, 27, 49, tunica)
    s.rect(25, 50, 27, 51, verde)
    s.rect(14, 36, 25, 44, verde)
    for x, y in ((14, 36), (25, 36), (14, 44), (25, 44)):
        s.quitar(x, y)
    s.poly([(14, 39), (8, 37), (14, 42)], verde)
    s.poly([(25, 39), (31, 37), (25, 42)], verde)
    s.pixs([(16, 36), (18, 35), (21, 35), (23, 36)], "#e8e8e0")
    ojos = s.fijo("#3a4a2a")
    s.rect(16, 40, 17, 40, ojos)
    s.rect(22, 40, 23, 40, ojos)
    s.pixs([(16, 39), (17, 39), (22, 39), (23, 39)], s.fijo("#6f9440"))
    s.rect(19, 43, 20, 43, s.fijo("#6a8a40"))
    s.rect(28, 40, 28, SUELO, "#6a4a2a", "frente")


@personaje("general_grievous", "General Grievous")
def _(s):
    hueso, gris, capa = "#ece6d6", "#8a8a96", "#5a2a2a"
    s.poly([(12, 22), (27, 22), (32, SUELO), (7, SUELO)], capa, "fondo")
    for x in (15, 22):
        s.rect(x, 37, x + 2, 50, gris)
        s.rect(x, 38, x + 2, 41, hueso)
        s.rect(x - 1, 51, x + 3, SUELO, hueso)
    s.rect(14, 23, 25, 36, hueso)
    s.rect(15, 25, 24, 25, gris)
    s.rect(15, 28, 24, 28, gris)
    s.rect(18, 29, 21, 33, s.fijo("#5c6a48"))
    s.rect(11, 23, 13, 38, hueso)
    s.rect(26, 23, 28, 38, hueso)
    s.rect(11, 29, 13, 29, gris)
    s.rect(26, 29, 28, 29, gris)
    s.rect(16, 11, 23, 21, hueso)
    s.rect(17, 10, 22, 10, hueso)
    s.rect(17, 15, 22, 17, s.fijo("#2a2a30"))
    s.rect(18, 19, 21, 21, gris)
    for x in (17, 21):
        s.rect(x, 15, x + 1, 16, "#ffd23a", "efectos")
    s.g = SimpleNamespace(mi=(11, 39, 13, 40), md=(26, 39, 28, 40))
    s.rect(*s.g.mi, gris)
    s.rect(*s.g.md, gris)
    s.sable("azul", "i", 14)
    s.sable("verde", "d", 14)


@personaje("r2d2", "R2-D2")
def _(s):
    astromecanico(s, "#eef0f4", "#2f5fc8", "#c4c8d4")


# ======================================================================
# Clones y la Remesa Mala
# ======================================================================
def tatuaje(s, puntos, color):
    s.pixs(puntos, s.fijo(color))


@personaje("fives", "Fives")
def _(s):
    clon(s, LEGION_501, kama=TRAJE_NEGRO)
    x1 = s.g.cab[2]
    tatuaje(s, [(x1 - 1, s.g.ojo_y - 2), (x1 - 1, s.g.ojo_y - 1), (x1 - 2, s.g.ojo_y - 2)], "#2a3a6a")
    s.funda("d")
    s.pistola("d")


@personaje("echo", "Echo")
def _(s):
    clon(s, LEGION_501, kama=TRAJE_NEGRO)
    s.rifle("d")


@personaje("comandante_cody", "Comandante Cody")
def _(s):
    clon(s, LEGION_212, antena=True)
    tatuaje(s, [(CENTRO - 4, s.g.ojo_y + 1), (CENTRO - 4, s.g.ojo_y + 2), (CENTRO - 5, s.g.ojo_y + 3)], "#e8b090")
    s.rifle("d")


@personaje("waxer", "Waxer")
def _(s):
    clon(s, LEGION_212)
    tatuaje(s, [(CENTRO + 3, s.g.ojo_y + 2), (CENTRO + 4, s.g.ojo_y + 2), (CENTRO + 3, s.g.ojo_y + 3)], "#e8892c")
    s.rifle("d")


@personaje("boil", "Boil")
def _(s):
    clon(s, LEGION_212)
    s.barba("bigote", NEGRO_PELO)
    s.rifle("d")


@personaje("hevy", "Hevy")
def _(s):
    clon(s, "#9aa2b0", complexion="fornido", casco=False)
    s.arma_pesada()


@personaje("axe", "Axe")
def _(s):
    s.cuerpo(piel=PIEL_CLON, torso=BLANCO_ARMADURA, piernas=BLANCO_ARMADURA, botas=BLANCO_ARMADURA,
             manos=TRAJE_NEGRO)
    s.armadura_clon(LEGION_501, marcas_piernas=False)
    s.rect(s.g.tor[0] + 2, s.g.tor[1] + 2, s.g.tor[2] - 2, s.g.tor[1] + 3, "#4a4a55")
    s.casco_completo(BLANCO_ARMADURA, "#e8c040", LEGION_501)


@personaje("hardcase", "Hardcase")
def _(s):
    clon(s, LEGION_501, casco=False)
    s.arma_pesada()


@personaje("jesse", "Jesse")
def _(s):
    clon(s, LEGION_501)
    y = s.g.ojo_y
    tatuaje(s, [(CENTRO - 1, y - 3), (CENTRO, y - 3), (CENTRO - 2, y - 2), (CENTRO + 1, y - 2),
                (CENTRO - 4, y + 2), (CENTRO + 3, y + 2), (CENTRO - 1, y + 3), (CENTRO, y + 3)], "#2f5fc8")
    s.rifle("d")


@personaje("dogma", "Dogma")
def _(s):
    clon(s, LEGION_501, pelo=("corto", NEGRO_PELO))
    s.rifle("d")


@personaje("kix", "Kix")
def _(s):
    clon(s, LEGION_501)
    rojo = s.fijo("#d03030")
    s.rect(CENTRO - 1, s.g.tor[1] + 2, CENTRO, s.g.tor[1] + 6, rojo)
    s.rect(CENTRO - 3, s.g.tor[1] + 3, CENTRO + 2, s.g.tor[1] + 4, rojo)
    tatuaje(s, [(s.g.cab[0], s.g.ojo_y - 2), (s.g.cab[0], s.g.ojo_y - 1), (s.g.cab[0] + 1, s.g.ojo_y - 2)], "#1a1a22")
    s.pistola("d")


@personaje("tup", "Tup")
def _(s):
    clon(s, LEGION_501, pelo=("coleta", NEGRO_PELO))
    tatuaje(s, [(CENTRO + 2, s.g.ojo_y + 2), (CENTRO + 2, s.g.ojo_y + 3)], "#2a3a6a")
    s.rifle("d")


@personaje("comandante_fox", "Comandante Fox")
def _(s):
    clon(s, GUARDIA, pelo=None, casco=False)
    s.casco_completo(BLANCO_ARMADURA, "#22222a", GUARDIA)
    s.rifle("d")


@personaje("noventa_y_nueve", "99")
def _(s):
    s.cuerpo("joven", "fornido", piel=PIEL_CLON, torso="#5e6878", piernas="#4e5868", botas=BOTAS, cabeza_ancho=12)
    s.cinturon("#3a3a44")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 + 1, y0, x1 - 1, y0, "#b07a52")
    s.cara(boca="#8a5a3a")
    s.pix(CENTRO - 3, s.g.ojo_y + 2, "#241c28")
    s.rect(x1 - 2, y0 + 2, x1 - 1, y0 + 3, "#b07a52")


def remesa(s, complexion="normal", acento="#4a4a55"):
    s.cuerpo("adulto", complexion, piel=PIEL_CLON, torso=REMESA, piernas=REMESA, botas="#4a4e58",
             manos=TRAJE_NEGRO)
    s.hombreras(acento)
    s.rect(s.g.tor[0], s.g.cin - 1, s.g.tor[2], s.g.cin - 1, TRAJE_NEGRO)
    s.cinturon("#3a3a44")


@personaje("tech", "Tech")
def _(s):
    remesa(s, "delgado", "#5a6a8a")
    s.pelo("corto", NEGRO_PELO)
    s.cara()
    s.gafas("#2a2a30", "#7ad8ff")
    s.pistola("d")


@personaje("hunter", "Hunter")
def _(s):
    remesa(s, acento="#6a4a3a")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0, y0 - 1, x1, y0 + 2, "#1c1c22")
    s.pixs([(CENTRO - 1, y0), (CENTRO, y0), (CENTRO - 1, y0 + 1)], s.fijo("#e8e8e8"))
    s.cara()
    tatuaje(s, [(x0 + 1, s.g.ojo_y - 1), (x0 + 2, s.g.ojo_y - 2), (x0 + 1, s.g.ojo_y + 2), (x0 + 2, s.g.ojo_y + 3),
                (x0 + 3, y1 - 1)], "#3a3a44")
    s.rect(s.g.tor[2] - 2, s.g.cin - 3, s.g.tor[2] - 2, s.g.cin + 1, "#c0c4cc", "frente")


@personaje("wrecker", "Wrecker")
def _(s):
    remesa(s, "enorme", "#a85a2a")
    s.cara()
    x0, y0, x1, y1 = s.g.cab
    s.rect(CENTRO - 3, s.g.ojo_y, CENTRO - 3, s.g.ojo_y + 1, s.fijo("#e8e8ec"))
    tatuaje(s, [(x0 + 1, y0 + 2), (x0 + 2, y0 + 3), (x0 + 2, y0 + 4), (x0 + 1, s.g.ojo_y + 3)], "#e6b49a")
    s.arma_pesada("#5a5a66")


@personaje("crosshair", "Crosshair")
def _(s):
    remesa(s, "delgado", "#5a5e6a")
    s.pelo("rapado", "#e4e4e8")
    s.cara()
    tatuaje(s, [(CENTRO + 1, s.g.ojo_y - 1), (CENTRO + 2, s.g.ojo_y - 1), (CENTRO + 3, s.g.ojo_y - 1),
                (CENTRO + 3, s.g.ojo_y), (CENTRO + 3, s.g.ojo_y + 1), (CENTRO + 1, s.g.ojo_y + 2),
                (CENTRO + 2, s.g.ojo_y + 2), (CENTRO + 3, s.g.ojo_y + 2)], "#3a3a44")
    s.rifle("d", largo=22)


@personaje("echo_ciborg", "Echo (cíborg)")
def _(s):
    clon(s, LEGION_501, pelo=None, casco=False, piel="#e0c6b4")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0, y0 - 1, x1, y0 + 2, "#8a8e9a")
    s.rect(x1 - 1, y0 + 3, x1, s.g.ojo_y + 1, "#8a8e9a")
    s.pix(x1, s.g.ojo_y - 1, s.fijo("#ff5050"))
    s.rect(*s.g.bi, "#8a8e9a")
    s.rect(*s.g.mi, "#c0c4cc")
    s.rect(s.g.mi[0] + 1, s.g.mi[3] + 1, s.g.mi[0] + 1, s.g.mi[3] + 2, "#c0c4cc")


# ======================================================================
# Jedi
# ======================================================================
@personaje("mace_windu", "Mace Windu")
def _(s):
    jedi(s, PIEL_OSCURA, tunica="#cbb38c", tabardo="#8a6a48")
    s.cara()
    s.sable("morado", "i")


@personaje("plo_koon", "Plo Koon")
def _(s):
    jedi(s, "#c8643a", tunica="#b09070", tabardo=MARRON, capa="#5a4030")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0, s.g.ojo_y - 1, x1, s.g.ojo_y + 1, "#1e1e26")
    s.rect(CENTRO - 4, s.g.ojo_y, CENTRO - 2, s.g.ojo_y, s.fijo("#5a5a6e"))
    s.rect(CENTRO + 1, s.g.ojo_y, CENTRO + 3, s.g.ojo_y, "#5a5a6e")
    s.rect(x0 + 1, s.g.ojo_y + 2, x1 - 1, y1, "#4a4a52")
    s.rect(CENTRO - 1, s.g.ojo_y + 2, CENTRO, y1, "#6a6a74")
    s.pixs([(x0 + 2, y0 + 1), (x1 - 2, y0 + 1), (CENTRO - 1, y0), (CENTRO, y0)], "#a84c2a")
    s.sable("azul", "i")


@personaje("kit_fisto", "Kit Fisto")
def _(s):
    jedi(s, "#4f9e5a")
    s.tentaculos("#4f9e5a", "#3b7a46")
    s.cara(boca="#f2f2ea")
    s.sable("verde", "i")


@personaje("ki_adi_mundi", "Ki-Adi-Mundi")
def _(s):
    jedi(s, PIEL_CLARA, tunica="#d6c6a6", tabardo="#9a7a58")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 + 1, y0 - 6, x1 - 1, y0, PIEL_CLARA)
    s.rect(x0 + 2, y0 - 8, x1 - 2, y0 - 7, PIEL_CLARA)
    s.rect(x0, y0 + 1, x0, y0 + 6, CANOSO)
    s.rect(x1, y0 + 1, x1, y0 + 6, CANOSO)
    s.barba("corta", CANOSO)
    s.cara()
    s.sable("azul", "i")


@personaje("jocasta_nu", "Jocasta Nu")
def _(s):
    jedi(s, "#f0d2b8", ("chongo", "#ecebe6"), tunica="#ddd4c2", tabardo="#a8916e", larga=True)
    s.cara(boca="#b07a6a")


@personaje("even_piell", "Even Piell")
def _(s):
    jedi(s, "#d4b48c", talla="nino")
    s.orejas("#d4b48c", largo=6, hacia_arriba=True)
    s.cara()
    s.rect(CENTRO + 2, s.g.ojo_y - 2, CENTRO + 2, s.g.ojo_y + 3, s.fijo("#8a3a30"))
    s.sable("verde", "i", largo=9)


@personaje("shaak_ti", "Shaak Ti")
def _(s):
    jedi(s, "#c8473a", tunica="#5a3a2a", tabardo="#3a2a22", larga=True)
    blanco = s.fijo("#f2f0ea")
    x0, y0, x1, y1 = s.g.cab
    s.pixs([(CENTRO - 1, y0 + 1), (CENTRO, y0 + 1), (CENTRO - 4, s.g.ojo_y - 2), (CENTRO + 3, s.g.ojo_y - 2),
            (CENTRO - 4, s.g.ojo_y + 2), (CENTRO + 3, s.g.ojo_y + 2), (CENTRO - 1, y1 - 1), (CENTRO, y1 - 1)], blanco)
    s.montrales("#f2f0ea", "#3a2a3a")
    s.cara()
    s.sable("azul", "i")


@personaje("luminara_unduli", "Luminara Unduli")
def _(s):
    jedi(s, "#a8c060", tunica="#30304a", tabardo="#22223a", larga=True)
    s.capucha("#30304a")
    s.cara(boca="#2a2a3a")
    tatuaje(s, [(x, s.g.cab[3] - 1) for x in range(CENTRO - 3, CENTRO + 3, 2)], "#2a2a3a")
    s.sable("verde", "i")


@personaje("barriss_offee", "Barriss Offee")
def _(s):
    jedi(s, "#b8cc70", tunica="#2a3456", tabardo="#1e2642", larga=True, talla="joven")
    s.capucha("#2a3456")
    s.cara()
    tatuaje(s, [(x, s.g.ojo_y + 3) for x in range(s.g.cab[0] + 1, s.g.cab[2], 2)], "#24305a")
    s.sable("azul", "i")


@personaje("quinlan_vos", "Quinlan Vos")
def _(s):
    jedi(s, "#b08050", tunica="#4a3a30", tabardo="#2e2622")
    s.pelo("rastas", NEGRO_PELO)
    s.cara()
    s.rect(s.g.cab[0], s.g.ojo_y + 2, s.g.cab[2], s.g.ojo_y + 2, s.fijo("#e8c040"))
    s.sable("verde", "i")


@personaje("depa_billaba", "Depa Billaba")
def _(s):
    jedi(s, "#c08a60", ("chongo", NEGRO_PELO), tunica="#cdb592")
    tatuaje(s, [(CENTRO - 1, s.g.cab[1] + 3), (CENTRO, s.g.cab[1] + 3), (CENTRO - 1, s.g.cab[1] + 4)], "#c02a2a")
    s.cara()
    s.sable("verde", "i")


@personaje("tiplar", "Tiplar")
def _(s):
    jedi(s, "#cbc252", tunica="#b8a07a", tabardo="#7a5a3a")
    s.cuernos("#9a9638", [(0, 2), (2, 3), (4, 4), (5, 4), (7, 3), (9, 2)])
    s.cara()
    s.sable("azul", "i")


@personaje("caleb_dume", "Caleb Dume")
def _(s):
    jedi(s, PIEL_MEDIA, ("trenza", CASTANO), talla="nino")
    s.cara()
    s.sable("azul", "i", largo=8)


@personaje("kalifa", "Kalifa")
def _(s):
    jedi(s, PIEL_MORENA, ("corto", NEGRO_PELO), talla="nino", tunica="#cfc0a0")
    s.cara()


# ======================================================================
# Sith, Separatistas y villanos
# ======================================================================
@personaje("canciller_palpatine", "Canciller Palpatine")
def _(s):
    s.cuerpo(piel="#ecd2bc", torso="#7a2232", piernas="#5a1826", botas=BOTAS, manos="#ecd2bc")
    s.tunica_larga("#7a2232", abierta="#4a1420")
    s.rect(CENTRO - 1, s.g.tor[1], CENTRO, s.g.cin, "#4a1420")
    s.rect(s.g.tor[0], s.g.tor[1], s.g.tor[2], s.g.tor[1], "#c9a24a")
    s.pelo("receso", "#a8998e")
    s.cara(boca="#a8706a")


@personaje("darth_sidious", "Darth Sidious")
def _(s):
    s.cuerpo(piel=PIEL_PALIDA, torso="#1c1a22", piernas="#1c1a22", botas=BOTAS, manos=PIEL_PALIDA)
    s.tunica_larga("#1c1a22")
    s.capucha("#1c1a22", cara_sombra="#2c2434")
    s.rect(CENTRO - 2, s.g.cab[3] - 1, CENTRO + 1, s.g.cab[3] - 1, PIEL_PALIDA)
    s.ojos_brillantes("#ffcf3a")
    s.sable("rojo", "d")


@personaje("conde_dooku", "Conde Dooku")
def _(s):
    s.cuerpo("alto", "delgado", piel=PIEL_CLARA, torso="#3a2e28", piernas="#2a221e", botas=BOTAS)
    s.capa("#4a2a1c")
    s.faldon("#3a2e28", 5)
    s.cinturon("#1e1a18", "#c9a24a")
    s.pelo("receso", CANOSO)
    s.barba("corta", CANOSO)
    s.cara()
    s.sable("rojo", "i")


@personaje("darth_vader", "Darth Vader")
def _(s):
    negro = "#1a1a20"
    s.cuerpo("alto", "fornido", piel=negro, torso=negro, piernas=negro, botas="#101014", manos=negro)
    s.capa("#121216")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0, y0 - 1, x1, y1, negro)
    s.rect(x0 - 1, y0 + 5, x1 + 1, y1 + 1, negro)
    s.rect(CENTRO - 4, s.g.ojo_y, CENTRO - 2, s.g.ojo_y + 1, s.fijo("#4a4a5c"))
    s.rect(CENTRO + 1, s.g.ojo_y, CENTRO + 3, s.g.ojo_y + 1, "#4a4a5c")
    s.rect(CENTRO - 1, s.g.ojo_y + 2, CENTRO, y1 - 1, "#3a3a44")
    s.rect(CENTRO - 2, y1 - 1, CENTRO + 1, y1, "#5a5a66")
    s.rect(CENTRO - 2, s.g.tor[1] + 3, CENTRO + 1, s.g.tor[1] + 5, "#5a5a66")
    for x, c in ((CENTRO - 2, "#e03030"), (CENTRO - 1, "#30c060"), (CENTRO, "#3070e0"), (CENTRO + 1, "#e0c030")):
        s.pix(x, s.g.tor[1] + 4, s.fijo(c))
    s.cinturon("#3a3a44")
    for x in (s.g.tor[0] + 1, CENTRO - 1, s.g.tor[2] - 2):
        s.rect(x, s.g.cin, x + 1, s.g.cin + 1, "#b8bcc8")
    s.sable("rojo", "i")


def tatuajes_zabrak(s, color="#141014"):
    x0, y0, x1, y1 = s.g.cab
    y = s.g.ojo_y
    tatuaje(s, [(x0 + 2, y0 + 1), (x0 + 3, y0 + 1), (x1 - 3, y0 + 1), (x1 - 2, y0 + 1), (CENTRO - 1, y0 + 2),
                (CENTRO, y0 + 2), (CENTRO - 1, y0 + 3), (CENTRO, y0 + 3), (CENTRO - 4, y - 1), (CENTRO + 3, y - 1),
                (CENTRO - 4, y), (CENTRO + 3, y), (x0 + 1, y + 2), (x0 + 1, y + 3), (x1 - 1, y + 2),
                (x1 - 1, y + 3), (CENTRO - 1, y + 2), (CENTRO, y + 2), (CENTRO - 2, y1 - 1), (CENTRO + 1, y1 - 1)],
            color)


@personaje("maul", "Maul")
def _(s):
    s.cuerpo(piel="#c42222", torso="#1e1e24", piernas="#aeb0bc", botas="#7a7c88", manos="#1e1e24")
    s.faldon("#1e1e24", 3)
    s.cinturon("#3a3a44")
    tatuajes_zabrak(s)
    s.cuernos("#e6d6a0", [(1, 2), (3, 1), (4, 2), (5, 1), (6, 2), (8, 2)])
    s.cara(ojos="#ffcc30")
    s.sable("rojo", "d", doble=True)


@personaje("savage_opress", "Savage Opress")
def _(s):
    s.cuerpo("alto", "enorme", piel="#d8b040", torso="#2a2228", piernas="#2a2228", botas="#18141a",
             manos="#2a2228")
    s.hombreras("#6a6a76", 4)
    s.cinturon("#4a4a55")
    tatuajes_zabrak(s)
    s.cuernos("#f0e8c8", [(0, 2), (1, 3), (3, 4), (5, 4), (6, 4), (8, 3), (9, 2)])
    s.cara(ojos="#ffcc30")
    s.sable("rojo", "d", doble=True)


@personaje("madre_talzin", "Madre Talzin")
def _(s):
    s.cuerpo("alto", "delgado", piel="#dcd2d2", torso="#7a1a22", piernas="#7a1a22", botas=BOTAS)
    s.tunica_larga("#7a1a22", abierta="#4a0a12")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 1, y0 - 2, x1 + 1, y0 + 1, "#4a0a12")
    for i, x in enumerate(range(x0 - 1, x1 + 2, 2)):
        s.rect(x, y0 - 6 + (i % 2) * 2, x, y0 - 3, "#7a1a22")
    s.cara(boca="#5a1a22")
    tatuaje(s, [(CENTRO - 1, y1 - 1), (CENTRO, y1 - 1), (CENTRO - 1, y1), (CENTRO, y1)], "#2a1a22")


@personaje("asajj_ventress", "Asajj Ventress")
def _(s):
    s.cuerpo(complexion="delgado", piel="#ece6e0", torso="#2a2630", piernas="#3a3540", botas="#1a181e",
             manos="#2a2630")
    s.faldon("#2a2630", 5)
    s.cinturon("#4a4552")
    tatuaje(s, [(CENTRO - 3, s.g.cab[1] + 1), (CENTRO - 3, s.g.cab[1] + 2), (CENTRO + 2, s.g.cab[1] + 1),
                (CENTRO + 2, s.g.cab[1] + 2), (CENTRO - 1, s.g.cab[1]), (CENTRO, s.g.cab[1])], "#8a8a9a")
    s.cara(ojos="#4a5a78")
    s.sable("rojo", "i")
    s.sable("rojo", "d")


@personaje("cad_bane", "Cad Bane")
def _(s):
    s.cuerpo(piel="#4a7ab8", torso="#5a4a3a", piernas="#3a3028", botas=BOTAS, brazos="#6a4a30",
             manos="#3a3028")
    s.tunica_larga("#6a4a30", abierta="#3a3028")
    s.sombrero("#5a3e28", "#2e2218")
    s.cara(ojos="#e02020")
    s.pixs([(s.g.cab[0] + 1, s.g.ojo_y + 2), (s.g.cab[2] - 1, s.g.ojo_y + 2)], s.fijo("#9a9aa8"))
    s.pistola("i")
    s.pistola("d")


@personaje("aurra_sing", "Aurra Sing")
def _(s):
    s.cuerpo(complexion="delgado", piel="#f2eae6", torso="#8a4a3a", piernas="#5a3a30", botas=BOTAS)
    s.cinturon("#3a2a22")
    s.rect(CENTRO + 2, s.g.cab[1] - 8, CENTRO + 2, s.g.cab[1] - 1, "#b8b0a8")
    s.cara(boca="#c03030")
    s.rifle("d")


@personaje("boba_fett", "Boba Fett")
def _(s):
    s.cuerpo("joven", piel=PIEL_MORENA, torso="#6a7a6a", piernas="#566456", botas=BOTAS)
    s.cinturon("#3a3a30")
    s.pelo("corto", NEGRO_PELO)
    s.cara()
    s.pistola("d")


@personaje("hondo_ohnaka", "Hondo Ohnaka")
def _(s):
    s.cuerpo(piel="#b88a62", torso="#7a2a22", piernas="#4a3a30", botas=BOTAS, brazos="#5a3a2a")
    s.faldon("#5a3a2a", 6)
    s.cinturon("#2a2018", "#c9a24a")
    s.gafas("#4a3a2a", "#e8a030", y=s.g.cab[1] + 1)
    s.cara()
    tatuaje(s, [(s.g.cab[0] + 1, s.g.ojo_y + 2), (s.g.cab[2] - 1, s.g.ojo_y + 2)], "#8a5a3a")
    s.pistola("d")


@personaje("wilhuff_tarkin", "Wilhuff Tarkin")
def _(s):
    s.cuerpo("alto", "delgado", piel=PIEL_CLARA, torso="#6a6e5a", piernas="#5a5e4a", botas="#16161a")
    s.cinturon("#16161a", "#b8bcc8")
    s.pixs([(s.g.tor[0] + 1, s.g.tor[1] + 2), (s.g.tor[0] + 2, s.g.tor[1] + 2)], s.fijo("#d03a3a"))
    s.pixs([(s.g.tor[0] + 1, s.g.tor[1] + 3), (s.g.tor[0] + 2, s.g.tor[1] + 3)], s.fijo("#3a6ad0"))
    s.pelo("receso", "#a8987c")
    s.cara()


@personaje("pong_krell", "Pong Krell")
def _(s):
    jedi(s, "#c8884a", tunica="#a07850", tabardo="#6e4a30", talla="alto", complexion="enorme")
    g = s.g
    x0, y0, x1, y1 = g.cab
    s.rect(x0 + 2, y0 - 2, x1 - 2, y0 - 1, "#c8884a")
    s.rect(CENTRO - 3, y1, CENTRO + 2, y1 + 3, "#d87a52", "frente")
    s.cara()
    brazo = "#a07850"
    s.rect(g.bi[0] - 4, g.tor[1] + 2, g.bi[0] - 1, g.tor[1] + 4, brazo, "fondo")
    s.rect(g.bd[2] + 1, g.tor[1] + 2, g.bd[2] + 4, g.tor[1] + 4, brazo, "fondo")
    manos = (g.mi, g.md)
    s.g.mi = (g.bi[0] - 5, g.tor[1] + 2, g.bi[0] - 3, g.tor[1] + 4)
    s.g.md = (g.bd[2] + 3, g.tor[1] + 2, g.bd[2] + 5, g.tor[1] + 4)
    s.rect(*s.g.mi, "#c8884a", "fondo")
    s.rect(*s.g.md, "#c8884a", "fondo")
    s.sable("azul", "i", largo=10)
    s.sable("azul", "d", largo=10)
    s.g.mi, s.g.md = manos


@personaje("rush_clovis", "Rush Clovis")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#3a2a3a", piernas="#2a2030", botas=BOTAS)
    s.rect(CENTRO - 3, s.g.tor[1], CENTRO + 2, s.g.tor[1] + 1, "#5a3a5a")
    s.cinturon("#1e1824")
    s.pelo("corto", NEGRO_PELO)
    s.cara()


@personaje("nute_gunray", "Nute Gunray")
def _(s):
    s.cuerpo(piel="#8a9a78", torso="#6a2a2a", piernas="#4a1e1e", botas=BOTAS)
    s.tunica_larga("#6a2a2a", abierta="#2a1a1a")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 + 1, y0 - 6, x1 - 1, y0 + 1, "#4a1a1a")
    s.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 1, "#c9a24a")
    s.cara(ojos="#d06a30", alto_ojo=1)
    s.rect(CENTRO - 2, y1 - 2, CENTRO + 1, y1 - 2, s.fijo("#5a6a4a"))


# ======================================================================
# Hutts y droides
# ======================================================================
def hutt(s, x0, y0, x1, piel, panza, ojos="#e08a1a"):
    """Hutt de frente: cuerpo de babosa de x0 a x1, con la cabeza arriba en y0."""
    ancho = x1 - x0
    s.elipse(x0, y0 + ancho // 3, x1, SUELO + 4, piel)
    s.rect(x0, SUELO - 1, x1, SUELO, piel)
    s.elipse(x0 + ancho // 6, y0, x1 - ancho // 6, y0 + ancho * 2 // 3, piel)
    s.elipse(x0 + ancho // 4, y0 + ancho // 2, x1 - ancho // 4, SUELO, panza)
    cx = (x0 + x1) // 2
    yo = y0 + ancho // 5
    for x in (cx - ancho // 6 - 1, cx + ancho // 6):
        s.rect(x, yo, x + 1, yo + 1, s.fijo(ojos))
        s.pix(x + 1, yo + 1, "#241c28")
    s.rect(x0 + ancho // 5, yo + ancho // 6 + 1, x1 - ancho // 5, yo + ancho // 6 + 1, s.fijo("#3a2a22"))
    s.rect(x0 + 2, y0 + ancho // 2 + 2, x0 + 4, y0 + ancho // 2 + 4, piel, "frente")
    s.rect(x1 - 4, y0 + ancho // 2 + 2, x1 - 2, y0 + ancho // 2 + 4, piel, "frente")


@personaje("jabba_el_hutt", "Jabba el Hutt")
def _(s):
    hutt(s, 3, 18, 36, "#a8955e", "#c8b884")


@personaje("rotta", "Rotta")
def _(s):
    hutt(s, 14, 42, 25, "#9aa060", "#c4c48a")


@personaje("ziro_el_hutt", "Ziro el Hutt")
def _(s):
    hutt(s, 6, 22, 33, "#9a78a8", "#c4a8c8", ojos="#f0d040")
    tatuaje(s, [(10, 34), (12, 36), (27, 34), (29, 36), (19, 26), (20, 26), (14, 44), (25, 44)], "#3a5ac8")
    for i, x in enumerate(range(11, 29)):
        s.pix(x, 35 + (i % 2), "#f0a0c8", "frente")


def astromecanico(s, cuerpo, panel, domo, ojo="#ff4040"):
    """Droide astromecánico: domo, cuerpo cilíndrico y tres patas."""
    plata = "#c4c8d4"
    s.rect(11, 39, 13, SUELO - 1, cuerpo)
    s.rect(26, 39, 28, SUELO - 1, cuerpo)
    s.rect(10, SUELO - 1, 14, SUELO, plata)
    s.rect(25, SUELO - 1, 29, SUELO, plata)
    s.rect(14, 38, 25, 51, cuerpo)
    s.rect(16, 41, 18, 47, panel)
    s.rect(21, 41, 23, 47, panel)
    s.rect(15, 49, 24, 49, panel)
    s.rect(18, 52, 21, SUELO, plata)
    s.elipse(14, 31, 25, 44, domo)
    s.rect(14, 38, 25, 38, cuerpo)
    s.rect(16, 34, 18, 35, panel)
    s.rect(21, 33, 22, 33, panel)
    s.rect(19, 35, 20, 36, s.fijo("#1a1a2a"))
    s.pix(19, 35, ojo, "efectos")


@personaje("r3s6", "R3-S6")
def _(s):
    astromecanico(s, "#eef0f4", "#c9a030", "#e8cc70", ojo="#40a0ff")
    s.rect(17, 33, 22, 34, "#a88a3a")


@personaje("c3po", "C-3PO")
def _(s):
    oro = "#d8b040"
    s.cuerpo(complexion="delgado", piel=oro, torso=oro, piernas=oro, botas="#b08a30", manos=oro)
    s.rect(s.g.tor[0] + 2, s.g.cin - 1, s.g.tor[2] - 2, s.g.cin + 1, "#5a4a3a")
    s.pixs([(CENTRO - 2, s.g.cin), (CENTRO + 1, s.g.cin)], s.fijo("#d03a3a"))
    s.pix(CENTRO, s.g.cin, s.fijo("#3a6ad0"))
    s.rect(CENTRO - 1, s.g.cab[3] - 2, CENTRO, s.g.cab[3] - 1, s.fijo("#5a4a2a"))
    s.ojos_brillantes("#ffe46a")


def droide_delgado(s, color, articulacion, alto_cabeza, cabeza):
    """Droide flaco de patas largas; `cabeza` dibuja la cabeza sobre el cuello."""
    for x in (16, 22):
        s.rect(x, 38, x + 1, SUELO, color)
        s.rect(x - 1, SUELO - 1, x + 2, SUELO, articulacion)
        s.rect(x, 45, x + 1, 46, articulacion)
    s.rect(15, 24, 24, 37, color)
    s.rect(17, 27, 22, 30, articulacion)
    for x in (12, 26):
        s.rect(x, 24, x + 1, 39, color)
        s.rect(x, 31, x + 1, 31, articulacion)
        s.rect(x - 1, 40, x + 2, 41, articulacion)
    s.rect(19, 24 - alto_cabeza, 20, 23, articulacion)
    cabeza(24 - alto_cabeza)


@personaje("az3", "AZ-3")
def _(s):
    def cabeza(y):
        s.rect(16, y - 8, 23, y, "#eef0f4")
        s.rect(17, y - 9, 22, y - 9, "#eef0f4")
        s.rect(17, y - 5, 22, y - 4, s.fijo("#2a2a3a"))
        s.pixs([(18, y - 5), (21, y - 5)], "#7ad8ff", "efectos")
    droide_delgado(s, "#e6e8ee", "#8a8e9a", 6, cabeza)


@personaje("tx20", "TX-20")
def _(s):
    def cabeza(y):
        s.rect(13, y - 4, 26, y, "#7a8090")
        s.rect(15, y - 5, 24, y - 5, "#7a8090")
        s.rect(11, y - 3, 12, y - 1, "#7a8090")
        s.rect(17, y - 2, 22, y - 2, s.fijo("#2a2a36"))
        s.pixs([(16, y - 2), (23, y - 2)], "#ffd23a", "efectos")
    droide_delgado(s, "#7a8090", "#3a5a8a", 3, cabeza)


# ======================================================================
# Especies y civiles
# ======================================================================
@personaje("whorm_loathsom", "Almirante Whorm Loathsom")
def _(s):
    s.cuerpo(complexion="fornido", piel="#d49a7a", torso="#5a6070", piernas="#4a5060", botas=BOTAS)
    s.cinturon("#2a2a34", "#c9a24a")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 1, s.g.ojo_y + 1, x0, y1 + 1, "#d49a7a")
    s.rect(x1, s.g.ojo_y + 1, x1 + 1, y1 + 1, "#d49a7a")
    s.cara(alto_ojo=1)
    s.rect(CENTRO - 3, y1 - 1, CENTRO + 2, y1 - 1, s.fijo("#7a3a32"))
    s.rect(x0 + 1, y0, x1 - 1, y0 + 1, "#3a3a44")


@personaje("wat_tambor", "Wat Tambor")
def _(s):
    s.cuerpo(complexion="fornido", piel="#b8bcc4", torso="#8a2a2a", piernas="#5a5e66", botas="#3a3e46",
             brazos="#9aa0a8", manos="#7a7e88")
    s.tunica_larga("#8a2a2a", abierta="#5a1a1a")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 + 2, s.g.ojo_y - 1, x1 - 2, y1 - 1, "#5a5e66")
    for x in range(x0 + 3, x1 - 1, 2):
        s.rect(x, s.g.ojo_y + 2, x, y1 - 2, "#8a8e98")
    s.pixs([(CENTRO - 2, s.g.ojo_y), (CENTRO + 1, s.g.ojo_y)], "#7affb0", "efectos")
    s.rect(x0, s.g.ojo_y + 2, x0, s.g.tor[1] + 2, "#4a4e56", "frente")
    s.rect(x1, s.g.ojo_y + 2, x1, s.g.tor[1] + 2, "#4a4e56", "frente")


@personaje("poggle_el_menor", "Poggle el Menor")
def _(s):
    piel = "#a8643a"
    s.cuerpo(complexion="delgado", piel=piel, torso=piel, piernas=piel, botas="#7a4a2a", cabeza_ancho=8)
    s.poly([(15, 26), (5, 14), (3, 30), (14, 34)], "#ddd2b2", "fondo")
    s.poly([(24, 26), (34, 14), (36, 30), (25, 34)], "#ddd2b2", "fondo")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0, y0 - 3, x1, y0, "#8a4a2a")
    s.pixs([(x0, y0 - 5), (x0 + 2, y0 - 4), (x1 - 2, y0 - 4), (x1, y0 - 5)], "#8a4a2a")
    ojo = s.fijo("#3a2010")
    s.rect(x0, s.g.ojo_y - 1, x0 + 2, s.g.ojo_y + 1, ojo)
    s.rect(x1 - 2, s.g.ojo_y - 1, x1, s.g.ojo_y + 1, ojo)
    s.rect(CENTRO - 2, s.g.tor[1], CENTRO + 1, s.g.cin + 3, "#c9a24a")
    s.baston("d", "#6a4a2a", punta="#e8d050")


@personaje("reina_karina", "Reina Karina la Grande")
def _(s):
    s.elipse(1, 30, 38, SUELO + 6, "#d8c890")
    s.rect(1, SUELO - 1, 38, SUELO, "#d8c890")
    for y in (36, 42, 48):
        s.rect(4, y, 35, y, s.fijo("#b0a070"))
    s.rect(14, 22, 25, 34, "#8a5a32")
    s.poly([(8, 13), (31, 13), (26, 3), (13, 3)], "#5a3a22")
    s.pixs([(13, 2), (17, 1), (22, 1), (26, 2)], "#5a3a22")
    s.rect(16, 11, 23, 19, "#a06a3a")
    s.rect(17, 20, 22, 21, "#a06a3a")
    s.pixs([(15, 20), (15, 21), (24, 20), (24, 21)], "#7a4a28")
    ojo = s.fijo("#2a1408")
    s.rect(16, 13, 18, 15, ojo)
    s.rect(21, 13, 23, 15, ojo)
    for y in (24, 29):
        s.rect(10, y, 13, y + 1, "#8a5a32")
        s.rect(26, y, 29, y + 1, "#8a5a32")


@personaje("satine_kryze", "Duquesa Satine Kryze")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#3a7a8a", piernas="#3a7a8a", botas=BOTAS)
    s.tunica_larga("#4a8a9a", abierta="#c9a24a")
    s.pelo("largo", RUBIO)
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 1, y0 - 6, x1 + 1, y0 + 1, "#2a5a6a")
    s.rect(x0, y0 - 7, x1, y0 - 7, "#2a5a6a")
    s.pixs([(CENTRO - 1, y0 - 4), (CENTRO, y0 - 4), (x0 + 1, y0 - 2), (x1 - 1, y0 - 2)], s.fijo("#e8c050"))
    s.cara(boca="#c0605a")


@personaje("bo_katan_kryze", "Bo-Katan Kryze")
def _(s):
    azul = "#3c5cae"
    s.cuerpo(piel=PIEL_CLARA, torso=azul, piernas="#3a4a6a", botas="#4a4a5a", brazos="#3a4a6a", manos="#2a2a34")
    s.mochila("#5a6a8a")
    s.hombreras(azul)
    s.rect(s.g.tor[0] + 1, s.g.tor[1] + 2, s.g.tor[2] - 1, s.g.tor[1] + 5, "#5a7ac8")
    s.cinturon("#2a2a34")
    s.pelo("corto", PELIRROJO)
    s.rect(s.g.cab[0], s.g.cab[1] + 6, s.g.cab[0], s.g.cab[3] - 1, PELIRROJO)
    s.rect(s.g.cab[2], s.g.cab[1] + 6, s.g.cab[2], s.g.cab[3] - 1, PELIRROJO)
    s.cara()
    s.casco_bajo_brazo(azul, base=azul, visor="#16161c")
    s.pistola("d")


@personaje("tal_merrik", "Senador Tal Merrik")
def _(s):
    s.cuerpo(piel="#dcdcec", torso="#b8bcc8", piernas="#9a9eaa", botas=BOTAS)
    s.tunica_larga("#b8bcc8", abierta="#6a6e7a")
    s.pelo("corto", NEGRO_PELO)
    s.cara()


@personaje("lux_bonteri", "Lux Bonteri")
def _(s):
    s.cuerpo("joven", piel=PIEL_CLARA, torso="#8a3a2a", piernas="#3a3a4a", botas=BOTAS, brazos="#6a4a30")
    s.cinturon("#2a2a30")
    s.pelo("corto", CASTANO)
    s.cara()


@personaje("saw_gerrera", "Saw Gerrera")
def _(s):
    s.cuerpo(piel=PIEL_MORENA, torso="#6a6a5a", piernas="#4a4a3a", botas=BOTAS)
    s.tabardo("#5a4430", 1)
    s.cinturon("#2a2a20")
    s.pelo("corto", NEGRO_PELO)
    s.cara()
    s.rifle("d")


@personaje("steela_gerrera", "Steela Gerrera")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#8a7a6a", piernas="#5a5040", botas=BOTAS)
    s.cinturon("#3a3020")
    s.pelo("largo", RUBIO)
    s.cara(boca="#c0706a")
    s.rifle("d", largo=20)


@personaje("cham_syndulla", "Cham Syndulla")
def _(s):
    s.cuerpo(piel="#7aa84a", torso="#7a6a52", piernas="#4a3a2a", botas=BOTAS)
    s.tabardo("#5a3a26", 2)
    s.cinturon("#2a2018")
    s.lekku("#7aa84a")
    s.cara()
    s.pistola("d")


@personaje("numa", "Numa")
def _(s):
    s.cuerpo("nino", piel="#5a8ad8", torso="#c8b890", piernas="#a89870", botas="#6a5a40")
    s.lekku("#5a8ad8")
    s.cara()


@personaje("mina_bonteri", "Senadora Mina Bonteri")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#6a3a7a", piernas="#6a3a7a", botas=BOTAS)
    s.tunica_larga("#6a3a7a", abierta="#3a1a4a")
    s.pelo("chongo", "#3a2a2a")
    s.cara(boca="#b0606a")


@personaje("reina_miraj_scintel", "Reina Miraj Scintel")
def _(s):
    s.cuerpo(complexion="delgado", piel="#d8a878", torso="#9a2a2a", piernas="#9a2a2a", botas=BOTAS)
    s.tunica_larga("#9a2a2a", abierta="#c9a24a")
    s.pelo("largo", "#d89a40")
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 2, y0 + 2, x0 - 2, y1 + 2, "#d89a40")
    s.rect(x1 + 2, y0 + 2, x1 + 2, y1 + 2, "#d89a40")
    s.pixs([(x0 + 1, y0 - 2), (CENTRO - 1, y0 - 3), (CENTRO, y0 - 3), (x1 - 1, y0 - 2)], s.fijo("#f0d050"))
    s.cara(ojos="#c89a20", boca="#8a3a3a")
    m = s.g.md
    s.linea([(m[2], m[3]), (m[2] + 3, m[3] + 4), (m[2] + 1, m[3] + 8), (m[2] + 4, m[3] + 11)], "#4a2a1a", "frente")


@personaje("moralo_eval", "Moralo Eval")
def _(s):
    s.cuerpo("alto", "delgado", piel="#8a9a7a", torso="#2a2a30", piernas="#2a2a30", botas=BOTAS)
    g = s.g
    for b in (g.bi, g.bd):
        s.rect(b[0], b[3], b[2], b[3] + 6, "#2a2a30")
    s.rect(g.mi[0], g.mi[1] + 6, g.mi[2], g.mi[3] + 6, "#8a9a7a")
    s.rect(g.md[0], g.md[1] + 6, g.md[2], g.md[3] + 6, "#8a9a7a")
    s.rect(g.cab[0] + 2, g.cab[3], g.cab[2] - 2, g.cab[3] + 2, "#8a9a7a")
    s.cara(ojos="#e8c030")


@personaje("letta_turmond", "Letta Turmond")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#8a7a6a", piernas="#5a5a6a", botas=BOTAS)
    s.pelo("largo", "#8a6a3a")
    s.cara(boca="#b0706a")


@personaje("bail_organa", "Senador Bail Organa")
def _(s):
    s.cuerpo(piel=PIEL_MORENA, torso="#3a2a22", piernas="#2a2018", botas=BOTAS, brazos="#5a3a2a")
    s.tunica_larga("#5a3a2a", abierta="#3a2a22")
    s.pelo("corto", NEGRO_PELO)
    s.barba("corta", NEGRO_PELO)
    s.cara()


@personaje("mon_mothma", "Senadora Mon Mothma")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#ecece6", piernas="#ecece6", botas=BOTAS)
    s.tunica_larga("#ecece6")
    s.pelo("corto", "#b8602a")
    s.cara(boca="#c07070")


def kaminoano(s, ropa, cresta=False):
    """Kaminoano: muy alto y flaco, cuello largo y ojos grandes y oscuros."""
    piel = "#e6ecf0"
    s.poly([(14, 25), (25, 25), (27, SUELO), (12, SUELO)], ropa)
    s.pliegues(12, 25, 27, SUELO - 1, ropa)
    s.rect(11, 26, 13, 41, ropa)
    s.rect(26, 26, 28, 41, ropa)
    s.rect(11, 42, 13, 43, piel)
    s.rect(26, 42, 28, 43, piel)
    s.rect(18, 15, 21, 25, piel)
    if cresta:
        s.poly([(16, 6), (23, 6), (21, 1), (18, 1)], "#d6dde4")
    s.rect(15, 5, 24, 12, piel)
    s.rect(16, 13, 23, 14, piel)
    for x, y in ((15, 5), (24, 5)):
        s.quitar(x, y)
    ojo = s.fijo("#1a1a28")
    s.rect(16, 8, 17, 10, ojo)
    s.rect(22, 8, 23, 10, ojo)
    s.rect(19, 13, 20, 13, s.fijo("#b8c0c8"))


@personaje("nala_se", "Nala Se")
def _(s):
    kaminoano(s, "#c8d0dc")


@personaje("lama_su", "Lama Su")
def _(s):
    kaminoano(s, "#b8bcd0", cresta=True)


@personaje("thrawn", "Thrawn")
def _(s):
    s.cuerpo(piel="#4a74c8", torso="#22222a", piernas="#1a1a20", botas="#101014")
    s.cinturon("#3a3a44", "#c9a24a")
    s.pixs([(s.g.tor[0] + 1, s.g.tor[1] + 2), (s.g.tor[0] + 2, s.g.tor[1] + 2)], s.fijo("#c9a24a"))
    s.pelo("corto", "#121218")
    s.ojos_brillantes("#ff3a3a")


@personaje("trace_martez", "Trace Martez")
def _(s):
    s.cuerpo("joven", "delgado", piel=PIEL_CLARA, torso="#6a7a6a", piernas="#5a6a5a", botas=BOTAS)
    s.cinturon("#3a3a30")
    s.pelo("largo", "#d0602a")
    s.gafas("#3a3a30", "#e8a030", y=s.g.cab[1] + 1)
    s.cara()


@personaje("rafa_martez", "Rafa Martez")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#4a3a4a", piernas="#3a3a4a", botas=BOTAS,
             brazos="#6a3a2a")
    s.cinturon("#2a2a30")
    s.pelo("largo", "#8a2a2a")
    s.cara(boca="#a0505a")


def trandoshano(s, ropa, piernas, complexion="fornido"):
    piel = "#7a9a4a"
    s.cuerpo(complexion=complexion, piel=piel, torso=ropa, piernas=piernas, botas="#3a3a2a", manos=piel)
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 1, s.g.ojo_y + 1, x1 + 1, y1, piel)
    s.rect(x0, s.g.ojo_y - 1, x1, s.g.ojo_y - 1, "#5a7a34")
    s.cara(ojos="#e07a20")
    s.rect(x0, y1 - 1, x1, y1 - 1, s.fijo("#3a4a20"))


@personaje("garnac", "Garnac")
def _(s):
    trandoshano(s, "#6a5a4a", "#4a4036")
    s.hombreras("#8a8a96")
    s.cinturon("#2a2a20")
    s.rifle("d")


@personaje("gha_nachkt", "Gha Nachkt")
def _(s):
    trandoshano(s, "#7a6248", "#5a4a38", complexion="normal")
    s.faldon("#7a6248", 6)
    s.cinturon("#3a2a1a")
    s.rect(s.g.tor[2] - 1, s.g.cin + 1, s.g.tor[2] + 2, s.g.cin + 5, "#9a7a52", "frente")


@personaje("chewbacca", "Chewbacca")
def _(s):
    pelaje, oscuro = "#7a5233", "#5a3a22"
    s.cuerpo("alto", "fornido", piel=pelaje, torso=pelaje, piernas=pelaje, botas=oscuro, manos=oscuro)
    x0, y0, x1, y1 = s.g.cab
    s.rect(x0 - 1, y0, x1 + 1, y1 + 2, pelaje)
    s.rect(x0 + 2, s.g.ojo_y + 1, x1 - 2, y1, "#a07a50")
    s.cara()
    s.rect(CENTRO - 1, s.g.ojo_y + 2, CENTRO, s.g.ojo_y + 2, s.fijo("#2a1a10"))
    for i in range(s.g.tor[2] - s.g.tor[0] + 1):
        s.pix(s.g.tor[0] + i, s.g.tor[1] + i, "#b8bcc8", "frente")
        s.pix(s.g.tor[0] + i + 1, s.g.tor[1] + i, "#7a7e8a", "frente")
    for x, y in ((x0, y0 + 2), (x1, y0 + 5), (s.g.tor[0] + 2, s.g.cin + 3), (s.g.pd[0] + 1, s.g.pd[1] + 6)):
        s.pix(x, y, oscuro)


@personaje("el_padre", "El Padre (Mortis)")
def _(s):
    s.cuerpo(piel=PIEL_CLARA, torso="#d8d0c0", piernas="#d8d0c0", botas=BOTAS)
    s.tunica_larga("#d8d0c0", abierta="#8a6a4a")
    s.pelo("largo", CANOSO)
    s.barba("larga", CANOSO)
    s.cara()


@personaje("el_hijo", "El Hijo (Mortis)")
def _(s):
    s.cuerpo(piel="#a8a0a8", torso="#2a1a1e", piernas="#2a1a1e", botas=BOTAS)
    s.tunica_larga("#2a1a1e", abierta="#7a1a1a")
    s.hombreras("#4a2a2e", 3)
    for b in (s.g.bi, s.g.bd):
        s.rect(b[0] + 1, b[1] - 2, b[0] + 1, b[1] - 1, "#4a2a2e")
    s.pelo("corto", "#1a1a1a")
    s.ojos_brillantes("#ff3030")


@personaje("la_hija", "La Hija (Mortis)")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_PALIDA, torso="#e8f0e0", piernas="#e8f0e0", botas=BOTAS)
    s.tunica_larga("#e8f0e0", abierta="#7ab87a")
    s.pelo("largo", "#8a4a2a")
    s.ojos_brillantes("#5aff7a")


@personaje("rako_hardeen", "Rako Hardeen")
def _(s):
    s.cuerpo(piel=PIEL_MEDIA, torso="#5a4a3a", piernas="#3a3a30", botas=BOTAS, brazos="#4a3a2e")
    s.cinturon("#2a2018")
    s.pelo("corto", CASTANO)
    s.barba("corta", "#7a5a40")
    s.cara()
    s.rifle("d", largo=20)


def corona(s, color="#e8c050"):
    x0, y0, x1, _ = s.g.cab
    s.rect(x0 + 1, y0 - 1, x1 - 1, y0, s.fijo(color))
    s.pixs([(x0 + 1, y0 - 2), (CENTRO - 1, y0 - 3), (CENTRO, y0 - 3), (x1 - 1, y0 - 2)], color)


@personaje("rey_rash", "Rey Sanjay Rash")
def _(s):
    s.cuerpo(complexion="delgado", piel=PIEL_CLARA, torso="#3a2a5a", piernas="#3a2a5a", botas=BOTAS)
    s.tunica_larga("#3a2a5a", abierta="#1e1430")
    s.pelo("corto", NEGRO_PELO)
    corona(s)
    s.cara()


@personaje("rey_dendup", "Rey Ramsis Dendup")
def _(s):
    s.cuerpo(piel=PIEL_MORENA, torso="#5a3a7a", piernas="#5a3a7a", botas=BOTAS)
    s.tunica_larga("#5a3a7a", abierta="#c9a24a")
    s.pelo("receso", CANOSO)
    s.barba("larga", CANOSO)
    corona(s)
    s.cara()


# ===== fin del catálogo =====


def dibujar(clave):
    s = Sprite()
    PERSONAJES[clave][1](s)
    return s.terminar()


def galeria(imagenes, columnas=12, escala=4):
    """Hoja de revisión: cada sprite con su nombre debajo."""
    try:
        fuente = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        fuente = ImageFont.load_default()
    celda_w, celda_h = ANCHO * escala, ALTO * escala + 16
    filas = (len(imagenes) + columnas - 1) // columnas
    hoja = Image.new("RGBA", (columnas * celda_w, filas * celda_h), "#3b3550")
    d = ImageDraw.Draw(hoja)
    for i, (clave, img) in enumerate(imagenes):
        x, y = (i % columnas) * celda_w, (i // columnas) * celda_h
        hoja.alpha_composite(img.resize((ANCHO * escala, ALTO * escala), Image.NEAREST), (x, y))
        nombre = PERSONAJES[clave][0]
        ancho = d.textlength(nombre, font=fuente)
        d.text((x + (celda_w - ancho) / 2, y + ALTO * escala + 1), nombre, fill="#f0ecf8", font=fuente)
    return hoja


def main(claves):
    (CARPETA / "sprites").mkdir(exist_ok=True)
    (CARPETA / "sprites_1x").mkdir(exist_ok=True)
    hechas = []
    for clave in claves:
        img = dibujar(clave)
        img.save(CARPETA / "sprites_1x" / f"{clave}.png")
        img.resize((ANCHO * ESCALA, ALTO * ESCALA), Image.NEAREST).save(CARPETA / "sprites" / f"{clave}.png")
        hechas.append((clave, img))
    galeria(hechas).save(CARPETA / "galeria.png")
    indice = {c: {"nombre": PERSONAJES[c][0], "sprite": f"sprites/{c}.png", "sprite_1x": f"sprites_1x/{c}.png"}
              for c in PERSONAJES}
    (CARPETA / "personajes.json").write_text(json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(hechas)} sprites generados en {CARPETA}")


if __name__ == "__main__":
    pedidas = sys.argv[1:]
    claves = [c for c in PERSONAJES if not pedidas or any(p in c for p in pedidas)]
    main(claves)
