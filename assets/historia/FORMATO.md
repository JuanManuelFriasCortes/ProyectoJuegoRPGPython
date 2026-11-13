# Formato de los datos del juego

El juego no lee `Historia.md` ni `Dialogos.md`: lee los archivos que genera `preparar_historia.py`. Todo se carga con `json.load` y queda en diccionarios y listas de Python.

| Archivo | Qué trae |
|---|---|
| `assets/historia/historia.json` | Las 312 fichas, los finales, los medidores, las banderas y las carpetas de imágenes y sonidos |
| `assets/historia/dialogos.json` | Los diálogos escritos, por ficha |
| `assets/sonidos/sonidos.json` | La voz de cada personaje y los sonidos de la interfaz |

## historia.json

```
historia["inicio"]             "D001": la primera ficha
historia["medidores"]          {"OSC": 2, "PAL": 3, ...}: con cuánto empieza cada medidor
historia["nombres_medidores"]  {"OSC": "Oscuridad", ...}: para mostrarlos en pantalla
historia["carpetas"]           dónde están las imágenes, la música y los sonidos
historia["pantalla"]           {"ancho": 1280, "alto": 720, "escala_fondo": 4}
historia["fondo_animado"]      cómo están acomodados los cuadros de los fondos animados
historia["nombres"]            {"anakin_skywalker": "Anakin Skywalker", ...}
historia["banderas"]           {"MORTIS_RECUERDA": "Anakin conserva el recuerdo de la visión de Mortis", ...}
historia["fichas"]             {"D001": {...}, "D002": {...}, ...}
historia["finales"]            {"FINAL 1": {...}, ..., "FP1": {...}, ...}
```

## Una ficha

```json
"D252": {
  "titulo": "\"Mátalo\"",
  "juega": "Anakin",
  "fuente": "película La venganza de los Sith",
  "rama": false,
  "bifurcacion": true,
  "acto": "ACTO VI — La caída",
  "capitulo": "Capítulo 38 · Batalla de Coruscant",
  "texto": "Le cortas las manos a Dooku. Palpatine ordena: \"Mátalo, Anakin. Mátalo ahora\".",
  "notas": [],
  "notas_guion": [],
  "opciones": [ ... ],
  "fondo": "pasillo_separatista",
  "personajes": [ ... ],
  "musica": "dooku"
}
```

- **`texto`**: lo que pasa en la escena. Si la ficha no tiene diálogo en `dialogos.json`, este texto se muestra como narración.
- **`notas`**: frases extra que solo se muestran si se cumple su requisito, por ejemplo `{"requiere": "ROTTA_GRAVE", "texto": "Jabba está todavía más furioso."}`.
- **`notas_guion`**: notas para quien escribe la historia. El juego no las muestra.
- **`rama`** y **`bifurcacion`**: solo informativos (ficha fuera del canon y decisión importante).

## Una opción

```json
{
  "letra": "B",
  "texto": "Perdonarlo y arrestarlo",
  "canon": false,
  "requiere": "",
  "efectos": ["OSC -1", "PAL -1", "DOOKU_PRISIONERO"],
  "efectos_si": [],
  "siguiente": "D253",
  "resultado": "",
  "resultado_requiere": ""
}
```

| Campo | Qué es |
|---|---|
| `requiere` | Si no está vacío, la opción solo aparece cuando se cumple (ver abajo) |
| `efectos` | Lo que cambia al elegirla (ver abajo) |
| `efectos_si` | Efectos que solo se aplican si se cumple su requisito. Solo D305 B lo usa: `{"requiere": "D273 B", "efectos": ["ORDEN66_DETENIDA"]}` |
| `siguiente` | La ficha que sigue (`"D253"`) o un final (`"FINAL 1"`, `"FP3"`) |
| `resultado` | Una frase de lo que pasó después de elegir ("99 muere."). Puede estar vacía |
| `resultado_requiere` | Si no está vacío, el `resultado` solo se muestra cuando se cumple. Solo D158 y D169 lo usan |
| `canon` | `true` en la opción de la película o la serie. Al jugador no se le muestra |

## Requisitos

Un requisito es un texto con piezas unidas por `" o "` y `" y "`:

| Pieza | Se cumple si… | Ejemplo |
|---|---|---|
| 3 palabras: medidor, `>=` o `<=`, número | el medidor es por lo menos o como máximo ese número | `"OSC >= 35"`, `"PAD <= 10"` |
| 1 palabra | esa bandera está prendida | `"MORTIS_RECUERDA"` |
| `sin` + bandera | esa bandera **no** está prendida | `"sin AHSOKA_DUDA_ORDEN"` |
| ficha + letra | el jugador ya eligió esa opción en la partida | `"D273 B"` |

- `"PAD >= 25 o ANAKIN_DUDA_ORDEN"`: basta con que se cumpla una de las dos.
- `"AHS >= 35 y sin AHSOKA_DUDA_ORDEN"`: se tienen que cumplir las dos.
- Primero se separa por `" o "`; cada parte se separa por `" y "`. Ningún requisito mezcla paréntesis.
- Un requisito vacío (`""`) siempre se cumple.

Para saber qué tipo de pieza es, basta con `pieza.split()` y ver cuántas palabras tiene y cuál es la primera.

## Efectos

| Efecto | Qué hace | Ejemplo |
|---|---|---|
| medidor + número con signo | suma o resta al medidor | `"AHS +2"`, `"OBI -1"` |
| 1 palabra | prende esa bandera | `"PLO_MUERTO"` |
| `quita` + bandera | apaga esa bandera | `"quita ROTTA_GRAVE"` |

