"""Convierte Historia.md y Dialogos.md en los archivos que carga el juego.

Uso:  python preparar_historia.py

Salida, junto a este archivo:
  historia.json   todo lo de cada ficha en un solo lugar: texto, opciones (requisito, efectos,
                  resultado y siguiente ficha), fondo, personajes y música; los finales con sus
                  variantes; los medidores iniciales y las 79 banderas.
  dialogos.json   los diálogos escritos, línea por línea, con el personaje que habla.

El formato está explicado en FORMATO.md. Este script solo convierte y revisa que los datos
estén bien formados (que cada requisito y cada efecto use la gramática simple, que cada
"siguiente" exista y que el camino del canon llegue al Final 1). La lógica del juego, la que
decide qué opciones se ven y aplica los efectos, la programa el equipo.

Si cambia Historia.md, Dialogos.md, escenas.json o musica.json, se vuelve a correr.
"""
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent
ASSETS = AQUI.parent
RAIZ = ASSETS.parent

MEDIDORES = {"OSC": 2, "PAL": 3, "OBI": 4, "AHS": 0, "PAD": 5, "CLO": 2, "PIS": 0}
NOMBRES_MEDIDORES = {"OSC": "Oscuridad", "PAL": "Influencia de Palpatine", "OBI": "Vínculo con Obi-Wan",
                     "AHS": "Vínculo con Ahsoka", "PAD": "Vínculo con Padmé", "CLO": "Lealtad de los clones",
                     "PIS": "Pistas de la conspiración"}
LINEA_FINAL = {"FINAL 1": "oscura", "FINAL 2": "oscura", "FINAL 3": "emperador", "FINAL 4": "luz",
               "FINAL 5": "luz", "FINAL 6": "exilio"}
# un efecto que solo se aplica según el camino: en D305 B, la Orden 66 solo se detiene si vienes de D273 B
EFECTOS_SI = {("D305", "B"): {"requiere": "D273 B", "efectos": ["ORDEN66_DETENIDA"]}}
CARPETAS = {
    "sprites": "assets/personajes/sprites_1x",
    "sprites_apagados": "assets/personajes/sprites_apagados",
    "sprites_holograma": "assets/personajes/sprites_holograma",
    "fondos": "assets/escenarios/fondos_1x",
    "fondos_animados": "assets/escenarios/animados_60",
    "musica": "assets/musica/pistas",
    "sonidos": "assets/sonidos",
}


def limpiar(texto):
    """Quita el formato de Markdown (asteriscos) y los espacios de sobra."""
    return re.sub(r"\s+", " ", texto.replace("**", "").replace("*", "")).strip()


def con_punto(texto):
    texto = texto.strip().rstrip(";").strip()
    texto = texto[0].upper() + texto[1:]
    return texto if texto.endswith((".", "!", "?", '"', "»")) else texto + "."


# ---------- gramática simple de requisitos y efectos ----------

def convertir_requisito(c):
    """'requiere PAD ≥ 25 o ⚑ ANAKIN_DUDA_ORDEN' -> 'PAD >= 25 o ANAKIN_DUDA_ORDEN'"""
    c = re.sub(r"^(si|requiere) ", "", c.strip())
    return c.replace("⚑ ", "").replace("≥", ">=").replace("≤", "<=")


def convertir_efecto(e):
    """'OSC +5' se queda igual; '⚑ X' -> 'X'; '*quita* ⚑ X' -> 'quita X'"""
    e = limpiar(e)
    if e.startswith("quita ⚑ "):
        return "quita " + e[len("quita ⚑ "):]
    return e.replace("⚑ ", "")


def revisar_requisito(req, banderas, opciones):
    errores = []
    if not req:
        return errores
    for alternativa in req.split(" o "):
        for atomo in alternativa.split(" y "):
            p = atomo.split()
            if len(p) == 3:
                ok = p[0] in MEDIDORES and p[1] in (">=", "<=") and p[2].isdigit()
            elif len(p) == 2 and p[0] == "sin":
                ok = p[1] in banderas
            elif len(p) == 2:
                ok = p[0] in opciones and p[1] in opciones[p[0]]
            else:
                ok = len(p) == 1 and p[0] in banderas
            if not ok:
                errores.append(f"requisito que no se entiende: '{atomo}' en '{req}'")
    return errores


