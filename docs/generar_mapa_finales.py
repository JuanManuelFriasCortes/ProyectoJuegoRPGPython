"""Mapa de los finales: lee Historia.md y genera mapa_finales.html (se abre con doble clic).

Uso:  python generar_mapa_finales.py

Muestra las cuatro líneas que se abren en D273, cómo se pasa de una a otra, qué opciones
necesitan una llave (un medidor o una bandera), cada final con sus variantes y una ruta de
ejemplo para llegar a él. Las rutas de RUTAS se validan contra el guion: si alguien cambia
una ficha y la ruta ya no funciona, el script lo avisa en vez de generar un mapa equivocado.
"""
import datetime
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HISTORIA = AQUI.parent / "Historia.md"
SALIDA = AQUI / "mapa_finales.html"

# carril de cada ficha desde la revelación (D273); el orden es el de izquierda a derecha en el mapa
CARRILES = [
    {"id": "emperador", "nombre": "Emperador", "desde": 305, "hasta": 308,
     "momentos": ["Matas a Palpatine", "La Orden 66 por tu mano", "Padmé decide"]},
    {"id": "oscura", "nombre": "Oscura · canon", "desde": 273, "hasta": 295,
     "momentos": ["Le cortas la mano a Mace", "Te arrodillas ante Sidious", "Orden 66 y Mustafar"]},
    {"id": "luz", "nombre": "Luz", "desde": 296, "hasta": 304,
     "momentos": ["Te niegas o dudas", "Enfrentas a Sidious", "Detener la Orden 66"]},
    {"id": "exilio", "nombre": "Exilio", "desde": 309, "hasta": 312,
     "momentos": ["Huyes con Padmé", "La llamada de Obi-Wan", "Los gemelos"]},
]
CARRIL_FINAL = {"FINAL 1": "oscura", "FINAL 2": "oscura", "FINAL 3": "emperador", "FINAL 4": "luz",
                "FINAL 5": "luz", "FINAL 6": "exilio", "FP5": "luz"}

# una ruta de ejemplo por final: (ficha, opción) hasta llegar; se valida contra el guion
CANON_HASTA_D278 = [("D273", "A"), ("D274", "A"), ("D275", "A"), ("D277", "A"), ("D278", "A")]
ORDEN_66 = [("D279", "A"), ("D281", "A"), ("D282", "A"), ("D283", "A"), ("D284", "A")]
RUTAS = {
    "FINAL 1": {"pasos": CANON_HASTA_D278 + ORDEN_66 + [
        ("D285", "A"), ("D286", "A"), ("D287", "A"), ("D289", "A"), ("D290", "A"), ("D291", "A"),
        ("D292", "A"), ("D293", "A"), ("D295", "A")],
        "otras": "Es el camino del canon: la opción ★ en cada ficha."},
    "FINAL 2": {"pasos": CANON_HASTA_D278 + ORDEN_66 + [
        ("D285", "A"), ("D286", "A"), ("D287", "A"), ("D289", "A"), ("D290", "A"), ("D291", "A"),
        ("D292", "A"), ("D293", "B"), ("D294", "B")],
        "otras": "También se llega si Padmé no va a Mustafar (D290 B o C)."},
    "FINAL 3": {"pasos": [("D273", "B"), ("D305", "A"), ("D306", "A"), ("D307", "A")],
                "otras": "También fingiendo lealtad para matarlo después (D278 C). Al final, Padmé se queda "
                         "contigo (D307 A) o la arrestas (D308 A). Si renuncias al poder por ella (D308 B), "
                         "te vas al exilio; si te entregas al Consejo (D305 B), pasas a la luz."},
    "FINAL 4": {"pasos": CANON_HASTA_D278 + [
        ("D279", "B"), ("D280", "B"), ("D296", "A"), ("D297", "B"), ("D298", "B"), ("D300", "A"),
        ("D301", "A"), ("D302", "A"), ("D303", "A"), ("D304", "A")],
        "otras": "Otras entradas a la luz: negarte a arrodillarte (D278 B), no poder hacerlo en el Templo "
                 "(D285 B), bajar el sable ante Obi-Wan (D293 C) o dejar que Mace se encargue de Sidious "
                 "(D275 B, D277 B o C). En vez de cortar la transmisión en D298, puedes defender el Templo "
                 "con el 501.° (D299 B). Sin alguna de esas dos, en D304 solo queda el Final 5. Otra vía: "
                 "si matas a Palpatine en D273 y luego te entregas al Consejo (D305 B), la Orden 66 nunca "
                 "se da y también cuenta."},
    "FINAL 5": {"pasos": CANON_HASTA_D278 + ORDEN_66 + [
        ("D285", "B"), ("D296", "A"), ("D297", "B"), ("D298", "A"), ("D299", "C"), ("D300", "A"),
        ("D301", "A"), ("D302", "A"), ("D303", "A"), ("D304", "B")],
        "otras": "Sirve cualquier entrada a la luz. Lo que define este final es no detener la Orden 66 ni "
                 "salvar el Templo: en D304 solo aparece la opción B."},
    "FINAL 6": {"pasos": [("D273", "A"), ("D274", "A"), ("D275", "C"), ("D276", "B"), ("D309", "A"),
                          ("D310", "A"), ("D311", "B"), ("D312", "A")],
                "otras": "Otras salidas al exilio: D273 C, la plataforma de Mustafar (D291 B), huir en vez de "
                         "enfrentar a Sidious (D296 B) o renunciar al trono (D308 B). Ojo: si contestas la "
                         "llamada de Obi-Wan (D310 B) vuelves a la línea oscura, y si Padmé te pide volver a "
                         "ayudar (D311 A) pasas a la luz."},
    "FP5": {"pasos": CANON_HASTA_D278 + [("D279", "B"), ("D280", "B"), ("D296", "A"), ("D297", "C")],
            "otras": "Se llega desde la línea de la luz, al enfrentar a Sidious."},
}


