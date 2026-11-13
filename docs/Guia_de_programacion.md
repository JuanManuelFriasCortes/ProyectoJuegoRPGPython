# Guía de programación del juego, pedazo por pedazo

Cómo se fue armando el juego en `game/main.py` y `game/logica.py`: qué hace cada pedazo, dónde va y por qué está hecho así. Sirve para entender el código, explicarlo en clase y retomarlo después.

- **Se corre desde la raíz del proyecto:** `python game/main.py`. Las rutas `assets/...` son relativas a esa carpeta.
- **La lógica se prueba sola, sin ventana:** `python game/logica.py`.
- **Si la ventana "solo da un flashazo",** hubo un error. Está en la terminal, en un bloque que empieza con `Traceback`; las dos últimas líneas dicen en qué línea tronó y por qué.
- **El formato de los datos** (`historia.json`, `dialogos.json`) está explicado en `assets/historia/FORMATO.md`.

## Orden del archivo `game/main.py`

```
imports
constantes (ANCHO, ALTO, FPS)
funciones (partir_en_renglones, cargar_ficha)
pygame.init(), ventana y reloj
cargar historia.json y crear el estado del jugador
fuentes y la caja del texto
cargar la primera ficha y las variables del juego (modo, seleccion...)
while jugando:
    eventos (teclado)
    dibujar (fondo, personajes, pestaña, caja, texto u opciones, final)
    flip y tick
pygame.quit()
```

---

## Parte 1 · La ventana

### Pedazo 1 · Arrancar pygame y crear la ventana

```python
import pygame

ANCHO = 1280
ALTO = 720
FPS = 60

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Star Wars: La Guerra de los Clones")
reloj = pygame.time.Clock()
```

- **Las constantes** van en mayúsculas porque no cambian en todo el juego. Todos los datos (posiciones y tamaños) están hechos para **1280×720**, así que ese tamaño no se cambia.
- **`pygame.init()`** enciende pygame, una sola vez.
- **`set_mode((ANCHO, ALTO))`** crea la ventana. Lleva paréntesis dobles porque el tamaño va como una tupla. Devuelve `pantalla`, la "hoja" donde se dibuja todo.
- **`Clock()`** crea un reloj que después limita el juego a 60 cuadros por segundo.

### Pedazo 2 · El ciclo del juego

```python
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            jugando = False

    pantalla.fill((10, 12, 30))
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
```

- **Todo juego repite, 60 veces por segundo:** revisar qué hizo el jugador, actualizar, dibujar y esperar.
- **`pygame.event.get()`** da la lista de lo que pasó desde la vuelta anterior. `QUIT` es la X de la ventana; `KEYDOWN` con `K_ESCAPE` es la tecla Esc.
- **`flip()`** muestra lo dibujado y **`tick(FPS)`** frena el ciclo a 60 vueltas por segundo.
- **`pygame.quit()`** va sin sangría: se ejecuta una vez, al salir del `while`.

---

## Parte 2 · Fondo animado y personajes

### Pedazo 3 · El fondo animado

Antes del `while`:

```python
hoja = pygame.image.load("assets/escenarios/animados_60/christophsis.png").convert()

cuadros = []
for t in range(144):
    x = (t % 12) * 320
    y = (t // 12) * 180
    cuadros.append(hoja.subsurface((x, y, 320, 180)))

cuadro_actual = 0
```

Dentro del `while`, en lugar del `fill`:

```python
    fondo = pygame.transform.scale(cuadros[cuadro_actual], (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))
    cuadro_actual = (cuadro_actual + 1) % 144
```

- **pygame no reproduce GIF animados.** Por eso cada fondo animado es una sola imagen con 144 cuadros acomodados en una cuadrícula de 12 columnas.
- **`t % 12`** (residuo) da la columna y **`t // 12`** (división entera) da la fila; por 320 y por 180 dan la posición del cuadro en la hoja. **`subsurface`** recorta ese rectángulo.
- **En cada vuelta** se agranda el cuadro que toca (×4, de 320×180 a 1280×720) y se pega. **`% 144`** regresa a 0 al llegar al final, y así la animación se repite sin brincos.
- **Se agranda un cuadro por vuelta, y no los 144 al cargarlos,** para ahorrar memoria: agrandados ocuparían unos 500 MB; chicos, unos 33 MB.

