"""Escena completa en video a 60 fps: fondo animado, personajes, diálogo que se escribe solo,
la decisión, la reacción a la opción elegida y la música que le toca a la ficha.

Uso:
    python escena_completa.py                   # los cuatro ejemplos (en paralelo)
    python escena_completa.py D252 --opcion B   # una ficha, con la opción que se quiera (por defecto, la del canon)

Los diálogos salen de Dialogos.md (en la raíz); el reparto, de escenas.json; la música, de musica.json;
el fondo, de escenarios/animados_60 (si no existe, de animados_1x a 10 fps); la voz de cada
personaje mientras se escribe y los sonidos del cursor, de sonidos/sonidos.json.
Salida en escenas_completas/: D###.mp4 y D###_guion_grafico.png (un cuadro por línea).
"""
import array
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import wave
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from cuadro_de_texto import (ALTO_UI, ANCHO_UI, ASSETS, COLORES, CUADRO, RAIZ, envolver, guardar,
                             leer_ficha, marco)
from armar_escenas import componer_escena  # noqa: E402  (cuadro_de_texto ya agregó su carpeta)

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "escenas_completas"
EJEMPLOS = {"D002": "A", "D022": "A", "D252": "B", "D267": "A"}   # D252 toma la rama, no el canon

FPS = 60
LETRAS_POR_SEGUNDO = 40  # velocidad de la máquina de escribir
LECTURA = 20             # letras por segundo para calcular cuánto se queda la línea completa
CAMBIO = 0.2             # segundos que tarda en iluminarse quien habla y oscurecerse el resto
ENTRADA = 0.4            # segundos del fundido cuando un personaje entra o sale
DESLIZ = 0.15            # segundos que tarda el cursor en pasar de una opción a otra
ANCHO, ALTO = 1280, 720
TOPE_UI = 440            # la interfaz solo ocupa de aquí para abajo: se compone solo esa franja
MUESTREO = 44100
SONIDOS_LUFS = -29.0     # sonoridad de las voces y clics: bastante debajo de la música (-21)

ESCENAS = json.loads((ASSETS / "escenas" / "escenas.json").read_text(encoding="utf-8"))
PERSONAJES = json.loads((ASSETS / "personajes" / "personajes.json").read_text(encoding="utf-8"))
MUSICA = json.loads((ASSETS / "musica" / "musica.json").read_text(encoding="utf-8"))
SONIDOS = json.loads((ASSETS / "sonidos" / "sonidos.json").read_text(encoding="utf-8"))

FUENTES = {
    "normal": ImageFont.truetype("arial.ttf", 15),
    "cursiva": ImageFont.truetype("ariali.ttf", 15),
    "negrita": ImageFont.truetype("arialbd.ttf", 11),
    "opcion": ImageFont.truetype("arial.ttf", 14),
    "opcion_b": ImageFont.truetype("arialbd.ttf", 14),
    "chica": ImageFont.truetype("arial.ttf", 9),
    "titulo": ImageFont.truetype("arialbd.ttf", 22),
}
NARRADOR = (196, 206, 232, 255)


# ---------- lectura de datos ----------

def lineas(texto):
    """Pasos de la escena en orden: ("dice", etiqueta, texto) por cada `Nombre: lo que dice`
    y ("entra" | "sale", nombre) por cada `[entra Nombre]` o `[sale Nombre]`."""
    pasos = []
    for m in re.finditer(r"^(?:\[(entra|sale) ([^\]]+)\]|([^:\n>#\[-][^:\n]{0,29}): (.+))$", texto, re.M):
        pasos.append((m.group(1), m.group(2).strip()) if m.group(1)
                     else ("dice", m.group(3).strip(), m.group(4).strip()))
    return pasos


def leer_dialogos():
    """{ficha: (pasos antes de decidir, {letra: pasos de la reacción})}"""
    texto = (RAIZ / "Dialogos.md").read_text(encoding="utf-8")
    dialogos = {}
    for bloque in re.split(r"^## ", texto, flags=re.M)[1:]:
        partes = re.split(r"^### ([A-F])\b.*$", bloque, flags=re.M)
        reacciones = {letra: lineas(cuerpo) for letra, cuerpo in zip(partes[1::2], partes[2::2])}
        dialogos[bloque[:4]] = (lineas(partes[0]), reacciones)
    return dialogos