def limpiar(texto):
    """Quita el formato de Markdown (asteriscos) y espacios de sobra."""
    return re.sub(r"\s+", " ", texto.replace("**", "").replace("*", "")).strip()


def leer_opcion(letra, linea):
    condiciones = re.findall(r"\*\(((?:si|requiere) [^)]*)\)\*", linea)
    antes, _, despues = linea.partition("→")
    texto = limpiar(re.sub(r"\*\((?:si|requiere) [^)]*\)\*", "", antes).replace("★", ""))
    m = re.match(r"\s*(D\d{3}|FINAL \d|FP\d)\s*(.*)", despues)
    destino, resto = (m.group(1), m.group(2)) if m else ("", despues)
    notas = [limpiar(n) for n in re.findall(r"\*\(([^)]*)\)\*", resto)]
    resto = re.sub(r"\*\([^)]*\)\*", "", resto)
    efectos = [limpiar(e) for e in resto.split("·") if limpiar(e)]
    return {"letra": letra, "texto": texto, "canon": "★" in linea, "condicion": " · ".join(condiciones),
            "destino": destino, "efectos": efectos, "nota": " ".join(notas)}


def leer_historia():
    texto = re.sub(r"```.*?```", "", HISTORIA.read_text(encoding="utf-8"), flags=re.S)
    fichas = {}
    for m in re.finditer(r"^#### (D\d{3}) · (.+?)\n(.*?)(?=^#### |^## |^# |\Z)", texto, re.S | re.M):
        cuerpo = m.group(3)
        juega = re.search(r"\*\*Juega:\*\* ([^·\n]+)", cuerpo)
        fichas[m.group(1)] = {
            "id": m.group(1), "titulo": limpiar(m.group(2)), "juega": juega.group(1).strip() if juega else "",
            "opciones": [leer_opcion(l, resto) for l, resto in re.findall(r"^- \*\*([A-F])\)\*\* (.+)$", cuerpo, re.M)],
        }
    finales = {}
    for m in re.finditer(r"^### (FINAL \d|FP\d) · (.+?)\n(.*?)(?=^### |^## |^# |\Z)", texto, re.S | re.M):
        clave, cuerpo = m.group(1), m.group(3)
        llega = re.search(r"\*\*Se llega por:\*\* (.+)", cuerpo)
        lineas = [l.strip() for l in cuerpo.splitlines() if l.strip()]
        parrafos = [limpiar(l) for l in lineas if not l.startswith(("**", "- "))]
        finales[clave] = {
            "id": clave, "nombre": limpiar(re.sub(r"\*\(canon\)\*", "", m.group(2))),
            "canon": "(canon)" in m.group(2), "carril": CARRIL_FINAL.get(clave, "prematuro"),
            "llega": limpiar(llega.group(1)) if llega else "", "texto": " ".join(parrafos),
            "variantes": [limpiar(l[2:]) for l in lineas if l.startswith("- ")],
        }
    return fichas, finales


def carril_de(ficha_id):
    n = int(ficha_id[1:])
    return next(c["id"] for c in CARRILES if c["desde"] <= n <= c["hasta"])


def validar_rutas(fichas):
    """Cada paso debe existir y llevar a la ficha del paso siguiente (o al final de la ruta)."""
    for final, ruta in RUTAS.items():
        pasos = ruta["pasos"]
        for i, (ficha, letra) in enumerate(pasos):
            opcion = next((o for o in fichas[ficha]["opciones"] if o["letra"] == letra), None)
            assert opcion, f"{final}: {ficha} no tiene opción {letra}"
            esperado = pasos[i + 1][0] if i + 1 < len(pasos) else final
            assert opcion["destino"] == esperado, \
                f"{final}: {ficha} {letra} lleva a {opcion['destino']}, la ruta esperaba {esperado}"


