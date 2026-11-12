"""Sonidos del juego hechos con código (no son de las películas).

- Voces: tonos suaves de tecnología que suenan mientras se escribe el texto, como ondas: un
  seno puro cuyo tono sube y baja en curva durante el sonido, con volumen en campana (entra y
  sale sin golpe) y un eco corto que lo hace sentir como una onda que se expande. Registro de
  220 a 760 Hz. Cada personaje tiene su voz (más grave, más aguda, con más o menos ondulación)
  y cada voz trae varias variantes para que no suene siempre igual.
- Interfaz: el tono del cursor y el de confirmar, con el mismo estilo.

Uso:  python generar_sonidos.py
Salida, junto a este archivo (WAV de 44.1 kHz, 16 bits, mono):
  voces/<voz>_<n>.wav   VARIANTES por voz
  ui/cursor.wav, ui/confirmar.wav
  sonidos.json          voz de cada personaje, archivos de cada voz y cada cuántas letras suena
"""
import array
import json
import math
import random
import wave
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ASSETS = AQUI.parent
MUESTREO = 44100
VARIANTES = 6
CADA_LETRAS = 4          # suena cada 4 letras: a 40 letras por segundo, unas 10 veces por segundo
ECOS = ((0.030, 0.35), (0.060, 0.12))   # (retraso en s, volumen): la "onda" que se expande

# voz: (tono base en Hz, ondulación en semitonos, ondas durante el sonido, duración en s, volumen 0-1)
VOCES = {
    "narrador":  (520, 0.6, 0.5, 0.050, 0.30),   # casi plano y corto: no compite con los personajes
    "anakin":    (480, 2.0, 1.0, 0.075, 0.45),
    "vader":     (250, 1.0, 0.75, 0.090, 0.50),
    "ahsoka":    (620, 2.5, 1.2, 0.070, 0.42),
    "obi_wan":   (440, 1.8, 1.0, 0.075, 0.45),
    "padme":     (560, 2.0, 1.0, 0.070, 0.42),
    "yoda":      (450, 3.5, 2.0, 0.085, 0.42),   # ondula mucho
    "jedi":      (460, 1.8, 1.0, 0.075, 0.42),
    "alta":      (580, 2.0, 1.0, 0.070, 0.42),
    "clon":      (400, 1.2, 1.5, 0.065, 0.42),
    "palpatine": (300, 2.5, 0.8, 0.090, 0.45),
    "dooku":     (340, 1.5, 0.8, 0.085, 0.45),
    "sith":      (320, 2.0, 1.0, 0.085, 0.45),
    "grievous":  (330, 3.0, 2.5, 0.080, 0.42),
    "villano":   (380, 1.8, 1.0, 0.080, 0.42),
    "general":   (500, 1.8, 1.0, 0.075, 0.42),
    "hutt":      (220, 3.0, 1.5, 0.100, 0.50),   # el más grave
    "wookiee":   (290, 3.5, 1.8, 0.090, 0.45),
    "pequeno":   (760, 3.0, 1.5, 0.060, 0.38),
    "droide":    (700, 5.0, 2.0, 0.080, 0.38),   # astromecánicos: la onda más marcada
    "protocolo": (600, 0.8, 1.0, 0.060, 0.38),   # 3PO y droides tácticos: casi planos
    "mortis":    (400, 1.5, 0.6, 0.110, 0.40),   # lento, casi etéreo
}

PERSONAJES = {
    "anakin": ["anakin_skywalker"], "vader": ["darth_vader"], "ahsoka": ["ahsoka_tano"],
    "obi_wan": ["obi_wan_kenobi", "rako_hardeen"], "padme": ["padme_amidala"], "yoda": ["yoda"],
    "jedi": ["mace_windu", "plo_koon", "kit_fisto", "ki_adi_mundi", "even_piell", "quinlan_vos", "caleb_dume"],
    "alta": ["luminara_unduli", "shaak_ti", "barriss_offee", "jocasta_nu", "depa_billaba", "tiplar", "kalifa",
             "satine_kryze", "bo_katan_kryze", "mon_mothma", "steela_gerrera", "mina_bonteri", "letta_turmond",
             "trace_martez", "rafa_martez", "aurra_sing", "reina_karina", "reina_miraj_scintel", "nala_se"],
    "clon": ["capitan_rex", "fives", "echo", "comandante_cody", "waxer", "boil", "hevy", "axe", "hardcase",
             "jesse", "dogma", "kix", "tup", "comandante_fox", "noventa_y_nueve", "tech", "hunter", "wrecker",
             "crosshair", "echo_ciborg"],
    "palpatine": ["canciller_palpatine", "darth_sidious"], "dooku": ["conde_dooku"],
    "sith": ["maul", "savage_opress", "asajj_ventress", "madre_talzin", "pong_krell"],
    "grievous": ["general_grievous"],
    "villano": ["cad_bane", "boba_fett", "hondo_ohnaka", "wilhuff_tarkin", "nute_gunray", "wat_tambor",
                "poggle_el_menor", "moralo_eval", "gha_nachkt", "garnac", "whorm_loathsom", "rey_rash", "thrawn"],
    "hutt": ["jabba_el_hutt", "ziro_el_hutt"], "wookiee": ["chewbacca"], "pequeno": ["rotta", "numa"],
    "droide": ["r2d2", "r3s6"], "protocolo": ["c3po", "az3", "tx20"],
    "mortis": ["el_padre", "el_hijo", "la_hija"],
}


