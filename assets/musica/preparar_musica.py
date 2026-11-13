"""Música del juego: importa las canciones, las convierte a OGG con el volumen parejo
y arma musica.json (qué pista suena en cada ficha y en cada final).

Uso:
    python preparar_musica.py                     # convierte lo que haya en originales/ y arma musica.json
    python preparar_musica.py --importar          # antes, mueve las canciones desde Descargas
    python preparar_musica.py --importar CARPETA  # ... o desde otra carpeta

Cada pista se reconoce por un pedazo de su título (columna `busca`), así que el
archivo puede llamarse como lo nombre el descargador. Los audios no van a git
(son de John Williams y Kevin Kiner): quien clone el repo los baja con los links
de PISTAS y corre este script con --importar.

Si una pista todavía no tiene archivo, musica.json la marca con "archivo": null
y el juego debe tocar su "respaldo".
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ASSETS = AQUI.parent
ORIGINALES = AQUI / "originales"
PISTAS_DIR = AQUI / "pistas"
DESCARGAS = Path.home() / "Downloads"
EXTENSIONES = {".mp3", ".m4a", ".webm", ".opus", ".ogg", ".wav", ".flac"}

VOLUMEN = -18.0     # sonoridad objetivo (LUFS); las pistas suaves suben solo hasta donde deja el pico
PICO_MAX = -1.0     # pico máximo (dBTP) para que la ganancia no sature
CALIDAD = 5         # calidad Vorbis (~160 kbps)

# clave: (título, autor, de dónde sale, link, busca en el nombre del archivo, respaldo)
PISTAS = {
    "menu":             ("Main Title", "John Williams", "Star Wars: A New Hope",
                         "https://www.youtube.com/watch?v=e9lapdvLSGw", r"^main title", None),
    "clone_wars":       ("Star Wars Main Title & A Galaxy Divided", "Kevin Kiner", "Star Wars: The Clone Wars (2008)",
                         "https://www.youtube.com/watch?v=iKZgzM8Ghns", r"galaxy divided", "menu"),
    "teth":             ("Battle of Teth", "Kevin Kiner", "Star Wars: The Clone Wars (2008)",
                         "https://www.youtube.com/watch?v=bUgwpyurJVc", r"battle of teth", "batalla_clones"),
    "batalla_clones":   ("Grievous and the Droids", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=Ossn_cc6SyQ", r"grievous and the droids", None),
    "geonosis":         ("Love Pledge and the Arena", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=QU2HpDUlUzY", r"love pledge", "batalla_clones"),
    "batalla_espacial": ("Star Wars and the Revenge of the Sith", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=NMYUsYMDqgc", r"star wars and the revenge of the sith",
                         "batalla_clones"),
    "grievous":         ("General Grievous", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=ApJumkyz7F0", r"^general grievous", "batalla_clones"),
    "dooku":            ("Confrontation with Count Dooku and Finale", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=HaaGq6k8ZXM", r"count dooku", "duelo_sith"),
    "duelo_sith":       ("Duel of the Fates", "John Williams", "Star Wars: The Phantom Menace",
                         "https://www.youtube.com/watch?v=D_2bluVPsb0", r"duel of the fates", "batalla_clones"),
    "amor":             ("Across the Stars", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=7wMiMDBHnJ0", r"across the stars", "calma"),
    "calma":            ("The Meadow Picnic", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=8HiQD_3S8OM", r"meadow picnic", "amor"),
    "palpatine":        ("Palpatine's Teachings", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=3gqnXj5RngA", r"palpatine.?s teachings", "visiones"),
    "templo":           ("Yoda and the Younglings", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=4K_zN6bNd3s", r"yoda and the younglings", "fuerza"),
    "tatooine":         ("Return to Tatooine", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=4x5xORsCKYs", r"return to tatooine", "despedida"),
    "persecucion":      ("Zam the Assassin and the Chase Through Coruscant", "John Williams",
                         "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=1PQ-nAskDcM", r"zam the assassin", "batalla_clones"),
    "viaje":            ("Departing Coruscant", "John Williams", "Star Wars: Attack of the Clones",
                         "https://www.youtube.com/watch?v=8AGajwqVgNE", r"departing coruscant", "calma"),
    "hutt":             ("Jabba the Hutt", "John Williams (Boston Pops)", "Star Wars: Return of the Jedi",
                         "https://www.youtube.com/watch?v=NkVAOowrG1s", r"jabba", "tatooine"),
    "fuerza":           ("The Hologram / Binary Sunset", "John Williams", "Star Wars: A New Hope",
                         "https://www.youtube.com/watch?v=tV4js7fgIuo", r"binary sunset", "templo"),
    "despedida":        ("Padmé's Ruminations", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=ZfEz9hpOlho", r"ruminations", "tatooine"),
    "visiones":         ("Anakin's Dream", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=2MqBvcjxJ70", r"anakin.?s dream", "palpatine"),
    "revelacion":       ("Anakin's Betrayal", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=m2p-im7cxa4", r"anakin.?s betrayal", "orden66"),
    "orden66":          ("Anakin's Dark Deeds", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=FVWr249AUq4", r"dark deeds", "revelacion"),
    "mustafar":         ("Battle of the Heroes", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=xaqF9mRLu38", r"battle of the heroes", "duelo_sith"),
    "imperio":          ("The Imperial March (Darth Vader's Theme)", "John Williams", "Star Wars: The Empire Strikes Back",
                         "https://www.youtube.com/watch?v=s3SZ5sIMY6o", r"imperial march", "palpatine"),
    "creditos":         ("A New Hope and End Credits", "John Williams", "Star Wars: Revenge of the Sith",
                         "https://www.youtube.com/watch?v=ZK52tEenER8", r"new hope and end credits", "menu"),
}

# lo que suena en cada escenario si la ficha no dice otra cosa
POR_ESCENARIO = {
    "christophsis": "batalla_clones", "monasterio_teth": "teth", "dunas_tatooine": "tatooine",
    "palacio_hutt": "hutt", "cabina": "viaje", "puente_crucero": "batalla_espacial",
    "espacio_batalla": "batalla_espacial", "pasillo_republica": "viaje", "pasillo_separatista": "grievous",
    "oficina_canciller": "palpatine", "fabrica_droides": "batalla_clones", "hangar_republica": "viaje",
    "puesto_avanzado": "batalla_clones", "pueblo_colonia": "batalla_clones", "departamento_padme": "amor",
    "senado": "palpatine", "plataforma_coruscant": "viaje", "templo_pasillo": "templo",
    "templo_exterior": "templo", "consejo_jedi": "templo", "ciudadela": "persecucion",
    "niveles_bajos": "persecucion", "mustafar": "mustafar", "geonosis": "geonosis",
    "palacio_elegante": "visiones", "palacio_mandalore": "calma", "kamino": "visiones",
    "dathomir": "duelo_sith", "jungla": "batalla_clones", "mortis": "fuerza", "umbara": "batalla_clones",
    "moraband": "visiones", "dagobah": "fuerza", "utapau": "grievous", "naboo": "calma",
    "campo_batalla": "batalla_clones",
}

# fichas (o rangos) que cambian la música del escenario, en orden de la historia
POR_FICHA = {
    # Acto I
    "D001": "clone_wars", "D017-D018": "dooku", "D027": "despedida", "D029": "amor",
    "D034-D035": "grievous", "D036": "viaje", "D041": "fuerza", "D052-D055": "persecucion",
    # Acto II
    "D060-D061": "persecucion", "D063-D064": "persecucion", "D076-D077": "persecucion", "D078": "visiones",
    "D081-D082": "persecucion", "D085": "persecucion", "D087": "persecucion", "D089": "fuerza",
    "D090-D092": "batalla_clones", "D093": "fuerza", "D094": "visiones", "D099-D100": "persecucion",
    "D103-D104": "duelo_sith", "D109": "visiones", "D111": "visiones", "D113": "imperio", "D114": "visiones",
    "D118": "viaje", "D122": "despedida", "D124-D125": "persecucion", "D126": "viaje",
    # Acto III
    "D130": "despedida", "D133": "visiones", "D135": "despedida", "D144-D145": "tatooine",
    "D146": "despedida", "D149-D150": "persecucion", "D153": "dooku", "D154": "palpatine",
    "D158": "grievous", "D159-D162": "duelo_sith",
    # Acto IV
    "D171": "despedida", "D173-D176": "duelo_sith", "D177": "despedida", "D178": "fuerza",
    "D179": "batalla_clones", "D180": "palpatine", "D181": "duelo_sith", "D183": "palpatine",
    "D184": "persecucion", "D191": "despedida", "D193": "persecucion", "D194-D195": "visiones",
    "D196-D197": "despedida", "D198": "fuerza",
    # Acto V
    "D206": "persecucion", "D208": "despedida", "D210": "visiones", "D213-D214": "persecucion",
    "D217": "visiones", "D220": "fuerza", "D222": "fuerza", "D226": "palpatine", "D228": "visiones",
    "D229": "visiones", "D230": "amor", "D231": "persecucion", "D232": "despedida", "D233": "visiones",
    "D234": "visiones", "D235": "persecucion", "D236-D237": "visiones", "D238-D239": "palpatine",
    "D243": "fuerza", "D249": "fuerza",
    # Acto VI
    "D252": "dooku", "D255": "amor", "D256": "visiones", "D261-D262": "visiones", "D267-D268": "duelo_sith",
    "D270": "persecucion", "D273-D280": "revelacion", "D281-D285": "orden66", "D286": "despedida",
    "D287": "orden66", "D288": "despedida", "D289": "orden66", "D290": "despedida",
    "D294-D295": "imperio",
    # línea de la luz
    "D296": "revelacion", "D297": "duelo_sith", "D298": "persecucion", "D299": "orden66",
    "D300": "fuerza", "D302": "fuerza", "D304": "fuerza",
    # línea del emperador
    "D305": "imperio", "D306": "orden66", "D307": "despedida", "D308": "imperio",
    # línea del exilio
    "D309": "persecucion", "D311": "despedida", "D312": "calma",
}

FINALES = {
    "FINAL 1": "imperio", "FINAL 2": "imperio", "FINAL 3": "palpatine", "FINAL 4": "creditos",
    "FINAL 5": "despedida", "FINAL 6": "fuerza",
    "FP1": "visiones", "FP2": "visiones", "FP3": "revelacion", "FP4": "despedida", "FP5": "despedida",
}


def normalizar(nombre):
    """Nombre de archivo comparable: minúsculas y sin los signos 'anchos' que pone el descargador."""
    return nombre.lower().replace("＂", '"').replace("：", ":").replace("’", "'")


def importar(carpeta):
    """Mueve a originales/<clave>.<ext> cada canción de `carpeta` que coincida con una pista."""
    ORIGINALES.mkdir(exist_ok=True)
    audios = [a for a in carpeta.iterdir() if a.suffix.lower() in EXTENSIONES]
    for clave, (titulo, *_, busca, _respaldo) in PISTAS.items():
        candidatos = sorted((a for a in audios if re.search(busca, normalizar(a.stem))),
                            key=lambda a: a.stat().st_mtime, reverse=True)
        if not candidatos:
            continue
        if list(ORIGINALES.glob(f"{clave}.*")):
            print(f"  {clave}: ya estaba en originales/, dejo {candidatos[0].name} donde está")
            continue
        if len(candidatos) > 1:
            print(f"  {clave}: hay {len(candidatos)} archivos que coinciden, tomo el más nuevo")
        destino = ORIGINALES / f"{clave}{candidatos[0].suffix.lower()}"
        shutil.move(str(candidatos[0]), destino)
        print(f"  {candidatos[0].name}  ->  originales/{destino.name}")


def medir(archivo):
    """Sonoridad integrada (LUFS) y pico real (dBTP) con el filtro loudnorm de ffmpeg."""
    salida = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(archivo),
                             "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    datos = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", salida).group(0))
    return float(datos["input_i"]), float(datos["input_tp"])


def duracion(archivo):
    salida = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "csv=p=0", str(archivo)], capture_output=True, text=True).stdout
    return round(float(salida))


def reemplazar(temporal, destino, intentos=6):
    """os.replace con reintentos: OneDrive bloquea los archivos un instante (OSError 22)."""
    for intento in range(intentos):
        try:
            os.replace(temporal, destino)
            return
        except OSError:
            time.sleep(0.5 * (intento + 1))
    raise OSError(f"No se pudo reemplazar {destino}: sigue bloqueado")


def convertir(clave, original):
    """originales/<clave>.* -> pistas/<clave>.ogg con ganancia fija (no comprime la dinámica)."""
    destino = PISTAS_DIR / f"{clave}.ogg"
    if destino.exists() and destino.stat().st_mtime > original.stat().st_mtime:
        return destino
    sonoridad, pico = medir(original)
    ganancia = min(VOLUMEN - sonoridad, PICO_MAX - pico)
    temporal = destino.with_name(f"{clave}.tmp.ogg")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(original),
                    "-vn", "-map_metadata", "-1", "-af", f"volume={ganancia:.2f}dB",
                    "-ar", "44100", "-ac", "2", "-c:a", "libvorbis", "-q:a", str(CALIDAD),
                    "-metadata", f"title={PISTAS[clave][0]}", str(temporal)], check=True)
    reemplazar(temporal, destino)
    print(f"  {clave}: {sonoridad:.1f} LUFS, ganancia {ganancia:+.1f} dB")
    return destino


def expandir(rango):
    if "-" not in rango:
        return [rango]
    a, b = (int(x[1:]) for x in rango.split("-"))
    return [f"D{n:03d}" for n in range(a, b + 1)]


def mapa_fichas():
    """Pista de cada ficha: la de su escenario, salvo que POR_FICHA diga otra."""
    escenarios = json.loads((ASSETS / "escenarios" / "fichas.json").read_text(encoding="utf-8"))
    faltan = set(escenarios.values()) - set(POR_ESCENARIO)
    assert not faltan, f"escenarios sin música: {sorted(faltan)}"
    fichas = {f: POR_ESCENARIO[e] for f, e in sorted(escenarios.items())}
    for rango, pista in POR_FICHA.items():
        for ficha in expandir(rango):
            assert ficha in fichas, f"{ficha} no existe"
            fichas[ficha] = pista
    usadas = set(fichas.values()) | set(FINALES.values()) | {"menu", "creditos"}
    assert usadas <= set(PISTAS), f"pistas desconocidas: {sorted(usadas - set(PISTAS))}"
    sin_uso = set(PISTAS) - usadas
    if sin_uso:
        print("  Aviso: pistas que no suenan en ninguna ficha:", ", ".join(sorted(sin_uso)))
    return fichas


def main(argumentos):
    if shutil.which("ffmpeg") is None:
        raise SystemExit("Falta ffmpeg (winget install Gyan.FFmpeg)")
    if "--importar" in argumentos:
        resto = [a for a in argumentos if not a.startswith("--")]
        carpeta = Path(resto[0]) if resto else DESCARGAS
        print(f"Importando desde {carpeta}")
        importar(carpeta)

    PISTAS_DIR.mkdir(exist_ok=True)
    print("Convirtiendo a OGG")
    pistas, faltan = {}, []
    for clave, (titulo, autor, fuente, link, _busca, respaldo) in PISTAS.items():
        originales = sorted(ORIGINALES.glob(f"{clave}.*")) if ORIGINALES.exists() else []
        ya_hecha = PISTAS_DIR / f"{clave}.ogg"
        archivo = convertir(clave, originales[0]) if originales else (ya_hecha if ya_hecha.exists() else None)
        if archivo is None:
            faltan.append(clave)
        pistas[clave] = {
            "titulo": titulo, "autor": autor, "fuente": fuente, "youtube": link,
            "archivo": f"pistas/{clave}.ogg" if archivo else None,
            "duracion_s": duracion(archivo) if archivo else None,
            "respaldo": respaldo,
        }
    for clave in faltan:        # el respaldo de una pista que falta debe existir
        assert pistas[pistas[clave]["respaldo"]]["archivo"], f"{clave}: su respaldo tampoco está"

    musica = {"menu": "menu", "creditos": "creditos", "pistas": pistas,
              "fichas": mapa_fichas(), "finales": FINALES}
    (AQUI / "musica.json").write_text(json.dumps(musica, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"musica.json: {len(pistas) - len(faltan)} de {len(pistas)} pistas, {len(musica['fichas'])} fichas")
    if faltan:
        print("Faltan (suena su respaldo):", ", ".join(f"{c} -> {pistas[c]['respaldo']}" for c in faltan))


if __name__ == "__main__":
    main(sys.argv[1:])