def main():
    fichas, finales = leer_historia()
    validar_rutas(fichas)
    desde, hasta = CARRILES[1]["desde"], max(c["hasta"] for c in CARRILES)
    mapa = {f"D{n:03d}": dict(fichas[f"D{n:03d}"], carril=carril_de(f"D{n:03d}")) for n in range(desde, hasta + 1)}
    # de dónde salen los finales prematuros que no están después de D273
    for ficha in fichas.values():
        for o in ficha["opciones"]:
            if o["destino"].startswith("FP") and o["destino"] in finales:
                finales[o["destino"]].setdefault("desde", []).append(
                    {"ficha": ficha["id"], "titulo": ficha["titulo"], "letra": o["letra"], "texto": o["texto"]})
    datos = {
        "generado": datetime.date.today().isoformat(),
        "carriles": [{k: c[k] for k in ("id", "nombre", "momentos")} | {"rango": f"D{c['desde']}–D{c['hasta']}",
                      "fichas": c["hasta"] - c["desde"] + 1} for c in CARRILES],
        "fichas": mapa, "finales": finales,
        "rutas": {k: {"pasos": v["pasos"], "otras": v["otras"]} for k, v in RUTAS.items()},
    }
    incrustado = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    SALIDA.write_text(PLANTILLA.replace("__DATOS__", incrustado), encoding="utf-8")
    llaves = sum(1 for f in mapa.values() for o in f["opciones"] if o["condicion"])
    print(f"{SALIDA.name}: {len(mapa)} fichas (D{desde}–D{hasta}), {len(finales)} finales, "
          f"{llaves} opciones con llave, {len(RUTAS)} rutas validadas")


PLANTILLA = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapa de finales</title>
<style>
:root {
  --fondo: #f4f3ef; --superficie: #ffffff; --superficie-2: #f8f7f3; --tinta: #1c1d24; --tenue: #5f606d;
  --linea: #dad7cf; --oscura: #b42318; --luz: #175cd3; --emperador: #7a2fbf; --exilio: #067a55;
  --prematuro: #6b6b6b; --llave: #8a5a00; --llave-fondo: #fff1cc; --marca: rgba(23, 92, 211, .08);
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-tema="claro"]) {
    --fondo: #0d0f15; --superficie: #161922; --superficie-2: #1b1f2a; --tinta: #e8e9ef; --tenue: #a3a6b8;
    --linea: #2b2f3d; --oscura: #ff6b5b; --luz: #6aa9ff; --emperador: #c49bff; --exilio: #3fd09a;
    --prematuro: #a0a0a0; --llave: #f2c14e; --llave-fondo: #3a2f10; --marca: rgba(106, 169, 255, .10);
    color-scheme: dark;
  }
}
:root[data-tema="oscuro"] {
  --fondo: #0d0f15; --superficie: #161922; --superficie-2: #1b1f2a; --tinta: #e8e9ef; --tenue: #a3a6b8;
  --linea: #2b2f3d; --oscura: #ff6b5b; --luz: #6aa9ff; --emperador: #c49bff; --exilio: #3fd09a;
  --prematuro: #a0a0a0; --llave: #f2c14e; --llave-fondo: #3a2f10; --marca: rgba(106, 169, 255, .10);
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--fondo); color: var(--tinta);
  font: 15px/1.5 system-ui, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; }
main { max-width: 1240px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 28px; margin: 0 0 4px; letter-spacing: -.01em; }
h2 { font-size: 20px; margin: 40px 0 6px; }
p.sub, .tenue { color: var(--tenue); }
p.sub { margin: 0 0 16px; max-width: 760px; }
header { display: flex; gap: 16px; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; }
button { font: inherit; color: inherit; cursor: pointer; }
.tema { border: 1px solid var(--linea); background: var(--superficie); border-radius: 8px; padding: 6px 12px; }
.leyenda { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 13px; color: var(--tenue); margin: 8px 0 0; }
.leyenda span { display: inline-flex; align-items: center; gap: 6px; }
.punto { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.c-emperador { --c: var(--emperador); } .c-oscura { --c: var(--oscura); } .c-luz { --c: var(--luz); }
.c-exilio { --c: var(--exilio); } .c-prematuro { --c: var(--prematuro); }
.llave { display: inline-block; font-size: 12px; line-height: 1.3; color: var(--llave); background: var(--llave-fondo);
  border-radius: 6px; padding: 1px 7px; font-weight: 600; }
.marco { background: var(--superficie); border: 1px solid var(--linea); border-radius: 12px; padding: 12px;
  overflow-x: auto; }
svg text { fill: var(--tinta); font-family: system-ui, "Segoe UI", Roboto, sans-serif; }
svg .tenue { fill: var(--tenue); }
svg .halo { paint-order: stroke; stroke: var(--superficie); stroke-width: 4px; stroke-linejoin: round; }
svg .fin { cursor: pointer; }
svg .fin:hover rect { stroke-width: 2.5; }
/* finales */
.finales { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 12px; }
.final { background: var(--superficie); border: 1px solid var(--linea); border-top: 4px solid var(--c);
  border-radius: 12px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; }
.final h3 { margin: 0; font-size: 17px; }
.final .etiqueta { font-size: 12px; font-weight: 700; color: var(--c); text-transform: uppercase; letter-spacing: .04em; }
.final p { margin: 0; }
.final ul { margin: 0; padding-left: 18px; font-size: 13.5px; color: var(--tenue); }
.final .ver { align-self: flex-start; border: 1px solid var(--c); color: var(--c); background: transparent;
  border-radius: 8px; padding: 5px 12px; font-weight: 600; }
.final .ver:hover { background: var(--marca); }
.final.activo { box-shadow: 0 0 0 2px var(--c); }
.prematuros { width: 100%; border-collapse: collapse; background: var(--superficie); border-radius: 12px;
  overflow: hidden; border: 1px solid var(--linea); font-size: 14px; }
.prematuros th, .prematuros td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--linea); vertical-align: top; }
.prematuros th { background: var(--superficie-2); font-size: 13px; color: var(--tenue); }
/* explorador */
.filtros { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 12px; align-items: center; }
.filtros button { border: 1px solid var(--linea); background: var(--superficie); border-radius: 999px; padding: 4px 12px;
  font-size: 13px; }
