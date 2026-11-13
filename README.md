# Proyecto Juego RPG — Star Wars: La Guerra de los Clones

Proyecto final de la materia **Programación en Python** (Semestre 7, UAA).

## Descripción

Juego **RPG de toma de decisiones** ambientado en la historia de *Star Wars: La Guerra de los Clones*. El jugador avanza por los acontecimientos de la guerra y, en momentos clave, elige qué hacer. Cada decisión cambia el rumbo de la historia y lleva a distintos desenlaces, así que el final depende de lo que el jugador haya elegido.

## Equipo

Proyecto en parejas:

- Juan Manuel Frías Cortés
- Sara Alexandra Chamorro Cuevas

## Estado

La historia, el arte, la música y los sonidos están listos. Falta programar el juego.

## Qué hay en el repositorio

| Ruta | Qué es |
|---|---|
| `Historia.md` | El guion: 312 fichas de decisión, 6 finales y 5 finales prematuros |
| `Dialogos.md` | Los diálogos de las fichas que ya los tienen |
| `assets/historia/` | `historia.json` y `dialogos.json`, los datos que carga el juego, y `FORMATO.md`, que los explica |
| `assets/personajes/` | 96 personajes en pixel art (normales, oscurecidos y en holograma) |
| `assets/escenarios/` | 36 fondos, fijos y animados a 10 y a 60 cuadros por segundo |
| `assets/escenas/` | Quién aparece en cada ficha y dónde |
| `assets/musica/` | Qué canción suena en cada ficha (los audios no se suben, ver abajo) |
| `assets/sonidos/` | Las voces que suenan al escribir el texto y los sonidos de la interfaz |
| `assets/ejemplos/` | Escenas de ejemplo con diálogo, de la etapa de bocetos |
| `docs/mapa_finales.html` | Mapa de los finales: se abre con doble clic |

Cada carpeta de `assets/` tiene el script de Python que generó su contenido, por si hay que rehacerlo.

## Requisitos

- Python 3.10 o más nuevo
- `pip install -r requirements.txt` (instala pygame)

## Música

Las canciones son de las películas y no se suben al repositorio. Para tenerlas:

1. Bajar cada canción con el link de YouTube que está en `assets/musica/preparar_musica.py` (lista `PISTAS`).
2. Dejar los archivos en la carpeta de Descargas.
3. Correr `python assets/musica/preparar_musica.py --importar`, que las reconoce por su título, las convierte a OGG y las pone en su lugar.

El juego funciona sin música si faltan.

## Aviso

Proyecto académico sin fines de lucro. *Star Wars* y *La Guerra de los Clones* son marcas registradas de Lucasfilm Ltd. y The Walt Disney Company; este proyecto no está afiliado a ellas ni cuenta con su respaldo.