### Pedazo 4 · Un personaje

```python
anakin = pygame.image.load("assets/personajes/sprites_1x/anakin_skywalker.png").convert_alpha()
anakin = pygame.transform.scale(anakin, (40 * 8, 56 * 8))
```

```python
    pantalla.blit(anakin, (220, 152))
```

- **`convert_alpha()`** conserva la transparencia del sprite; con `convert()` saldría un rectángulo negro alrededor.
- **Los sprites miden 40×56** y los de adelante van ×8.
- **El orden importa:** lo último que se dibuja queda encima. El personaje va después del fondo.
- *(Este pedazo se reemplazó en el 6, cuando los personajes empezaron a salir del JSON.)*

---

## Parte 3 · Leer la historia

### Pedazo 5 · Cargar `historia.json`

```python
import json
```

```python
with open("assets/historia/historia.json", encoding="utf-8") as archivo:
    historia = json.load(archivo)
```

- **`with open(...)`** abre el archivo y lo cierra solo al terminar el bloque. `encoding="utf-8"` es para que lea bien los acentos.
- **`json.load`** convierte todo el archivo en diccionarios y listas de Python.
- **Las rutas se arman uniendo textos con `+`:** `"assets/escenarios/animados_60/" + ficha["fondo"] + ".png"`.

### Pedazo 6 · Los personajes de la ficha

```python
personajes = []
for p in ficha["personajes"]:
    carpeta = "assets/personajes/sprites_1x/"
    if p["holograma"]:
        carpeta = "assets/personajes/sprites_holograma/"
    imagen = pygame.image.load(carpeta + p["clave"] + ".png").convert_alpha()
    imagen = pygame.transform.scale(imagen, (40 * p["escala"], 56 * p["escala"]))
    if p["girado"]:
        imagen = pygame.transform.rotate(imagen, 90)
    personajes.append((imagen, (p["izquierda"], p["arriba"])))
```

```python
    for imagen, posicion in personajes:
        pantalla.blit(imagen, posicion)
```

- **Cada `p`** es un diccionario con la clave del personaje, su escala (×8 adelante, ×5 o ×6 atrás), su posición ya calculada y si es holograma o está tirado.
- **Los hologramas** usan la versión azul que ya está preparada. Los que están **girados** (en el suelo) se rotan 90°.
- **Se guarda una tupla `(imagen, (x, y))`** y al dibujar se **desempaqueta** en el `for`.
- **Vienen ordenados** en el JSON (primero los de atrás), así que los de adelante quedan encima solos.

---

## Parte 4 · El cuadro de texto

### Pedazo 7 · La caja

```python
fuente = pygame.font.SysFont("arial", 30)
caja = pygame.Rect(20, 472, 1240, 232)
```

```python
    pygame.draw.rect(pantalla, (10, 14, 34), caja)
    pygame.draw.rect(pantalla, (122, 200, 255), caja, 3)
```

- **`Rect(x, y, ancho, alto)`** guarda un rectángulo. La caja ocupa el tercio de abajo de la pantalla.
- **`draw.rect`** sin el último número rellena; **con un `3`** dibuja solo el borde, de 3 píxeles.
- **`fuente.render(texto, False, color)`** convierte un texto en imagen. `False` es para que no se suavice y quede con bordes duros, como el pixel art.

### Pedazo 8 · Función `partir_en_renglones`

```python
def partir_en_renglones(texto, fuente, ancho_maximo):
    renglones = []
    renglon = ""
    for palabra in texto.split():
        if renglon == "":
            prueba = palabra
        else:
            prueba = renglon + " " + palabra
        if fuente.size(prueba)[0] <= ancho_maximo:
            renglon = prueba
        else:
            renglones.append(renglon)
            renglon = palabra
    if renglon != "":
        renglones.append(renglon)
    return renglones
```