.filtros button.activo { border-color: var(--c, var(--tinta)); color: var(--c, var(--tinta)); font-weight: 700;
  box-shadow: inset 0 0 0 1px var(--c, var(--tinta)); }
.ruta { background: var(--superficie); border: 1px solid var(--linea); border-radius: 12px; padding: 12px 14px;
  margin-bottom: 14px; display: none; }
.ruta.visible { display: block; }
.ruta .pasos { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin: 6px 0; }
.ruta .paso { font-size: 13px; border: 1px solid var(--linea); border-radius: 6px; padding: 2px 8px; background: var(--superficie-2);
  text-decoration: none; color: var(--tinta); }
.ruta .paso.con-llave { border-color: var(--llave); background: var(--llave-fondo); color: var(--llave); font-weight: 700; }
.ruta .flecha { color: var(--tenue); font-size: 12px; }
.carriles { display: grid; grid-template-columns: repeat(4, minmax(250px, 1fr)); gap: 12px; align-items: start; }
.carril > h3 { margin: 0 0 8px; font-size: 15px; color: var(--c); border-bottom: 3px solid var(--c); padding-bottom: 4px; }
.ficha { background: var(--superficie); border: 1px solid var(--linea); border-left: 4px solid var(--c); border-radius: 10px;
  padding: 10px 12px; margin-bottom: 10px; transition: opacity .2s, box-shadow .2s; scroll-margin-top: 80px; }
.ficha h4 { margin: 0; font-size: 14.5px; }
.ficha .juega { font-size: 12px; color: var(--tenue); margin-bottom: 6px; }
.opcion { display: grid; grid-template-columns: 22px 1fr; gap: 2px 6px; font-size: 13.5px; padding: 5px 6px;
  border-radius: 6px; transition: opacity .2s, background .2s; }
.opcion + .opcion { border-top: 1px dashed var(--linea); }
.opcion .letra { font-weight: 800; color: var(--tenue); }
.opcion .estrella { color: var(--llave); margin-left: 3px; }
.opcion .detalle { display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: center; grid-column: 2; font-size: 12.5px; }
.opcion .efectos { color: var(--tenue); }
.destino { font-weight: 700; text-decoration: none; color: var(--c); border: 1px solid var(--c); border-radius: 6px;
  padding: 0 6px; font-size: 12px; white-space: nowrap; }
.destino:hover { background: var(--marca); }
.atenuada { opacity: .28; }
.en-ruta { box-shadow: 0 0 0 2px var(--c); }
.opcion.elegida { background: var(--marca); }
.opcion.elegida .letra { color: var(--c); }
.destello { animation: destello 1.2s ease-out; }
@keyframes destello { 0% { box-shadow: 0 0 0 4px var(--c); } 100% { box-shadow: 0 0 0 0 transparent; } }
footer { margin-top: 48px; font-size: 13px; color: var(--tenue); }
@media (max-width: 900px) { .carriles { grid-template-columns: 1fr; } h1 { font-size: 24px; } }
@media (prefers-reduced-motion: reduce) { .destello { animation: none; } * { transition: none !important; } }
</style>
</head>
<body>
<main>
<header>
  <div>
    <h1>Mapa de los finales</h1>
    <p class="sub">Desde <b>D273</b>, cuando Palpatine revela que es Sith, la historia se parte en cuatro líneas.
    Los <b>puntos y banderas</b> no eligen el final: abren opciones (llaves). El final lo decide el camino que tomas.</p>
  </div>
  <button class="tema" id="tema" type="button">Cambiar tema</button>
</header>
<div class="leyenda">
  <span><i class="punto" style="background:var(--emperador)"></i>Emperador</span>
  <span><i class="punto" style="background:var(--oscura)"></i>Oscura (canon)</span>
  <span><i class="punto" style="background:var(--luz)"></i>Luz</span>
  <span><i class="punto" style="background:var(--exilio)"></i>Exilio</span>
  <span>★ opción del canon</span>
  <span><span class="llave">llave</span> solo aparece si tienes ese medidor o esa bandera</span>
  <span><b>D278 B</b> = ficha D278, opción B</span>