def revisar_efecto(e, banderas):
    p = e.split()
    if len(p) == 2 and p[0] in MEDIDORES and re.fullmatch(r"[+-]\d+", p[1]):
        return []
    if len(p) == 2 and p[0] == "quita" and p[1] in banderas:
        return []
    if len(p) == 1 and p[0] in banderas:
        return []
    return [f"efecto que no se entiende: '{e}'"]


# ---------- sprites listos para el juego ----------

def preparar_sprites(claves):
    """Por cada personaje, dos versiones más del sprite (a 40x56, como sprites_1x):
    apagada (más oscura, para cuando habla otro) y holograma (azul y translúcida).
    Así el juego solo elige qué archivo cargar."""
    for carpeta in ("sprites_apagados", "sprites_holograma"):
        (RAIZ / CARPETAS[carpeta]).mkdir(exist_ok=True)
    for clave in claves:
        sprite = Image.open(RAIZ / CARPETAS["sprites"] / f"{clave}.png").convert("RGBA")
        r, g, b, a = sprite.split()
        r, g, b = (canal.point(lambda v: int(v * 0.55)) for canal in (r, g, b))
        Image.merge("RGBA", (r, g, b, a)).save(RAIZ / CARPETAS["sprites_apagados"] / f"{clave}.png")
        azul = ImageOps.colorize(sprite.convert("RGB").convert("L"), black=(16, 60, 150), white=(190, 240, 255)).convert("RGBA")
        azul.putalpha(a.point(lambda v: v * 200 // 255))
        azul.save(RAIZ / CARPETAS["sprites_holograma"] / f"{clave}.png")


def posicion_en_pantalla(p, cache={}):
    """Esquina de arriba a la izquierda del sprite ya escalado (y girado, si está tirado en el suelo),
    con los pies en (x, y_pies): así el juego solo dibuja la imagen en (izquierda, arriba)."""
    if p["clave"] not in cache:
        cache[p["clave"]] = Image.open(RAIZ / CARPETAS["sprites"] / f"{p['clave']}.png").convert("RGBA")
    s = cache[p["clave"]].resize((40 * p["escala"], 56 * p["escala"]), Image.NEAREST)
    if p.get("girado"):
        s = s.rotate(90, expand=True)
    return p["x"] - s.width // 2, p["y_pies"] - s.getbbox()[3]


# ---------- Historia.md ----------

def leer_banderas(texto):
    tabla = texto[texto.index("# APÉNDICE A"):texto.index("# APÉNDICE B")]
    return {nombre: limpiar(desc) for nombre, desc in re.findall(r"^\| `(\w+)` \| (.+?) \| .+? \| .+? \|$", tabla, re.M)}


def leer_notas(notas):
    """Notas del contexto. 'Si ⚑ X, texto' se vuelve {requiere, texto}; lo demás son notas para quien
    escribe (el juego no las muestra)."""
    para_juego, para_guion = [], []
    for nota in notas:
        for clausula in re.split(r"(?<=[.;])\s+(?=[Ss]i )", nota):
            m = re.match(r"[Ss]i (⚑ \w+(?:\s+(?:o|y)\s+⚑ \w+)*)(?: sigue activa)?, (.+)$", clausula.strip())
            if m and not m.group(2).lower().startswith("o si "):
                para_juego.append({"requiere": convertir_requisito(m.group(1)), "texto": con_punto(m.group(2))})
            else:
                para_guion.append(limpiar(clausula))
    return para_juego, para_guion


def leer_opcion(ficha, letra, linea):
    antes, _, despues = linea.partition("→")
    requisito = re.findall(r"\*\(((?:si|requiere) [^)]*)\)\*", antes)
    texto = limpiar(re.sub(r"\*\((?:si|requiere) [^)]*\)\*", "", antes).replace("★", ""))
    m = re.match(r"\s*(D\d{3}|FINAL \d|FP\d)\s*(.*)", despues)
    siguiente, resto = m.group(1), m.group(2)
    notas = re.findall(r"\*\(([^)]*)\)\*", resto)
    efectos = [convertir_efecto(e) for e in re.sub(r"\*\([^)]*\)\*", "", resto).split("·") if limpiar(e)]
    efectos_si = []
    if (ficha, letra) in EFECTOS_SI:
        especial = EFECTOS_SI[(ficha, letra)]
        efectos = [e for e in efectos if e not in especial["efectos"]]
        efectos_si.append(especial)
        notas = []                                  # la nota solo explicaba esa condición
    resultado, resultado_requiere = "", ""
    if notas:
        mm = re.match(r"si (⚑ \w+(?:\s+(?:o|y)\s+⚑ \w+)*), (.+)$", notas[0].strip())
        if mm:
            resultado_requiere, resultado = convertir_requisito(mm.group(1)), con_punto(mm.group(2))
        else:
            resultado = con_punto(limpiar(notas[0]))
    return {"letra": letra, "texto": texto, "canon": "★" in antes,
            "requiere": convertir_requisito(requisito[0]) if requisito else "",
            "efectos": efectos, "efectos_si": efectos_si, "siguiente": siguiente,
            "resultado": resultado, "resultado_requiere": resultado_requiere}


def leer_fichas(texto, escenas, musica):
    marcas = [(m.start(), m.group(1)) for m in re.finditer(r"^# (ACTO .+)$", texto, re.M)]
    capitulos = [(m.start(), m.group(1)) for m in re.finditer(r"^## (Capítulo .+)$", texto, re.M)]
    ultimo = lambda lista, pos: limpiar(max((x for x in lista if x[0] < pos), default=(0, ""))[1])
    fichas = {}
    for m in re.finditer(r"^#### (D\d{3}) · (.+?)\n(.*?)(?=^#### |^## |^# |\Z)", texto, re.S | re.M):
        clave, cuerpo = m.group(1), m.group(3)
        lineas = cuerpo.strip().splitlines()
        cabecera = [limpiar(p) for p in lineas[0].split(" · ")]
        contexto = " ".join(l.strip() for l in lineas[1:] if l.strip() and not l.startswith("- **"))
        notas, notas_guion = leer_notas(re.findall(r"\*\(([^)]*)\)\*", contexto))
        escena = escenas[clave]
        fichas[clave] = {
            "titulo": limpiar(m.group(2)),
            "juega": cabecera[0].replace("Juega: ", ""),
            "fuente": next((p.replace("Fuente: ", "") for p in cabecera if p.startswith("Fuente:")), ""),
            "rama": "Rama" in cabecera,
            "bifurcacion": any("Bifurcación mayor" in p for p in cabecera),
            "acto": ultimo(marcas, m.start()),
            "capitulo": ultimo(capitulos, m.start()),
            "texto": limpiar(re.sub(r"\*\([^)]*\)\*", "", contexto)),
            "notas": notas,
            "notas_guion": notas_guion,
            "opciones": [leer_opcion(clave, letra, l) for letra, l in re.findall(r"^- \*\*([A-F])\)\*\* (.+)$", cuerpo, re.M)],
            "fondo": escena["fondo"],
            "personajes": [{"clave": p["clave"], "escala": p["escala"],
                            "izquierda": posicion_en_pantalla(p)[0], "arriba": posicion_en_pantalla(p)[1],
                            "holograma": bool(p.get("holograma")), "girado": bool(p.get("girado"))}
                           for p in sorted(escena["personajes"], key=lambda p: p["y_pies"])],
            "musica": musica["fichas"][clave],
        }
    return fichas


def leer_finales(texto, musica):
    seccion = texto[texto.index("## Finales principales"):texto.index("# APÉNDICE A")]
    finales = {}
    for m in re.finditer(r"^### (FINAL \d|FP\d) · (.+?)\n(.*?)(?=^### |^## |^# |\Z)", seccion, re.S | re.M):
        clave, cuerpo = m.group(1), m.group(3)
        lineas = [l.strip() for l in cuerpo.splitlines() if l.strip()]
        llega = re.search(r"\*\*Se llega por:\*\* (.+)", cuerpo).group(1)
        if clave.startswith("FP"):                  # "D011 C. Rotta muere..." -> "Rotta muere..."
            texto_final = limpiar(re.sub(r"^D\d{3} [A-F](?: o D\d{3} [A-F])*\.\s*", "", llega))
        else:
            texto_final = " ".join(limpiar(l) for l in lineas if not l.startswith(("**", "- ")))
        variantes = []
        for cond, txt in re.findall(r"^- \*\(([^)]*)\)\* (.+)$", cuerpo, re.M):
            txt = limpiar(txt)
            if cond.startswith("según "):           # "según D303": una variante por opción
                ficha = cond.split()[1]
                partes = [p.strip() for p in re.split(r";\s*o\s+", txt)]
                for letra, parte in zip("ABC", partes):
                    variantes.append({"requiere": f"{ficha} {letra}",
                                      "texto": con_punto(parte if letra == "A" else "Anakin " + parte)})
                continue
            cond = re.sub(r"^si (eligió|llegó desde) ", "", cond)
            variantes.append({"requiere": convertir_requisito(cond), "texto": con_punto(txt)})
        finales[clave] = {"nombre": limpiar(re.sub(r"\*\(canon\)\*", "", m.group(2))),
                          "canon": "(canon)" in m.group(2), "linea": LINEA_FINAL.get(clave, "prematuro"),
                          "texto": texto_final, "variantes": variantes,
                          "musica": musica["finales"].get(clave, "despedida")}
    return finales


# ---------- Dialogos.md ----------

def leer_dialogos(fichas, nombres):
    texto = (RAIZ / "Dialogos.md").read_text(encoding="utf-8")

    def clave_de(nombre, ficha):
        """El personaje que dice la línea: primero entre los que están en la escena, luego entre todos."""
        n = nombre.lower()
        en_escena = [p["clave"] for p in fichas[ficha]["personajes"]]
        for c in en_escena + list(nombres):
            if n in nombres[c].lower():
                return c
        return None

    def lineas(bloque, ficha):
        salida = []
        for m in re.finditer(r"^(?:\[(entra|sale) ([^\]]+)\]|([^:\n>#\[-][^:\n]{0,29}): (.+))$", bloque, re.M):
            if m.group(1):
                quien = m.group(2).strip()
                salida.append({"tipo": m.group(1), "quien": quien, "clave": clave_de(quien, ficha), "texto": ""})
            else:
                quien = m.group(3).strip()
                narra = quien.lower() == "narra"
                salida.append({"tipo": "narra" if narra else "dice", "quien": "" if narra else quien,
                               "clave": None if narra else clave_de(quien, ficha), "texto": m.group(4).strip()})
        return salida

    dialogos = {}
    for bloque in re.split(r"^## ", texto, flags=re.M)[1:]:
        ficha = bloque[:4]
        partes = re.split(r"^### ([A-F])\b.*$", bloque, flags=re.M)
        dialogos[ficha] = {"antes": lineas(partes[0], ficha),
                           "reacciones": {letra: lineas(cuerpo, ficha) for letra, cuerpo in zip(partes[1::2], partes[2::2])}}
    return dialogos


# ---------- revisión ----------

def revisar(historia, dialogos):
    fichas, finales, banderas = historia["fichas"], historia["finales"], historia["banderas"]
    opciones = {f: [o["letra"] for o in d["opciones"]] for f, d in fichas.items()}
    errores = []
    for f, d in fichas.items():
        for nota in d["notas"]:
            errores += revisar_requisito(nota["requiere"], banderas, opciones)
        for o in d["opciones"]:
            if o["siguiente"] not in fichas and o["siguiente"] not in finales:
                errores.append(f"{f} {o['letra']}: lleva a {o['siguiente']}, que no existe")
            errores += revisar_requisito(o["requiere"], banderas, opciones)
            errores += revisar_requisito(o["resultado_requiere"], banderas, opciones)
            for e in o["efectos"]:
                errores += revisar_efecto(e, banderas)
            for es in o["efectos_si"]:
                errores += revisar_requisito(es["requiere"], banderas, opciones)
                for e in es["efectos"]:
                    errores += revisar_efecto(e, banderas)
    for fin, d in finales.items():
        for v in d["variantes"]:
            errores += revisar_requisito(v["requiere"], banderas, opciones)
    for f, d in dialogos.items():
        if f not in fichas:
            errores.append(f"Dialogos.md: {f} no existe")
            continue
        for letra in d["reacciones"]:
            if letra not in opciones[f]:
                errores.append(f"Dialogos.md: {f} no tiene opción {letra}")
        for linea in d["antes"] + [l for r in d["reacciones"].values() for l in r]:
            if linea["tipo"] in ("entra", "sale") and not linea["clave"]:
                errores.append(f"Dialogos.md: {f}: no sé quién es '{linea['quien']}'")
    # el camino del canon (siempre ★) debe llegar al Final 1 sin pasar dos veces por la misma ficha
    actual, pasos, vistas = historia["inicio"], 0, set()
    while actual in fichas and actual not in vistas:
        vistas.add(actual)
        canon = [o for o in fichas[actual]["opciones"] if o["canon"]]
        if len(canon) != 1:
            errores.append(f"{actual}: tiene {len(canon)} opciones ★")
            break
        actual, pasos = canon[0]["siguiente"], pasos + 1
    if actual != "FINAL 1":
        errores.append(f"el camino del canon termina en {actual}, no en FINAL 1")
    return errores, pasos


def main():
    texto = re.sub(r"```.*?```", "", (RAIZ / "Historia.md").read_text(encoding="utf-8"), flags=re.S)
    escenas = json.loads((ASSETS / "escenas" / "escenas.json").read_text(encoding="utf-8"))
    musica = json.loads((ASSETS / "musica" / "musica.json").read_text(encoding="utf-8"))
    personajes = json.loads((ASSETS / "personajes" / "personajes.json").read_text(encoding="utf-8"))
    nombres = {c: p["nombre"] for c, p in personajes.items()}

    historia = {
        "inicio": "D001",
        "medidores": MEDIDORES,
        "nombres_medidores": NOMBRES_MEDIDORES,
        "carpetas": CARPETAS,
        "pantalla": {"ancho": 1280, "alto": 720, "escala_fondo": 4},
        "fondo_animado": {"cuadros": 144, "columnas": 12, "ancho": 320, "alto": 180, "fps": 60},
        "nombres": nombres,
        "banderas": leer_banderas(texto),
        "fichas": leer_fichas(texto, escenas, musica),
        "finales": leer_finales(texto, musica),
    }
    dialogos = leer_dialogos(historia["fichas"], nombres)
    errores, pasos = revisar(historia, dialogos)
    if errores:
        print("\n".join(errores))
        raise SystemExit(f"{len(errores)} errores: no se escribieron los archivos")
    preparar_sprites(nombres)

    (AQUI / "historia.json").write_text(json.dumps(historia, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "dialogos.json").write_text(json.dumps(dialogos, ensure_ascii=False, indent=1), encoding="utf-8")
    fichas = historia["fichas"].values()
    print(f"historia.json: {len(historia['fichas'])} fichas, {sum(len(f['opciones']) for f in fichas)} opciones "
          f"({sum(1 for f in fichas for o in f['opciones'] if o['requiere'])} con requisito), "
          f"{len(historia['finales'])} finales, {len(historia['banderas'])} banderas, "
          f"{sum(len(f['notas']) for f in fichas)} notas para el juego y "
          f"{sum(len(f['notas_guion']) for f in fichas)} para quien escribe")
    print(f"dialogos.json: {len(dialogos)} fichas con diálogo")
    print(f"El camino del canon llega al Final 1 en {pasos} decisiones")


if __name__ == "__main__":
    main()