```python
    y = caja.y + 24
    for renglon in renglones:
        imagen_texto = fuente.render(renglon, False, (236, 240, 250))
        pantalla.blit(imagen_texto, (caja.x + 24, y))
        y += 36
```

- **Una función** recibe datos (parámetros), hace algo y devuelve un resultado con `return`.
- **Va armando un renglón palabra por palabra.** `fuente.size(prueba)[0]` dice cuánto mediría en pantalla; si ya no cabe, guarda el renglón y empieza otro.
- **Al dibujar,** cada renglón baja 36 píxeles (`y += 36`).
- **Con esta letra, todos los textos de las 312 fichas caben en 1 o 2 renglones.**

### Pedazo 9 · La pestaña con quién juega

```python
fuente_nombre = pygame.font.SysFont("arial", 22, bold=True)
```

```python
    nombre = fuente_nombre.render(ficha["juega"].upper(), False, (255, 214, 102))
    pestana = pygame.Rect(caja.x + 12, caja.y - 34, nombre.get_width() + 32, 36)
    pygame.draw.rect(pantalla, (10, 14, 34), pestana)
    pygame.draw.rect(pantalla, (122, 200, 255), pestana, 3)
    pantalla.blit(nombre, (pestana.x + 16, pestana.y + 6))
```

- **La pestaña** asoma 34 píxeles arriba de la caja, y su ancho se ajusta al nombre (`get_width()`).
- **Se dibuja antes que la caja,** para que el borde de la caja quede encima de su parte de abajo y se vean unidas.
- **El título de la ficha** va en la barra de la ventana (`set_caption`).

### Pedazo 10 · Con Enter, del texto a las opciones

```python
modo = "texto"
```

```python
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if modo == "texto":
                modo = "opciones"
```

```python
    if modo == "texto":
        ...renglones del texto...
    else:
        pregunta = fuente.render("¿Qué haces?", False, (196, 206, 232))
        pantalla.blit(pregunta, (caja.x + 24, caja.y + 20))
        y = caja.y + 64
        for opcion in opciones:
            ...cada opción, 36 píxeles más abajo...
```

- **La variable `modo`** dice qué está mostrando el cuadro. Es el mismo dibujo con dos estados.
- **El jugador nunca ve la ★ del canon.**

### Pedazo 11 · Mover la selección con ↑ y ↓

```python
seleccion = 0
```

```python
        if evento.type == pygame.KEYDOWN and modo == "opciones":
            if evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(opciones)
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(opciones)
```

```python
        for i, opcion in enumerate(opciones):
            color = (236, 240, 250)
            marca = "   "
            if i == seleccion:
                color = (255, 214, 102)
                marca = "► "
            texto_opcion = fuente.render(marca + opcion["letra"] + ") " + opcion["texto"], False, color)
            pantalla.blit(texto_opcion, (caja.x + 24, y))
            y += 36
```

- **`seleccion`** es la posición de la opción marcada en la lista (0, 1, 2…).
- **`% len(opciones)`** hace que desde la última se regrese a la primera, y al revés.
- **`enumerate`** da cada opción junto con su número; la marcada va en amarillo y con `►`.

---

## Parte 5 · Pasar de ficha

### Pedazo 12 · Función `cargar_ficha`

```python
def cargar_ficha(clave):
    ficha = historia["fichas"][clave]
    pygame.display.set_caption(clave + " · " + ficha["titulo"])
    ...el fondo animado (pedazo 3)...
    ...los personajes (pedazo 6)...
    ...las líneas del texto o del diálogo (pedazos 8, 18, 20 y 23)...
    opciones = logica.opciones_visibles(ficha, estado)
    return ficha, cuadros, personajes, renglones, opciones
```

```python
ficha_actual = estado["ficha"]
ficha, cuadros, personajes, renglones, opciones = cargar_ficha(ficha_actual)
cuadro_actual = 0
modo = "texto"
seleccion = 0
```