</div>

<h2>Las cuatro líneas</h2>
<p class="sub">Las flechas entre líneas son las decisiones que te cambian de camino. En dorado, las que necesitan llave.
Toca un final para ver una ruta que llega a él.</p>
<div class="marco"><svg id="mapa" viewBox="0 0 1070 620" role="img" aria-label="Mapa de las cuatro líneas y los finales"></svg></div>

<h2>Los finales</h2>
<div class="finales" id="finales"></div>

<h2>Finales prematuros</h2>
<p class="sub">Derrotas que cortan la partida antes de tiempo, por decisiones extremas.</p>
<table class="prematuros" id="prematuros"><thead><tr><th>Final</th><th>Dónde</th><th>Qué pasa</th></tr></thead><tbody></tbody></table>

<h2 id="explorador">Ficha por ficha</h2>
<p class="sub">Todas las fichas desde D273, con cada opción, su llave y a dónde lleva. Toca un destino para saltar a él.</p>
<div class="filtros" id="filtros"><span class="tenue">Ver ruta a:</span></div>
<div class="ruta" id="ruta"></div>
<div class="carriles" id="carriles"></div>

<footer id="pie"></footer>
</main>

<script type="application/json" id="datos">__DATOS__</script>
<script>
"use strict";
const D = JSON.parse(document.getElementById("datos").textContent);
const SVG = "http://www.w3.org/2000/svg";
const CARRIL = Object.fromEntries(D.carriles.map((c, i) => [c.id, Object.assign({ i }, c)]));
const carrilDe = (dest) => D.fichas[dest] ? D.fichas[dest].carril : (D.finales[dest] ? D.finales[dest].carril : null);

// ---------- tema ----------
(function () {
  const raiz = document.documentElement;
  try { const t = localStorage.getItem("mapa-tema"); if (t) raiz.dataset.tema = t; } catch (e) {}
  document.getElementById("tema").addEventListener("click", () => {
    const oscuroAhora = getComputedStyle(raiz).colorScheme.includes("dark");
    raiz.dataset.tema = oscuroAhora ? "claro" : "oscuro";
    try { localStorage.setItem("mapa-tema", raiz.dataset.tema); } catch (e) {}
  });
})();

// ---------- utilidades ----------
function el(etiqueta, atributos, ...hijos) {
  const n = document.createElement(etiqueta);
  for (const [k, v] of Object.entries(atributos || {})) {
    if (k === "class") n.className = v; else if (k.startsWith("on")) n.addEventListener(k.slice(2), v); else n.setAttribute(k, v);
  }
  for (const h of hijos) if (h != null) n.append(h);
  return n;
}
function s(etiqueta, atributos, texto) {
  const n = document.createElementNS(SVG, etiqueta);
  for (const [k, v] of Object.entries(atributos || {})) n.setAttribute(k, v);
  if (texto != null) n.textContent = texto;
  return n;
}
function color(id) { return `var(--${id})`; }
function enlaceDestino(dest) {
  const carril = carrilDe(dest) || "prematuro";
  const href = D.fichas[dest] ? `#f-${dest}` : `#final-${dest.replace(" ", "-")}`;
  return el("a", { class: `destino c-${carril}`, href, onclick: (e) => { e.preventDefault(); irA(href.slice(1)); } }, `→ ${dest}`);
}
function irA(id) {
  const n = document.getElementById(id);
  if (!n) return;
  n.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
  n.classList.remove("destello"); void n.offsetWidth; n.classList.add("destello");
}