def datos_de_historia(ficha):
    """Acto y capítulo de la ficha, letra de la opción canónica y destino de cada opción."""
    texto = re.sub(r"```.*?```", "", (RAIZ / "Historia.md").read_text(encoding="utf-8"), flags=re.S)
    inicio = re.search(rf"^#### {ficha} · ", texto, re.M).start()
    acto = re.findall(r"^# (ACTO [IVX]+)", texto[:inicio], re.M)[-1]
    capitulo = re.findall(r"^## (Capítulo .+)$", texto[:inicio], re.M)[-1]
    cuerpo = re.search(r"^#### .+?(?=^#### |^## |^# |\Z)", texto[inicio:], re.S | re.M).group(0)
    canon, destinos = None, {}
    for letra, resto in re.findall(r"^- \*\*([A-F])\)\*\* (.+)$", cuerpo, re.M):
        if "★" in resto:
            canon = letra
        destino = re.search(r"→ (D\d{3}|FINAL \d|FP\d)", resto)
        destinos[letra] = destino.group(1) if destino else ""
    titulos = dict(re.findall(r"^#### (D\d{3}) · (.+)$", texto, re.M))
    return f"{acto} · {capitulo}", canon, destinos, titulos


def quien_habla(etiqueta, escena):
    """Clave del personaje en pantalla que dice la línea; None si narra o si habla alguien fuera de cuadro."""
    if etiqueta.lower() == "narra":
        return None
    for p in escena["personajes"]:
        if etiqueta.lower() in PERSONAJES[p["clave"]]["nombre"].lower():
            return p["clave"]
    return None


def voz_de(etiqueta, escena):
    """Voz (familia de chirridos) de quien dice la línea; si no está en pantalla, se busca entre todos."""
    if etiqueta.lower() == "narra":
        return SONIDOS["narrador"]
    clave = quien_habla(etiqueta, escena) or next(
        (c for c, p in PERSONAJES.items() if etiqueta.lower() in p["nombre"].lower()), None)
    return SONIDOS["personajes"].get(clave, SONIDOS["por_defecto"])


def pista_de(ficha):
    clave = MUSICA["fichas"][ficha]
    pista = MUSICA["pistas"][clave]
    archivo = pista["archivo"] or MUSICA["pistas"][pista["respaldo"]]["archivo"]
    ruta = ASSETS / "musica" / archivo if archivo else None
    return ruta if ruta and ruta.exists() else None


