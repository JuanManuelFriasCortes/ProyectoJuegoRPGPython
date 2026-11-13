"""Arma escenas.json: para cada ficha del guion, el fondo y quién aparece, dónde y a qué escala.

Uso:  python armar_escenas.py            (genera escenas.json, posiciones.json y las hojas de revisión)
      python armar_escenas.py --lista    (además imprime el reparto de cada ficha, para revisarlo)

Cómo decide el reparto:
  1. El personaje que juega la ficha (línea "Juega:" de Historia.md) siempre aparece, adelante.
  2. Se agregan los personajes que el contexto de la ficha nombra (no las opciones).
  3. AJUSTES corrige a mano lo que el texto no puede saber: quién solo se menciona y no
     está, quién aparece por holograma, quién está tirado en el suelo.
Cómo decide el lugar: cada escenario tiene lugares adelante (x8, pies en y=600, detrás del
cuadro de texto) y atrás (x5 o x6, pies en y=470, completos encima del cuadro).
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ASSETS = Path(__file__).resolve().parent.parent
RAIZ = ASSETS.parent
CARPETA = Path(__file__).resolve().parent
SPRITES = ASSETS / "personajes" / "sprites_1x"
FICHAS_FONDO = json.loads((ASSETS / "escenarios" / "fichas.json").read_text(encoding="utf-8"))

TOPE_CUADRO = 472         # y donde empieza el cuadro de texto (pantalla de 1280x720)
PIES_ADELANTE = 600
PIES_ATRAS = 470
MAX_PERSONAJES = 5

# ----------------------------------------------------------------------
# Nombres en el texto -> clave del sprite
# ----------------------------------------------------------------------
NOMBRES = [
    (r"\bAnakin\b", "anakin_skywalker"), (r"\bAhsoka\b", "ahsoka_tano"), (r"\bObi-Wan\b", "obi_wan_kenobi"),
    (r"\bPadmé\b", "padme_amidala"), (r"\bRex\b", "capitan_rex"), (r"\bFives\b", "fives"), (r"\bEcho\b", "echo"),
    (r"\bCody\b", "comandante_cody"), (r"\bYoda\b", "yoda"), (r"\bMace\b", "mace_windu"), (r"\bPlo\b", "plo_koon"),
    (r"\bKit Fisto\b", "kit_fisto"), (r"\bPalpatine\b|\bCanciller\b", "canciller_palpatine"),
    (r"\bSidious\b", "darth_sidious"), (r"\bDooku\b", "conde_dooku"), (r"\bGrievous\b", "general_grievous"),
    (r"\bMaul\b", "maul"), (r"\bSavage\b", "savage_opress"), (r"\bTalzin\b", "madre_talzin"),
    (r"\bVentress\b", "asajj_ventress"), (r"\bQuinlan\b", "quinlan_vos"), (r"\bBarriss\b", "barriss_offee"),
    (r"\bLuminara\b", "luminara_unduli"), (r"\bBane\b", "cad_bane"), (r"\bAurra Sing\b", "aurra_sing"),
    (r"\bBoba\b", "boba_fett"), (r"\bHondo\b", "hondo_ohnaka"), (r"\bTarkin\b", "wilhuff_tarkin"),
    (r"\bKrell\b", "pong_krell"), (r"\bClovis\b", "rush_clovis"), (r"\bGunray\b", "nute_gunray"),
    (r"\bJabba\b", "jabba_el_hutt"), (r"\bRotta\b", "rotta"), (r"\bZiro\b", "ziro_el_hutt"),
    (r"\b3PO\b|C-3PO", "c3po"), (r"\bR2\b|R2-D2", "r2d2"), (r"\bR3\b|R3-S6", "r3s6"), (r"\bAZ-3\b", "az3"),
    (r"\bTX-20\b", "tx20"), (r"\bLoathsom\b", "whorm_loathsom"), (r"\bTambor\b", "wat_tambor"),
    (r"\bPoggle\b", "poggle_el_menor"), (r"\bKarina\b", "reina_karina"), (r"\bSatine\b", "satine_kryze"),
    (r"\bBo-Katan\b", "bo_katan_kryze"), (r"\bMerrik\b", "tal_merrik"), (r"\bLux\b", "lux_bonteri"),
    (r"\bSaw\b", "saw_gerrera"), (r"\bSteela\b", "steela_gerrera"), (r"\bCham\b", "cham_syndulla"),
    (r"\bNuma\b", "numa"), (r"\bWaxer\b", "waxer"), (r"\bBoil\b", "boil"), (r"\bHevy\b", "hevy"),
    (r"\bAxe\b", "axe"), (r"\bHardcase\b", "hardcase"), (r"\bJesse\b", "jesse"), (r"\bDogma\b", "dogma"),
    (r"\bKix\b", "kix"), (r"\bTup\b", "tup"), (r"\bFox\b", "comandante_fox"), (r"\b99\b", "noventa_y_nueve"),
    (r"\bTech\b", "tech"), (r"\bHunter\b", "hunter"), (r"\bWrecker\b", "wrecker"), (r"\bCrosshair\b", "crosshair"),
    (r"\bKi-Adi\b", "ki_adi_mundi"), (r"\bJocasta\b", "jocasta_nu"), (r"\bPiell\b", "even_piell"),
    (r"\bShaak Ti\b", "shaak_ti"), (r"\bMina\b", "mina_bonteri"), (r"\bMiraj\b", "reina_miraj_scintel"),
    (r"\bMoralo\b", "moralo_eval"), (r"\bLetta\b", "letta_turmond"), (r"\bBail\b", "bail_organa"),
    (r"\bMon Mothma\b", "mon_mothma"), (r"\bNala Se\b", "nala_se"), (r"\bLama Su\b", "lama_su"),
    (r"\bThrawn\b", "thrawn"), (r"\bTrace\b", "trace_martez"), (r"\bRafa\b", "rafa_martez"),
    (r"\bCaleb\b", "caleb_dume"), (r"\bDepa\b", "depa_billaba"), (r"\bGarnac\b", "garnac"),
    (r"\bKalifa\b", "kalifa"), (r"\bChewbacca\b", "chewbacca"), (r"\bGha Nachkt\b", "gha_nachkt"),
    (r"\bTiplar\b", "tiplar"), (r"\bHardeen\b", "rako_hardeen"), (r"\bRash\b", "rey_rash"),
    (r"\bDendup\b", "rey_dendup"),
]
JUEGA = {
    "Anakin": "anakin_skywalker", "Ahsoka": "ahsoka_tano", "Obi-Wan": "obi_wan_kenobi", "Padmé": "padme_amidala",
    "Rex": "capitan_rex", "Fives": "fives", "Waxer": "waxer", "Mace Windu": "mace_windu", "Yoda": "yoda",
    "Asajj Ventress": "asajj_ventress", "Maul": "maul", "Satine Kryze": "satine_kryze", "Conde Dooku": "conde_dooku",
    "Quinlan Vos": "quinlan_vos", "Barriss Offee": "barriss_offee", "Echo": "echo", "Caleb Dume": "caleb_dume",
}
GRANDES = {"jabba_el_hutt", "ziro_el_hutt", "reina_karina"}

# ----------------------------------------------------------------------
# Lugares de cada escenario (x en una pantalla de 1280x720)
# ----------------------------------------------------------------------
POR_DEFECTO = {"adelante": [380, 900, 640], "atras": [190, 1090, 820, 520], "escala_atras": 5}
LUGARES = {
    "oficina_canciller": {"adelante": [300, 980, 760], "atras": [1060, 560, 180]},
    "palacio_hutt": {"adelante": [260, 1030, 440], "atras": [150, 1130], "trono": (640, 532)},
    "consejo_jedi": {"adelante": [640, 380, 900],
                     "atras": [144, 1134, 252, 1026, 428, 852], "pies_atras": [532, 532, 512, 512, 500, 500]},
    "templo_exterior": {"adelante": [250, 1030], "atras": [640, 420, 860], "escala_atras": 6},
    "senado": {"adelante": [380, 900, 180], "atras": [210, 1070, 1180]},
    "kamino": {"adelante": [330, 950, 640], "atras": [150, 1130, 800]},
    "pasillo_separatista": {"adelante": [470, 860, 640], "atras": [1020, 250, 760]},
    "pasillo_republica": {"adelante": [470, 860, 640], "atras": [1020, 250, 760]},
    "mustafar": {"adelante": [330, 980, 660], "atras": [660, 180, 1100], "escala_atras": 6},
    "puente_crucero": {"adelante": [380, 900, 640], "atras": [180, 1100, 520]},
    "cabina": {"adelante": [640, 330, 950], "atras": [190, 1090]},
    "departamento_padme": {"adelante": [430, 820, 1060], "atras": [1000, 250, 640]},
}
ESCALA_ADELANTE = 8

# ----------------------------------------------------------------------
# Correcciones a mano
#   "solo": reparto completo (reemplaza lo detectado)
#   "quitar": personajes que solo se mencionan y no están en la escena
#   "agregar": personajes que están aunque el texto no los nombre
#   "holo": aparecen por holograma      "girado": tirados en el suelo
#   "atras": van en la fila de atrás aunque haya lugar adelante
# ----------------------------------------------------------------------
ANA, AHS, OBI, PAD, PAL = "anakin_skywalker", "ahsoka_tano", "obi_wan_kenobi", "padme_amidala", "canciller_palpatine"
REX, SID, DOO, MACE, YODA = "capitan_rex", "darth_sidious", "conde_dooku", "mace_windu", "yoda"
AJUSTES = {
    # Acto I
    "D001": {"solo": [ANA, OBI, REX]},
    "D002": {"solo": [ANA, AHS, OBI, REX], "atras": [OBI, REX]},
    "D003": {"solo": [ANA, YODA, AHS], "holo": [YODA], "atras": [AHS]},
    "D006": {"solo": [OBI, "whorm_loathsom"]},
    "D008": {"solo": [ANA, PAL], "holo": [PAL]},
    "D009": {"solo": [ANA, REX, AHS]},
    "D010": {"agregar": [AHS]},
    "D011": {"solo": [ANA, AHS, "asajj_ventress", "rotta"], "holo": ["asajj_ventress"]},
    "D012": {"agregar": [REX]},
    "D013": {"quitar": [ANA, AHS]},
    "D015": {"solo": [ANA, AHS, "rotta", PAL], "holo": [PAL]},
    "D016": {"solo": [ANA, AHS, "rotta"]},
    "D017": {"agregar": ["rotta"]},
    "D018": {"solo": [AHS]},
    "D019": {"solo": [PAD, "c3po", "ziro_el_hutt", DOO], "holo": [DOO]},
    "D021": {"quitar": ["jabba_el_hutt"]},
    "D022": {"agregar": [AHS]},
    "D023": {"holo": [PAD]},
    "D025": {"quitar": ["plo_koon"]},
    "D026": {"agregar": [AHS]},
    "D027": {"solo": [AHS]},
    "D029": {"solo": [PAD, "c3po"]},
    "D030": {"solo": [ANA, OBI]},
    "D033": {"solo": [ANA, OBI], "holo": [OBI]},
    "D034": {"solo": [ANA, AHS, "r3s6"]},
    "D035": {"solo": [AHS, "general_grievous"]},
    "D036": {"solo": [ANA, "r3s6"]},
    "D039": {"agregar": ["hevy"]},
    "D040": {"agregar": ["echo", "fives"]},
    "D043": {"quitar": [ANA]},
    "D046": {"atras": ["tx20"]},
    "D052": {"quitar": ["ziro_el_hutt"]},
    "D054": {"quitar": [ANA]},
    "D055": {"quitar": ["ziro_el_hutt"], "holo": [PAL]},
    "D056": {"agregar": [PAD]},
    # Acto II
    "D060": {"solo": [ANA, AHS]},
    "D063": {"agregar": [SID], "holo": [SID]},
    "D064": {"solo": [AHS]},
    "D065": {"solo": [OBI, MACE, YODA]},
    "D067": {"solo": [ANA, PAD, MACE]},
    "D073": {"quitar": ["poggle_el_menor"]},
    "D074": {"solo": [ANA, "luminara_unduli"]},
    "D077": {"quitar": [AHS]},
    "D079": {"holo": [PAL]},
    "D085": {"quitar": ["boba_fett"]},
    "D087": {"quitar": ["kit_fisto"]},
    "D089": {"agregar": ["echo", "hevy"]},
    "D090": {"quitar": ["general_grievous", "asajj_ventress"]},
    "D094": {"solo": [AHS]},
    "D096": {"agregar": [PAD]},
    "D097": {"quitar": [PAD]},
    "D102": {"solo": ["asajj_ventress"]},
    "D103": {"quitar": [DOO], "agregar": [OBI]},
    "D105": {"quitar": [DOO]},
    "D106": {"solo": [ANA]},
    "D107": {"agregar": ["el_padre"]},
    "D108": {"solo": [ANA, "el_hijo", "la_hija", OBI, AHS], "atras": [OBI, AHS]},
    "D109": {"agregar": ["el_padre"]},
    "D110": {"agregar": ["el_hijo"]},
    "D112": {"solo": [ANA, "la_hija", AHS], "girado": [AHS]},
    "D113": {"agregar": ["el_hijo"]},
    "D114": {"agregar": ["el_padre"]},
    "D115": {"agregar": ["el_hijo", "el_padre"]},
    "D116": {"agregar": ["el_padre"]},
    "D117": {"agregar": [AHS, OBI]},
    "D118": {"solo": [ANA, AHS]},
    "D121": {"agregar": [AHS, REX]},
    "D123": {"solo": [ANA, "wilhuff_tarkin", MACE, YODA]},
    "D124": {"quitar": ["kalifa"]},
    "D126": {"quitar": [AHS]},
    # Acto III
    "D127": {"agregar": [REX]},
    "D129": {"quitar": ["pong_krell"], "agregar": ["hardcase", "jesse"]},
    "D131": {"quitar": ["pong_krell"], "agregar": ["fives"]},
    "D133": {"quitar": [DOO]},
    "D134": {"agregar": ["dogma"]},
    "D137": {"agregar": [ANA]},
    "D138": {"solo": [ANA, AHS, REX]},
    "D139": {"agregar": ["reina_miraj_scintel"]},
    "D142": {"agregar": ["reina_miraj_scintel"], "girado": ["reina_miraj_scintel"]},
    "D143": {"agregar": [AHS, REX]},
    "D144": {"agregar": [AHS]},
    "D145": {"agregar": [MACE, YODA]},
    "D146": {"solo": [ANA, OBI], "girado": [OBI]},
    "D147": {"solo": [OBI, YODA, MACE]},
    "D148": {"solo": ["rako_hardeen", "cad_bane", "moralo_eval"]},
    "D150": {"solo": ["rako_hardeen", DOO]},
    "D152": {"quitar": ["rako_hardeen"]},
    "D157": {"quitar": [DOO]},
    "D161": {"quitar": [SID]},
    "D163": {"quitar": ["maul"]},
    # Acto IV
    "D165": {"solo": [ANA, "lux_bonteri", MACE]},
    "D168": {"solo": [AHS, "steela_gerrera"]},
    "D169": {"solo": [ANA, MACE, YODA]},
    "D175": {"holo": ["satine_kryze"]},
    "D177": {"girado": ["satine_kryze"]},
    "D179": {"quitar": ["satine_kryze"]},
    "D181": {"solo": ["maul", "madre_talzin"]},
    "D183": {"quitar": ["asajj_ventress"], "holo": [SID]},
    "D184": {"quitar": ["letta_turmond"]},
    "D187": {"solo": [ANA]},
    "D189": {"solo": [ANA]},
    "D191": {"agregar": [MACE, YODA]},
    "D195": {"agregar": [AHS, "wilhuff_tarkin"]},
    # Acto V
    "D203": {"holo": [PAL], "agregar": ["lama_su"]},
    "D207": {"agregar": [REX]},
    "D208": {"solo": [ANA, REX, "fives"], "girado": ["fives"]},
    "D212": {"solo": [ANA, PAL]},
    "D215": {"quitar": [PAL]},
    "D216": {"quitar": ["kit_fisto"]},
    "D217": {"solo": [OBI, MACE, YODA, "plo_koon"]},
    "D218": {"agregar": [YODA, OBI, "ki_adi_mundi"]},
    "D220": {"agregar": [MACE, OBI]},
    "D221": {"agregar": ["r2d2"]},
    "D223": {"solo": [YODA, SID, DOO, ANA], "holo": [ANA]},
    "D227": {"quitar": [PAL]},
    "D228": {"solo": [MACE, YODA, OBI]},
    "D229": {"quitar": [DOO]},
    "D235": {"solo": [ANA, OBI]},
    "D237": {"quitar": [PAD]},
    "D238": {"quitar": [PAD]},
    "D239": {"quitar": [PAD]},
    "D240": {"agregar": ["thrawn"]},
    "D241": {"solo": [REX, ANA]},
    "D242": {"solo": [ANA, REX, "hunter", "tech", "wrecker"]},
    "D243": {"solo": [REX, "echo_ciborg"]},
    "D244": {"solo": [ANA, "echo_ciborg", "tech"]},
    "D245": {"solo": ["echo_ciborg", REX, "hunter"]},
    "D247": {"quitar": ["maul"], "agregar": ["trace_martez"]},
    "D248": {"quitar": ["maul"]},
    # Acto VI
    "D249": {"quitar": ["maul", "general_grievous", PAL], "agregar": [OBI]},
    "D251": {"agregar": [OBI]},
    "D252": {"solo": [ANA, DOO, PAL, OBI], "atras": [PAL], "girado": [OBI]},
    "D253": {"solo": [ANA, OBI, PAL], "girado": [OBI]},
    "D254": {"solo": [ANA, OBI, PAL]},
    "D256": {"solo": [ANA]},
    "D257": {"quitar": [PAD]},
    "D258": {"agregar": [ANA]},
    "D261": {"agregar": [OBI, MACE, YODA, "ki_adi_mundi"]},
    "D262": {"quitar": [PAL]},
    "D264": {"solo": [ANA, OBI, MACE, YODA]},
    "D266": {"quitar": [PAL]},
    "D267": {"quitar": [SID], "agregar": [REX]},
    "D269": {"solo": [AHS, REX, "maul"], "atras": ["maul"]},
    "D272": {"girado": ["general_grievous"]},
    "D273": {"solo": [ANA, PAL]},
    "D275": {"solo": [ANA]},
    "D278": {"quitar": [MACE]},
    "D280": {"agregar": [SID]},
    "D281": {"agregar": [AHS]},
    "D283": {"quitar": ["fives"]},
    "D287": {"agregar": ["nute_gunray", "wat_tambor", "poggle_el_menor"]},
    "D289": {"holo": [ANA, SID]},
    "D290": {"quitar": [ANA]},
    "D292": {"agregar": [PAD], "atras": [PAD]},
    "D294": {"agregar": [SID]},
    "D295": {"solo": ["darth_vader", SID]},
    "D298": {"solo": [ANA, MACE]},
    "D300": {"agregar": [AHS]},
    "D302": {"quitar": [PAL], "agregar": ["bail_organa", "mon_mothma"]},
    "D303": {"agregar": [YODA, OBI]},
    "D304": {"agregar": [ANA]},
    "D305": {"girado": [SID]},
    "D306": {"quitar": [PAL]},
    "D307": {"quitar": [ANA, PAL]},
    "D310": {"holo": [PAL]},
    "D311": {"quitar": [PAL], "agregar": [ANA]},
    "D312": {"agregar": [ANA]},
}
# en la cámara del Consejo, los maestros que no juegan la ficha van a sus sillones (fila de atrás)
MAESTROS = {MACE, YODA, OBI, "ki_adi_mundi", "plo_koon", "kit_fisto", "shaak_ti"}


def leer_fichas():
    texto = (RAIZ / "Historia.md").read_text(encoding="utf-8")
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)   # la ficha de ejemplo de la cabecera no cuenta
    fichas = {}
    for m in re.finditer(r"^#### (D\d{3}) · (.+?)\n(.*?)(?=^#### |^## |^# |\Z)", texto, re.S | re.M):
        clave, titulo, cuerpo = m.groups()
        juega = re.search(r"\*\*Juega:\*\* ([^·\n]+)", cuerpo).group(1).strip()
        contexto = " ".join(l.strip() for l in cuerpo.splitlines()[1:] if l.strip() and not l.startswith("- **"))
        contexto = re.sub(r"\*\((Si|si) [^)]*\)\*", "", contexto)
        fichas[clave] = (titulo.strip(), juega, contexto)
    return fichas


def detectar(contexto):
    """Personajes nombrados en el contexto, en el orden en que aparecen."""
    encontrados = []
    for patron, clave in NOMBRES:
        m = re.search(patron, contexto)
        if m:
            encontrados.append((m.start(), clave))
    return [c for _, c in sorted(encontrados)]


def alto_visible(clave):
    """Alto en píxeles (a x8) desde la primera fila con dibujo hasta los pies."""
    img = Image.open(SPRITES / f"{clave}.png")
    return (img.height - img.getbbox()[1]) * ESCALA_ADELANTE


def reparto_de(ficha, juega, contexto):
    ajuste = AJUSTES.get(ficha, {})
    if "solo" in ajuste:
        nombres = list(ajuste["solo"])
    else:
        nombres = [juega] + [c for c in detectar(contexto) if c != juega]
        nombres = [n for n in nombres if n not in ajuste.get("quitar", ())]
        nombres += [n for n in ajuste.get("agregar", ()) if n not in nombres]
    vistos = []
    for n in nombres:
        if n not in vistos:
            vistos.append(n)
    return vistos[:MAX_PERSONAJES], ajuste


def acomodar(fondo, juega, nombres, ajuste):
    lugares = {**POR_DEFECTO, **LUGARES.get(fondo, {})}
    adelante, atras = list(lugares["adelante"]), list(lugares["atras"])
    pies_atras = list(lugares.get("pies_atras", [PIES_ATRAS] * len(atras)))
    escala_atras = lugares.get("escala_atras", 5)
    colocados = []
    for clave in nombres:
        extra = {}
        if clave in ajuste.get("holo", ()):
            extra["holograma"] = True
        if clave in ajuste.get("girado", ()):
            extra["girado"] = True
        if clave in GRANDES and "trono" in lugares:
            x, y = lugares["trono"]
            colocados.append({"clave": clave, "x": x, "y_pies": y, "escala": ESCALA_ADELANTE, **extra})
            continue
        quiere_atras = (clave in ajuste.get("atras", ()) or extra.get("girado") or extra.get("holograma")
                        or (fondo == "consejo_jedi" and clave in MAESTROS and clave != juega))
        if adelante and not quiere_atras:
            x = adelante.pop(0)
            alto = alto_visible(clave)
            # los muy chicos (Yoda, droides, Rotta) suben para que se vea más que la cabeza
            y = PIES_ADELANTE if alto >= 220 else TOPE_CUADRO + alto // 4
            colocados.append({"clave": clave, "x": x, "y_pies": y, "escala": ESCALA_ADELANTE, **extra})
        elif atras:
            colocados.append({"clave": clave, "x": atras.pop(0), "y_pies": pies_atras.pop(0),
                              "escala": 6 if extra.get("girado") or extra.get("holograma") else escala_atras,
                              **extra})
    return colocados


def sombra(lienzo, x, y, ancho):
    """Elipse oscura y pixelada (a la resolución del fondo, x4) bajo los pies."""
    capa = Image.new("RGBA", (lienzo.width // 4, lienzo.height // 4), (0, 0, 0, 0))
    cx, cy, rx = x // 4, y // 4, max(3, ancho // 8)
    ImageDraw.Draw(capa).ellipse([cx - rx, cy - 2, cx + rx, cy + 1], fill=(16, 8, 24, 110))
    lienzo.alpha_composite(capa.resize(lienzo.size, Image.NEAREST))


def holograma(sprite):
    """Versión azul y translúcida del sprite: conserva el detalle (tiñe por luminosidad)
    y lleva líneas de barrido cada 8 píxeles."""
    gris = sprite.convert("RGB").convert("L")
    azul = ImageOps.colorize(gris, black=(16, 60, 150), white=(190, 240, 255)).convert("RGBA")
    alfa = sprite.getchannel("A").point(lambda a: a * 215 // 255)
    lineas = Image.new("L", sprite.size, 255)
    d = ImageDraw.Draw(lineas)
    for y in range(0, sprite.height, 8):
        d.rectangle([0, y, sprite.width, y + 1], fill=0)
    azul.putalpha(Image.composite(alfa, alfa.point(lambda a: a * 120 // 255), lineas))
    return azul


def apagar(sprite, brillo=0.55):
    """El sprite más oscuro, sin tocar la transparencia: así se ve quién no está hablando."""
    r, g, b, a = sprite.split()
    r, g, b = (canal.point(lambda v: int(v * brillo)) for canal in (r, g, b))
    return Image.merge("RGBA", (r, g, b, a))


def componer_escena(escena, fondo=None, apagados=()):
    """Fondo de 1280x720 con los personajes de la escena acomodados (sin cuadro de texto).
    `fondo` permite pasar un cuadro del fondo animado en lugar del fondo fijo;
    los personajes de `apagados` salen oscurecidos."""
    if fondo is None:
        fondo = Image.open(ASSETS / "escenarios" / "fondos" / f"{escena['fondo']}.png")
    lienzo = fondo.convert("RGBA")
    for p in sorted(escena["personajes"], key=lambda p: p["y_pies"]):
        s = Image.open(SPRITES / f"{p['clave']}.png").convert("RGBA")
        s = s.resize((s.width * p["escala"], s.height * p["escala"]), Image.NEAREST)
        if p.get("girado"):
            s = s.rotate(90, expand=True)
        caja = s.getbbox()
        if p["clave"] in apagados:
            s = apagar(s)
        if p.get("holograma"):
            s = holograma(s)
        else:
            sombra(lienzo, p["x"], p["y_pies"], caja[2] - caja[0])
        lienzo.alpha_composite(s, (p["x"] - s.width // 2, p["y_pies"] - caja[3]))
    return lienzo


def miniatura(escena):
    """Composición reducida (320x180) para las hojas de revisión, con el lugar del cuadro marcado."""
    lienzo = componer_escena(escena)
    ImageDraw.Draw(lienzo).rectangle([20, TOPE_CUADRO, 1260, 704], fill=(10, 14, 34, 220), outline=(122, 200, 255))
    return lienzo.resize((320, 180), Image.NEAREST)


def hojas_revision(escenas):
    try:
        fuente = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        fuente = ImageFont.load_default()
    actos = [(1, 58), (59, 126), (127, 164), (165, 198), (199, 248), (249, 312)]
    (CARPETA / "revision").mkdir(exist_ok=True)
    for i, (a, b) in enumerate(actos, start=1):
        claves = [f"D{n:03d}" for n in range(a, b + 1)]
        cols = 6
        filas = (len(claves) + cols - 1) // cols
        hoja = Image.new("RGBA", (cols * 320, filas * 196), "#24202e")
        d = ImageDraw.Draw(hoja)
        for k, f in enumerate(claves):
            x, y = (k % cols) * 320, (k // cols) * 196
            hoja.alpha_composite(miniatura(escenas[f]), (x, y))
            d.text((x + 4, y + 182), f"{f} · {escenas[f]['titulo'][:44]}", fill="#f0ecf8", font=fuente)
        hoja.save(CARPETA / "revision" / f"acto_{i}.png")


def main():
    fichas = leer_fichas()
    escenas, posiciones = {}, {}
    for ficha, (titulo, juega_txt, contexto) in fichas.items():
        juega = JUEGA[juega_txt]
        fondo = FICHAS_FONDO[ficha]
        nombres, ajuste = reparto_de(ficha, juega, contexto)
        escenas[ficha] = {"titulo": titulo, "fondo": fondo, "juega": juega,
                          "personajes": acomodar(fondo, juega, nombres, ajuste)}
    for fondo in sorted(set(FICHAS_FONDO.values())):
        lugares = {**POR_DEFECTO, **LUGARES.get(fondo, {})}
        posiciones[fondo] = {
            "adelante": [{"x": x, "y_pies": PIES_ADELANTE, "escala": ESCALA_ADELANTE} for x in lugares["adelante"]],
            "atras": [{"x": x, "y_pies": y, "escala": lugares.get("escala_atras", 5)}
                      for x, y in zip(lugares["atras"], lugares.get("pies_atras", [PIES_ATRAS] * 9))],
            **({"trono": {"x": lugares["trono"][0], "y_pies": lugares["trono"][1], "escala": ESCALA_ADELANTE}}
               if "trono" in lugares else {}),
        }
    (CARPETA / "escenas.json").write_text(json.dumps(escenas, ensure_ascii=False, indent=1), encoding="utf-8")
    (CARPETA / "posiciones.json").write_text(json.dumps(posiciones, ensure_ascii=False, indent=1), encoding="utf-8")
    if "--lista" in sys.argv:
        for f, e in escenas.items():
            gente = ", ".join(p["clave"] + ("(holo)" if p.get("holograma") else "") +
                              ("(suelo)" if p.get("girado") else "") for p in e["personajes"])
            print(f"{f} {e['fondo'][:14]:14} | {gente}")
    hojas_revision(escenas)
    print(f"{len(escenas)} escenas guardadas en {CARPETA}")


if __name__ == "__main__":
    main()