// ---------- mapa general (SVG) ----------
function dibujarMapa() {
  const svg = document.getElementById("mapa");
  const X0 = 30, ANCHO = 170, PASO = 280, ARRIBA = 140, ABAJO = 470;
  const xIzq = (id) => X0 + CARRIL[id].i * PASO, xCen = (id) => xIzq(id) + ANCHO / 2, xDer = (id) => xIzq(id) + ANCHO;
  const defs = s("defs");
  for (const id of ["emperador", "oscura", "luz", "exilio", "llave"]) {
    const m = s("marker", { id: `pt-${id}`, viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" });
    m.append(s("path", { d: "M0,0 L10,5 L0,10 z", style: `fill:${color(id)}` }));
    defs.append(m);
  }
  svg.append(defs);
  const linea = (d, id, punteada) => {
    svg.append(s("path", { d, fill: "none", style: "stroke:var(--superficie)", "stroke-width": 7 }));
    svg.append(s("path", { d, fill: "none", style: `stroke:${color(id)}`, "stroke-width": 2.2,
      "stroke-dasharray": punteada ? "6 4" : "none", "marker-end": `url(#pt-${id})` }));
  };
  // las etiquetas llevan un rectángulo de fondo: así las líneas no se asoman entre palabra y palabra
  const conFondo = (t) => {
    svg.append(t);
    const b = t.getBBox();
    svg.insertBefore(s("rect", { x: b.x - 4, y: b.y - 1, width: b.width + 8, height: b.height + 2, rx: 4,
      style: "fill:var(--superficie)" }), t);
  };
  const texto = (x, y, t, extra) => conFondo(s("text", Object.assign({ x, y, "font-size": 12, "text-anchor": "middle" }, extra || {}), t));
  // etiqueta de una lista de opciones: dos por renglón, las de llave en dorado
  const etiquetaOpciones = (x, yAbajo, lista) => {
    const renglones = [];
    for (let i = 0; i < lista.length; i += 2) renglones.push(lista.slice(i, i + 2));
    renglones.forEach((r, k) => {
      const t = s("text", { x, y: yAbajo - (renglones.length - 1 - k) * 15, "font-size": 12, "text-anchor": "middle" });
      r.forEach((o, j) => {
        if (j) t.append(s("tspan", { class: "tenue" }, " · "));
        t.append(s("tspan", o.llave ? { style: "fill:var(--llave);font-weight:700" } : {}, o.id));
      });
      conFondo(t);
    });
  };

  // carriles
  for (const c of D.carriles) {
    const x = xIzq(c.id);
    svg.append(s("rect", { x, y: ARRIBA, width: ANCHO, height: ABAJO - ARRIBA, rx: 12,
      style: `fill:var(--superficie-2);stroke:${color(c.id)}`, "stroke-width": 2 }));
    svg.append(s("rect", { x, y: ARRIBA, width: ANCHO, height: 6, rx: 3, style: `fill:${color(c.id)}` }));
    svg.append(s("text", { x: x + 12, y: ARRIBA + 30, "font-size": 16, "font-weight": 700, style: `fill:${color(c.id)}` }, c.nombre));
    svg.append(s("text", { x: x + 12, y: ARRIBA + 48, "font-size": 12, class: "tenue" }, `${c.rango} · ${c.fichas} fichas`));
    c.momentos.forEach((m, k) => svg.append(s("text", { x: x + 12, y: ARRIBA + 78 + k * 20, "font-size": 12.5 }, `${k + 1}. ${m}`)));
  }
  // finales dentro de cada carril
  const finalesPorCarril = {};
  for (const f of Object.values(D.finales)) if (CARRIL[f.carril]) (finalesPorCarril[f.carril] = finalesPorCarril[f.carril] || []).push(f);
  for (const [carril, lista] of Object.entries(finalesPorCarril)) {
    const grandes = lista.filter((f) => f.id.startsWith("FINAL")), chicos = lista.filter((f) => f.id.startsWith("FP"));
    const ancho = (ANCHO - 16 - (grandes.length - 1) * 8) / grandes.length;
    grandes.forEach((f, k) => cajaFinal(f, xIzq(carril) + 8 + k * (ancho + 8), 390, ancho, 66));
    chicos.forEach((f) => cajaFinal(f, xIzq(carril) + 8, 352, ANCHO - 16, 28));
  }
  function cajaFinal(f, x, y, ancho, alto) {
    const g = s("g", { class: "fin", tabindex: 0, role: "button", "aria-label": `${f.id}: ${f.nombre}` });
    g.addEventListener("click", () => elegirRuta(f.id, true));
    g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); elegirRuta(f.id, true); } });
    g.append(s("rect", { x, y, width: ancho, height: alto, rx: 8, style: `fill:var(--superficie);stroke:${color(f.carril)}`, "stroke-width": 1.5 }));
    if (alto < 40) {
      g.append(s("text", { x: x + ancho / 2, y: y + 18, "font-size": 11.5, "text-anchor": "middle" }, `${f.id} · ${f.nombre}`));
    } else {
      g.append(s("text", { x: x + ancho / 2, y: y + 20, "font-size": 12, "font-weight": 800, "text-anchor": "middle", style: `fill:${color(f.carril)}` }, f.id));
      partir(f.nombre, 13).forEach((r, k) => g.append(s("text", { x: x + ancho / 2, y: y + 38 + k * 14, "font-size": 11.5, "text-anchor": "middle" }, r)));
    }
    svg.append(g);
  }

  // salidas de D273
  const d273 = D.fichas.D273, xo = xCen("oscura");
  svg.append(s("rect", { x: xo - 110, y: 16, width: 220, height: 56, rx: 10, style: "fill:var(--superficie);stroke:var(--tinta)", "stroke-width": 1.5 }));
  svg.append(s("text", { x: xo, y: 38, "font-size": 14, "font-weight": 800, "text-anchor": "middle" }, "D273 · La revelación"));
  svg.append(s("text", { x: xo, y: 58, "font-size": 12, "text-anchor": "middle", class: "tenue" }, "Palpatine confiesa que es Sith"));
  for (const o of d273.opciones) {
    const c = carrilDe(o.destino), xd = xCen(c);
    const desde = c === "oscura" ? xo : (xd < xo ? xo - 70 : xo + 70);
    const d = c === "oscura" ? `M${xo},72 L${xo},${ARRIBA - 4}` : `M${desde},72 C${desde},110 ${xd},96 ${xd},${ARRIBA - 4}`;
    linea(d, c);
    const etiqueta = `${o.letra}${o.canon ? " ★" : ""} · ${o.condicion ? o.condicion.replace("requiere ", "") : "sin llave"}`;
    const xt = c === "oscura" ? xo + 8 : (xd + desde) / 2, anchor = c === "oscura" ? "start" : "middle";
    texto(xt, c === "oscura" ? 112 : 102, etiqueta, o.condicion ? { "text-anchor": anchor, style: "fill:var(--llave);font-weight:700" } : { "text-anchor": anchor });
  }

  // cambios de carril (sin contar D273)
  const pares = {};
  for (const f of Object.values(D.fichas)) {
    if (f.id === "D273") continue;
    for (const o of f.opciones) {
      const c = carrilDe(o.destino);
      if (c && CARRIL[c] && c !== f.carril) (pares[`${f.carril}>${c}`] = pares[`${f.carril}>${c}`] || []).push({ id: `${f.id} ${o.letra}`, llave: !!o.condicion });
    }
  }
  // vecinos: flecha horizontal en el hueco entre carriles; lejanos: arco por debajo
  const ALTURA_HUECO = { "oscura>emperador": 300, "oscura>luz": 330, "luz>exilio": 262, "exilio>luz": 345 };
  const ARCOS = { "exilio>oscura": [500, -30, 30], "oscura>exilio": [530, -10, 0], "emperador>luz": [560, 30, 0], "emperador>exilio": [590, -10, 30] };
  for (const [par, lista] of Object.entries(pares)) {
    const [a, b] = par.split(">"), destinoColor = b;
    if (Math.abs(CARRIL[a].i - CARRIL[b].i) === 1) {
      const y = ALTURA_HUECO[par] || 300, izqADer = CARRIL[a].i < CARRIL[b].i;
      const x1 = izqADer ? xDer(a) : xIzq(a), x2 = izqADer ? xIzq(b) : xDer(b);
      linea(`M${x1},${y} L${x2 + (izqADer ? -3 : 3)},${y}`, destinoColor);
      etiquetaOpciones((x1 + x2) / 2, y - 8, lista);
    } else {
      const [prof, dxa, dxb] = ARCOS[par] || [600, 0, 0];
      const x1 = xCen(a) + dxa, x2 = xCen(b) + dxb;
      linea(`M${x1},${ABAJO} L${x1},${prof - 8} Q${x1},${prof} ${x1 + Math.sign(x2 - x1) * 8},${prof} L${x2 - Math.sign(x2 - x1) * 8},${prof} Q${x2},${prof} ${x2},${prof - 8} L${x2},${ABAJO + 4}`, destinoColor, true);
      const xs = { "exilio>oscura": 800, "oscura>exilio": 830, "emperador>luz": 255, "emperador>exilio": 520 }[par] || (x1 + x2) / 2;
      etiquetaOpciones(xs, prof - 5, lista);
    }
  }
}
function partir(texto, max) {
  const renglones = [];
  let actual = "";
  for (const palabra of texto.split(" ")) {
    if ((actual + " " + palabra).trim().length > max && actual) { renglones.push(actual); actual = palabra; }
    else actual = (actual + " " + palabra).trim();
  }
  if (actual) renglones.push(actual);
  return renglones.slice(0, 2);
}