`int("+2")` y `int("-1")` funcionan directo en Python.

## Finales

```json
"FINAL 2": {
  "nombre": "Vader sin máscara",
  "canon": false,
  "linea": "oscura",
  "texto": "Anakin vuelve de Mustafar sin quemaduras...",
  "variantes": [
    {"requiere": "D294 A", "texto": "Padmé vive en el palacio imperial..."},
    {"requiere": "CRISTAL_REPUBLICA", "texto": "El proyecto de la superarma se adelanta años."}
  ],
  "musica": "imperio"
}
```

Al llegar a un final se muestra `texto` y, debajo, cada variante cuyo requisito se cumpla. `linea` es `oscura`, `luz`, `emperador`, `exilio` o `prematuro` (FP1 a FP5).

## El estado del jugador (propuesta)

Todo lo que el juego necesita recordar de una partida cabe en un diccionario. Guardar la partida es escribirlo con `json.dump`.

```json
{
  "ficha": "D252",
  "medidores": {"OSC": 41, "PAL": 23, "OBI": 7, "AHS": 45, "PAD": 18, "CLO": 29, "PIS": 16},
  "banderas": ["AHSOKA_SOSPECHA", "BARRISS_AMIGA"],
  "elecciones": ["D001 A", "D002 C", "D004 A"]
}
```

`elecciones` sirve para los requisitos del tipo `"D273 B"` y para las variantes de los finales.

## dialogos.json

```json
"D002": {
  "antes": [
    {"tipo": "narra", "quien": "", "clave": null, "texto": "Christophsis. Los droides se repliegan..."},
    {"tipo": "dice", "quien": "Rex", "clave": "capitan_rex", "texto": "¡General! Una lanzadera..."},
    {"tipo": "entra", "quien": "Ahsoka", "clave": "ahsoka_tano", "texto": ""}
  ],
  "reacciones": {
    "A": [{"tipo": "dice", "quien": "Anakin", "clave": "anakin_skywalker", "texto": "Está bien, pequeña..."}]
  }
}
```

- `antes`: lo que se dice antes de la decisión. `reacciones`: lo que se dice después, según la letra elegida.
- `tipo`: `narra` (narrador, sin nombre), `dice` (habla un personaje), `entra` o `sale` (un personaje aparece o se va).
- `clave`: el personaje en pantalla que habla. Se usa para iluminarlo y oscurecer al resto, y para escoger su voz.
- Quien tiene un `entra` no está en pantalla al empezar la ficha.

## Imágenes

Las rutas se arman con la carpeta, el nombre y la extensión: `historia["carpetas"]["sprites"] + "/" + clave + ".png"`.

**Fondo.** `ficha["fondo"]` es el nombre del escenario.
- Fijo: `carpetas["fondos"]/<fondo>.png` (320×180). Se escala ×4 para llenar 1280×720.
- Animado: `carpetas["fondos_animados"]/<fondo>.png` tiene 144 cuadros de 320×180 en una cuadrícula de 12 columnas. El cuadro `t` empieza en `x = (t % 12) * 320`, `y = (t // 12) * 180`. A 60 cuadros por segundo, el ciclo dura 2.4 s y se repite.

**Personajes.** `ficha["personajes"]` ya viene en orden de dibujo: primero los de atrás.

```json
{"clave": "obi_wan_kenobi", "escala": 6, "izquierda": 82, "arriba": 290, "holograma": false, "girado": true}
```

1. Se carga el sprite de 40×56 de la carpeta que toca:
   - `sprites_holograma` si `holograma` es `true`,
   - `sprites_apagados` si habla otro personaje,
   - `sprites` en los demás casos.
2. Se escala por `escala`: queda de `40 * escala` × `56 * escala`.
3. Si `girado` es `true`, se gira 90° (contra las manecillas del reloj), porque está tirado en el suelo.
4. Se dibuja con su esquina de arriba a la izquierda en (`izquierda`, `arriba`), en una pantalla de 1280×720.

Para que los píxeles se vean marcados, se escala sin suavizar: en pygame, `pygame.transform.scale`.

## Sonidos

- **Música:** `carpetas["musica"]/<musica>.ogg`, con `ficha["musica"]` o `final["musica"]`. Si el archivo no existe (por ejemplo, si Sara todavía no baja la música), el juego sigue sin música.
- **Voces al escribir:** en `assets/sonidos/sonidos.json`:
  - `personajes[clave]` da la voz de cada personaje,
  - `voces[voz]` da sus 6 archivos,
  - `narrador` es la voz del narrador,
  - `cada_letras` (4) dice cada cuántas letras suena un archivo al azar de esa voz.
- **Interfaz:** `ui.cursor` al mover la selección y `ui.confirmar` al elegir.

## Si cambia algo

Se vuelve a correr, en este orden, solo lo que haga falta:

1. `assets/escenarios/generar_escenarios.py`: si cambian los fondos.
2. `assets/escenas/armar_escenas.py`: si cambia quién aparece en una ficha.
3. `assets/musica/preparar_musica.py`: si cambia la música.
4. `assets/historia/preparar_historia.py`: **siempre** que cambie `Historia.md`, `Dialogos.md` o cualquiera de los anteriores.
5. `docs/generar_mapa_finales.py`: si cambian las fichas de D273 en adelante.
