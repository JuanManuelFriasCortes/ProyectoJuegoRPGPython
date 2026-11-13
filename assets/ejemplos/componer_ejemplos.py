"""Arma imágenes de ejemplo: personajes acomodados sobre los escenarios del juego.

Uso:  python componer_ejemplos.py

Cada escena se arma sobre el fondo de 1280x720. Los personajes de adelante van
a x8 y los de atrás más chicos (x5 o x6) y más arriba, para dar profundidad.
Cada uno lleva una sombra pixelada en los pies.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent
SPRITES = ASSETS / "personajes" / "sprites_1x"
FONDOS = ASSETS / "escenarios" / "fondos"
SALIDA = Path(__file__).resolve().parent
ESCALA_FONDO = 4          # el fondo de 320x180 está escalado x4

# cada escena: (archivo, fondo, [(personaje, x del centro, y de los pies, escala, girado)])
ESCENAS = [
    ("D002_christophsis", "christophsis", [
        ("capitan_rex", 150, 640, 6, False),
        ("obi_wan_kenobi", 1080, 640, 6, False),
        ("anakin_skywalker", 380, 712, 8, False),
        ("ahsoka_tano", 760, 712, 8, False),
    ]),
    ("D022_trono_de_jabba", "palacio_hutt", [
        ("jabba_el_hutt", 640, 532, 8, False),
        ("anakin_skywalker", 250, 712, 8, False),
        ("rotta", 420, 712, 8, False),
        ("ahsoka_tano", 1030, 712, 8, False),
    ]),
    ("D197_escaleras_del_templo", "templo_exterior", [
        ("ahsoka_tano", 640, 650, 6, False),
        ("anakin_skywalker", 250, 712, 8, False),
    ]),
    ("D252_matalo", "pasillo_separatista", [
        ("canciller_palpatine", 1010, 560, 5, False),
        ("obi_wan_kenobi", 240, 700, 8, True),
        ("conde_dooku", 900, 712, 8, False),
        ("anakin_skywalker", 600, 712, 8, False),
    ]),
    ("D261_sin_rango_de_maestro", "consejo_jedi", [
        ("ki_adi_mundi", 144, 532, 5, False),
        ("plo_koon", 252, 512, 5, False),
        ("yoda", 428, 500, 5, False),
        ("mace_windu", 852, 500, 5, False),
        ("obi_wan_kenobi", 1026, 512, 5, False),
        ("shaak_ti", 1134, 532, 5, False),
        ("anakin_skywalker", 640, 712, 8, False),
    ]),
    ("D277_duelo_en_la_oficina", "oficina_canciller", [
        ("darth_sidious", 1010, 690, 8, False),
        ("mace_windu", 760, 712, 8, False),
        ("anakin_skywalker", 260, 712, 8, False),
    ]),
    ("D292_mustafar", "mustafar", [
        ("padme_amidala", 660, 650, 6, False),
        ("anakin_skywalker", 330, 712, 8, False),
        ("obi_wan_kenobi", 980, 712, 8, False),
    ]),
]


def sombra(lienzo, x, y, ancho):
    """Elipse oscura y pixelada (a la resolución del fondo) bajo los pies."""
    capa = Image.new("RGBA", (lienzo.width // ESCALA_FONDO, lienzo.height // ESCALA_FONDO), (0, 0, 0, 0))
    cx, cy, rx = x // ESCALA_FONDO, y // ESCALA_FONDO, max(3, ancho // (2 * ESCALA_FONDO))
    ImageDraw.Draw(capa).ellipse([cx - rx, cy - 2, cx + rx, cy + 1], fill=(16, 8, 24, 110))
    lienzo.alpha_composite(capa.resize(lienzo.size, Image.NEAREST))


def componer(fondo, personajes):
    lienzo = Image.open(FONDOS / f"{fondo}.png").convert("RGBA")
    for clave, x, y_pies, escala, girado in sorted(personajes, key=lambda p: p[2]):
        sprite = Image.open(SPRITES / f"{clave}.png").convert("RGBA")
        sprite = sprite.resize((sprite.width * escala, sprite.height * escala), Image.NEAREST)
        if girado:   # tirado en el suelo (Obi-Wan inconsciente)
            sprite = sprite.rotate(90, expand=True)
            caja = sprite.getbbox()
            sombra(lienzo, x, y_pies, caja[2] - caja[0])
            lienzo.alpha_composite(sprite, (x - sprite.width // 2, y_pies - caja[3]))
            continue
        sombra(lienzo, x, y_pies, 13 * escala)
        lienzo.alpha_composite(sprite, (x - sprite.width // 2, y_pies - sprite.height))
    return lienzo


def main():
    miniaturas = []
    for archivo, fondo, personajes in ESCENAS:
        img = componer(fondo, personajes)
        img.save(SALIDA / f"{archivo}.png")
        miniaturas.append(img.resize((640, 360), Image.NEAREST))
    hoja = Image.new("RGBA", (1280, 360 * ((len(miniaturas) + 1) // 2)), "#24202e")
    for i, m in enumerate(miniaturas):
        hoja.alpha_composite(m, ((i % 2) * 640, (i // 2) * 360))
    hoja.save(SALIDA / "todos_los_ejemplos.png")
    print(f"{len(miniaturas)} ejemplos en {SALIDA}")


if __name__ == "__main__":
    main()