// ---------- tarjetas de finales ----------
function dibujarFinales() {
  const caja = document.getElementById("finales");
  for (const f of Object.values(D.finales)) {
    if (!f.id.startsWith("FINAL") && f.id !== "FP5") continue;
    const ruta = D.rutas[f.id];
    const linea = f.carril === "prematuro" ? "Final prematuro" : `Línea ${CARRIL[f.carril].nombre.split(" · ")[0].toLowerCase()}`;
    caja.append(el("article", { class: `final c-${f.carril}`, id: `final-${f.id.replace(" ", "-")}` },
      el("div", { class: "etiqueta" }, `${f.id} · ${linea}${f.canon ? " · canon" : ""}`),
      el("h3", {}, f.nombre),
      el("p", {}, f.texto || f.llega),
      ruta ? el("p", { class: "tenue" }, el("b", {}, "Cómo llegar: "), ruta.otras) : null,
      f.variantes.length ? el("ul", {}, ...f.variantes.map((v) => el("li", {}, v))) : null,
      ruta ? el("button", { class: "ver", type: "button", onclick: () => elegirRuta(f.id, true) }, "Ver la ruta ficha por ficha") : null));
  }
  const cuerpo = document.querySelector("#prematuros tbody");
  for (const f of Object.values(D.finales)) {
    if (!f.id.startsWith("FP")) continue;
    const desde = (f.desde || []).map((o) => `${o.ficha} ${o.letra} (${o.titulo})`).join(", ");
    cuerpo.append(el("tr", { id: `final-${f.id}` }, el("td", {}, el("b", {}, f.id), ` · ${f.nombre}`), el("td", {}, desde), el("td", {}, f.llega)));
  }
}