- **Lo que se cargaba una sola vez antes del `while` se metió en una función** para poder repetirlo cada vez que cambia la ficha.
- **Una función puede leer variables de afuera** (`historia`, `fuente`, `caja`, `estado`) siempre que existan cuando se llama. Por eso se llama hasta después de crearlas.
- **Devuelve cinco cosas a la vez,** y se reciben en cinco variables, en el mismo orden.

### Pedazo 13 · Enter elige y pasa a la siguiente ficha

```python
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if modo == "texto":
                modo = "opciones"
            elif modo == "final":
                jugando = False
            elif modo == "opciones":
                elegida = opciones[seleccion]
                logica.elegir(elegida, ficha_actual, estado)
                ficha_actual = estado["ficha"]
                if ficha_actual in historia["fichas"]:
                    ficha, cuadros, personajes, renglones, opciones = cargar_ficha(ficha_actual)
                    modo = "texto"
                    seleccion = 0
                else:
                    ...pantalla del final (pedazo 19)...
```

- **Tiene que ser `elif`.** Con dos `if` seguidos, un solo Enter cambiaba el modo a `"opciones"` y en la misma tecla elegía la opción A, y el jugador nunca veía las decisiones.
- **`in historia["fichas"]`** revisa si la siguiente es una ficha. Si no, es un final.
- **Solo debe haber un bloque de Enter.** Hubo un error por dejar el viejo y el nuevo juntos.

---

## Parte 6 · La lógica (`game/logica.py`)

Va en un archivo aparte porque no tiene gráficos: se prueba en la consola y es la parte central para explicar. En `main.py` se usa con `import logica` y `logica.funcion(...)`.

### Pedazo 14 · El estado del jugador

```python
def nuevo_estado(historia):
    estado = {
        "ficha": historia["inicio"],
        "medidores": dict(historia["medidores"]),
        "banderas": [],
        "elecciones": [],
    }
    return estado
```

- **El estado** guarda todo lo que el juego recuerda de una partida: en qué ficha vas, los 7 medidores, las banderas prendidas y lo que elegiste (`"D252 B"`).
- **`dict(...)` hace una copia.** Sin ella, al subir la Oscuridad del jugador también cambiaría el valor inicial guardado en `historia`.
- **`if __name__ == "__main__":`** marca las pruebas: solo corren con `python game/logica.py`, no cuando `main.py` importa el archivo.

### Pedazo 15 · `cumple_pieza` y `cumple`

```python
def cumple_pieza(pieza, estado):
    partes = pieza.split()
    if len(partes) == 3:
        medidor = partes[0]
        numero = int(partes[2])
        if partes[1] == ">=":
            return estado["medidores"][medidor] >= numero
        else:
            return estado["medidores"][medidor] <= numero
    if len(partes) == 1:
        return partes[0] in estado["banderas"]
    if partes[0] == "sin":
        return partes[1] not in estado["banderas"]
    return pieza in estado["elecciones"]


def cumple(requisito, estado):
    if requisito == "":
        return True
    for alternativa in requisito.split(" o "):
        todas = True
        for pieza in alternativa.split(" y "):
            if not cumple_pieza(pieza, estado):
                todas = False
        if todas:
            return True
    return False
```

- **Las cuatro clases de pieza se distinguen por cuántas palabras tienen:**
  - `"OSC >= 35"` (3 palabras) es un medidor.
  - `"MORTIS_RECUERDA"` (1) es una bandera.
  - `"sin X"` (2, empieza con `sin`) es una bandera apagada.
  - `"D273 B"` (2) es una elección.
- **`cumple`** separa primero por `" o "`, donde basta una alternativa, y luego por `" y "`, donde tienen que cumplirse todas.
- **Un `return` termina la función ahí mismo.**

### Pedazo 16 · `aplicar`

```python
def aplicar(efectos, estado):
    for efecto in efectos:
        partes = efecto.split()
        if partes[0] == "quita":
            if partes[1] in estado["banderas"]:
                estado["banderas"].remove(partes[1])
        elif len(partes) == 2:
            estado["medidores"][partes[0]] += int(partes[1])
        else:
            if efecto not in estado["banderas"]:
                estado["banderas"].append(efecto)
```

