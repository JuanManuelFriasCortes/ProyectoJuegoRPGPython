"""Pantalla completa de una ficha: escenario, personajes y cuadro de texto con las opciones.

Uso:  python cuadro_de_texto.py D252     (cualquier ficha de D001 a D312)

El texto sale de Historia.md (título, quién juega, contexto y opciones) y el
reparto (quién aparece, dónde y a qué escala) de assets/escenas/escenas.json.
El cuadro ocupa el tercio de abajo; los personajes de adelante quedan con la
cabeza y el torso por encima, como en una novela visual.
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ASSETS / "escenas"))
from armar_escenas import componer_escena  # noqa: E402

RAIZ = ASSETS.parent
SALIDA = Path(__file__).resolve().parent
UI = 2                    # la interfaz se dibuja a 640x360 y se escala x2 (píxeles marcados)
ANCHO_UI, ALTO_UI = 1280 // UI, 720 // UI

# zona reservada para el cuadro, en coordenadas de 640x360 (en 1280x720: de y=472 a y=704)
CUADRO = (10, 236, 630, 352)

COLORES = {
    "fondo": (10, 14, 34, 246),
    "borde": (122, 200, 255, 255),
    "borde_oscuro": (20, 40, 80, 255),
    "texto": (236, 240, 250, 255),
    "tenue": (150, 170, 210, 255),
    "nombre": (255, 214, 102, 255),
    "elegida": (255, 214, 102, 255),
}


def leer_ficha(ficha):
    """Saca de Historia.md el título, quién juega, el contexto y las opciones visibles."""
    texto = (RAIZ / "Historia.md").read_text(encoding="utf-8")
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)   # la ficha de ejemplo de la cabecera no cuenta
    m = re.search(rf"^#### {ficha} · (.+?)\n(.*?)(?=^#### |^## |^# |\Z)", texto, re.S | re.M)
    if not m:
        raise SystemExit(f"No encontré la ficha {ficha} en Historia.md")
    titulo, cuerpo = m.group(1).strip(), m.group(2)
    juega = re.search(r"\*\*Juega:\*\* ([^·\n]+)", cuerpo).group(1).strip()
    contexto, opciones = [], []
    for linea in cuerpo.splitlines()[1:]:
        if linea.startswith("- **"):
            if "*(si " in linea or "*(requiere" in linea:
                continue      # opción condicionada: solo aparece si se cumple la condición
            letra, resto = re.match(r"- \*\*([A-F])\)\*\* (.+)", linea).groups()
            resto = resto.split("→")[0].replace("★", "").strip()
            opciones.append(f"{letra}) {resto}")
        elif linea.strip():
            contexto.append(linea.strip())
    contexto = " ".join(contexto)
    contexto = re.sub(r"\*\((Si|si) [^)]*\)\*", "", contexto)       # notas de variante para el guionista
    contexto = re.sub(r"[*_]", "", contexto).strip()
    return titulo, juega, contexto, opciones


def envolver(d, texto, fuente, ancho):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if d.textlength(prueba, font=fuente) <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def marco(d, caja, relleno):
    x0, y0, x1, y1 = caja
    d.rectangle(caja, fill=relleno)
    d.rectangle([x0, y0, x1, y1], outline=COLORES["borde_oscuro"])
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], outline=COLORES["borde"])
    for cx, cy in ((x0 + 1, y0 + 1), (x1 - 1, y0 + 1), (x0 + 1, y1 - 1), (x1 - 1, y1 - 1)):
        d.point((cx, cy), fill=COLORES["borde_oscuro"])


def interfaz(ficha, titulo, juega, contexto, opciones, elegida=0):
    capa = Image.new("RGBA", (ANCHO_UI, ALTO_UI), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.fontmode = "1"      # sin suavizado: letras con píxeles duros, como el resto del juego
    normal = ImageFont.truetype("arial.ttf", 11)
    negrita = ImageFont.truetype("arialbd.ttf", 11)
    chica = ImageFont.truetype("arial.ttf", 9)

    x0, y0, x1, y1 = CUADRO
    marco(d, CUADRO, COLORES["fondo"])
    ancho_nombre = int(d.textlength(juega.upper(), font=negrita)) + 16
    marco(d, (x0 + 6, y0 - 15, x0 + 6 + ancho_nombre, y0 + 1), COLORES["fondo"])
    d.text((x0 + 14, y0 - 12), juega.upper(), font=negrita, fill=COLORES["nombre"])
    d.text((x1 - 8 - d.textlength(f"{ficha} · {titulo}", font=chica), y0 - 11), f"{ficha} · {titulo}",
           font=chica, fill=COLORES["tenue"])

    y = y0 + 8
    for linea in envolver(d, contexto, normal, x1 - x0 - 24)[:3]:
        d.text((x0 + 12, y), linea, font=normal, fill=COLORES["texto"])
        y += 14
    y += 4
    d.line([(x0 + 12, y - 2), (x1 - 12, y - 2)], fill=COLORES["borde_oscuro"])
    for i, opcion in enumerate(opciones[:4]):
        color = COLORES["elegida"] if i == elegida else COLORES["texto"]
        if i == elegida:
            d.polygon([(x0 + 12, y + 3), (x0 + 12, y + 9), (x0 + 15, y + 6)], fill=color)
        d.text((x0 + 20, y), opcion, font=negrita if i == elegida else normal, fill=color)
        y += 14
    return capa.resize((ANCHO_UI * UI, ALTO_UI * UI), Image.NEAREST)


def guardar(img, destino, intentos=6, **opciones):
    """Guarda sin chocar con OneDrive: escribe a un temporal y lo reemplaza; si el archivo
    está bloqueado un instante (OSError 22 o PermissionError), espera y reintenta."""
    import os
    import time
    temporal = destino.with_name(destino.stem + ".tmp" + destino.suffix)
    img.save(temporal, **opciones)
    for intento in range(intentos):
        try:
            os.replace(temporal, destino)
            return
        except OSError:
            time.sleep(0.5 * (intento + 1))
    raise OSError(f"No se pudo reemplazar {destino}: sigue bloqueado")


def main(ficha="D252", animado=False):
    escenas = json.loads((ASSETS / "escenas" / "escenas.json").read_text(encoding="utf-8"))
    escena = escenas[ficha]
    titulo, juega, contexto, opciones = leer_ficha(ficha)
    ui = interfaz(ficha, titulo, juega, contexto, opciones)
    if not animado:
        lienzo = componer_escena(escena)
        lienzo.alpha_composite(ui)
        destino = SALIDA / f"{ficha}_con_cuadro_de_texto.png"
        guardar(lienzo, destino)
        print("Guardado:", destino)
        return
    # pantalla animada: cada cuadro del fondo animado + personajes + cuadro de texto
    tira = Image.open(ASSETS / "escenarios" / "animados_1x" / f"{escena['fondo']}.png").convert("RGB")
    ancho, alto = 320, 180
    cuadros = []
    for t in range(tira.width // ancho):
        fondo = tira.crop((t * ancho, 0, (t + 1) * ancho, alto)).resize((1280, 720), Image.NEAREST)
        lienzo = componer_escena(escena, fondo)
        lienzo.alpha_composite(ui)
        cuadros.append(lienzo.convert("RGB"))
    muestra = Image.new("RGB", (1280, 720 * 2))
    muestra.paste(cuadros[0], (0, 0))
    muestra.paste(cuadros[len(cuadros) // 2], (0, 720))
    paleta = muestra.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    gif = [c.quantize(palette=paleta, dither=Image.Dither.NONE) for c in cuadros]
    destino = SALIDA / f"{ficha}_animado.gif"
    guardar(gif[0], destino, save_all=True, append_images=gif[1:], duration=100, loop=0, disposal=1)
    print("Guardado:", destino)


if __name__ == "__main__":
    fichas = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(*(fichas[:1] or ["D252"]), animado="--animado" in sys.argv)