// ---------- explorador ficha por ficha ----------
function dibujarCarriles() {
  const caja = document.getElementById("carriles");
  for (const c of D.carriles) {
    const col = el("section", { class: `carril c-${c.id}` }, el("h3", {}, `${c.nombre} · ${c.rango}`));
    for (const f of Object.values(D.fichas).filter((x) => x.carril === c.id)) {
      const tarjeta = el("article", { class: `ficha c-${c.id}`, id: `f-${f.id}`, "data-ficha": f.id },
        el("h4", {}, `${f.id} · ${f.titulo}`), el("div", { class: "juega" }, `Juega: ${f.juega}`));
      for (const o of f.opciones) {
        const detalle = el("div", { class: "detalle" },
          o.condicion ? el("span", { class: "llave" }, o.condicion) : null,
          o.efectos.length ? el("span", { class: "efectos" }, o.efectos.join(" · ")) : null,
          o.destino ? enlaceDestino(o.destino) : null);
        tarjeta.append(el("div", { class: "opcion", "data-letra": o.letra },
          el("span", { class: "letra" }, o.letra, o.canon ? el("span", { class: "estrella", title: "canon" }, "★") : null),
          el("span", {}, o.texto, o.nota ? el("span", { class: "tenue" }, ` (${o.nota})`) : null),
          detalle));
      }
      col.append(tarjeta);
    }
    caja.append(col);
  }
  const filtros = document.getElementById("filtros");
  filtros.append(el("button", { type: "button", class: "activo", "data-final": "", onclick: () => elegirRuta(null) }, "Ninguna"));
  for (const id of Object.keys(D.rutas))
    filtros.append(el("button", { type: "button", class: `c-${D.finales[id].carril}`, "data-final": id, onclick: () => elegirRuta(id) }, id));
}

function elegirRuta(id, desplazar) {
  document.querySelectorAll("#filtros button").forEach((b) => b.classList.toggle("activo", (b.dataset.final || null) === id));
  document.querySelectorAll(".final").forEach((f) => f.classList.toggle("activo", id && f.id === `final-${id.replace(" ", "-")}`));
  const caja = document.getElementById("ruta");
  document.querySelectorAll(".ficha").forEach((n) => { n.classList.remove("atenuada", "en-ruta"); });
  document.querySelectorAll(".opcion").forEach((n) => n.classList.remove("atenuada", "elegida"));
  caja.replaceChildren();
  caja.classList.toggle("visible", !!id);
  if (!id) return;
  const ruta = D.rutas[id], f = D.finales[id], elegidas = new Map(ruta.pasos);
  document.querySelectorAll(".ficha").forEach((n) => {
    const ficha = n.dataset.ficha;
    if (!elegidas.has(ficha)) { n.classList.add("atenuada"); return; }
    n.classList.add("en-ruta");
    n.querySelectorAll(".opcion").forEach((o) => o.classList.add(o.dataset.letra === elegidas.get(ficha) ? "elegida" : "atenuada"));
  });
  const pasos = el("div", { class: "pasos" });
  ruta.pasos.forEach(([ficha, letra], k) => {
    const o = D.fichas[ficha].opciones.find((x) => x.letra === letra);
    if (k) pasos.append(el("span", { class: "flecha" }, "→"));
    pasos.append(el("a", { class: `paso${o.condicion ? " con-llave" : ""}`, href: `#f-${ficha}`, title: `${D.fichas[ficha].titulo}: ${o.texto}${o.condicion ? " (" + o.condicion + ")" : ""}`,
      onclick: (e) => { e.preventDefault(); irA(`f-${ficha}`); } }, `${ficha} ${letra}`));
  });
  pasos.append(el("span", { class: "flecha" }, "→"), el("b", { class: `c-${f.carril}`, style: "color:var(--c)" }, `${id} · ${f.nombre}`));
  const llaves = ruta.pasos.map(([ficha, letra]) => [ficha, D.fichas[ficha].opciones.find((x) => x.letra === letra)]).filter(([, o]) => o.condicion);
  caja.append(el("div", {}, el("b", {}, `Ruta de ejemplo a ${id}`), el("span", { class: "tenue" }, ` · ${ruta.pasos.length} decisiones`)), pasos,
    el("div", { class: "tenue" }, ...(llaves.length
      ? ["Llaves en esta ruta: ", ...llaves.flatMap(([ficha, o], k) => [k ? " " : "", el("span", { class: "llave" }, `${ficha} ${o.letra}: ${o.condicion}`)])]
      : ["Esta ruta no necesita llaves."])),
    el("p", { class: "tenue", style: "margin:6px 0 0" }, ruta.otras));
  if (desplazar) document.getElementById("explorador").scrollIntoView({ behavior: "smooth" });
}

dibujarMapa();
dibujarFinales();
dibujarCarriles();
document.getElementById("pie").textContent =
  `Generado de Historia.md el ${D.generado} con docs/generar_mapa_finales.py. Si cambia el guion, se vuelve a correr el script.`;
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