- **Hay tres tipos de efecto:** `"OSC +5"` (medidor), `"PLO_MUERTO"` (prender bandera) y `"quita X"` (apagar bandera).
- **`quita` se revisa primero** porque también tiene 2 palabras, igual que un medidor.
- **No necesita `return`:** el diccionario del estado se modifica directamente.

### Pedazo 17 · Conectar la lógica con el juego

```python
def opciones_visibles(ficha, estado):
    visibles = []
    for opcion in ficha["opciones"]:
        if cumple(opcion["requiere"], estado):
            visibles.append(opcion)
    return visibles


def elegir(opcion, clave_ficha, estado):
    estado["elecciones"].append(clave_ficha + " " + opcion["letra"])
    aplicar(opcion["efectos"], estado)
    for extra in opcion["efectos_si"]:
        if cumple(extra["requiere"], estado):
            aplicar(extra["efectos"], estado)
    estado["ficha"] = opcion["siguiente"]
```

En `main.py`:

```python
import logica
estado = logica.nuevo_estado(historia)    # después de cargar historia.json
```

- **`opciones_visibles`** deja solo las opciones cuyo requisito se cumple. Así aparecen las llaves de los finales, como "Matarlo ahí mismo" con `OSC >= 35`.
- **`elegir` hace todo lo de una decisión:** anota la elección, aplica los efectos, aplica los efectos condicionados (solo D305 B los tiene) y guarda la siguiente ficha.

---

## Parte 7 · Consecuencias y finales

### Pedazo 18 · Notas: el texto cambia según tus banderas

En `cargar_ficha`:

```python
    texto = ficha["texto"]
    for nota in ficha["notas"]:
        if logica.cumple(nota["requiere"], estado):
            texto = texto + " " + nota["texto"]
    renglones = partir_en_renglones(texto, fuente, caja.width - 48)
```

- **Algunas fichas agregan una frase si prendiste cierta bandera.** Por ejemplo, D022 con `ROTTA_GRAVE`: "Jabba está todavía más furioso."
- **Se reutiliza `cumple`:** las notas usan los mismos requisitos que las opciones.

### Pedazo 19 · La pantalla del final

En el bloque de Enter, cuando la siguiente no es una ficha:

```python
                else:
                    final = historia["finales"][ficha_actual]
                    texto_final = final["texto"]
                    for variante in final["variantes"]:
                        if logica.cumple(variante["requiere"], estado):
                            texto_final = texto_final + " " + variante["texto"]
                    renglones_final = partir_en_renglones(texto_final, fuente, 1100)
                    modo = "final"
```

Antes de `pygame.display.flip()`:

```python
    if modo == "final":
        pantalla.fill((4, 6, 14))
        titulo_final = fuente_nombre.render(ficha_actual + " · " + final["nombre"], False, (255, 214, 102))
        pantalla.blit(titulo_final, (90, 120))
        y = 180
        for renglon in renglones_final:
            imagen_texto = fuente.render(renglon, False, (236, 240, 250))
            pantalla.blit(imagen_texto, (90, y))
            y += 40
        aviso = fuente_nombre.render("Enter para salir", False, (150, 170, 210))
        pantalla.blit(aviso, (90, 640))
```

- **El texto del final** se arma con su texto base más las **variantes** cuyo requisito se cumple. Algunas dependen de banderas y otras de elecciones, como `"D294 A"`.
- **El fondo casi negro** tapa todo lo que se dibujó antes en esa vuelta. Por eso va justo antes de `flip`.
- **Enter en el final cierra el juego.** Cuando exista el menú de título, regresará al menú.

---

## Parte 8 · Diálogos

### Pedazo 20 · Diálogos línea por línea

```python
with open("assets/historia/dialogos.json", encoding="utf-8") as archivo:
    dialogos = json.load(archivo)
```

En `cargar_ficha`, en lugar de un solo texto, se arma una **lista de líneas**: si la ficha tiene diálogo, son sus líneas; si no, es una sola línea con el texto de la ficha.