def ondulado(tono, ondulacion, ondas, duracion, desfase=0.0, deslizamiento=0.0):
    """Seno puro cuyo tono sube y baja como una onda: `ondulacion` semitonos hacia arriba y hacia
    abajo, `ondas` vueltas durante el sonido. El volumen tiene forma de campana: entra y sale suave."""
    n = int(duracion * MUESTREO)
    fase, muestras = 0.0, []
    for i in range(n):
        x = i / n
        semitonos = ondulacion * math.sin(2 * math.pi * (ondas * x + desfase)) + deslizamiento * x
        fase += 2 * math.pi * tono * 2 ** (semitonos / 12) / MUESTREO     # fase acumulada: sin saltos
        muestras.append(math.sin(fase) * math.sin(math.pi * x) ** 1.5)
    return muestras


def con_eco(muestras, volumen):
    """Suma copias retrasadas y más bajas (ECOS) y deja el pico en `volumen` (1 = -6 dB)."""
    salida = muestras + [0.0] * int(max(r for r, _ in ECOS) * MUESTREO)
    for retraso, ganancia in ECOS:
        d = int(retraso * MUESTREO)
        for i, m in enumerate(muestras):
            salida[i + d] += m * ganancia
    pico = max(abs(m) for m in salida) or 1
    return [m / pico * volumen * 0.5 for m in salida]


def voz(nombre, variante):
    tono, ondulacion, ondas, duracion, volumen = VOCES[nombre]
    rnd = random.Random(f"{nombre}-{variante}")
    return con_eco(ondulado(tono * 2 ** (rnd.uniform(-2, 2) / 12),     # cada variante, un poco más arriba o abajo
                            ondulacion * rnd.uniform(0.8, 1.2), ondas * rnd.uniform(0.8, 1.2),
                            duracion * rnd.uniform(0.9, 1.1),
                            desfase=rnd.random(), deslizamiento=rnd.uniform(-1.0, 1.0)), volumen)


def guardar_wav(ruta, muestras):
    ruta.parent.mkdir(exist_ok=True)
    datos = array.array("h", (int(max(-1.0, min(1.0, m)) * 32767) for m in muestras))
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(MUESTREO)
        w.writeframes(datos.tobytes())


def main():
    claves = set(json.loads((ASSETS / "personajes" / "personajes.json").read_text(encoding="utf-8")))
    asignados = {c: v for v, lista in PERSONAJES.items() for c in lista}
    desconocidos = set(asignados) - claves
    assert not desconocidos, f"personajes que no existen: {sorted(desconocidos)}"

    voces = {}
    for nombre in VOCES:
        voces[nombre] = []
        for n in range(1, VARIANTES + 1):
            guardar_wav(AQUI / "voces" / f"{nombre}_{n}.wav", voz(nombre, n))
            voces[nombre].append(f"voces/{nombre}_{n}.wav")
    # interfaz: un tono corto que baja al mover el cursor y dos que suben al confirmar
    guardar_wav(AQUI / "ui" / "cursor.wav", con_eco(ondulado(880, 0.5, 0.5, 0.045, deslizamiento=-2), 0.35))
    guardar_wav(AQUI / "ui" / "confirmar.wav",
                con_eco(ondulado(660, 0.5, 0.5, 0.08) + ondulado(990, 0.8, 0.8, 0.12), 0.45))

    sonidos = {
        "cada_letras": CADA_LETRAS,
        "narrador": "narrador",
        "por_defecto": "general",
        "personajes": {c: asignados.get(c, "general") for c in sorted(claves)},
        "voces": voces,
        "ui": {"cursor": "ui/cursor.wav", "confirmar": "ui/confirmar.wav"},
    }
    (AQUI / "sonidos.json").write_text(json.dumps(sonidos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(VOCES)} voces x {VARIANTES} variantes, 2 sonidos de interfaz; "
          f"{len(asignados)} personajes con voz propia, {len(claves) - len(asignados)} con la general")


if __name__ == "__main__":
    main()