def fondos_de(clave):
    """Cuadros del fondo animado a 320x180, uno por cuadro de video (a 60 fps)."""
    rejilla = ASSETS / "escenarios" / "animados_60" / f"{clave}.png"
    if rejilla.exists():
        hoja = Image.open(rejilla).convert("RGBA")
        columnas = hoja.width // 320
        return [hoja.crop(((t % columnas) * 320, (t // columnas) * 180, (t % columnas + 1) * 320, (t // columnas + 1) * 180))
                for t in range(columnas * (hoja.height // 180))]
    tira = Image.open(ASSETS / "escenarios" / "animados_1x" / f"{clave}.png").convert("RGBA")
    repetir = FPS // 10                            # sin la versión a 60 fps: cada cuadro de 100 ms se repite
    return [tira.crop((t * 320, 0, (t + 1) * 320, 180)) for t in range(tira.width // 320) for _ in range(repetir)]


# ---------- dibujo de la interfaz (a 640x360, escalada x2 como el resto) ----------

def lienzo_ui():
    capa = Image.new("RGBA", (ANCHO_UI, ALTO_UI), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.fontmode = "1"
    return capa, d


def franja(capa):
    """La interfaz escalada a 1280x720, recortada a la franja de abajo donde está el cuadro."""
    return capa.resize((ANCHO, ALTO), Image.NEAREST).crop((0, TOPE_UI, ANCHO, ALTO))


def pestana(d, texto):
    x0, y0 = CUADRO[0], CUADRO[1]
    ancho = int(d.textlength(texto, font=FUENTES["negrita"])) + 16
    marco(d, (x0 + 6, y0 - 15, x0 + 6 + ancho, y0 + 1), COLORES["fondo"])
    d.text((x0 + 14, y0 - 12), texto, font=FUENTES["negrita"], fill=COLORES["nombre"])


def cuadro_dialogo(etiqueta, texto, visibles, salto):
    """`salto` es cuánto sube el ▼ (en píxeles de 640x360); None mientras se escribe la línea."""
    capa, d = lienzo_ui()
    x0, y0, x1, y1 = CUADRO
    marco(d, CUADRO, COLORES["fondo"])
    narra = etiqueta.lower() == "narra"
    if not narra:
        pestana(d, etiqueta.upper())
    fuente = FUENTES["cursiva"] if narra else FUENTES["normal"]
    restantes, y = visibles, y0 + 13
    for renglon in envolver(d, texto, fuente, x1 - x0 - 30):     # se envuelve el texto completo: las
        d.text((x0 + 15, y), renglon[:max(restantes, 0)], font=fuente,   # palabras no brincan de renglón
               fill=NARRADOR if narra else COLORES["texto"])
        restantes -= len(renglon) + 1
        y += 20
    if salto is not None:
        b = y1 - 12 - salto
        d.polygon([(x1 - 18, b), (x1 - 10, b), (x1 - 14, b + 5)], fill=COLORES["borde"])
    return franja(capa)


def cuadro_decision(juega, opciones, cursor_y, elegida, relleno):
    """`cursor_y` es la altura de la flecha (se desliza entre opciones); `relleno`, de 0 a 1,
    cuánto se ha llenado la barra de la opción confirmada."""
    capa, d = lienzo_ui()
    x0, y0, x1, _ = CUADRO
    marco(d, CUADRO, COLORES["fondo"])
    pestana(d, juega.upper())
    d.text((x0 + 15, y0 + 11), "¿Qué haces?", font=FUENTES["cursiva"], fill=NARRADOR)
    primera = y0 + 36
    marcada = round((cursor_y - primera) / 21)
    for i, opcion in enumerate(opciones):
        y = primera + i * 21
        activa = i == marcada
        d.text((x0 + 24, y), opcion, font=FUENTES["opcion_b" if activa else "opcion"],
               fill=COLORES["elegida"] if activa else COLORES["texto"])
    if relleno > 0:                                # la barra crece de izquierda a derecha
        y = primera + elegida * 21
        caja = (x0 + 10, y - 2, x0 + 10 + int((x1 - x0 - 20) * relleno), y + 16)
        d.rectangle(caja, fill=COLORES["elegida"])
        oscura, do = lienzo_ui()
        do.text((x0 + 24, y), opciones[elegida], font=FUENTES["opcion_b"], fill=COLORES["fondo"])
        recorte = oscura.crop((caja[0], caja[1], caja[2] + 1, caja[3] + 1))
        capa.paste(recorte, caja[:2], recorte)
    else:
        d.polygon([(x0 + 14, cursor_y + 4), (x0 + 14, cursor_y + 12), (x0 + 18, cursor_y + 8)],
                  fill=COLORES["elegida"])
    return franja(capa)


def tarjeta(arriba, centro, abajo):
    """Pantalla negra con texto centrado: el título al empezar y el "continúa en" al terminar."""
    capa, d = lienzo_ui()
    d.rectangle([0, 0, ANCHO_UI, ALTO_UI], fill=(4, 6, 14, 255))
    for texto, fuente, color, y in ((arriba, FUENTES["chica"], COLORES["tenue"], 148),
                                    (centro, FUENTES["titulo"], COLORES["texto"], 164),
                                    (abajo, FUENTES["negrita"], COLORES["nombre"], 198)):
        d.text(((ANCHO_UI - d.textlength(texto, font=fuente)) / 2, y), texto, font=fuente, fill=color)
    return capa.resize((ANCHO, ALTO), Image.NEAREST).convert("RGB")


# ---------- línea de tiempo y video ----------

def segundos(s):
    return max(1, round(s * FPS))


def suave(x):
    """Curva de 0 a 1 que arranca y frena despacio (smoothstep): los cambios no se ven de golpe."""
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def linea_de_tiempo(escena, dialogo_antes, reaccion, n_opciones, elegida):
    """Lista de cuadros (personajes, interfaz).
    `personajes` es (estado, estado_anterior, mezcla): cada estado es (presentes, apagados) y,
    mientras cambia quién habla o alguien entra, se mezcla el anterior con el nuevo.
    `interfaz` es ("dialogo", etiqueta, texto, visibles, salto) o ("decision", cursor_y, relleno).
    Además devuelve en qué cuadros se toma la foto para el guion gráfico y los sonidos
    [(cuadro, archivo)]: la voz de quien habla cada CADA_LETRAS letras, el clic del cursor
    y el de confirmar."""
    cuadros, fotos, sonidos = [], [], []
    reparto = {p["clave"] for p in escena["personajes"]}
    rnd = random.Random(escena["titulo"])
    ultimo = {"archivo": None}

    def sonar(archivo_o_voz):
        if archivo_o_voz in SONIDOS["voces"]:      # una voz: variante al azar, sin repetir la anterior
            opciones = [a for a in SONIDOS["voces"][archivo_o_voz] if a != ultimo["archivo"]]
            archivo_o_voz = rnd.choice(opciones)
            ultimo["archivo"] = archivo_o_voz
        sonidos.append((len(cuadros), archivo_o_voz))
    entran = {quien_habla(paso[1], escena) for paso in dialogo_antes + reaccion if paso[0] == "entra"}
    estado = {"presentes": frozenset(reparto - entran), "visto": None}

    def transicion(nuevo, n):
        """Qué capa de personajes toca en el cuadro n desde que empezó el estado `nuevo`."""
        visto = estado["visto"]
        if visto is None or visto == nuevo:
            return (nuevo, None, 1.0)
        duracion = segundos(ENTRADA if visto[0] != nuevo[0] else CAMBIO)
        return (nuevo, visto, suave((n + 1) / duracion)) if n < duracion else (nuevo, None, 1.0)

    def decir(etiqueta, texto):
        habla = quien_habla(etiqueta, escena)
        presentes = estado["presentes"]
        nuevo = (presentes, frozenset(presentes - {habla}) if habla else frozenset())
        escribir = segundos(len(texto) / LETRAS_POR_SEGUNDO)
        quieto = segundos(max(1.2, len(texto) / LECTURA))
        voz, letras, previas = voz_de(etiqueta, escena), 0, 0
        for n in range(escribir + quieto):
            visibles = min(len(texto), math.ceil((n + 1) * LETRAS_POR_SEGUNDO / FPS))
            for letra in texto[previas:visibles]:
                if letra.isalnum():
                    letras += 1
                    if letras % SONIDOS["cada_letras"] == 1:
                        sonar(voz)
            previas = visibles
            salto = None if n < escribir else round(1.5 + 1.5 * math.sin((n - escribir) / FPS * 2 * math.pi * 1.4))
            cuadros.append((transicion(nuevo, n), ("dialogo", etiqueta, texto, visibles, salto)))
            if n == escribir - 1:
                fotos.append(len(cuadros) - 1)
        estado["visto"] = nuevo

    def seguir(pasos):
        for paso in pasos:
            if paso[0] == "dice":
                decir(paso[1], paso[2])
                continue
            cambio = {quien_habla(paso[1], escena)} - {None}
            estado["presentes"] = frozenset(estado["presentes"] | cambio if paso[0] == "entra"
                                            else estado["presentes"] - cambio)

    seguir(dialogo_antes)
    primera = CUADRO[1] + 36
    nuevo, n = (estado["presentes"], frozenset()), 0

    def decidir(cursor_y, relleno=0.0):
        nonlocal n
        cuadros.append((transicion(nuevo, n), ("decision", round(cursor_y), relleno)))
        n += 1

    sonar(SONIDOS["ui"]["cursor"])                 # aparecen las opciones
    for _ in range(segundos(1.6)):
        decidir(primera)
    for paso in range(1, elegida + 1):             # el cursor baja opción por opción
        sonar(SONIDOS["ui"]["cursor"])
        for k in range(segundos(DESLIZ)):
            decidir(primera + 21 * (paso - 1 + suave((k + 1) / segundos(DESLIZ))))
        for _ in range(segundos(0.45)):
            decidir(primera + 21 * paso)
    for _ in range(segundos(0.4)):
        decidir(primera + 21 * elegida)
    sonar(SONIDOS["ui"]["confirmar"])
    for k in range(segundos(0.25)):                # se confirma: la barra se llena
        decidir(primera + 21 * elegida, suave((k + 1) / segundos(0.25)))
    for _ in range(segundos(0.7)):
        decidir(primera + 21 * elegida, 1.0)
    fotos.append(len(cuadros) - 1)
    estado["visto"] = nuevo
    seguir(reaccion)
    return cuadros, fotos, sonidos


def pista_de_sonidos(sonidos, desfase, total, destino):
    """WAV con todos los chirridos y clics en su momento (`desfase` = cuadros de la tarjeta inicial)."""
    muestras = {}
    pista = array.array("f", [0.0]) * round(total / FPS * MUESTREO)
    for cuadro_n, archivo in sonidos:
        if archivo not in muestras:
            with wave.open(str(ASSETS / "sonidos" / archivo)) as w:
                muestras[archivo] = array.array("h", w.readframes(w.getnframes()))
        inicio = round((desfase + cuadro_n) / FPS * MUESTREO)
        for i, m in enumerate(muestras[archivo][:len(pista) - inicio]):
            pista[inicio + i] += m / 32768
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(MUESTREO)
        w.writeframes(array.array("h", (int(max(-1.0, min(1.0, m)) * 32767) for m in pista)).tobytes())


def sonoridad(archivo):
    """Sonoridad integrada (LUFS) de un audio, con el filtro loudnorm de ffmpeg."""
    salida = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(archivo),
                             "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    valor = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", salida).group(0))["input_i"]
    return float(valor) if valor not in ("-inf", "inf") else None


def reemplazar(temporal, destino, intentos=6):
    """os.replace con reintentos: OneDrive bloquea los archivos un instante (OSError 22)."""
    for intento in range(intentos):
        try:
            os.replace(temporal, destino)
            return
        except OSError:
            time.sleep(0.5 * (intento + 1))
    raise OSError(f"No se pudo reemplazar {destino}: sigue bloqueado")


def hacer_escena(ficha, letra=None, dialogos=None):
    dialogos = dialogos or leer_dialogos()
    escena = ESCENAS[ficha]
    titulo, juega, _contexto, opciones = leer_ficha(ficha)
    acto_capitulo, canon, destinos, titulos = datos_de_historia(ficha)
    letra = letra or canon
    letras = [o[0] for o in opciones]
    if letra not in letras:
        raise SystemExit(f"{ficha}: la opción {letra} no se ve en esta partida (visibles: {', '.join(letras)})")
    antes, reacciones = dialogos[ficha]

    cuadros, fotos, sonidos = linea_de_tiempo(escena, antes, reacciones.get(letra, []), len(opciones),
                                              letras.index(letra))
    nombre_juega = PERSONAJES[escena["juega"]]["nombre"]
    inicio = tarjeta(acto_capitulo.upper(), f"{ficha} · {titulo}", f"Juegas como {nombre_juega}")
    destino = destinos[letra]
    fin = tarjeta(f"Elegiste {letra}", f"Continúa en {destino}", titulos.get(destino, ""))
    entrada, salida, fundido = segundos(2.4), segundos(2.4), segundos(0.6)
    total = entrada + len(cuadros) + salida
    duracion = total / FPS

    fondos = fondos_de(escena["fondo"])
    transparente = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
    capas, mezclas, interfaces = {}, {}, {}

    def capa(estado):
        if estado not in capas:
            presentes, apagados = estado
            visibles = dict(escena, personajes=[p for p in escena["personajes"] if p["clave"] in presentes])
            capas[estado] = componer_escena(visibles, transparente, apagados)
        return capas[estado]

    def cuadro(t, personajes, interfaz):
        nuevo, anterior, mezcla = personajes
        if anterior is None:
            gente = capa(nuevo)
        else:                                      # cambia quién habla o alguien entra: mezcla suave
            clave = (nuevo, anterior, round(mezcla, 3))
            if clave not in mezclas:
                mezclas.clear()
                mezclas[clave] = Image.blend(capa(anterior), capa(nuevo), mezcla)
            gente = mezclas[clave]
        if interfaz not in interfaces:
            interfaces.clear()
            if interfaz[0] == "dialogo":
                interfaces[interfaz] = cuadro_dialogo(*interfaz[1:])
            else:
                interfaces[interfaz] = cuadro_decision(nombre_juega, opciones, interfaz[1], letras.index(letra), interfaz[2])
        imagen = fondos[t % len(fondos)].resize((ANCHO, ALTO), Image.NEAREST)
        imagen.alpha_composite(gente)
        imagen.alpha_composite(interfaces[interfaz], (0, TOPE_UI))
        return imagen.convert("RGB")

    SALIDA.mkdir(exist_ok=True)
    temporal = SALIDA / f"{ficha}.tmp.mp4"
    efectos = SALIDA / f"{ficha}.tmp.wav"
    pista_de_sonidos(sonidos, entrada, total, efectos)
    medida = sonoridad(efectos)
    ganancia = SONIDOS_LUFS - medida if medida is not None else 0.0
    # audio: la música (con fundidos) y los efectos, cada uno a su volumen, mezclados en una sola pista
    estereo = "aformat=sample_rates=44100:channel_layouts=stereo"
    musica = pista_de(ficha)
    comando = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ANCHO}x{ALTO}", "-r", str(FPS), "-i", "-"]
    if musica:
        comando += ["-i", str(musica), "-i", str(efectos), "-filter_complex",
                    f"[1:a]atrim=0:{duracion:.3f},afade=t=in:d=2,afade=t=out:st={duracion - 3:.2f}:d=3,"
                    f"volume=-3dB,{estereo}[m];[2:a]volume={ganancia:.1f}dB,{estereo}[s];"
                    "[m][s]amix=inputs=2:duration=longest:normalize=0[a]"]
    else:
        comando += ["-i", str(efectos), "-filter_complex", f"[1:a]volume={ganancia:.1f}dB,{estereo}[a]"]
    comando += ["-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "160k", "-shortest",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-tune", "animation",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporal)]
    ffmpeg = subprocess.Popen(comando, stdin=subprocess.PIPE)

    guion = [inicio]
    for t in range(entrada):                       # título y fundido hacia la escena
        if t < entrada - fundido:
            ffmpeg.stdin.write(inicio.tobytes())
        else:
            escena_t = cuadro(t, *cuadros[0])
            ffmpeg.stdin.write(Image.blend(inicio, escena_t, suave((t - entrada + fundido + 1) / fundido)).tobytes())
    ultimo = None
    for i, (personajes, interfaz) in enumerate(cuadros):
        ultimo = cuadro(entrada + i, personajes, interfaz)
        ffmpeg.stdin.write(ultimo.tobytes())
        if i in fotos:
            guion.append(ultimo)
    for t in range(salida):                        # fundido hacia el "continúa en" (el fondo sigue vivo)
        if t < fundido:
            escena_t = cuadro(entrada + len(cuadros) + t, *cuadros[-1])
            ffmpeg.stdin.write(Image.blend(escena_t, fin, suave((t + 1) / fundido)).tobytes())
        else:
            ffmpeg.stdin.write(fin.tobytes())
    guion.append(fin)
    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        raise SystemExit(f"ffmpeg falló con {ficha}")
    reemplazar(temporal, SALIDA / f"{ficha}.mp4")
    efectos.unlink()

    # guion gráfico: una foto por línea, en columnas de 3
    columnas, mini = 3, (640, 360)
    filas = -(-len(guion) // columnas)
    hoja = Image.new("RGB", (columnas * (mini[0] + 8) + 8, filas * (mini[1] + 8) + 8), (12, 14, 24))
    for n, foto in enumerate(guion):
        hoja.paste(foto.resize(mini, Image.LANCZOS), (8 + (n % columnas) * (mini[0] + 8), 8 + (n // columnas) * (mini[1] + 8)))
    guardar(hoja, SALIDA / f"{ficha}_guion_grafico.png")
    pista = musica.stem if musica else "sin música"
    return (f"{ficha}: opción {letra}, {duracion:.0f} s a {FPS} fps, música {pista}, "
            f"{len(sonidos)} sonidos ({ganancia:+.1f} dB)  ->  escenas_completas/{ficha}.mp4")


def hacer(pedido):
    return hacer_escena(*pedido)


def main(argumentos):
    fichas = [a for a in argumentos if re.fullmatch(r"D\d{3}", a)]
    letra = argumentos[argumentos.index("--opcion") + 1] if "--opcion" in argumentos else None
    pedidas = list(({f: letra for f in fichas} if fichas else EJEMPLOS).items())
    if len(pedidas) == 1:
        print(hacer(pedidas[0]))
        return
    with Pool(min(4, len(pedidas))) as pool:       # una escena por núcleo
        for resultado in pool.imap(hacer, pedidas):
            print(resultado, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