```python
    lineas = []
    if clave in dialogos:
        for linea in dialogos[clave]["antes"]:
            ...una línea por cada "dice" o "narra"...
    else:
        lineas.append({"quien": "", ..., "renglones": partir_en_renglones(texto, fuente, caja.width - 48)})
```

```python
            if modo == "texto":
                if linea_actual < len(lineas) - 1:
                    linea_actual += 1
                else:
                    modo = "opciones"
```

- **Cada línea es un diccionario** con quién habla (`"quien"`) y sus renglones ya partidos. Se parten una vez, al cargar la ficha.
- **`linea_actual`** es el número de la línea que se ve. Enter avanza, y después de la última aparecen las opciones.
- **La pestaña dice quién habla.** El narrador (`quien` vacío) no lleva pestaña, y en las opciones dice quién juega.

### Pedazo 21 · Máquina de escribir

```python
letras = 0      # se reinicia en cada línea nueva y en cada ficha nueva
```

```python
        restantes = letras
        for renglon in lineas[linea_actual]["renglones"]:
            if restantes > 0:
                imagen_texto = fuente.render(renglon[:restantes], False, (236, 240, 250))
                pantalla.blit(imagen_texto, (caja.x + 24, y))
            restantes -= len(renglon)
            y += 36
```

```python
    if modo == "texto" or modo == "reaccion":
        letras += 1
```

- **`letras`** cuenta cuántas letras de la línea ya se ven. Sube 1 en cada vuelta, o sea 60 por segundo.
- **`renglon[:restantes]`** (rebanado) toma solo las primeras letras. El `if restantes > 0` evita que un número negativo corte desde el final.
- **Cada línea guarda `"largo"`** (`len(texto)`), y el Enter ahora tiene tres casos: si se está escribiendo, completa la línea; si ya está completa, avanza; si era la última, muestra las opciones.

### Pedazo 22 · Reacciones y resultados

```python
def lineas_de_reaccion(clave, opcion):
    ...las líneas de dialogos[clave]["reacciones"][letra], si existen...
    ...más el "resultado" de la opción ("99 muere.") como narración...
    return lineas
```

```python
            pasar = False
            ...
            elif modo == "opciones":
                logica.elegir(elegida, ficha_actual, estado)
                lineas = lineas_de_reaccion(ficha_actual, elegida)
                if len(lineas) > 0:
                    modo = "reaccion"
                    linea_actual = 0
                    letras = 0
                else:
                    pasar = True

            if pasar:
                ...cargar la siguiente ficha o la pantalla del final...
```

- **`modo = "reaccion"`** funciona igual que el texto (letra por letra, y Enter completa o avanza), pero al terminar pasa a la siguiente ficha en lugar de mostrar opciones.
- **`pasar`** es una bandera propia del código. Hace que el bloque que carga la siguiente ficha esté **una sola vez**, aunque se use desde dos lugares: al elegir sin reacción y al terminar la reacción.

### Pedazo 23 · Iluminar a quien habla, y quién entra o sale

Cada personaje guarda dos imágenes:

```python
        personajes.append({"clave": p["clave"], "imagen": imagen, "apagada": apagada, "posicion": (p["izquierda"], p["arriba"])})
```

Cada línea guarda quién habla y quiénes están en escena:

```python
        presentes = list(todos)
        ...quien tiene "entra" se quita al principio...
        for linea in dialogos[clave]["antes"]:
            if linea["tipo"] == "entra":
                presentes.append(linea["clave"])
            elif linea["tipo"] == "sale":
                presentes.remove(linea["clave"])
            else:
                lineas.append({..., "clave": linea["clave"], "presentes": list(presentes), ...})
```

Al dibujar:

```python
    for p in personajes:
        if modo == "texto" or modo == "reaccion":
            linea = lineas[linea_actual]
            if p["clave"] not in linea["presentes"]:
                continue
            if linea["clave"] is not None and linea["clave"] != p["clave"]:
                pantalla.blit(p["apagada"], p["posicion"])
                continue
        pantalla.blit(p["imagen"], p["posicion"])
```

- **Los personajes pasan de tupla a diccionario,** porque ya son cuatro datos y con nombres se leen mejor.
- **`list(...)` hace copias.** Cada línea guarda su propia lista de presentes; sin la copia, todas compartirían la misma lista y cambiarían juntas.
- **`continue`** salta al siguiente personaje. **`is not None`** pregunta si la línea tiene a alguien que habla; el narrador trae `None`.
- **En D002,** Ahsoka no está al inicio y aparece cuando baja de la lanzadera. Mientras habla Rex, los demás se ven apagados.

## Parte 9 · Sonido

### Pedazo 24 · La música

```python
import os
```

```python
def poner_musica(nombre, actual):
    if nombre == actual:
        return actual
    ruta = "assets/musica/pistas/" + nombre + ".ogg"
    if not os.path.exists(ruta):
        pygame.mixer.music.stop()
        return nombre
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, fade_ms=1500)
    return nombre
```

```python
musica_actual = poner_musica(ficha["musica"], "")                 # al arrancar
musica_actual = poner_musica(ficha["musica"], musica_actual)      # al cargar cada ficha
musica_actual = poner_musica(final["musica"], musica_actual)      # al llegar a un final
```

- **Solo cambia si es otra canción.** Muchas fichas seguidas comparten canción y no debe reiniciarse en cada una.
- **La función devuelve la canción que quedó sonando** y se guarda en `musica_actual`, para compararla la próxima vez.
- **`os.path.exists`** revisa si el archivo existe. Si no está (por ejemplo, porque la música no se ha bajado), el juego sigue sin música y sin tronar.
- **`pygame.mixer.music`** es la música de fondo:
  - `load` carga el archivo;
  - `set_volume(0.6)` la deja al 60%, para que no tape los sonidos;
  - `play(-1, fade_ms=1500)` la toca en bucle (`-1`) con una entrada suave de 1.5 segundos.

### Pedazo 25 · Voces al escribir, cursor y confirmar

```python
import random
```

```python
with open("assets/sonidos/sonidos.json", encoding="utf-8") as archivo:
    sonidos = json.load(archivo)

voces = {}
for nombre_voz in sonidos["voces"]:
    voces[nombre_voz] = []
    for archivo_voz in sonidos["voces"][nombre_voz]:
        voces[nombre_voz].append(pygame.mixer.Sound("assets/sonidos/" + archivo_voz))
sonido_cursor = pygame.mixer.Sound("assets/sonidos/" + sonidos["ui"]["cursor"])
sonido_confirmar = pygame.mixer.Sound("assets/sonidos/" + sonidos["ui"]["confirmar"])
```

```python
    if modo == "texto" or modo == "reaccion":
        linea = lineas[linea_actual]
        if letras < linea["largo"]:
            letras += 1
            if letras % sonidos["cada_letras"] == 1:
                if linea["clave"] is None:
                    voz = sonidos["narrador"]
                else:
                    voz = sonidos["personajes"].get(linea["clave"], sonidos["por_defecto"])
                random.choice(voces[voz]).play()
```

- **`pygame.mixer.Sound`** es para efectos cortos: se cargan completos en memoria y pueden sonar varios a la vez. La música larga va con `pygame.mixer.music`.
- **`voces` es un diccionario de listas:** cada voz con sus 6 variantes ya cargadas. Se cargan una vez al inicio.
- **`letras % 4 == 1`** hace que la voz suene en la letra 1, 5, 9… y no en cada letra, que serían 60 por segundo.
- **`letras` ya no sube sin fin:** solo mientras la línea se está escribiendo. Así las voces se callan cuando el texto está completo.
- **`random.choice(lista)`** escoge una variante al azar, para que no suene siempre igual.
- **`diccionario.get(clave, por_defecto)`** no truena si la clave no existe; devuelve el valor por defecto. Sirve para los personajes sin voz propia.
- **`sonido_cursor.play()`** suena al mover la flecha y **`sonido_confirmar.play()`** al elegir una opción.

## Parte 10 · Menú, guardado y detalles finales

### Pedazo 26 · Menú de título, y guardar y cargar la partida

En `logica.py` (es lógica, no lleva gráficos):

```python
import json

def guardar_partida(estado, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estado, archivo, ensure_ascii=False, indent=1)


def cargar_partida(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)
```

En `main.py`:

```python
ARCHIVO_PARTIDA = "partida_guardada.json"

def opciones_del_menu():
    if os.path.exists(ARCHIVO_PARTIDA):
        return ["Continuar", "Nueva partida", "Salir"]
    return ["Nueva partida", "Salir"]
```

```python
modo = "titulo"     # el juego empieza en el menú
```

```python
            elif modo == "titulo":
                elegido = opciones_menu[seleccion_menu]
                if elegido == "Salir":
                    jugando = False
                elif elegido == "Nueva partida":
                    estado = logica.nuevo_estado(historia)
                    pasar = True
                else:
                    estado = logica.cargar_partida(ARCHIVO_PARTIDA)
                    pasar = True
```

- **El estado del jugador ya es un diccionario,** así que guardar la partida es escribirlo como JSON con `json.dump`, y cargarla es leerlo con `json.load`. Es la ventaja de haber guardado todo en un solo diccionario desde el pedazo 14.
- **Se guarda solo al llegar a cada ficha** (en el `if pasar:`). Al llegar a un final, el archivo se borra con `os.remove`, porque la partida ya terminó.
- **"Nueva partida" y "Continuar" solo cambian el `estado` y ponen `pasar = True`.** El mismo bloque de siempre carga `estado["ficha"]`: la bandera `pasar` se reutiliza otra vez.
- **"Continuar" solo aparece si existe el archivo** (`os.path.exists`).
- **Esc:** en el menú cierra el juego; jugando, regresa al menú. **Enter en un final** regresa al menú.
- **El menú se dibuja encima:** el fondo animado, una capa negra semitransparente (`Surface` con `set_alpha(150)`), el título y las opciones centradas con `(ANCHO - ancho_del_texto) // 2`.
- **`partida_guardada.json` va en el `.gitignore`:** cada quien tiene la suya.

### Pedazo 27 · Pantalla completa y medidores en pantalla

```python
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED)
```

```python
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
            ver_medidores = not ver_medidores
```

```python
    if ver_medidores and modo != "titulo":
        texto_medidores = ""
        for clave_medidor in estado["medidores"]:
            texto_medidores = texto_medidores + clave_medidor + " " + str(estado["medidores"][clave_medidor]) + "   "
        ...se dibuja arriba a la izquierda...
```

- **`pygame.SCALED`:** el juego sigue pensando en 1280×720 y pygame agranda todo al tamaño de la pantalla. Ninguna posición cambia. **F11** alterna entre ventana y pantalla completa.
- **F1 muestra los medidores y cuántas banderas hay.** Sirve para probar las llaves de los finales. `not` invierte un `True`/`False`, y `str(número)` convierte un número en texto para poder unirlo con `+`.
- **Se quitó el `print` de prueba** que escribía los medidores en la terminal.

## Controles

| Tecla | Qué hace |
|---|---|
| Enter | Completar la línea, avanzar, elegir y aceptar en el menú |
| ↑ ↓ | Mover la selección (opciones y menú) |
| Esc | Jugando: regresar al menú (la partida queda guardada). En el menú: salir |
| F11 | Pantalla completa o ventana |
| F1 | Mostrar u ocultar los medidores |

---

## Errores corregidos en el camino

- **Las pruebas de `cumple` habían quedado dentro de `nuevo_estado`,** y cada partida empezaba con Oscuridad 40 y `MORTIS_RECUERDA`. Se movieron al bloque `if __name__ == "__main__":`. Las pruebas van solo ahí.

---

## Lo que falta

**Los 27 pedazos del plan están terminados: el juego está completo.** Queda pendiente:
- **Guion:** acortar el texto de la opción D304 B, que no cabe en un renglón.
- **Diálogos:** escribir los de más fichas en `Dialogos.md` y correr `python assets/historia/preparar_historia.py`. Las fichas sin diálogo funcionan con su texto como narración.
