# Guion de decisiones — *Star Wars: La Guerra de los Clones* (RPG)

> Proyecto final de **Programación en Python** (UAA, Semestre 7) · Juan Manuel Frías Cortés y Sara Alexandra Chamorro Cuevas.
> Documento de trabajo: aquí se escribe y se corrige la historia completa antes de programar el juego.

## Qué es este documento

La historia del juego, escrita como **fichas de decisión**. Cada ficha es un globo de texto en el que el jugador elige qué hacer. El protagonista es **Anakin Skywalker**, pero en algunos momentos el jugador controla a otros personajes (Ahsoka, Obi-Wan, Padmé, Rex, Fives, Yoda…) y lo que ellos deciden también afecta a Anakin.

La historia va desde la Batalla de Christophsis (el inicio de la película *The Clone Wars*, 2008) hasta que Anakin se convierte en Darth Vader. Sigue la **columna canónica**: la película, las siete temporadas de la serie, *La venganza de los Sith* y las novelas y cómics canónicos de la época. Cada decisión puede mantener el canon o mover al jugador hacia otras líneas temporales.

## Cómo leer una ficha

```
#### D025 · La señal de Plo Koon
**Juega:** Anakin · **Fuente:** TCW 1x02 Rising Malevolence

Contexto de la escena…

- **A)** Desobedecer e ir a buscarlos ★ → D026 · AHS +1 · OBI -1
- **B)** Obedecer al Consejo → D027 · AHS -2 · ⚑ PLO_MUERTO
```

- **Juega**: el personaje que controla el jugador en esa ficha.
- **Fuente**: la obra canónica de donde sale la escena. *TCW 1x02* es *The Clone Wars*, temporada 1, episodio 2.
- **Rama**: ficha que no existe en el canon. Aparece justo después de la ficha que la abre y casi siempre regresa a la columna canónica.
- **⟡ Bifurcación mayor**: decisión que cambia el rumbo de la historia a largo plazo.
- **★**: la opción que sigue el canon. Si se elige siempre ★ desde D001, se recorre la historia oficial y se llega al Final 1.
- **→ D026**: la ficha siguiente. **→ FINAL n** o **→ FPn** termina la partida.
- **AHS +1**: suma o resta a un medidor. **⚑ BANDERA**: la prende. ***quita* ⚑ BANDERA**: la apaga.
- ***(si …)*** o ***(requiere …)*** antes de una opción: esa opción solo aparece si se cumple la condición. `≥` es "por lo menos" y `≤` es "como máximo": *OSC ≤ 32* quiere decir que tu oscuridad no pase de 32.
- *(Texto en cursiva dentro del contexto)*: la escena cambia según las banderas activas.

## Contador

**Total: 312 fichas de decisión** (281 en la columna canónica y 31 de rama).

| Acto | Fichas |
|---|---|
| Acto I | 58 |
| Acto II | 68 |
| Acto III | 38 |
| Acto IV | 34 |
| Acto V | 50 |
| Acto VI | 64 |

Siguiendo solo las opciones ★ se recorren 281 fichas y se llega al **FINAL 1**. Los medidores con los que el canon llega al final son: OSC 50 · PAL 26 · OBI 8 · AHS 45 · PAD 12 · CLO 29 · PIS 16.

## Medidores

Siete números que acumulan lo que el jugador ha decidido. Cuando el jugador controla a otro personaje, sus decisiones mueven los mismos medidores: lo que hace Ahsoka cambia su vínculo con Anakin, y lo que descubren Fives, Padmé o Yoda suma pistas.

| Medidor | Nombre | Inicia en | Qué mide |
|---|---|---|---|
| **OSC** | Oscuridad | 2 | Cuánto ha cedido Anakin a la ira, el miedo y el apego |
| **PAL** | Influencia de Palpatine | 3 | Cuánto confía Anakin en el Canciller |
| **OBI** | Vínculo con Obi-Wan | 4 | La relación maestro-alumno |
| **AHS** | Vínculo con Ahsoka | 0 | La relación con su padawan |
| **PAD** | Vínculo con Padmé | 5 | La confianza dentro del matrimonio secreto |
| **CLO** | Lealtad de los clones | 2 | Cuánto confían Rex y el 501.° en Anakin y entre ellos |
| **PIS** | Pistas de la conspiración | 0 | Cuánto saben los buenos sobre Sidious y los chips |

**Umbrales** (provisionales): están calibrados para que el camino canónico **no** los alcance. Para abrirlos hay que jugar distinto del canon.

Desde D273, **toda salida del camino canónico pide una llave**. Así el final depende de cómo jugaste toda la partida y no solo de la última decisión. Quien juega siempre ★ solo puede llegar al Final 1. En las simulaciones de partidas, quien se inclina hacia un personaje o un medidor en un tercio de sus decisiones suele abrir la llave de su camino.

| Ficha | Condición | Qué abre |
|---|---|---|
| D196 | AHS ≥ 35 | Ahsoka puede volver a la Orden |
| D207 | PIS ≥ 12 | Creerle a Fives y llevarlo ante el Consejo |
| D208 | PIS ≥ 15 | Quitar los chips del 501.° |
| D265 | OBI ≥ 15 | Contarle todo a Obi-Wan antes de Utapau |
| D273 | OSC ≥ 35 | Matar a Palpatine en su oficina (emperador) |
| D273, D291, D292 | PAD ≥ 25 | Huir con Padmé o contenerse en Mustafar |
| D275 | OBI ≥ 20 o PIS ≥ 25 | Quedarte y confiar en Mace (luz) |
| D276 | PAD ≥ 25 | Padmé te pide huir esa noche (exilio) |
| D277 | OBI ≥ 20 o PIS ≥ 25 o PAL ≤ 12 | Ayudar a Mace a arrestar a Sidious, o dejar que lo mate (luz) |
| D278 | AHS ≥ 55 | Negarse a arrodillarse ante Sidious (luz) |
| D278 | OSC ≥ 45 | Fingir lealtad para matar a Sidious después (emperador) |
| D280 | OBI ≥ 20 o AHS ≥ 50 | Dudar y salir de la oficina (luz) |
| D285 | OSC ≤ 32 | No poder matar a los iniciados (luz) |
| D290 | PAD ≤ 10 | Padmé no va a Mustafar (Final 2) |
| D293 | OBI ≥ 15 | Bajar el sable ante Obi-Wan (luz) |
| D293 | PAL ≥ 31 | Retirarte y volver con Sidious (Final 2) |
| D296, D308 | PAD ≥ 25 | Huir con Padmé o renunciar al trono por ella (exilio) |
| D298 | PIS ≥ 25 | Cortar la transmisión de la Orden 66 |
| D305 | OBI ≥ 20 | Entregarte al Consejo después de matar a Palpatine (luz) |

## Personajes jugables

| Personaje | Fichas |
|---|---|
| Anakin | 170 |
| Ahsoka | 38 |
| Obi-Wan | 28 |
| Padmé | 23 |
| Rex | 17 |
| Fives | 11 |
| Yoda | 5 |
| Mace Windu | 4 |
| Maul | 4 |
| Asajj Ventress | 3 |
| Quinlan Vos | 3 |
| Waxer | 1 |
| Satine Kryze | 1 |
| Conde Dooku | 1 |
| Barriss Offee | 1 |
| Echo | 1 |
| Caleb Dume | 1 |

## Mapa de la historia

| Acto | Del capítulo… al… | Fichas | Fuentes principales |
|---|---|---|---|
| I · Una nueva aprendiz | Christophsis → Crisis de rehenes | D001–D058 | película *The Clone Wars*, TCW temporada 1 |
| II · Sombras sobre la República | El robo del holocrón → Padawan perdida | D059–D126 | TCW temporadas 2 y 3 |
| III · Guerra sin honor | Umbara → Ecos de Dathomir | D127–D164 | TCW temporada 4 |
| IV · Traiciones | Onderon → El Jedi equivocado | D165–D198 | TCW temporada 5, cómic *Son of Dathomir* |
| V · La conspiración | El chip → El camino de Ahsoka | D199–D248 | TCW temporadas 6 y 7, *Dark Disciple*, *Crystal Crisis on Utapau*, *Thrawn: Alliances* |
| VI · La caída | Batalla de Coruscant → Mustafar y las líneas finales | D249–D312 | *La venganza de los Sith*, TCW temporada 7, *Kanan: The Last Padawan*, *The Bad Batch* |

## Bifurcaciones mayores

| Ficha | Momento | Qué cambia |
|---|---|---|
| D116 | Mortis | Si Anakin conserva el recuerdo de su futuro como Vader (⚑ MORTIS_RECUERDA), se abren opciones de rechazo en el Acto VI |
| D196 | Juicio de Ahsoka | Ahsoka vuelve a la Orden y está con Anakin al final |
| D207 | El almacén | Fives sobrevive y la verdad del chip puede llegar al Consejo |
| D231 | *Discípula oscura* | Dooku muere o se rinde antes de *La venganza de los Sith* |
| D252 | La Mano Invisible | Anakin perdona a Dooku |
| D269 | Asedio de Mandalore | Ahsoka le advierte a Anakin lo que dijo Maul |
| D273 | La revelación | La historia se separa en cuatro líneas: oscura (canon), luz, emperador y exilio |
| D277 | El duelo en la oficina | Mace, Sidious o ninguno de los dos sale vivo |

## Finales

| Final | Nombre | Línea | Se llega por |
|---|---|---|---|
| FINAL 1 | Lord Vader *(canon)* | Oscura | D295 |
| FINAL 2 | Vader sin máscara | Oscura | D294 |
| FINAL 3 | Emperador Skywalker | Emperador | D307, D308 |
| FINAL 4 | El Elegido | Luz | D304 (con la Orden 66 detenida o el Templo salvado) |
| FINAL 5 | La luz que resiste | Luz | D304 (sin eso) |
| FINAL 6 | El exilio | Exilio | D312 |
| FP1–FP5 | Finales prematuros | — | D011, D109, D115, D149, D194, D297 |

El detalle de cada final y sus variantes está en la sección **FINALES**, al final del guion.

## Pendientes para decidir entre los dos

- **Nombre del juego.**
- **¿El jugador ve los medidores?** Pueden mostrarse en pantalla o quedar ocultos para que las consecuencias sorprendan.
- **Escenas fuertes:** la matanza del Templo (D285) y el estrangulamiento de Padmé (D292) son canon y están escritas como decisiones. Hay que confirmar que el tono es aceptable para la entrega.
- **Umbrales:** se calibran cuando el juego se pueda probar. Los valores de arriba son el punto de partida.

# ACTO I — Una nueva aprendiz

*22 ABY. De la Batalla de Christophsis a la crisis de rehenes en el Senado. Anakin recibe a Ahsoka y la guerra todavía parece una aventura.*

## Capítulo 1 · Christophsis

#### D001 · Las ruinas de cristal
**Juega:** Anakin · **Fuente:** película *The Clone Wars* (2008)

Christophsis está sitiada. El ejército droide del almirante Whorm Loathsom avanza entre las torres de cristal y el bloqueo separatista impide que lleguen refuerzos. Obi-Wan te pide sostener la línea hasta el amanecer.

- **A)** Sostener la línea junto a Rex y sus hombres ★ → D002 · CLO +1
- **B)** Saltar solo sobre los droides para ganar tiempo → D002 · OSC +1 · OBI -1
- **C)** Replegarse a la segunda línea, como sugiere Obi-Wan → D002 · OBI +1 · CLO -1

#### D002 · Una padawan inesperada
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

En plena tregua aterriza una lanzadera con una joven togruta: Ahsoka Tano. Trae un mensaje del Maestro Yoda: será tu padawan, no la de Obi-Wan. Tú nunca pediste una.

- **A)** Aceptarla con ironía y ponerla a prueba ★ → D004 · AHS +1
- **B)** Decir que es un error y pedir hablar con Yoda → D003 · AHS -1
- **C)** Recibirla con calidez → D004 · AHS +2

#### D003 · Llamada a Yoda
**Juega:** Anakin · **Rama**

El holograma de Yoda parpadea: "Mucho que enseñarle tienes. Y mucho que aprender de ella, también". Ahsoka escucha todo desde la puerta.

- **A)** Aceptar la orden y disculparte con Ahsoka → D004 · AHS +1
- **B)** Aceptarla de mala gana; que sepa que no la querías → D004 · AHS -1 · ⚑ AHSOKA_A_PRUEBA

#### D004 · El generador del escudo
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Un escudo de energía protege a los droides. Ahsoka encontró un paso entre los escombros hasta el generador, pero es estrecho y no hay vuelta atrás.

- **A)** Dejar que Ahsoka guíe por su paso ★ → D005 · AHS +1
- **B)** Ir tú solo; que Ahsoka se quede con Rex → D005 · AHS -1 · CLO +1

#### D005 · Droidekas
**Juega:** Ahsoka · **Fuente:** película *The Clone Wars*

Dentro del generador, dos droidekas cierran el paso mientras Anakin coloca las cargas. *(Si Anakin la dejó afuera, Ahsoka cubre desde la azotea con Rex.)*

- **A)** Distraer a los droidekas para que Anakin termine ★ → D006 · AHS +1
- **B)** Quedarse oculta, como le ordenaron → D006
- **C)** Lanzarse de frente contra ellos → D006 · AHS +2 · ⚑ AHSOKA_TEMERARIA

#### D006 · Té con el enemigo
**Juega:** Obi-Wan · **Fuente:** película *The Clone Wars*

Para darle tiempo a Anakin, finges negociar una rendición con Loathsom y pides té. El almirante se impacienta.

- **A)** Seguir conversando hasta la señal de Anakin ★ → D007 · OBI +1
- **B)** Atacar antes de la señal → D007 · OBI -1 · CLO -1

#### D007 · Después de la batalla
**Juega:** Anakin

Christophsis es de la República. Ahsoka arriesgó demasiado, pero sin ella no lo habrían logrado. Obi-Wan te pregunta qué piensas de tu nueva padawan. *(Si ⚑ AHSOKA_A_PRUEBA, Ahsoka espera que la regreses al Templo.)*

- **A)** Regañarla en privado, pero reconocer su talento ★ → D008 · AHS +1
- **B)** Decirle a Obi-Wan que no está lista → D008 · AHS -2 · OBI +1
- **C)** Celebrar con ella y restarle importancia al riesgo → D008 · AHS +2 · OBI -1 · *quita* ⚑ AHSOKA_A_PRUEBA

#### D008 · Un mensaje privado
**Juega:** Anakin

Llega la orden del Consejo: el hijo de Jabba el Hutt fue secuestrado y hay que rescatarlo. Al mismo tiempo entra un mensaje privado del Canciller Palpatine para felicitarte por Christophsis.

- **A)** Dejar el mensaje para después e ir directo a la misión ★ → D009
- **B)** Contestar al Canciller; dice que el Consejo no ve lo que vales → D009 · PAL +1
- **C)** Contestar y luego contarle a Obi-Wan lo que te dijo → D009 · PAL +1 · OBI +1

## Capítulo 2 · Teth

#### D009 · El acantilado del monasterio
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Rotta, el hijo de Jabba, está en un monasterio B'omarr en lo alto de un acantilado de Teth. Los AT-TE trepan la pared de roca bajo fuego droide.

- **A)** Subir junto a los caminantes y los clones ★ → D010 · CLO +1
- **B)** Adelantarte con Ahsoka para limpiar las torretas → D010 · AHS +1 · CLO -1
- **C)** Esperar apoyo aéreo antes de subir → D010 · ⚑ ROTTA_GRAVE

#### D010 · El huttlet
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Encuentran a Rotta solo, enfermo y llorando. Demasiado fácil.

- **A)** Cargarlo y salir de inmediato ★ → D011
- **B)** Tomarte el tiempo de atenderlo con el botiquín → D011 · AHS +1 · *quita* ⚑ ROTTA_GRAVE
- **C)** Revisar el monasterio antes de irse → D011 · PIS +1 *(un registro droide muestra que alguien quería culpar a los Jedi)*

#### D011 · La trampa de Ventress
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Los droides rodean el monasterio y destruyen tus naves. Asajj Ventress se burla por holograma: "Los Hutts creerán que los Jedi mataron al niño".

- **A)** Correr al hangar: hay una nave vieja, la *Twilight* ★ → D013
- **B)** Hacerte fuerte en las murallas → D012
- **C)** Dejar a Rotta y sacar con vida a tus clones → FP1

#### D012 · Las murallas
**Juega:** Anakin · **Rama**

Los clones caen uno tras otro mientras siguen llegando droides.

- **A)** Ordenar la retirada al hangar → D013 · CLO -1
- **B)** Destrozar droides con furia hasta abrir paso → D013 · OSC +2 · CLO +1

#### D013 · Duelo en Teth
**Juega:** Obi-Wan · **Fuente:** película *The Clone Wars*

Llegas con refuerzos y encuentras a Ventress en el patio. Anakin y Ahsoka siguen dentro.

- **A)** Cubrir la huida de Anakin y dejar escapar a Ventress ★ → D014 · OBI +1
- **B)** Perseguir a Ventress hasta su nave → D014 · PIS +1 *(la escuchas informar al Conde Dooku)*

#### D014 · La Twilight
**Juega:** Ahsoka · **Fuente:** película *The Clone Wars*

R2 intenta arrancar la nave mientras los droides entran al hangar. Alguien tiene que contener la puerta.

- **A)** Contener la puerta con el sable ★ → D015 · AHS +1
- **B)** Tirar la grúa del hangar para bloquear el paso → D015 · CLO +1

#### D015 · Rumbo a Tatooine
**Juega:** Anakin

Rotta empeora. Ahsoka sugiere desviarse a una fragata médica; el Canciller pide que lo mantengas informado.

- **A)** Ir directo a Tatooine ★ → D016
- **B)** Desviarse a la fragata médica → D016 · AHS +1 · *quita* ⚑ ROTTA_GRAVE
- **C)** Informar primero al Canciller → D016 · PAL +1

#### D016 · Estrellados en el desierto
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Los cazas separatistas derriban la *Twilight* sobre las dunas. Hay que llegar a pie al palacio de Jabba, y Dooku los espera.

- **A)** Tú cargas a Rotta; Ahsoka se lleva el señuelo ★ → D017
- **B)** Ahsoka carga a Rotta; tú haces de señuelo → D017 · AHS +2 · ⚑ AHSOKA_LLEVA_ROTTA

## Capítulo 3 · Tatooine y Coruscant

#### D017 · Dooku en las dunas
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

El Conde Dooku te cierra el paso. *(Si ⚑ AHSOKA_LLEVA_ROTTA, cargas el señuelo y Dooku tarda en notarlo.)* "Tu ira te hace fuerte, joven Skywalker".

- **A)** Defenderte lo justo y escapar ★ → D018
- **B)** Pelear en serio para derrotarlo → D018 · OSC +2
- **C)** Calmarte, provocar un derrumbe de arena con la Fuerza y huir → D018 · OSC -1

#### D018 · MagnaGuardias
**Juega:** Ahsoka · **Fuente:** película *The Clone Wars*

Dos MagnaGuardias de Dooku alcanzan a Ahsoka. *(Si ⚑ AHSOKA_LLEVA_ROTTA, el niño va en su espalda.)*

- **A)** Pelear de frente para ganar tiempo ★ → D019 · AHS +1
- **B)** Esconderse en un cañón y dejar un rastro falso → D019

#### D019 · El palacio de Ziro
**Juega:** Padmé · **Fuente:** película *The Clone Wars*

Padmé sospecha de Ziro, tío de Jabba, y va a su palacio en Coruscant con C-3PO. Lo oye hablar con Dooku por holograma: él organizó el secuestro.

- **A)** Seguir escuchando escondida y grabarlo ★ → D020 · PIS +1
- **B)** Salir a pedir escolta de clones antes de actuar → D021

#### D020 · Atrapada
**Juega:** Padmé · **Fuente:** película *The Clone Wars*

Ziro la descubre y la encierra. C-3PO sigue libre.

- **A)** Ganar tiempo con Ziro mientras 3PO llama a los clones ★ → D022 · PAD +1
- **B)** Intentar escapar sola → D022 · ⚑ PADME_HERIDA

#### D021 · Sin pruebas
**Juega:** Padmé · **Rama**

Cuando vuelve con la escolta, Ziro ya borró todo. No hay grabación que convenza a Jabba.

- **A)** Pedir al Canciller que interceda ante los Hutts → D022 · PAL +1 · ⚑ ZIRO_ESCAPA
- **B)** Confiar en que Anakin convenza a Jabba en persona → D022 · PAD +1 · ⚑ ZIRO_ESCAPA

#### D022 · El trono de Jabba
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Entregas a Rotta. Jabba te acusa de haberlo dañado y ordena ejecutarte. *(Si ⚑ ROTTA_GRAVE sigue activa, Jabba está todavía más furioso.)*

- **A)** Mantener la calma y esperar la prueba de Padmé ★ → D023 · PAD +1
- **B)** Amenazar a Jabba con el sable → D023 · OSC +1
- **C)** *(si ⚑ ZIRO_ESCAPA)* Ofrecer a Jabba la cabeza de Ziro a cambio del tratado → D023 · OSC +1 · PIS +1

#### D023 · Hutts y República
**Juega:** Anakin · **Fuente:** película *The Clone Wars*

Jabba acepta el tratado: la República podrá usar sus rutas hiperespaciales. Padmé aparece en el holograma para cerrarlo, y Ahsoka está a tu lado.

- **A)** Agradecerle con formalidad de senadora ★ → D024
- **B)** Dejar escapar un "te extrañé" frente a Ahsoka → D024 · PAD +1 · ⚑ AHSOKA_SOSPECHA
- **C)** *(si ⚑ PADME_HERIDA)* Exigir saber quién la lastimó → D024 · OSC +1 · PAD +1 · ⚑ AHSOKA_SOSPECHA

#### D024 · Arena de Tatooine
**Juega:** Anakin

Antes de despegar, Ahsoka nota que miras el horizonte. Aquí creciste como esclavo; aquí murió tu madre.

- **A)** Cambiar de tema y despegar ★ → D025
- **B)** Contarle a Ahsoka de tu madre → D025 · AHS +2
- **C)** Recordar a los tusken y apretar los puños → D025 · OSC +1

## Capítulo 4 · La Malevolencia

#### D025 · La señal de Plo Koon
**Juega:** Anakin · **Fuente:** TCW 1x02 *Rising Malevolence*

Un arma de iones nueva destruyó la flota del Maestro Plo Koon. El Consejo ordena no buscar sobrevivientes porque es demasiado peligroso. Ahsoka te mira: Plo fue quien la encontró de niña.

- **A)** Desobedecer e ir a buscarlos ★ → D026 · AHS +1 · OBI -1
- **B)** Obedecer al Consejo → D027 · AHS -2 · ⚑ PLO_MUERTO
- **C)** Pedir permiso directo al Canciller → D026 · PAL +2

#### D026 · La cápsula
**Juega:** Anakin · **Fuente:** TCW 1x02 *Rising Malevolence*

Encuentran la cápsula de Plo con tres clones vivos, justo cuando la *Malevolencia* regresa a rematarlos.

- **A)** Rescatar a todos y huir por los pelos ★ → D028 · CLO +1
- **B)** Dejar que Ahsoka pilotee mientras tú cubres con los cañones → D028 · AHS +1

#### D027 · Sin sobrevivientes
**Juega:** Ahsoka · **Rama**

Plo Koon muere en el espacio. Ahsoka se encierra en su cabina. *(A partir de aquí, las escenas canónicas de Plo las hace Kit Fisto.)*

- **A)** Culpar a Anakin por obedecer → D028 · AHS -1
- **B)** Aceptar el dolor y entrenar más duro → D028 · AHS +1

#### D028 · Escuadrón Sombra
**Juega:** Anakin · **Fuente:** TCW 1x03 *Shadow of Malevolence*

Lideras bombarderos Y-wing contra la *Malevolencia*. La ruta corta pasa por una nebulosa llena de neebrays.

- **A)** Cruzar la nebulosa ★ → D029 · CLO +1
- **B)** Atacar de frente → D029 · CLO -2

#### D029 · El yate de Padmé
**Juega:** Padmé · **Fuente:** TCW 1x04 *Destroy Malevolence*

El yate de Padmé cae en el rayo tractor de Grievous. Ella nota algo raro: su ruta pasaba justo por donde estaba la *Malevolencia*.

- **A)** Esconderse con 3PO y enviar coordenadas a Anakin ★ → D030 · PAD +1
- **B)** Revisar quién trazó su ruta antes de que la capturen → D030 · PIS +1 · ⚑ PADME_DUDA_RUTA

#### D030 · A bordo de la Malevolencia
**Juega:** Anakin · **Fuente:** TCW 1x04 *Destroy Malevolence*

Obi-Wan y tú abordan la nave. Hay que destruir el hiperimpulsor antes de que Grievous huya, pero Padmé está en otro sector.

- **A)** Ir primero por Padmé ★ → D031 · PAD +1 · OBI -1
- **B)** Sabotear el hiperimpulsor con Obi-Wan primero → D031 · OBI +1 · PAD -1

#### D031 · Grievous huye
**Juega:** Obi-Wan · **Fuente:** TCW 1x04 *Destroy Malevolence*

La *Malevolencia* va directo a estrellarse contra una luna y Grievous corre a su nave de escape.

- **A)** Dejarlo ir y sacar a todos a tiempo ★ → D032 · OBI +1
- **B)** Perseguirlo hasta el último segundo → D032 · CLO -1 · OBI -1

#### D032 · Felicitaciones del Canciller
**Juega:** Anakin

Palpatine te recibe en su oficina: "Arriesgaste todo por la senadora Amidala. Eso no es debilidad, Anakin; es lo que el Consejo nunca entenderá".

- **A)** Aceptar el elogio y sus invitaciones a conversar ★ → D033 · PAL +1
- **B)** Agradecer con cortesía y guardar distancia → D033 · PAL -1 · OBI +1
- **C)** *(si ⚑ PADME_DUDA_RUTA)* Preguntarle quién trazó la ruta de Padmé → D033 · PIS +1 · PAL -1

## Capítulo 5 · R2 perdido

#### D033 · Bothawui
**Juega:** Anakin · **Fuente:** TCW 1x06 *Downfall of a Droid*

En la batalla de Bothawui pierdes a R2-D2, que lleva en la memoria todos tus códigos y tácticas. Obi-Wan dice que es solo un droide.

- **A)** Ir a buscarlo, digan lo que digan ★ → D034 · OBI -1
- **B)** Dejarlo y aceptar al droide nuevo, R3-S6 → D036 · OBI +1 · ⚑ R2_PERDIDO

#### D034 · El chatarrero
**Juega:** Anakin · **Fuente:** TCW 1x07 *Duel of the Droids*

El chatarrero Gha Nachkt le vendió a R2 a Grievous. Está en la estación Skytop.

- **A)** Infiltrarte con Ahsoka y R3 ★ → D035
- **B)** Asaltar la estación con Rex → D035 · CLO +1 · AHS -1

#### D035 · Ahsoka contra Grievous
**Juega:** Ahsoka · **Fuente:** TCW 1x07 *Duel of the Droids*

Mientras Anakin busca a R2, Grievous en persona sale a cazar a Ahsoka.

- **A)** Esquivarlo y huir al punto de encuentro ★ → D037 · AHS +1
- **B)** Plantarle cara en duelo → D037 · AHS +1 · ⚑ AHSOKA_TEMERARIA

#### D036 · Sin R2
**Juega:** Anakin · **Rama**

R3-S6 resulta ser un espía de Grievous y la flota cae en una emboscada.

- **A)** Usar a R3 como cebo para llegar hasta Grievous y recuperar a R2 → D037 · CLO +1 · *quita* ⚑ R2_PERDIDO
- **B)** Culpar al Consejo por no dejarte buscarlo → D037 · OSC +1 · OBI -1

#### D037 · Reunión
**Juega:** Anakin

*(Si ⚑ R2_PERDIDO sigue activa, la escena es con R3 desactivado y R2 no vuelve en el resto del juego.)* Los técnicos quieren borrarle la memoria a R2 por seguridad.

- **A)** Negarte: R2 se queda como está ★ → D038
- **B)** Permitir el borrado → D038 · OBI +1 · AHS -1

## Capítulo 6 · Los novatos

#### D038 · La luna de Rishi
**Juega:** Rex · **Fuente:** TCW 1x05 *Rookies*

Rex y Cody inspeccionan un puesto de escucha. Droides comando lo tomaron; solo quedan tres novatos vivos: Hevy, Echo y Fives.

- **A)** Retomar la base con los novatos ★ → D039 · CLO +1
- **B)** Retomarla solo con Cody; los novatos esperan → D039 · CLO -1

#### D039 · El plan de Rex
**Juega:** Fives · **Fuente:** TCW 1x05 *Rookies*

Rex propone disfrazarse con cabezas de droide para engañar a los comandos. Echo quiere seguir el reglamento al pie de la letra.

- **A)** Seguir el plan de Rex ★ → D040 · CLO +1
- **B)** Seguir a Echo y el reglamento → D040

#### D040 · Hevy
**Juega:** Rex · **Fuente:** TCW 1x05 *Rookies*

La flota separatista se acerca. Alguien tiene que quedarse a volar la base y Hevy se ofrece.

- **A)** Dejar que Hevy se quede ★ → D041 · CLO +1
- **B)** Volver por Hevy aunque la base explote tarde → D041 · CLO +2 · ⚑ HEVY_VIVE

#### D041 · Los nombres
**Juega:** Anakin

Rex te cuenta lo de Rishi y te pide que recuerdes los nombres de los novatos. "No somos números, señor".

- **A)** Aprender sus nombres y tratarlos como personas ★ → D042 · CLO +2
- **B)** "Son soldados, Rex. Así sobreviven" → D042 · CLO -1

## Capítulo 7 · Ryloth

#### D042 · El mando del escuadrón
**Juega:** Anakin · **Fuente:** TCW 1x19 *Storm Over Ryloth*

Para romper el bloqueo de Ryloth hace falta alguien al frente de los bombarderos del Escuadrón Azul. Ahsoka quiere el mando.

- **A)** Darle el mando a Ahsoka ★ → D043 · AHS +1
- **B)** Dirigir tú el escuadrón → D045 · AHS -1 · CLO +1

#### D043 · Romper el bloqueo
**Juega:** Ahsoka · **Fuente:** TCW 1x19 *Storm Over Ryloth*

El ataque va mal. Axe, su líder de vuelo, pide retirarse; Anakin le dijo que retroceder también es una opción.

- **A)** Insistir en el ataque ★ → D044 · CLO -2 · ⚑ AHSOKA_CULPA
- **B)** Ordenar la retirada a tiempo → D045 · AHS +1 · CLO +1
- **C)** *(si ⚑ AHSOKA_TEMERARIA)* Lanzarse ella misma contra la fragata → D044 · CLO -3 · ⚑ AHSOKA_CULPA

#### D044 · La lección
**Juega:** Anakin · **Fuente:** TCW 1x19 *Storm Over Ryloth*

Ahsoka perdió a casi todo el Escuadrón Azul y no quiere volver a mandar a nadie.

- **A)** "Vas a perder hombres. Hay que seguir", y devolverle el mando ★ → D045 · AHS +2 · *quita* ⚑ AHSOKA_CULPA
- **B)** Quitarle el mando → D045 · AHS -2
- **C)** Culpar al Consejo por darte una niña en plena guerra → D045 · AHS +1 · OSC +1 · OBI -1

#### D045 · La Defensora
**Juega:** Anakin · **Fuente:** TCW 1x19 *Storm Over Ryloth*

Tu crucero, la *Defensora*, está deshecho, pero puede abrir el bloqueo si lo lanzas contra la fragata separatista.

- **A)** Evacuar y lanzar la nave ★ → D046 · CLO +1
- **B)** Intentar salvar la nave → D046 · CLO -1

#### D046 · Los inocentes
**Juega:** Obi-Wan · **Fuente:** TCW 1x20 *Innocents of Ryloth*

En tierra, el droide TX-20 usa a los civiles twi'lek como escudo para sus cañones.

- **A)** Avanzar despacio para proteger a los civiles ★ → D047 · CLO +1
- **B)** Avanzar rápido y aceptar el riesgo → D047 · CLO -1 · ⚑ CIVILES_MUERTOS

#### D047 · Numa
**Juega:** Waxer · **Fuente:** TCW 1x20 *Innocents of Ryloth*

Waxer y Boil encuentran a Numa, una niña twi'lek que conoce túneles bajo la ciudad. Boil no confía en ella.

- **A)** Seguir a Numa por los túneles ★ → D048 · CLO +1
- **B)** Hacerle caso a Boil y avanzar por la superficie → D048 · CLO -1

#### D048 · Cham Syndulla
**Juega:** Mace Windu · **Fuente:** TCW 1x21 *Liberty on Ryloth*

Para liberar Lessu necesitas a la guerrilla de Cham Syndulla, que ve a la República como otro invasor. *(Si ⚑ CIVILES_MUERTOS, Cham desconfía todavía más.)*

- **A)** Prometer que Ryloth decidirá su propio futuro ★ → D049
- **B)** Ordenarle que obedezca a la República → D049 · CLO -1

#### D049 · Wat Tambor
**Juega:** Mace Windu · **Fuente:** TCW 1x21 *Liberty on Ryloth*

Lessu es libre y el emir Wat Tambor está capturado. Cham quiere ejecutarlo en la plaza.

- **A)** Llevarlo a juicio en la República ★ → D050
- **B)** Entregárselo a Cham → D050 · ⚑ TAMBOR_EJECUTADO

#### D050 · La mano firme
**Juega:** Anakin

De vuelta en Coruscant, Palpatine comenta lo de Ryloth: "A veces la democracia necesita una mano firme para sobrevivir".

- **A)** Darle la razón a medias ★ → D051 · PAL +1
- **B)** "Los twi'leks merecen gobernarse solos" → D051 · PAL -1 · PAD +1

#### D051 · Una noche con Padmé
**Juega:** Anakin

Visitas a Padmé en secreto. Te pregunta cómo estás de verdad.

- **A)** Contarle la verdad sobre lo que viste ★ → D052 · PAD +1
- **B)** Esconder tu enojo para no preocuparla → D052 · OSC +1
- **C)** Decirle que algún día dejarás la Orden por ella → D052 · PAD +2 · ⚑ ANAKIN_DUDA_ORDEN

## Capítulo 8 · Crisis de rehenes

#### D052 · El edificio del Senado
**Juega:** Anakin · **Fuente:** TCW 1x22 *Hostage Crisis*

Estás en el Senado sin tu sable (lo dejaste en la oficina de Padmé) cuando Cad Bane y sus mercenarios toman el edificio. Exigen la liberación de Ziro el Hutt. *(Si ⚑ ZIRO_ESCAPA, Ziro sigue libre y Bane exige la de sus socios presos.)*

- **A)** Esconderte y observar ★ → D053
- **B)** Atacar de inmediato, sin sable → D053 · OSC +1 · CLO -1

#### D053 · Las bombas
**Juega:** Anakin · **Fuente:** TCW 1x22 *Hostage Crisis*

Bane coloca explosivos en el edificio. Puedes arrastrarte por los ductos para desactivarlos o salir a enfrentarlo.

- **A)** Desactivarlos en silencio ★ → D054
- **B)** Enfrentar a Bane y sus hombres → D054 · OSC +1 · PAD -1

#### D054 · El sable
**Juega:** Padmé · **Fuente:** TCW 1x22 *Hostage Crisis*

Bane encuentra el sable de Anakin entre las cosas de Padmé y sospecha que hay un Jedi cerca.

- **A)** Fingir que es un recuerdo y no decir nada ★ → D055 · PAD +1
- **B)** Hacerle llegar el sable a Anakin a escondidas → D055 · PAD +1 · ⚑ SABLE_RECUPERADO

#### D055 · El Canciller cede
**Juega:** Anakin · **Fuente:** TCW 1x22 *Hostage Crisis*

Palpatine acepta liberar a Ziro para salvar a los senadores. Bane saldrá del edificio usando rehenes como escudo.

- **A)** Dejarlos salir para no arriesgar a los rehenes ★ → D056
- **B)** Seguirlos de cerca aunque Bane lo note → D056 · OSC +1 · PAD -1

#### D056 · La plataforma
**Juega:** Anakin · **Fuente:** TCW 1x22 *Hostage Crisis*

En la plataforma, Bane activa un detonador conectado a los rehenes y escapa.

- **A)** Desactivar las bombas con ayuda de Padmé ★ → D057 · PAD +1
- **B)** Ir tras Bane y dejar las bombas a Padmé → D057 · PAD -1 · OSC +1
- **C)** *(si ⚑ SABLE_RECUPERADO)* Enfrentar a Bane con tu sable antes de que despegue → D057 · ⚑ BANE_CAPTURADO

#### D057 · Ziro libre
**Juega:** Anakin

La política acaba de soltar a un criminal. Estás furioso y necesitas hablar con alguien.

- **A)** Desahogarte con Palpatine ★ → D058 · PAL +1 · OSC +1
- **B)** Hablar con Obi-Wan → D058 · OBI +1
- **C)** Hablar con Padmé → D058 · PAD +1

#### D058 · Preguntas de padawan
**Juega:** Anakin

Ahsoka nota que desapareces algunas noches. *(Si ⚑ AHSOKA_SOSPECHA, ya tiene una idea de a dónde vas.)*

- **A)** Mentirle ★ → D059
- **B)** "Visito a una vieja amiga" → D059 · AHS +1 · ⚑ AHSOKA_SOSPECHA
- **C)** Contarle todo sobre Padmé → D059 · AHS +2 · ⚑ AHSOKA_SABE

# ACTO II — Sombras sobre la República

*22–21 ABY. Del robo del holocrón a la isla de los cazadores trandoshanos. La guerra se vuelve personal: Clovis, Satine, Mortis y la primera visión de lo que Anakin podría llegar a ser.*

## Capítulo 9 · El robo del holocrón

#### D059 · Guardia en el Archivo
**Juega:** Ahsoka · **Fuente:** TCW 2x01 *Holocron Heist*

Como castigo por imprudente, Ahsoka hace guardia en el Archivo del Templo con la Maestra Jocasta Nu. Esa noche alguien se cuela para robar un holocrón. *(Si ⚑ BANE_CAPTURADO, es Cad Bane: escapó de prisión hace una semana y nadie sabe quién pagó para sacarlo.)*

- **A)** Perseguir sola el ruido que oyó ★ → D060 · AHS +1
- **B)** Dar la alarma a los guardias del Templo → D060
- **C)** *(si ⚑ BANE_CAPTURADO)* Pedir al Consejo que investigue quién liberó a Bane → D060 · PIS +2

#### D060 · El cristal de memoria
**Juega:** Anakin · **Fuente:** TCW 2x02 *Cargo of Doom*

Bane robó además un cristal kyber con la lista de todos los niños sensibles a la Fuerza de la galaxia. Su nave escapa de Bothawui.

- **A)** Abordar la nave de Bane con Ahsoka ★ → D061
- **B)** Abordarla solo y dejar a Ahsoka al mando de la fragata → D061 · AHS -1 · CLO +1

#### D061 · Abrir el holocrón
**Juega:** Anakin · **Fuente:** TCW 2x02 *Cargo of Doom*

Bane atrapa a Ahsoka y le apunta a la cabeza: o abres el holocrón para él o la mata.

- **A)** Abrir el holocrón para salvarla ★ → D062 · AHS +2 · OSC +1
- **B)** Negarte y confiar en que ella se libere sola → D062 · AHS -1 · OBI +1

#### D062 · El interrogatorio
**Juega:** Anakin · **Fuente:** TCW 2x03 *Children of the Force*

Bane ya secuestró a varios bebés sensibles a la Fuerza y está preso en el crucero. No piensa hablar. Obi-Wan y Mace proponen unir sus mentes con la tuya para obligarlo.

- **A)** Unir tu mente a las de ellos aunque le duela ★ → D063 · OSC +1 · OBI +1
- **B)** Estrangularlo con la Fuerza hasta que hable → D063 · OSC +3 · PIS +1

#### D063 · La instalación de Mustafar
**Juega:** Anakin · **Fuente:** TCW 2x03 *Children of the Force*

La pista lleva a Mustafar. Dentro, un holograma encapuchado da órdenes: convertir a los niños en espías al servicio de los Sith.

- **A)** Asaltar la instalación sin perder tiempo ★ → D064 · CLO +1
- **B)** Esperar oculto y escuchar al encapuchado → D064 · PIS +2 · ⚑ SIDIOUS_VISTO *(su voz te parece conocida)*

#### D064 · El último niño
**Juega:** Ahsoka · **Fuente:** TCW 2x03 *Children of the Force*

Bane huye en una nave y un bebé quedó atrás en la sala que se incendia.

- **A)** Salvar al niño ★ → D065 · AHS +1
- **B)** Perseguir a Bane → D065 · AHS -1 · PIS +1

#### D065 · El informe
**Juega:** Obi-Wan

Viste lo cerca que estuvo Anakin de cruzar una línea con Bane. El Consejo quiere tu informe.

- **A)** Hablarlo con Anakin en privado ★ → D066 · OBI +1
- **B)** Informar al Consejo de todo → D066 · OBI -1 · ⚑ CONSEJO_VIGILA

#### D066 · Los niños de la Fuerza
**Juega:** Anakin

Palpatine comenta el caso: "Los Jedi también se llevan a los niños de sus familias, ¿no es así? Tú lo sabes mejor que nadie".

- **A)** Pensar que tal vez tiene razón ★ → D067 · PAL +1
- **B)** Defender a la Orden → D067 · PAL -1 · OBI +1
- **C)** Pensar en tu madre → D067 · OSC +1

## Capítulo 10 · El espía del Senado

#### D067 · Rush Clovis
**Juega:** Anakin · **Fuente:** TCW 2x04 *Senate Spy*

El Consejo pide a Padmé que espíe al senador Rush Clovis, con quien tuvo una relación, porque sospechan que ayuda a los separatistas. Tú serás su piloto.

- **A)** Objetar, pero aceptar la misión ★ → D068 · OSC +1
- **B)** Pedirle a Padmé que no vaya → D068 · PAD -1
- **C)** Confiar en ella por completo → D068 · PAD +2

#### D068 · Cato Neimoidia
**Juega:** Padmé · **Fuente:** TCW 2x04 *Senate Spy*

Clovis lleva a Padmé a una cena en Cato Neimoidia y le coquetea. Ella necesita entrar a la fundición de droides.

- **A)** Seguirle el juego para conseguir los datos ★ → D069 · PIS +1
- **B)** Romper la fachada y regresar → D069 · PAD +1

#### D069 · El beso
**Juega:** Anakin · **Fuente:** TCW 2x04 *Senate Spy*

Desde la nave ves por la transmisión cómo Clovis besa a Padmé.

- **A)** Aguantar y reclamárselo después ★ → D070 · OSC +1 · PAD -1
- **B)** Entrar y golpear a Clovis → D070 · OSC +2 · ⚑ CLOVIS_RESENTIDO
- **C)** Confiar en ella y no moverte → D070 · PAD +1 · OSC -1

#### D070 · El antídoto
**Juega:** Anakin · **Fuente:** TCW 2x04 *Senate Spy*

Nute Gunray envenenó a Padmé y Clovis tiene el antídoto.

- **A)** Amenazar a Clovis hasta que lo entregue ★ → D071 · OSC +1
- **B)** Convencerlo de que Gunray también lo va a traicionar → D071 · PIS +1
- **C)** Golpearlo hasta que hable → D071 · OSC +2 · ⚑ CLOVIS_RESENTIDO

#### D071 · La discusión
**Juega:** Anakin · **Fuente:** TCW 2x04 *Senate Spy*

En Coruscant, Padmé está molesta: "No puedo hacer mi trabajo si dudas de mí".

- **A)** Disculparte ★ → D072 · PAD +1
- **B)** Insistir en que se equivocó → D072 · PAD -2 · OSC +1
- **C)** Proponerle hacer público el matrimonio → D072 · PAD +1 · ⚑ ANAKIN_DUDA_ORDEN

## Capítulo 11 · Segunda Batalla de Geonosis

#### D072 · Punto Lluvia
**Juega:** Anakin · **Fuente:** TCW 2x05 *Landing at Point Rain*

La República vuelve a Geonosis. Ki-Adi-Mundi te reta a ver quién destruye más droides; Luminara pide apoyo en su flanco.

- **A)** Aceptar el reto de Ki-Adi ★ → D073 · CLO +1
- **B)** Cubrir el flanco de Luminara aunque pierdas la apuesta → D073 · OBI +1

#### D073 · La fábrica
**Juega:** Ahsoka · **Fuente:** TCW 2x06 *Weapons Factory*

Ahsoka y Barriss Offee entran a la fábrica de droides de Poggle. Barriss es disciplinada y metódica; Ahsoka quiere improvisar.

- **A)** Seguir el plan de Barriss ★ → D074 · ⚑ BARRISS_AMIGA
- **B)** Imponer su propio plan → D074 · AHS +1

#### D074 · Enterradas
**Juega:** Anakin · **Fuente:** TCW 2x06 *Weapons Factory*

La fábrica explota con Ahsoka y Barriss dentro. Luminara te pide aceptarlo: "Tienes que dejarla ir".

- **A)** Excavar con la Fuerza hasta encontrarlas ★ → D075 · AHS +2 · OSC +1
- **B)** Aceptar la pérdida → D075 · AHS -2 · OBI +1 *(sobreviven igual, y Ahsoka sabe que te rendiste)*

#### D075 · Las catacumbas
**Juega:** Obi-Wan · **Fuente:** TCW 2x07 *Legacy of Terror*

Rescatan a Luminara de las catacumbas de la reina Karina, donde gusanos controlan a los geonosianos muertos.

- **A)** Sellar las catacumbas ★ → D076
- **B)** Llevarse una muestra de los gusanos para estudiarla → D076 · ⚑ MUESTRA_GUSANOS

#### D076 · Gusanos cerebrales
**Juega:** Ahsoka · **Fuente:** TCW 2x08 *Brain Invaders*

En una nave médica, los gusanos infectan a los clones y a Barriss, que ataca a Ahsoka y le suplica: "¡Mátame antes de que te mate!".

- **A)** Negarse a matarla y resistir ★ → D077 · AHS +1 · ⚑ BARRISS_AMIGA
- **B)** Dejarla inconsciente con la Fuerza, aunque la lastime → D077

#### D077 · El frío
**Juega:** Anakin · **Fuente:** TCW 2x08 *Brain Invaders*

Obi-Wan descubre que el frío mata a los gusanos. Ahsoka debe bajar la temperatura de la nave, pero no contesta.

- **A)** Confiar en que lo logre ★ → D078 · AHS +1
- **B)** Volar hasta la nave aunque Obi-Wan te lo prohíba → D078 · OBI -1 · OSC +1
- **C)** *(si ⚑ MUESTRA_GUSANOS)* Mandarle a Ahsoka los datos de la muestra → D078 · AHS +1 · OBI +1

#### D078 · Las dudas de Barriss
**Juega:** Ahsoka

Ya a salvo, Barriss le confiesa algo: "¿No te parece que ya no somos guardianes de la paz, sino soldados?".

- **A)** Darle la razón, pero decirle que hay que seguir ★ → D079 · ⚑ BARRISS_AMIGA
- **B)** "Los Jedi hacemos lo correcto" → D079
- **C)** Contarle a Anakin lo que dijo Barriss → D079 · AHS +1 · ⚑ BARRISS_VIGILADA

#### D079 · Poggle el Menor
**Juega:** Anakin

Poggle está capturado. El Canciller pide que tú lo lleves personalmente a Coruscant.

- **A)** Aceptar ★ → D080 · PAL +1
- **B)** Que lo lleve Luminara, como pide el Consejo → D080 · OBI +1

## Capítulo 12 · Mandalore

#### D080 · La duquesa
**Juega:** Obi-Wan · **Fuente:** TCW 2x12 *The Mandalore Plot*

En Mandalore investigas a la Guardia de la Muerte y te reencuentras con la duquesa Satine Kryze, a quien amaste de joven.

- **A)** Protegerla sin admitir lo que sientes ★ → D081
- **B)** Confesarle que la sigues queriendo → D081 · ⚑ OBI_SATINE

#### D081 · El Coronet
**Juega:** Anakin · **Fuente:** TCW 2x13 *Voyage of Temptation*

Escoltas a Satine en el crucero *Coronet* y escuchas a escondidas: "Si me hubieras dicho una palabra, habría dejado la Orden por ti", le dice Obi-Wan.

- **A)** Burlarte de Obi-Wan ★ → D082 · OBI +1
- **B)** Preguntarle en serio si habría dejado la Orden → D082 · OBI +2 · ⚑ OBI_CONFIESA_SATINE
- **C)** Callarte y guardar el dato para usarlo después → D082 · OSC +1

#### D082 · El traidor del Coronet
**Juega:** Anakin · **Fuente:** TCW 2x13 *Voyage of Temptation*

El senador Tal Merrik es de la Guardia de la Muerte. Toma a Satine de rehén y exige que Obi-Wan se rinda.

- **A)** Atacar a Merrik por la espalda ★ → D083 · OSC +1 · OBI +1
- **B)** Negociar con él → D083 · OBI -1 *(Merrik escapa y sabotea los motores)*

#### D083 · La duquesa acusada
**Juega:** Obi-Wan · **Fuente:** TCW 2x14 *Duchess of Mandalore*

Satine está acusada de asesinato en Coruscant y huye. Ayudarla te pone fuera de las reglas.

- **A)** Ayudarla de lejos, como Jedi ★ → D084
- **B)** Esconderla tú mismo → D084 · ⚑ OBI_SATINE

#### D084 · La pregunta
**Juega:** Anakin

De vuelta en el Templo lo piensas: Obi-Wan amó a alguien y siguió siendo Jedi.

- **A)** No decir nada ★ → D085
- **B)** Contarle a Obi-Wan lo de Padmé → D085 · OBI +2 · ⚑ OBI_SABE_MATRIMONIO
- **C)** *(si ⚑ OBI_CONFIESA_SATINE o ⚑ OBI_SATINE)* Preguntarle cómo logró dejarla ir → D085 · OBI +1 · OSC -1

## Capítulo 13 · Cazados

#### D085 · Atrapados en Vanqor
**Juega:** Anakin · **Fuente:** TCW 2x20 *Death Trap*

Boba Fett, infiltrado entre cadetes clon, quería matar a Mace Windu para vengar a su padre. El *Endurance* se estrella en Vanqor y Mace y tú quedan atrapados bajo los escombros.

- **A)** Mandar a R2 por ayuda ★ → D086
- **B)** *(si ⚑ R2_PERDIDO)* Arrastrarte herido a buscar ayuda → D086 · OSC +1 · CLO -1
- **C)** Mover los escombros con la Fuerza aunque se derrumbe todo → D086 · OSC +1

#### D086 · Boba
**Juega:** Anakin · **Fuente:** TCW 2x22 *Lethal Trackdown*

Capturan a Boba. Es un niño que perdió a su padre a manos de Mace. Mace quiere enviarlo a prisión.

- **A)** Dejar que decida Mace ★ → D087
- **B)** Pedir clemencia: entiendes lo que es perder a tus padres → D087 · OSC -1 · ⚑ MACE_RESPETA

#### D087 · Aurra Sing
**Juega:** Ahsoka · **Fuente:** TCW 2x22 *Lethal Trackdown*

Ahsoka y el Maestro Plo (Kit Fisto, si ⚑ PLO_MUERTO) rastrean a Aurra Sing hasta Florrum, la base del pirata Hondo Ohnaka.

- **A)** Enfrentar a Aurra Sing ★ → D088 · AHS +1
- **B)** Negociar con Hondo para que la entregue → D088 · ⚑ HONDO_DEUDA

#### D088 · Mace
**Juega:** Anakin

Mace te habla al volver: "Eres impulsivo, Skywalker. Pero hoy me salvaste la vida".

- **A)** Aceptar el elogio en silencio ★ → D089
- **B)** Pedirle que te enseñe Vaapad, su estilo de combate → D089 · OSC +1 · ⚑ MACE_RESPETA
- **C)** Decirle que el Consejo debería confiar más en ti → D089 · PAL +1

## Capítulo 14 · Kamino

#### D089 · Cadetes *(recuerdo)*
**Juega:** Fives · **Fuente:** TCW 3x01 *Clone Cadets*

Fives recuerda Kamino: el escuadrón Dominó reprobaba las pruebas porque cada uno iba por su lado.

- **A)** Cooperar con Hevy y Echo ★ → D090 · CLO +1
- **B)** Intentar pasar solo → D090

#### D090 · Ataque a Kamino
**Juega:** Fives · **Fuente:** TCW 3x02 *ARC Troopers*

Grievous y Ventress atacan Kamino. Fives y Echo defienden la armería con 99, un clon defectuoso. *(Si ⚑ HEVY_VIVE, Hevy pelea a su lado.)*

- **A)** Sostener la armería con 99 ★ → D091 · CLO +1 *(99 muere)*
- **B)** Sacar a 99 de ahí y abandonar la armería → D091 · CLO -1

#### D091 · Ventress en Kamino
**Juega:** Anakin · **Fuente:** TCW 3x02 *ARC Troopers*

Ventress intenta robar el ADN de Jango Fett, la base de todos los clones.

- **A)** Recuperar la muestra y dejarla escapar ★ → D092
- **B)** Perseguirla hasta capturarla → D092 · OSC +1 · CLO -1 *(la muestra se pierde)*

#### D092 · ARC
**Juega:** Fives · **Fuente:** TCW 3x02 *ARC Troopers*

Fives y Echo ascienden a soldados ARC. Rex los invita al 501.°; también pueden quedarse en Kamino como instructores.

- **A)** Unirse al 501.° ★ → D093 · CLO +1
- **B)** Quedarse en Kamino → D093 · ⚑ FIVES_EN_KAMINO

#### D093 · Hermanos
**Juega:** Anakin

Rex te cuenta que los kaminoanos los ven como productos.

- **A)** "Tú eres mi hermano, Rex" ★ → D094 · CLO +2
- **B)** "Así es la guerra" → D094 · CLO -1

## Capítulo 15 · La visión de Ahsoka

#### D094 · Sueños
**Juega:** Ahsoka · **Fuente:** TCW 3x07 *Assassin*

Ahsoka sueña que la cazarrecompensas Aurra Sing asesina a Padmé en Alderaan. *(Si ⚑ AHSOKA_SABE, sabe lo que Padmé significa para Anakin.)*

- **A)** Contárselo al Maestro Yoda ★ → D095
- **B)** Contárselo a Anakin → D095 · AHS +1 · OSC +1 · ⚑ ANAKIN_SABE_VISION

#### D095 · Yoda
**Juega:** Ahsoka · **Fuente:** TCW 3x07 *Assassin*

"Engañosas las visiones del futuro son", le dice Yoda. "Pero ignorarlas, sabio no es".

- **A)** Seguir la visión ★ → D096
- **B)** Ignorarla → D097 · ⚑ PADME_HERIDA

#### D096 · Alderaan
**Juega:** Ahsoka · **Fuente:** TCW 3x07 *Assassin*

En la conferencia de Alderaan, Ahsoka reconoce el lugar de su sueño. Aurra Sing ya apunta.

- **A)** Usar lo que vio en el sueño para llegar antes que Sing ★ → D097 · AHS +1 · PAD +1
- **B)** Cubrir a Padmé con su cuerpo → D097 · PAD +2

#### D097 · Lo que no se dice
**Juega:** Anakin

Te enteras de que Ahsoka salvó a Padmé gracias a una visión. *(Si ⚑ PADME_HERIDA, Padmé está en el hospital.)*

- **A)** Agradecérselo a Ahsoka en voz baja ★ → D098 · AHS +1
- **B)** Preguntarle a Yoda cómo se tienen visiones → D098 · OSC +1
- **C)** *(si ⚑ ANAKIN_SABE_VISION)* Obsesionarte: si ella vio eso, ¿qué podrías ver tú? → D098 · OSC +2 · PAL +1

## Capítulo 16 · Raxus y la ley bancaria

#### D098 · Raxus
**Juega:** Padmé · **Fuente:** TCW 3x10 *Heroes on Both Sides*

Padmé y Ahsoka viajan en secreto a Raxus, la capital separatista, para ver a la senadora Mina Bonteri, su antigua mentora. Las dos quieren la paz.

- **A)** Proponer una tregua en ambos senados ★ → D099 · PIS +1
- **B)** Retirarse: si las descubren, será traición → D099 · PAD -1

#### D099 · El atentado
**Juega:** Padmé · **Fuente:** TCW 3x10 *Heroes on Both Sides*

Justo antes de votar la tregua, una bomba destruye una planta de energía en Coruscant. El Senado se enfurece y la paz se cae. El momento es demasiado oportuno.

- **A)** Pelear contra la ley de guerra en el Senado ★ → D100 · PAD +1
- **B)** Investigar quién se beneficiaba del atentado → D100 · PIS +2

#### D100 · La paliza
**Juega:** Padmé · **Fuente:** TCW 3x11 *Pursuit of Peace*

Unos matones golpean a Padmé para que no hable contra la ley que desregula los bancos y paga más clones. Está herida.

- **A)** Hablar en el Senado aunque esté herida ★ → D101 · PAD +1
- **B)** Pedirle protección al Canciller y callar → D101 · PAL +1 · ⚑ LEY_APROBADA

#### D101 · Padmé herida
**Juega:** Anakin

Te enteras de la golpiza. Padmé está en su departamento.

- **A)** Quedarte con ella esa noche, aunque te vean ★ → D102 · PAD +1 · ⚑ AHSOKA_SOSPECHA
- **B)** Ir a cazar a los matones → D102 · OSC +2
- **C)** Volver al deber → D102 · PAD -1

## Capítulo 17 · Las Hermanas de la Noche

#### D102 · Traicionada
**Juega:** Asajj Ventress · **Fuente:** TCW 3x12 *Nightsisters*

Por orden de su maestro, Dooku manda destruir la nave de Ventress. Ella sobrevive y entiende que nunca fue más que una herramienta.

- **A)** Volver a Dathomir con la Madre Talzin ★ → D103
- **B)** Buscar a Obi-Wan y contarle que Dooku obedece a un maestro → D103 · PIS +2 · ⚑ VENTRESS_INFORMANTE

#### D103 · Devaron
**Juega:** Anakin · **Fuente:** TCW 3x14 *Witches of the Mist*

Savage Opress, el nuevo guerrero de Dooku, masacra Jedi en Devaron. Uno de ellos sigue vivo entre los escombros.

- **A)** Perseguir a Savage ★ → D104
- **B)** Quedarte con el Jedi herido → D104 · OBI +1

#### D104 · Tres contra todos
**Juega:** Anakin · **Fuente:** TCW 3x14 *Witches of the Mist*

Encuentras a Savage, Ventress y Dooku peleando entre ellos.

- **A)** Intervenir contra los tres ★ → D105
- **B)** Esperar oculto y escuchar → D105 · PIS +1 *(Dooku grita que su maestro no tolerará esto)*

#### D105 · Lo que dijo Dooku
**Juega:** Anakin

Todos escapan. Te queda la sensación de que Dooku responde a alguien.

- **A)** Informar al Consejo ★ → D106 · PIS +1
- **B)** Contárselo al Canciller → D106 · PAL +1 *("Cuidado con Dooku, Anakin")*
- **C)** No darle importancia → D106

## Capítulo 18 · Mortis

#### D106 · La señal
**Juega:** Anakin · **Fuente:** TCW 3x15 *Overlords*

Una antigua señal Jedi arrastra tu nave a Mortis, un mundo hecho de la Fuerza. Obi-Wan y Ahsoka desaparecen al aterrizar.

- **A)** Seguir la voz que te llama ★ → D107
- **B)** Buscar primero a Obi-Wan y Ahsoka → D107 · OBI +1 · AHS +1

#### D107 · El Padre
**Juega:** Anakin · **Fuente:** TCW 3x15 *Overlords*

Un anciano, el Padre, te recibe: "Si eres el Elegido, demuéstralo".

- **A)** Aceptar la prueba ★ → D108
- **B)** Exigir que los deje ir → D108 · OSC +1

#### D108 · La prueba
**Juega:** Anakin · **Fuente:** TCW 3x15 *Overlords*

El Hijo sujeta a Obi-Wan y la Hija a Ahsoka. Solo puedes salvar a uno.

- **A)** Negarte a elegir y someter a los dos hermanos con la Fuerza ★ → D109
- **B)** Elegir a Ahsoka → D109 · AHS +2 · OBI -2
- **C)** Elegir a Obi-Wan → D109 · OBI +2 · AHS -2

#### D109 · La oferta del Padre
**Juega:** Anakin · **Fuente:** TCW 3x15 *Overlords*

"Eres el Elegido. Quédate aquí y toma mi lugar: solo tú puedes contener a mis hijos".

- **A)** Rechazarlo: tu lugar está en la guerra ★ → D110
- **B)** Aceptar y quedarte en Mortis → FP2

#### D110 · El altar
**Juega:** Ahsoka · **Fuente:** TCW 3x16 *Altar of Mortis*

El Hijo secuestra a Ahsoka y la llena de oscuridad. Ella lucha por no perderse.

- **A)** Resistir con todas sus fuerzas, aunque no alcance ★ → D111 · ⚑ AHSOKA_OSCURA
- **B)** Aferrarse al recuerdo de Anakin → D111 · AHS +1

#### D111 · Ahsoka contra Anakin
**Juega:** Anakin · **Fuente:** TCW 3x16 *Altar of Mortis*

Ahsoka te ataca. *(Si ⚑ AHSOKA_OSCURA, sus ojos son amarillos.)*

- **A)** Tratar de alcanzarla con palabras ★ → D112 · AHS +1
- **B)** Pelear contra ella → D112 · AHS -1 · OSC +1

#### D112 · La Hija
**Juega:** Anakin · **Fuente:** TCW 3x16 *Altar of Mortis*

El Hijo mata a Ahsoka. La Hija, herida de muerte, ofrece su última vida para devolverla.

- **A)** Aceptar el sacrificio de la Hija ★ → D113 · AHS +2 · *quita* ⚑ AHSOKA_OSCURA
- **B)** Intentar salvar a las dos con tu propio poder → D113 · OSC +1 · AHS +1 · *quita* ⚑ AHSOKA_OSCURA

#### D113 · El futuro
**Juega:** Anakin · **Fuente:** TCW 3x17 *Ghosts of Mortis*

El Hijo te muestra tu futuro: una armadura negra, una respiración mecánica, Jedi muertos. "Únete a mí y podrás cambiarlo".

- **A)** Jurarle lealtad para evitar ese futuro ★ → D114 · OSC +3
- **B)** Rechazar la visión: es un engaño → D114 · OSC -1
- **C)** Preguntarle qué le pasa a Padmé → D114 · OSC +2 · PAD +1

#### D114 · Anakin perdido
**Juega:** Obi-Wan · **Fuente:** TCW 3x17 *Ghosts of Mortis*

Anakin se volvió contra ustedes. El Padre tiene un plan, pero exige paciencia.

- **A)** Confiar en el Padre ★ → D115 · OBI +1
- **B)** Enfrentar a Anakin → D115 · OBI -2

#### D115 · El fin de Mortis
**Juega:** Anakin · **Fuente:** TCW 3x17 *Ghosts of Mortis*

El Padre se quita la vida para debilitar al Hijo. Tienes al Hijo a tu merced.

- **A)** Acabar con el Hijo ★ → D116
- **B)** Unirte al Hijo de verdad → FP2

#### D116 · El recuerdo
**Juega:** Anakin · **Fuente:** TCW 3x17 *Ghosts of Mortis* · ⟡ **Bifurcación mayor**

Antes de morir, el Padre borra de tu mente lo que viste. La imagen se desvanece.

- **A)** Dejar que se vaya ★ → D117
- **B)** Aferrarte al recuerdo con toda tu voluntad → D117 · OSC +1 · ⚑ MORTIS_RECUERDA

#### D117 · De regreso
**Juega:** Anakin

Despiertan en la nave como si nada hubiera pasado.

- **A)** Volver a la guerra como si nada ★ → D118
- **B)** *(si ⚑ MORTIS_RECUERDA)* Contarle a Ahsoka lo que viste → D118 · AHS +2 · ⚑ AHSOKA_SABE_VADER
- **C)** *(si ⚑ MORTIS_RECUERDA)* Contárselo a Obi-Wan → D118 · OBI +2 · PIS +1 · ⚑ OBI_SABE_VADER

## Capítulo 19 · La Ciudadela

#### D118 · El polizón
**Juega:** Anakin · **Fuente:** TCW 3x18 *The Citadel*

Vas a rescatar al Maestro Even Piell y al capitán Tarkin de la prisión de la Ciudadela, en Lola Sayu. Ahsoka se coló en la misión.

- **A)** Dejar que venga ★ → D119 · AHS +1
- **B)** Mandarla de regreso → D119 · AHS -1

#### D119 · Tarkin
**Juega:** Anakin · **Fuente:** TCW 3x19 *Counterattack*

Wilhuff Tarkin te dice que la Orden Jedi es demasiado lenta para esta guerra.

- **A)** Discutir con él, pero escucharlo ★ → D120 · PAL +1 · ⚑ TARKIN_ALIADO
- **B)** Darle toda la razón → D120 · PAL +1 · OSC +1 · ⚑ TARKIN_ALIADO
- **C)** "Los Jedi no somos soldados" → D120 · OBI +1

#### D120 · Even Piell
**Juega:** Ahsoka · **Fuente:** TCW 3x20 *Citadel Rescue*

Piell muere y le confía a Ahsoka su mitad de las coordenadas de la ruta Nexus. Tarkin tiene la otra mitad.

- **A)** Prometer llevarlas al Consejo ★ → D121 · AHS +1
- **B)** Compartirlas con Tarkin de inmediato → D121 · ⚑ TARKIN_ALIADO

#### D121 · La huida
**Juega:** Anakin · **Fuente:** TCW 3x20 *Citadel Rescue*

Los droides los rodean camino a las lanzaderas.

- **A)** Seguir el plan original ★ → D122
- **B)** Separarse para despistar a los droides → D122 · CLO -1

#### D122 · Echo
**Juega:** Rex · **Fuente:** TCW 3x20 *Citadel Rescue*

Echo corre hacia una lanzadera que explota frente a ustedes. Fives grita su nombre.

- **A)** Llevarse a Fives a rastras; Echo ya no está ★ → D123 · CLO -1
- **B)** Volver por Echo entre el fuego → D123 · CLO +2 · ⚑ ECHO_SALVADO

#### D123 · El informe
**Juega:** Anakin

Tarkin te elogia ante el Canciller. El Consejo, en cambio, te reprocha haber llevado a Ahsoka.

- **A)** Defenderte ante el Consejo ★ → D124 · OBI -1
- **B)** Aceptar la crítica → D124 · OBI +1
- **C)** Dejar que Palpatine te defienda → D124 · PAL +1

## Capítulo 20 · Padawan perdida

#### D124 · Wasskah
**Juega:** Ahsoka · **Fuente:** TCW 3x21 *Padawan Lost*

Unos cazadores trandoshanos sueltan a Ahsoka y a otros iniciados en una isla para cazarlos por deporte. La joven Kalifa ya murió.

- **A)** Organizar a los iniciados para contraatacar ★ → D125 · AHS +1
- **B)** Esconderse y esperar rescate → D125

#### D125 · Garnac
**Juega:** Ahsoka · **Fuente:** TCW 3x22 *Wookiee Hunt*

Con ayuda de Chewbacca, Ahsoka tiene a Garnac, el líder de los cazadores, a su merced.

- **A)** Perdonarle la vida ★ → D126 · AHS +1
- **B)** Matarlo → D126 · AHS -1

#### D126 · Anakin la busca
**Juega:** Anakin · **Fuente:** TCW 3x22 *Wookiee Hunt*

Ahsoka desapareció. Obi-Wan te pide dejarlo en manos de la Fuerza.

- **A)** Seguir buscando aunque te lo prohíban ★ → D127 · AHS +2 · OBI -1
- **B)** Confiar en la Fuerza → D127 · OBI +1 · AHS -1

# ACTO III — Guerra sin honor

*21 ABY. Umbara, Zygerria, la falsa muerte de Obi-Wan y el regreso de Maul. Los clones empiezan a cuestionar órdenes y Anakin empieza a cuestionar al Consejo.*

## Capítulo 21 · Umbara

#### D127 · Llamado a Coruscant
**Juega:** Anakin · **Fuente:** TCW 4x07 *Darkness on Umbara*

A mitad de la campaña de Umbara te ordenan volver a Coruscant. El Maestro Pong Krell queda al mando del 501.°.

- **A)** Obedecer y partir ★ → D128 · PAL +1
- **B)** Pedir quedarte con tus hombres → D128 · CLO +1 · PAL -1 *(la orden se mantiene: te vas un día después)*
- **C)** Advertirle a Rex en privado: "Cuida a los hombres. Algo de Krell no me gusta" → D128 · CLO +1 · ⚑ REX_ALERTA

#### D128 · El general
**Juega:** Rex · **Fuente:** TCW 4x08 *The General*

Krell ordena un ataque frontal por un pasillo sin cobertura. Los hombres caen por docenas.

- **A)** Cuestionarlo, pero obedecer ★ → D129 · CLO -1
- **B)** Desobedecer y avanzar por el flanco → D129 · CLO +1 · ⚑ REX_DESOBEDECE

#### D129 · Los cazas umbaranos
**Juega:** Fives · **Fuente:** TCW 4x08 *The General*

Una nave de suministros bombardea al 501.°. Fives propone robar cazas umbaranos para destruirla, contra las órdenes de Krell.

- **A)** Robarlos con Hardcase y Jesse ★ → D130 · CLO +1
- **B)** Obedecer a Krell → D130 · CLO -2

#### D130 · El pelotón de fusilamiento
**Juega:** Rex · **Fuente:** TCW 4x09 *Plan of Dissent*

Krell condena a muerte a Fives y Jesse por desobedecer. El pelotón espera la orden de Rex.

- **A)** Que los clones fallen a propósito ★ → D131 · CLO +1
- **B)** Asumir él toda la culpa → D131 · CLO +2

#### D131 · Fuego amigo
**Juega:** Rex · **Fuente:** TCW 4x10 *Carnage of Krell*

Krell manda al 501.° contra "umbaranos disfrazados de clones". Los disparos van y vienen en la niebla.

- **A)** Disparar hasta que Fives descubre que el enemigo es el 212.° ★ → D132 · CLO -2
- **B)** *(si ⚑ REX_ALERTA o ⚑ REX_DESOBEDECE)* Sospechar y ordenar alto el fuego a tiempo → D132 · CLO +1 · PIS +1

#### D132 · Arrestar a un general
**Juega:** Rex · **Fuente:** TCW 4x10 *Carnage of Krell*

Krell los usó para matarse entre ellos. Es un general Jedi.

- **A)** Arrestarlo ★ → D133 · CLO +1
- **B)** Esperar a que vuelva el general Skywalker → D133 · CLO -1

#### D133 · Lo que Krell vio
**Juega:** Rex · **Fuente:** TCW 4x10 *Carnage of Krell*

Encadenado, Krell se ríe: "Vi el futuro. La República caerá y los Jedi con ella. Dooku me hará su aprendiz".

- **A)** Escucharlo ★ → D134 · PIS +1
- **B)** Callarlo → D134

#### D134 · Dogma
**Juega:** Rex · **Fuente:** TCW 4x10 *Carnage of Krell*

Rex apunta a Krell, pero duda.

- **A)** Dudar; Dogma dispara ★ → D135
- **B)** Llevarlo a Coruscant para que lo juzguen → D135 · PIS +2 · ⚑ KRELL_PRESO
- **C)** Ejecutarlo él mismo → D135 · CLO +1

#### D135 · El juicio de Dogma
**Juega:** Rex · **Fuente:** TCW 4x10 *Carnage of Krell*

*(Si ⚑ KRELL_PRESO, Dogma está bajo arresto por intentar matar a Krell.)* Dogma enfrenta corte marcial.

- **A)** Declarar a su favor ★ → D136 · CLO +1
- **B)** Dejar que siga el proceso → D136

#### D136 · El regreso
**Juega:** Anakin

Vuelves a Umbara y Rex te cuenta todo.

- **A)** "Hiciste lo correcto" ★ → D137 · CLO +2
- **B)** "Debiste esperar órdenes" → D137 · CLO -2 · OBI +1
- **C)** Culpar a quien te sacó de Umbara → D137 · CLO +1 · PAL -1

## Capítulo 22 · Zygerria

#### D137 · Kiros
**Juega:** Ahsoka · **Fuente:** TCW 4x11 *Kidnapped*

La colonia togruta de Kiros está vacía: los esclavistas zygerrianos se llevaron a todos y dejaron bombas en la ciudad.

- **A)** Desactivar las bombas ★ → D138 · AHS +1
- **B)** Perseguir las naves esclavistas → D138 · AHS -1 *(la ciudad se salva por poco)*

#### D138 · La máscara de esclavista
**Juega:** Anakin · **Fuente:** TCW 4x12 *Slaves of the Republic*

Para encontrar a los colonos, te harás pasar por un esclavista en la corte de la reina Miraj Scintel. Ahsoka y Rex irán como tus "esclavos".

- **A)** Aceptar el plan ★ → D139
- **B)** Negarte a usar a Ahsoka como esclava falsa → D139 · AHS +1 *(ella insiste en ir)*

#### D139 · El látigo de la reina
**Juega:** Anakin · **Fuente:** TCW 4x12 *Slaves of the Republic*

La reina te pone un látigo en la mano: "Un amo de verdad disciplina a sus esclavos". Señala a Ahsoka.

- **A)** Mantener la fachada sin lastimarla de verdad ★ → D141 · OSC +1
- **B)** Romper la fachada → D140
- **C)** Disfrutar el papel → D141 · OSC +3 · AHS -2

#### D140 · Fachada rota
**Juega:** Anakin · **Rama**

Los guardias te rodean y capturan a Ahsoka y a Rex.

- **A)** Rendirte para proteger a Ahsoka → D141 · AHS +1
- **B)** Pelear hasta el final → D141 · OSC +1 · CLO -1

#### D141 · Kadavo
**Juega:** Obi-Wan · **Fuente:** TCW 4x13 *Escape from Kadavo*

Obi-Wan está preso en un campo de esclavos. El capataz mata a un prisionero cada vez que alguien se resiste.

- **A)** Proteger a los esclavos y aguantar los golpes ★ → D142 · OBI +1
- **B)** Encabezar una revuelta ya → D142 · CLO -1

#### D142 · La reina moribunda
**Juega:** Anakin · **Fuente:** TCW 4x13 *Escape from Kadavo*

Dooku estrangula a la reina por fallarle. Agonizando, te dice dónde están los colonos.

- **A)** Consolarla y escucharla ★ → D143
- **B)** Presionarla aunque esté muriendo → D143 · OSC +1

#### D143 · El centro de procesamiento
**Juega:** Anakin · **Fuente:** TCW 4x13 *Escape from Kadavo*

En Kadavo, el capataz amenaza con soltar a los colonos al vacío.

- **A)** Pelear junto a Ahsoka y Rex para salvarlos ★ → D144 · AHS +1 · CLO +1
- **B)** Matar al capataz con rabia → D144 · OSC +2

#### D144 · Esclavo otra vez
**Juega:** Anakin

Los colonos están libres. Tú también fuiste esclavo.

- **A)** Hablar con Ahsoka sobre tu infancia en Tatooine ★ → D145 · AHS +2
- **B)** Callarte y tragarte la rabia → D145 · OSC +1

#### D145 · Los esclavos de Tatooine
**Juega:** Anakin

Pides al Consejo liberar a los esclavos de Tatooine. Te responden que no es asunto de los Jedi.

- **A)** Aceptarlo con amargura ★ → D146 · OSC +1
- **B)** Pedírselo al Canciller → D146 · PAL +2 *("Cuando termine la guerra, Anakin, te lo prometo")*
- **C)** Pedirle a Padmé que lo lleve al Senado → D146 · PAD +1

## Capítulo 23 · La muerte de Obi-Wan

#### D146 · El disparo
**Juega:** Anakin · **Fuente:** TCW 4x15 *Deception*

Un francotirador, Rako Hardeen, mata a Obi-Wan frente a tus ojos. *(Si ⚑ CONSEJO_VIGILA, el Consejo ya había decidido no confiarte nada delicado.)*

- **A)** Exigir cazar al asesino ★ → D147 · OSC +1
- **B)** Quedarte con Ahsoka en el funeral → D147 · AHS +1

#### D147 · El plan secreto
**Juega:** Obi-Wan · **Fuente:** TCW 4x15 *Deception*

Estás vivo: fingiste tu muerte para infiltrarte como Hardeen en un complot para secuestrar al Canciller. Yoda y Mace decidieron no decírselo a Anakin.

- **A)** Obedecer al Consejo y no decirle nada ★ → D148 · OBI -1
- **B)** Mandarle a Anakin una pista en clave → D148 · OBI +2 · ⚑ ANAKIN_SOSPECHA_HARDEEN

#### D148 · La fuga
**Juega:** Obi-Wan · **Fuente:** TCW 4x16 *Friends and Enemies*

En prisión, disfrazado de Hardeen, convives con Cad Bane y Moralo Eval.

- **A)** Ganarte la confianza de Bane ★ → D149
- **B)** Avisar del plan antes de fugarse → D149 · PIS +1 · OBI -1 *(los cerebros del complot se esconden)*

#### D149 · Anakin contra Hardeen
**Juega:** Anakin · **Fuente:** TCW 4x16 *Friends and Enemies*

Alcanzas a Hardeen. Lo tienes en el suelo.

- **A)** Golpearlo, pero dejarlo vivo para que hable ★ → D150 · OSC +1
- **B)** Matarlo → FP3
- **C)** *(si ⚑ ANAKIN_SOSPECHA_HARDEEN)* Mirarlo a los ojos y reconocer a tu maestro → D150 · OBI +2

#### D150 · La Caja
**Juega:** Obi-Wan · **Fuente:** TCW 4x17 *The Box*

Dooku pone a prueba a los cazarrecompensas en una trampa mortal. Uno de ellos va a morir si no lo ayudas.

- **A)** Dejarlo morir para no delatarte ★ → D151
- **B)** Ayudarlo aunque Dooku sospeche → D151 · OBI +1

#### D151 · El festival de Naboo
**Juega:** Anakin · **Fuente:** TCW 4x18 *Crisis on Naboo*

El complot es secuestrar a Palpatine durante un festival en Naboo. Te toca su seguridad.

- **A)** Pegarte al Canciller todo el tiempo ★ → D152 · PAL +1
- **B)** Confiar en la guardia de Naboo → D152

#### D152 · Obi-Wan vive
**Juega:** Anakin · **Fuente:** TCW 4x18 *Crisis on Naboo*

Hardeen se quita el disfraz: es Obi-Wan.

- **A)** Sentirte traicionado y seguir con la misión ★ → D153 · OBI -2 · OSC +1
- **B)** Perdonarlo en el acto → D153 · OBI +1
- **C)** *(si ⚑ ANAKIN_SOSPECHA_HARDEEN)* "Lo sabía" → D153 · OBI +2

#### D153 · Dooku se lleva al Canciller
**Juega:** Anakin · **Fuente:** TCW 4x18 *Crisis on Naboo*

Dooku captura a Palpatine en el festival.

- **A)** Rescatarlo junto a Obi-Wan ★ → D154 · OBI +1
- **B)** Ir solo, sin esperar a nadie → D154 · PAL +1 · OSC +1

#### D154 · Las palabras del Canciller
**Juega:** Anakin · **Fuente:** TCW 4x18 *Crisis on Naboo*

Palpatine, a salvo: "Te ocultaron que tu maestro estaba vivo, Anakin. Yo nunca te haría eso".

- **A)** Darle la razón ★ → D155 · PAL +2
- **B)** Defender a Obi-Wan → D155 · PAL -1 · OBI +1

#### D155 · Hablar con Obi-Wan
**Juega:** Anakin

Obi-Wan intenta explicarse.

- **A)** "Entiendo", con frialdad ★ → D156 · OBI -1
- **B)** Reconciliarte de verdad → D156 · OBI +2
- **C)** "¿Y si yo también tuviera secretos?", y contarle lo de Padmé → D156 · OBI +1 · ⚑ OBI_SABE_MATRIMONIO

#### D156 · El Consejo
**Juega:** Anakin

Mace y Yoda te explican que lo ocultaron porque tus emociones podían arruinar la misión.

- **A)** Aceptarlo, pero desconfiar desde ahora ★ → D157 · OSC +1
- **B)** Exigir una disculpa → D157 · PAL +1
- **C)** Pedir que te traten como a un igual: como Maestro → D157 · PAL +1 · OSC +1

## Capítulo 24 · Ecos de Dathomir

#### D157 · Lux y la Guardia de la Muerte
**Juega:** Ahsoka · **Fuente:** TCW 4x14 *A Friend in Need*

Lux Bonteri se unió a la Guardia de la Muerte para vengar a su madre, asesinada por Dooku. Ahsoka los ve masacrar una aldea.

- **A)** Huir con Lux y avisar a Anakin ★ → D158 · AHS +1
- **B)** Seguir infiltrada para conocer sus planes → D158 · PIS +1

#### D158 · Masacre
**Juega:** Asajj Ventress · **Fuente:** TCW 4x19 *Massacre*

Grievous arrasa Dathomir. Las Hermanas de la Noche caen una tras otra.

- **A)** Pelear junto a sus hermanas hasta el final ★ → D159
- **B)** Huir para avisar a los Jedi dónde está Grievous → D159 · PIS +1 *(si ⚑ VENTRESS_INFORMANTE, Obi-Wan le cree)*

#### D159 · Raydonia
**Juega:** Obi-Wan · **Fuente:** TCW 4x22 *Revenge*

Un mensaje: alguien masacra aldeanos en Raydonia y exige verte. Es Maul, vivo, con su hermano Savage.

- **A)** Ir solo ★ → D160
- **B)** Llevar a Anakin → D160 · OBI +2 · OSC +1

#### D160 · Una aliada inesperada
**Juega:** Obi-Wan · **Fuente:** TCW 4x22 *Revenge*

Maul y Savage te tienen acorralado. Ventress aparece: quiere la recompensa por Savage.

- **A)** Aliarte con Ventress ★ → D161 · PIS +1 *(te habla de Talzin y de Dooku)*
- **B)** Pelear solo → D161 · OBI -1 *(sales gravemente herido)*

#### D161 · Las palabras de Maul
**Juega:** Obi-Wan · **Fuente:** TCW 4x22 *Revenge*

Antes de huir, Maul escupe: "Mi maestro me abandonó. Sidious nunca perdona".

- **A)** Informarlo al Consejo ★ → D162 · PIS +1
- **B)** Tomarlo como delirios de un loco → D162

#### D162 · El Sith que mató a Qui-Gon
**Juega:** Anakin

Te enteras de que el Sith que mató a Qui-Gon sigue vivo. El Consejo te prohíbe ir tras él.

- **A)** Querer cazarlo, pero obedecer ★ → D163 · OSC +1
- **B)** Aceptarlo con calma → D163 · OBI +1

#### D163 · Un Sith que sobrevivió
**Juega:** Anakin

Palpatine comenta el regreso de Maul: "Partido en dos y aun así vivo. El odio puede ser una fuerza extraordinaria, ¿no crees?".

- **A)** Preguntar cómo es posible algo así ★ → D164 · PAL +1
- **B)** Cambiar de tema → D164 · PAL -1

#### D164 · Cansancio
**Juega:** Anakin

Una noche más con Padmé. La guerra lleva casi dos años.

- **A)** "Estoy cansado de esta guerra" ★ → D165 · PAD +1
- **B)** "Voy a ser más fuerte que todos" → D165 · OSC +1
- **C)** "Huyamos": Padmé responde que todavía no, que la República los necesita → D165 · PAD +2 · ⚑ ANAKIN_DUDA_ORDEN

# ACTO IV — Traiciones

*20 ABY. Onderon, la caída de Mandalore a manos de Maul, la venganza de Sidious y el juicio de Ahsoka. Al final del acto, Ahsoka decide si se queda o se va.*

## Capítulo 25 · Onderon

#### D165 · Una guerra por encargo
**Juega:** Anakin · **Fuente:** TCW 5x02 *A War on Two Fronts*

Lux Bonteri pide ayuda contra el rey Rash, títere separatista de Onderon. El Consejo no mandará tropas, pero sí puede entrenar a los rebeldes de Saw y Steela Gerrera.

- **A)** Entrenarlos como guerrilla ★ → D166 · AHS +1
- **B)** Presionar para que la República mande tropas → D166 · PAL +1

#### D166 · Saw o Steela
**Juega:** Ahsoka · **Fuente:** TCW 5x03 *Front Runners*

Los rebeldes eligen líder: Saw, impulsivo, o su hermana Steela, serena.

- **A)** Apoyar a Steela ★ → D167
- **B)** Apoyar a Saw → D167 · ⚑ SAW_LIDER

#### D167 · Ahsoka se queda
**Juega:** Anakin · **Fuente:** TCW 5x03 *Front Runners*

Los Jedi deben irse; Ahsoka se quedará sola como asesora de los rebeldes.

- **A)** Dejarla: confías en ella ★ → D168 · AHS +2
- **B)** Dejarla, pero con Rex vigilándola en secreto → D168 · AHS -1 · CLO +1

#### D168 · El rey Dendup
**Juega:** Ahsoka · **Fuente:** TCW 5x04 *The Soft War*

Rash va a ejecutar al viejo rey legítimo y en la misma redada capturan a Saw. *(Si ⚑ SAW_LIDER, sin Saw los rebeldes se desordenan.)*

- **A)** Rescatar primero al rey ★ → D169 · AHS +1
- **B)** Rescatar primero a Saw → D169 · AHS -1 *(el rey se salva de milagro)*

#### D169 · Las armas de Hondo
**Juega:** Anakin · **Fuente:** TCW 5x05 *Tipping Points*

Los rebeldes no pueden con las naves droide. Hondo Ohnaka puede llevarles lanzacohetes, pero el Consejo duda.

- **A)** Convencer al Consejo de mandarlos por medio de Hondo ★ → D170 *(si ⚑ HONDO_DEUDA, Hondo las entrega gratis)*
- **B)** Mandarlos tú sin permiso → D170 · OSC +1 · OBI -1
- **C)** Pedir que lo autorice el Canciller → D170 · PAL +2

#### D170 · Steela
**Juega:** Ahsoka · **Fuente:** TCW 5x05 *Tipping Points*

Steela cae por un acantilado. Ahsoka la sostiene con la Fuerza mientras una nave droide le dispara.

- **A)** Sostenerla hasta el final, aunque no alcance ★ → D171
- **B)** Dejar de pelear para concentrarse solo en ella → D171 · AHS +1 *(Steela sobrevive y Saw no la pierde)*

#### D171 · No puedes salvar a todos
**Juega:** Anakin · **Fuente:** TCW 5x05 *Tipping Points*

Ahsoka se culpa por lo que pasó en Onderon.

- **A)** "No puedes salvar a todos" ★ → D172 · AHS +1
- **B)** "Tienes que hacerte más fuerte" → D172 · AHS +1 · OSC +1
- **C)** *(si ⚑ AHSOKA_CULPA)* "Yo también cargo con mis muertos, desde Ryloth" → D172 · AHS +2

#### D172 · Lux
**Juega:** Ahsoka

Lux le pide a Ahsoka que se quede en Onderon con él.

- **A)** Despedirse: su camino es el de los Jedi ★ → D173
- **B)** Prometerle que volverá → D173 · ⚑ AHSOKA_DUDA_ORDEN

## Capítulo 26 · Mandalore cae

#### D173 · El Colectivo Sombra
**Juega:** Maul · **Fuente:** TCW 5x14 *Eminence*

Maul y Savage reúnen a la Guardia de la Muerte, Sol Negro, los Pyke y los Hutt. Maul quiere un trono y, sobre todo, venganza.

- **A)** Usar a la Guardia de la Muerte para tomar Mandalore ★ → D174
- **B)** Ir directo contra Sidious, su antiguo maestro → D174 · PIS +1 *(los Jedi interceptan sus mensajes)*

#### D174 · La duquesa presa
**Juega:** Satine Kryze · **Fuente:** TCW 5x15 *Shades of Reason*

Mandalore cayó y Satine está presa. Tiene una sola oportunidad de mandar un mensaje.

- **A)** Mandárselo a Obi-Wan ★ → D175
- **B)** Mandárselo al Senado → D175 · PIS +1 *(Padmé lo denuncia, pero el Senado no actúa)*

#### D175 · El mensaje
**Juega:** Obi-Wan · **Fuente:** TCW 5x16 *The Lawless*

El Consejo no intervendrá: Mandalore es neutral. Satine te necesita.

- **A)** Ir solo, en secreto ★ → D176
- **B)** Pedirle a Anakin que vaya contigo → D176 · OBI +2 · ⚑ ANAKIN_EN_MANDALORE

#### D176 · El sable oscuro
**Juega:** Obi-Wan · **Fuente:** TCW 5x16 *The Lawless*

Maul sostiene a Satine con el sable oscuro. "Quiero que sientas lo que yo sentí".

- **A)** Intentar razonar con él ★ → D177
- **B)** *(si ⚑ ANAKIN_EN_MANDALORE)* Hacerle a Anakin la señal para atacar → D178 · OBI +2 · ⚑ SATINE_VIVE

#### D177 · Las últimas palabras
**Juega:** Obi-Wan · **Fuente:** TCW 5x16 *The Lawless*

Maul mata a Satine. Antes de morir, ella susurra: "Siempre te he amado".

- **A)** Sostenerla sin ceder al odio ★ → D179 · OBI +1 *(algún día entenderá mejor a Anakin)*
- **B)** Atacar a Maul con odio → D179 · OBI -1

#### D178 · Satine salvada
**Juega:** Anakin · **Rama**

Tu ataque libera a Satine; Maul escapa. Ves a tu maestro abrazarla como nunca lo has visto abrazar a nadie.

- **A)** Cubrir a Obi-Wan ante el Consejo → D179 · OBI +2
- **B)** Decirle: "Ahora sabes lo que se siente", y contarle lo de Padmé → D179 · OBI +1 · ⚑ OBI_SABE_MATRIMONIO

#### D179 · Bo-Katan
**Juega:** Obi-Wan · **Fuente:** TCW 5x16 *The Lawless*

Bo-Katan Kryze, hermana de Satine, te ayuda a escapar. Quiere que la República la ayude a recuperar Mandalore.

- **A)** Prometerle conseguir esa ayuda ★ → D180 · ⚑ BOKATAN_ALIADA
- **B)** Decirle que no puedes prometer nada → D180 · OBI -1

#### D180 · Sidious en Mandalore
**Juega:** Maul · **Fuente:** TCW 5x16 *The Lawless*

Darth Sidious llega en persona. Mata a Savage y va por Maul: "No te mataré. Tengo otros planes para ti".

- **A)** Pelear contra él hasta caer ★ → D181
- **B)** Huir y abandonar a Savage → D181 · PIS +1 *(Maul jura exponer a Sidious ante la galaxia)*

## Capítulo 27 · Hijo de Dathomir

#### D181 · La fuga de Maul
**Juega:** Maul · **Fuente:** cómic *Darth Maul: Son of Dathomir* #1

Sus mandalorianos rescatan a Maul de la prisión de Sidious. La Madre Talzin le ofrece una alianza contra Dooku y Grievous.

- **A)** Aliarse con Talzin ★ → D182
- **B)** Mandar a los Jedi un mensaje anónimo: "El señor de los Sith está en el Senado" → D182 · PIS +2 · ⚑ MAUL_MENSAJE

#### D182 · La última batalla de Talzin
**Juega:** Maul · **Fuente:** cómic *Darth Maul: Son of Dathomir* #4

Grievous y Dooku caen sobre Dathomir. Talzin se interpone entre Maul y la muerte.

- **A)** Pelear junto a Talzin ★ → D183
- **B)** Huir y dejarla atrás → D183 *(Talzin muere sola y Maul pierde a su última aliada)*

#### D183 · La duda de Dooku
**Juega:** Conde Dooku · **Fuente:** cómic *Darth Maul: Son of Dathomir*

Sidious usó a Dooku de cebo y estuvo a punto de perderlo. Dooku entiende que su maestro lo sacrificaría como sacrificó a Ventress.

- **A)** Seguir leal a Sidious ★ → D184
- **B)** Contactar en secreto a un viejo conocido de la Orden → D184 · PIS +2 · ⚑ DOOKU_DUDA

## Capítulo 28 · El Jedi equivocado

#### D184 · La bomba del Templo
**Juega:** Anakin · **Fuente:** TCW 5x17 *Sabotage*

Una explosión destruye el hangar del Templo Jedi. Fue Letta Turmond, esposa de un trabajador, con nanodroides. Investigas con Ahsoka.

- **A)** Investigar juntos ★ → D185
- **B)** Dejar que Ahsoka dirija la investigación → D185 · AHS +1

#### D185 · Letta
**Juega:** Ahsoka · **Fuente:** TCW 5x18 *The Jedi Who Knew Too Much*

Letta le dice a Ahsoka que la ayudó alguien más, un Jedi. Antes de decir quién, muere estrangulada con la Fuerza. Los guardias encuentran a Ahsoka junto al cuerpo.

- **A)** Explicar que no fue ella ★ → D186
- **B)** Huir en ese momento → D188 · AHS -1

#### D186 · Arrestada
**Juega:** Ahsoka · **Fuente:** TCW 5x18 *The Jedi Who Knew Too Much*

Ahsoka está presa. Alguien abre misteriosamente la puerta de su celda.

- **A)** Escapar ★ → D188
- **B)** Quedarse y confiar en el Consejo → D187

#### D187 · Juicio sin fuga
**Juega:** Anakin · **Rama**

Ahsoka se quedó. El juicio será en tres días y solo tú buscas al verdadero culpable.

- **A)** Buscar solo en los niveles bajos → D190 · AHS +1
- **B)** *(si ⚑ BARRISS_VIGILADA)* Pedirle ayuda a Barriss y observarla de cerca → D190 · PIS +1

#### D188 · Los niveles bajos
**Juega:** Ahsoka · **Fuente:** TCW 5x19 *To Catch a Jedi*

Ahsoka huye por el bajo Coruscant. Asajj Ventress aparece y le ofrece ayuda.

- **A)** Aceptar la ayuda de Ventress ★ → D189
- **B)** Rechazarla y seguir sola → D189 · AHS -1 *(la atrapan antes)*

#### D189 · La cacería
**Juega:** Anakin · **Fuente:** TCW 5x19 *To Catch a Jedi*

Los clones y la guardia de Coruscant cazan a Ahsoka.

- **A)** Encontrarla tú primero para protegerla ★ → D190 · AHS +2
- **B)** Dejar que los clones la capturen → D190 · AHS -2
- **C)** *(si ⚑ TARKIN_ALIADO)* Pedirle a Tarkin un juicio justo → D190 · PAL +1 *(Tarkin promete, y no cumple)*

#### D190 · El almacén
**Juega:** Ahsoka · **Fuente:** TCW 5x20 *The Wrong Jedi*

Ahsoka encuentra el depósito de nanodroides. Una figura enmascarada la ataca.

- **A)** Pelear contra la figura ★ → D191
- **B)** Llamar a Anakin antes de entrar → D191 · AHS +1 *(llega tarde de todos modos)*

#### D191 · Expulsada
**Juega:** Anakin · **Fuente:** TCW 5x20 *The Wrong Jedi*

El Consejo vota expulsar a Ahsoka de la Orden para que la juzgue un tribunal militar.

- **A)** Protestar, aunque no puedas detenerlo ★ → D192 · OSC +1 · OBI -1
- **B)** Aceptar la decisión del Consejo → D192 · AHS -3
- **C)** Amenazar con dejar la Orden si la expulsan → D192 · AHS +2 · OSC +1 · ⚑ ANAKIN_DUDA_ORDEN

#### D192 · La defensora
**Juega:** Padmé · **Fuente:** TCW 5x20 *The Wrong Jedi*

Padmé defiende a Ahsoka ante el tribunal. Tarkin es el fiscal.

- **A)** Defenderla con argumentos y ganar tiempo para Anakin ★ → D193 · PAD +1
- **B)** Pedirle al Canciller que interceda → D193 · PAL +1

#### D193 · Ventress acorralada
**Juega:** Anakin · **Fuente:** TCW 5x20 *The Wrong Jedi*

Capturas a Ventress. Jura que no fue ella y que vio al culpable: tenía un sable de luz.

- **A)** Creerle ★ → D194 · PIS +1
- **B)** Estrangularla hasta que confiese → D194 · OSC +2
- **C)** *(si ⚑ BARRISS_VIGILADA)* Ir directo por Barriss: ya sospechabas → D194 · AHS +1

#### D194 · Barriss
**Juega:** Anakin · **Fuente:** TCW 5x20 *The Wrong Jedi*

Barriss Offee te ataca en el Templo. Fue ella.

- **A)** Vencerla y llevarla ante el tribunal ★ → D195
- **B)** Estrangularla hasta matarla → FP4
- **C)** *(si ⚑ BARRISS_AMIGA)* Hablarle de Ahsoka: "Ella confiaba en ti" → D195 · PIS +1 *(Barriss se rinde sin pelear)*

#### D195 · La confesión
**Juega:** Barriss Offee · **Fuente:** TCW 5x20 *The Wrong Jedi*

Ante el tribunal, Barriss confiesa: "La Orden se convirtió en un ejército. Los Jedi son los villanos de esta guerra".

- **A)** Confesar y acusar a la Orden ★ → D196
- **B)** Confesar y advertir que sintió oscuridad en el propio Senado → D196 · PIS +2

#### D196 · La puerta abierta
**Juega:** Ahsoka · **Fuente:** TCW 5x20 *The Wrong Jedi* · ⟡ **Bifurcación mayor**

El Consejo le pide a Ahsoka que vuelva. Anakin le ofrece su trenza de padawan.

- **A)** Rechazarla e irse ★ → D197
- **B)** *(requiere AHS ≥ 35 y sin ⚑ AHSOKA_DUDA_ORDEN)* Volver a la Orden → D198 · ⚑ AHSOKA_REGRESA

#### D197 · Las escaleras del Templo
**Juega:** Anakin · **Fuente:** TCW 5x20 *The Wrong Jedi*

Ahsoka baja las escaleras del Templo y se va.

- **A)** "Lo entiendo. Yo también he querido irme", y dejarla ir ★ → D199 · AHS +1
- **B)** Intentar retenerla, furioso con el Consejo → D199 · OSC +2
- **C)** *(si ⚑ ANAKIN_DUDA_ORDEN)* Dejar la Orden con ella → D309

#### D198 · Caballero Tano
**Juega:** Anakin · **Rama**

Ahsoka volvió. El Consejo la nombrará caballero Jedi.

- **A)** Pedir ser tú quien le corte la trenza → D199 · AHS +2
- **B)** Pedirle que siga un tiempo más como tu padawan → D199 · AHS +1 · OSC +1

# ACTO V — La conspiración

*20–19 ABY. Las piezas de la trampa de Sidious quedan a la vista de quien quiera verlas: el chip de los clones, Sifo-Dyas, la visión de Yoda. Lo que cada personaje haga con esas pistas decide qué tan preparada llega la Orden al final.*

## Capítulo 29 · El chip

#### D199 · Ringo Vinda
**Juega:** Rex · **Fuente:** TCW 6x01 *The Unknown*

En plena batalla, el clon Tup le dispara a la general Jedi Tiplar y murmura: "Los buenos soldados obedecen órdenes". *(Si ⚑ AHSOKA_REGRESA, la caballero Tano pelea con el 501.°.)*

- **A)** Someter a Tup y evitar que lo maten ★ → D200 · CLO +1
- **B)** Dispararle para detenerlo → D200 · CLO -1 *(Tup queda herido)*

#### D200 · Escolta a Kamino
**Juega:** Fives · **Fuente:** TCW 6x01 *The Unknown*

Tup está enfermo y los separatistas intentan llevárselo. Fives lo escolta a Kamino.

- **A)** Ir con Tup a Kamino ★ → D201 · CLO +1
- **B)** Pedirle al general Skywalker que vaya con ellos → D201 · ⚑ ANAKIN_EN_KAMINO

#### D201 · La autopsia
**Juega:** Fives · **Fuente:** TCW 6x02 *Conspiracy*

La doctora Nala Se quiere examinar a Tup a puerta cerrada. Fives desconfía y, con el droide médico AZ-3, encuentra un chip en el cerebro de Tup.

- **A)** Robar el chip con ayuda de AZ-3 ★ → D202 · PIS +2
- **B)** Avisar primero a la Maestra Shaak Ti → D202 · PIS +1 *(Nala Se esconde parte de la evidencia)*
- **C)** *(si ⚑ FIVES_EN_KAMINO)* Usar lo que sabe de los laboratorios para copiar todos los registros → D202 · PIS +3

#### D202 · El chip de Fives
**Juega:** Fives · **Fuente:** TCW 6x02 *Conspiracy*

Todos los clones tienen ese chip. Fives le pide a AZ-3 que le saque el suyo.

- **A)** Quitarse el chip ★ → D203 · ⚑ FIVES_SIN_CHIP
- **B)** Dejárselo para no levantar sospechas → D203

#### D203 · Lama Su
**Juega:** Fives · **Fuente:** TCW 6x03 *Fugitive*

Los kaminoanos dicen que el chip solo reduce la agresividad. El Canciller pide que Fives sea llevado a Coruscant. *(Si ⚑ ANAKIN_EN_KAMINO, Anakin escucha todo.)*

- **A)** Ir a Coruscant ★ → D204
- **B)** Escapar de Kamino con la evidencia directo hacia Rex → D206 · PIS +1

#### D204 · Ante el Canciller
**Juega:** Fives · **Fuente:** TCW 6x03 *Fugitive*

En la oficina de Palpatine, Fives está drogado y confundido. Palpatine sonríe demasiado tranquilo.

- **A)** Atacar al Canciller en la confusión ★ → D205
- **B)** Contenerse y negarse a la inyección → D205 · PIS +1 *(lo incriminan de todos modos, pero conserva la mente clara)*

#### D205 · Fugitivo
**Juega:** Fives · **Fuente:** TCW 6x04 *Orders*

Fives huye por Coruscant. Tiene una sola llamada.

- **A)** Llamar a Rex y al general Skywalker ★ → D207
- **B)** Llamar a la senadora Amidala → D207 · PIS +1 · PAD +1

#### D206 · De Kamino al 501
**Juega:** Rex · **Rama**

Fives llega con el chip en la mano y le cuenta todo a Rex.

- **A)** Llevarlo con el general Skywalker → D207
- **B)** Esconderlo y analizar el chip con el médico Kix → D207 · PIS +2

#### D207 · El almacén
**Juega:** Anakin · **Fuente:** TCW 6x04 *Orders* · ⟡ **Bifurcación mayor**

Fives, alterado, habla de una conspiración. El comandante Fox llega con sus tropas y le apunta.

- **A)** Intentar calmar a Fives mientras Fox apunta ★ → D208 *(Fox dispara: Fives muere)*
- **B)** Ponerte entre Fox y Fives con el sable encendido → D208 · CLO +2 · OSC +1 · ⚑ FIVES_VIVE
- **C)** *(requiere PIS ≥ 12)* Creerle a Fives y llevarlo tú mismo ante el Consejo → D208 · PIS +2 · ⚑ FIVES_VIVE

#### D208 · "Todo fue una conspiración"
**Juega:** Anakin · **Fuente:** TCW 6x04 *Orders*

*(Si Fives murió, esas fueron sus últimas palabras. Si ⚑ FIVES_VIVE, está en custodia Jedi.)* La versión oficial: un chip defectuoso.

- **A)** Aceptar la versión oficial ★ → D209
- **B)** *(si ⚑ FIVES_VIVE)* Exigir que el Consejo investigue los chips → D209 · PIS +3 · ⚑ CHIP_EXPUESTO
- **C)** *(si ⚑ FIVES_VIVE o PIS ≥ 15)* Pedirle a Kix que retire en secreto los chips del 501.° → D209 · CLO +2 · ⚑ 501_SIN_CHIP

## Capítulo 30 · Clovis y los bancos

#### D209 · Un viejo amigo
**Juega:** Padmé · **Fuente:** TCW 6x05 *An Old Friend*

Rush Clovis busca a Padmé: tiene pruebas de corrupción en el Clan Bancario.

- **A)** Ayudarlo a investigar ★ → D210 · PIS +1
- **B)** Negarse para no provocar a Anakin → D210 · PAD +1

#### D210 · Celos
**Juega:** Anakin · **Fuente:** TCW 6x06 *The Rise of Clovis*

Otra vez Clovis, otra vez cerca de Padmé. *(Si ⚑ CLOVIS_RESENTIDO, Clovis te provoca a propósito.)*

- **A)** Discutir con Padmé ★ → D211 · OSC +1 · PAD -1
- **B)** Confiar en ella y proteger a Clovis → D211 · PAD +2
- **C)** Golpear a Clovis → D211 · OSC +2 · PAD -2

#### D211 · Espacio
**Juega:** Padmé · **Fuente:** TCW 6x06 *The Rise of Clovis*

Padmé está harta de los celos de Anakin.

- **A)** Decirle que sin confianza no pueden seguir así ★ → D212 · PAD -1
- **B)** Ceder y alejarse de Clovis → D212 · PAD +1 · PIS -1

#### D212 · Scipio
**Juega:** Anakin · **Fuente:** TCW 6x07 *Crisis at the Heart*

Clovis, ahora al frente del Clan Bancario, se alió con Dooku. El Canciller te manda a Scipio: Padmé está ahí.

- **A)** Ir ★ → D213
- **B)** Preguntarle al Canciller por qué apoyó a Clovis al principio → D213 · PIS +1 · PAL -1

#### D213 · Rehén
**Juega:** Anakin · **Fuente:** TCW 6x07 *Crisis at the Heart*

Clovis tiene a Padmé y los droides invaden la bóveda.

- **A)** Atacar a Clovis ★ → D214
- **B)** Negociar con él → D214 · PAD +1

#### D214 · Colgando
**Juega:** Anakin · **Fuente:** TCW 6x07 *Crisis at the Heart*

Sostienes la mano de Clovis, y Clovis la de Padmé, sobre el vacío. Pesan demasiado.

- **A)** Aguantar; Clovis se suelta para salvarla ★ → D215
- **B)** Soltar tú a Clovis → D215 · OSC +2
- **C)** Intentar subir a los dos con la Fuerza → D215 · OSC +1 · PAD +1

#### D215 · Los bancos del Canciller
**Juega:** Anakin · **Fuente:** TCW 6x07 *Crisis at the Heart*

Tras la crisis, el Canciller toma el control del Clan Bancario. Padmé está preocupada: "Acumula demasiado poder".

- **A)** Defender al Canciller ★ → D216 · PAL +1 · PAD -1
- **B)** Darle la razón a Padmé → D216 · PAD +1 · PIS +1
- **C)** *(si ⚑ LEY_APROBADA)* "Desde la ley bancaria, todo pasa por él" → D216 · PIS +2

## Capítulo 31 · Sifo-Dyas

#### D216 · Oba Diah
**Juega:** Obi-Wan · **Fuente:** TCW 6x10 *The Lost One*

Plo Koon (Kit Fisto, si ⚑ PLO_MUERTO) y tú encuentran el sable del Maestro Sifo-Dyas en manos de los Pyke. Lo mataron por encargo.

- **A)** Seguir el rastro del pago ★ → D217 · PIS +1
- **B)** *(si ⚑ KRELL_PRESO)* Interrogar a Krell sobre lo que vio → D217 · PIS +2
- **C)** *(si ⚑ VENTRESS_INFORMANTE o ⚑ MAUL_MENSAJE)* Unirlo a lo que ya sabían de Dooku → D217 · PIS +2

#### D217 · Tyranus
**Juega:** Obi-Wan · **Fuente:** TCW 6x10 *The Lost One*

El que pagó es "Tyranus": el Conde Dooku. El mismo que contrató a Jango Fett para el ejército clon.

- **A)** Informar al Consejo y al Canciller ★ → D218 *(Palpatine pide encargarse él)*
- **B)** Informar solo al Consejo → D218 · PIS +2 · ⚑ INVESTIGACION_SECRETA

#### D218 · El Consejo decide
**Juega:** Mace Windu · **Fuente:** TCW 6x10 *The Lost One*

Un Sith creó el ejército que pelea por la República. Pero sin los clones, la guerra está perdida.

- **A)** Seguir usando a los clones y cerrar el caso ★ → D219
- **B)** *(si ⚑ CHIP_EXPUESTO o ⚑ INVESTIGACION_SECRETA)* Unir las pistas: el ejército lo hizo un Sith y tiene chips → D219 · PIS +3 · ⚑ CONSEJO_SOSPECHA_CLONES

#### D219 · Obi-Wan preocupado
**Juega:** Anakin

Notas a Obi-Wan inquieto desde hace días.

- **A)** No preguntar ★ → D220
- **B)** Preguntarle qué pasa → D220 · OBI +1 · PIS +1
- **C)** Preguntarle al Canciller qué inquieta al Consejo → D220 · PAL +1

## Capítulo 32 · El viaje de Yoda

#### D220 · Voces
**Juega:** Yoda · **Fuente:** TCW 6x11 *Voices*

Yoda oye la voz de Qui-Gon Jinn, muerto hace años. El Consejo teme que esté perdiendo la razón.

- **A)** Seguir la voz en secreto, solo con R2 ★ → D221
- **B)** Contárselo todo al Consejo → D221 · PIS -1 *(el Canciller se entera del viaje)*

#### D221 · Dagobah
**Juega:** Yoda · **Fuente:** TCW 6x11 *Voices*

En una cueva de Dagobah, Yoda enfrenta a su propia sombra.

- **A)** Encararla sin miedo ★ → D222 · PIS +1
- **B)** Atacarla → D222

#### D222 · Las sacerdotisas
**Juega:** Yoda · **Fuente:** TCW 6x12 *Destiny*

Las sacerdotisas de la Fuerza ponen a Yoda a prueba en su planeta de origen.

- **A)** Aceptar las pruebas ★ → D223
- **B)** Preguntarles por el futuro de Skywalker → D223 · PIS +1 · ⚑ YODA_VIO_ANAKIN

#### D223 · Moraband
**Juega:** Yoda · **Fuente:** TCW 6x13 *Sacrifice*

En el mundo natal de los Sith, Sidious y Dooku atacan la mente de Yoda con una ilusión: Anakin en peligro y una oferta para salvar a todos los Jedi.

- **A)** Sacrificarse en la ilusión para salvar a Anakin ★ → D224
- **B)** Pelear contra Sidious dentro de la visión → D224 · PIS +1

#### D224 · La lección
**Juega:** Yoda · **Fuente:** TCW 6x13 *Sacrifice*

Qui-Gon le enseña: esta guerra no se ganará, pero se puede preparar una victoria futura.

- **A)** Volver y no decir nada ★ → D225
- **B)** Contarle al Consejo lo que vio sobre Anakin → D225 · PIS +2 · OSC +1 · ⚑ CONSEJO_VIGILA

#### D225 · La mirada de Yoda
**Juega:** Anakin

Yoda volvió y te mira de un modo extraño. *(Si ⚑ YODA_VIO_ANAKIN, sabe más de lo que dice.)*

- **A)** Ignorarlo ★ → D226
- **B)** Preguntarle qué vio → D226 · OSC -1 · OBI +1
- **C)** *(si ⚑ MORTIS_RECUERDA)* Contarle a Yoda la visión de Mortis → D226 · PIS +2 · OSC -1 · ⚑ YODA_SABE_VADER

#### D226 · Lo que la Fuerza puede hacer
**Juega:** Anakin

Palpatine, en una cena: "Algunos dicen que la Fuerza puede salvar a quienes amamos de la muerte. Los Jedi jamás lo enseñarían".

- **A)** Escuchar con interés ★ → D227 · PAL +1
- **B)** Despedirte con cortesía → D227 · PAL -1

#### D227 · Mon Mothma y Bail
**Juega:** Padmé

Mon Mothma y Bail Organa le confían a Padmé su miedo: el Canciller no piensa soltar el poder.

- **A)** Unirse a ellos en secreto ★ → D228 · PIS +1
- **B)** Defender a Palpatine: es de Naboo y siempre la apoyó → D228 · PAL +1

## Capítulo 33 · Discípula oscura

#### D228 · La orden de matar
**Juega:** Mace Windu · **Fuente:** novela *Dark Disciple*

El Consejo discute algo nunca visto: asesinar al Conde Dooku para terminar la guerra.

- **A)** Autorizar el asesinato ★ → D229
- **B)** Rechazarlo: no es el camino Jedi → D233

#### D229 · Quinlan y Ventress
**Juega:** Quinlan Vos · **Fuente:** novela *Dark Disciple*

Quinlan Vos se alía con Asajj Ventress para llegar a Dooku. Ella le ofrece enseñarle el lado oscuro.

- **A)** Aceptar su entrenamiento ★ → D230
- **B)** Rechazar los métodos oscuros → D230 · ⚑ QUINLAN_LUZ

#### D230 · Amor
**Juega:** Quinlan Vos · **Fuente:** novela *Dark Disciple*

Quinlan y Ventress se enamoran.

- **A)** Admitirlo ★ → D231
- **B)** Reprimirlo → D231 *(Ventress se aleja y en el atentado estará sola)*

#### D231 · El atentado
**Juega:** Quinlan Vos · **Fuente:** novela *Dark Disciple* · ⟡ **Bifurcación mayor**

Quinlan tiene a Dooku frente a él.

- **A)** Atacar y fallar; Dooku lo captura ★ → D232
- **B)** *(si ⚑ QUINLAN_LUZ)* Atacar con calma y vencerlo → D233 · PIS +1 · ⚑ DOOKU_MUERTO_TEMPRANO
- **C)** *(si ⚑ DOOKU_DUDA)* Aceptar la rendición que Dooku ofrece a cambio de protección → D233 · PIS +3 · ⚑ DOOKU_PRISIONERO

#### D232 · El sacrificio de Ventress
**Juega:** Asajj Ventress · **Fuente:** novela *Dark Disciple*

Quinlan cayó al lado oscuro y Dooku está por matarlo con un rayo.

- **A)** Recibir el rayo por él ★ → D233
- **B)** Huir con Quinlan sin pelear → D233 *(Quinlan sigue tocado por la oscuridad)*

#### D233 · El Consejo también mata
**Juega:** Anakin

Te enteras de que el Consejo ordenó un asesinato. *(Si ⚑ DOOKU_MUERTO_TEMPRANO, Dooku está muerto; si ⚑ DOOKU_PRISIONERO, está preso en el Templo.)*

- **A)** "Entonces no son tan distintos de mí" ★ → D234 · OSC +1 · PAL +1
- **B)** "Al menos intentaron terminar la guerra" → D234 · OBI +1

## Capítulo 34 · Crisis en Utapau

#### D234 · Muerte en Utapau
**Juega:** Anakin · **Fuente:** *The Clone Wars Legacy*: *Crystal Crisis on Utapau*

Un Jedi apareció muerto en Utapau. Obi-Wan y tú investigan.

- **A)** Investigar junto a Obi-Wan ★ → D235
- **B)** Bajar solo a los sumideros → D235 · OSC +1

#### D235 · El cristal gigante
**Juega:** Anakin · **Fuente:** *Crystal Crisis on Utapau*

Alguien le vende a Grievous un cristal kyber enorme, capaz de alimentar un arma devastadora.

- **A)** Destruirlo ★ → D236
- **B)** Llevarlo a la República, como pide el Canciller → D236 · PAL +2 · ⚑ CRISTAL_REPUBLICA

#### D236 · Orgullo
**Juega:** Obi-Wan

Al terminar, Obi-Wan quiere decirle a Anakin algo que casi nunca dice.

- **A)** "Estoy orgulloso de ti" ★ → D237 · OBI +2
- **B)** Guardar la reserva Jedi → D237 · OBI -1

## Capítulo 35 · Batuu

#### D237 · Padmé desaparecida
**Juega:** Anakin · **Fuente:** novela *Thrawn: Alliances*

Padmé fue a Batuu a investigar un mensaje de su antigua doncella y dejó de responder.

- **A)** Ir a Batuu sin avisar al Consejo ★ → D238 · PAD +1 · OBI -1
- **B)** Pedir permiso primero → D238 · OBI +1 · PAD -1 *(llegas un día tarde)*

#### D238 · El oficial chiss
**Juega:** Anakin · **Fuente:** novela *Thrawn: Alliances*

En Batuu conoces a Thrawn, un oficial chiss que investiga lo mismo que Padmé.

- **A)** Aliarte con él ★ → D239
- **B)** Desconfiar y seguir solo → D239 · OSC +1

#### D239 · Las palabras de Thrawn
**Juega:** Anakin · **Fuente:** novela *Thrawn: Alliances*

Thrawn deduce lo que Padmé significa para ti: "El miedo a perder algo puede llevarte a destruirlo".

- **A)** Ignorar el comentario ★ → D240 · OSC +1
- **B)** Pensarlo en serio → D240 · OSC -1 · PAD +1

#### D240 · La fábrica de Batuu
**Juega:** Anakin · **Fuente:** novela *Thrawn: Alliances*

Encuentran a Padmé en una fábrica separatista a punto de volar.

- **A)** Rescatarla junto a Thrawn ★ → D241 · PAD +1
- **B)** Destruir la fábrica con rabia → D241 · OSC +2

## Capítulo 36 · La Remesa Mala

#### D241 · La voz de Echo
**Juega:** Rex · **Fuente:** TCW 7x01 *The Bad Batch*

Los separatistas predicen cada movimiento del 501.°. Rex sospecha que usan la mente de Echo, a quien todos creían muerto. *(Si ⚑ ECHO_SALVADO, Echo está vivo en el 501.°.)*

- **A)** Convencer al general Skywalker de buscarlo ★ → D242 · CLO +1
- **B)** Aceptar que está muerto → D242 · CLO -1
- **C)** *(si ⚑ ECHO_SALVADO)* Usar lo que sabe Echo para romper el algoritmo → D244 · CLO +1

#### D242 · Skako Minor
**Juega:** Anakin · **Fuente:** TCW 7x03 *On the Wings of Keeradaks*

Con la Remesa Mala llegas a Skako Minor, sede de la Unión Tecnológica. *(Si ⚑ TAMBOR_EJECUTADO, otro emir ocupa el lugar de Wat Tambor.)*

- **A)** Aliarte con los poletec y sus keeradaks ★ → D243
- **B)** Infiltrarte en silencio → D243 · CLO -1

#### D243 · Echo
**Juega:** Rex · **Fuente:** TCW 7x03 *On the Wings of Keeradaks*

Echo está vivo, convertido en cíborg y conectado a la computadora separatista.

- **A)** Desconectarlo aunque sea arriesgado ★ → D244 · CLO +2
- **B)** Dejarlo conectado para mandar información falsa → D244 · CLO -1 · PIS +1

#### D244 · Tech
**Juega:** Anakin

Mientras reparan a Echo, Tech, de la Remesa Mala, comenta que sus cerebros "no salieron como los kaminoanos querían".

- **A)** No darle importancia ★ → D245
- **B)** Preguntarle a qué se refiere → D245 · PIS +2
- **C)** *(si ⚑ FIVES_VIVE o ⚑ CHIP_EXPUESTO)* Pedirles a Tech y a Kix que retiren los chips del 501.° → D245 · CLO +2 · ⚑ 501_SIN_CHIP

#### D245 · El camino de Echo
**Juega:** Echo · **Fuente:** TCW 7x04 *Unfinished Business*

Echo puede quedarse con Rex o irse con la Remesa Mala.

- **A)** Irse con la Remesa Mala ★ → D246
- **B)** Quedarse con Rex → D246 · CLO +1

## Capítulo 37 · El camino de Ahsoka

#### D246 · Los niveles bajos
**Juega:** Ahsoka · **Fuente:** TCW 7x05 *Gone with a Trace*

Ahsoka vive en el bajo Coruscant y conoce a las hermanas Trace y Rafa Martez. *(Si ⚑ AHSOKA_REGRESA, está ahí en misión encubierta del Consejo.)*

- **A)** Ayudar a las hermanas ★ → D247
- **B)** Llamar a Anakin para saber de él → D247 · AHS +2

#### D247 · Los Pyke
**Juega:** Ahsoka · **Fuente:** TCW 7x08 *Together Again*

Rafa se metió en un trabajo de especia para los Pyke. Detrás de ellos asoma el Colectivo Sombra de Maul.

- **A)** Proteger a las hermanas ★ → D248
- **B)** Investigar la conexión entre los Pyke y Maul → D248 · PIS +1

#### D248 · Bo-Katan
**Juega:** Ahsoka · **Fuente:** TCW 7x08 *Together Again*

Bo-Katan Kryze encuentra a Ahsoka: Maul controla Mandalore y necesitan una Jedi. *(Si ⚑ BOKATAN_ALIADA, Bo-Katan ya cuenta con apoyo de la República.)*

- **A)** Aceptar y pedir ayuda a Anakin y Obi-Wan ★ → D249
- **B)** Ir sola con Bo-Katan → D249 · AHS -1

# ACTO VI — La caída

*19 ABY. Del rescate del Canciller sobre Coruscant hasta Mustafar. Aquí se cobran todos los medidores y banderas del juego: después de la revelación de Palpatine, la historia se separa en cuatro líneas (oscura/canon, luz, emperador y exilio).*

## Capítulo 38 · Batalla de Coruscant

#### D249 · Reencuentro
**Juega:** Anakin · **Fuente:** TCW 7x09 *Old Friends Not Forgotten*

Ahsoka y Bo-Katan piden ayuda contra Maul en Mandalore. En ese mismo momento, Grievous ataca Coruscant y secuestra al Canciller. *(Si ⚑ AHSOKA_REGRESA, Ahsoka es caballero y pide el apoyo como general. Si ⚑ SATINE_VIVE, Satine encabeza la resistencia junto a Bo-Katan.)*

- **A)** Ir a Coruscant y darle a Ahsoka a Rex y una división del 501.° ★ → D250 · AHS +1 · CLO +1
- **B)** Ir a Coruscant y que Ahsoka se arregle con los mandalorianos → D250 · AHS -2

#### D250 · Sobre Coruscant
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Droides zumbadores destrozan el caza de Obi-Wan. "¡Sigue sin mí!".

- **A)** Quitárselos de encima aunque te arriesgues ★ → D251 · OBI +1
- **B)** Obedecer y seguir → D251 · OBI -1 *(Obi-Wan aterriza de milagro)*

#### D251 · La Mano Invisible
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Encuentran a Palpatine encadenado. Entra el Conde Dooku. *(Si ⚑ DOOKU_MUERTO_TEMPRANO o ⚑ DOOKU_PRISIONERO, llega Grievous con sus MagnaGuardias: esta ficha se juega contra él y la siguiente no aparece.)*

- **A)** Pelear junto a Obi-Wan ★ → D252
- **B)** Mandar a Obi-Wan a liberar al Canciller y pelear solo → D252 · OSC +1
- **C)** *(si ⚑ DOOKU_DUDA)* Notar que Dooku duda y preguntarle quién es su maestro → D252 · PIS +2

#### D252 · "Mátalo"
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith* · ⟡ **Bifurcación mayor**

Le cortas las manos a Dooku. Palpatine ordena: "Mátalo, Anakin. Mátalo ahora".

- **A)** Matarlo ★ → D253 · OSC +3 · PAL +2
- **B)** Perdonarlo y arrestarlo → D253 · OSC -1 · PAL -1 · ⚑ DOOKU_PRISIONERO
- **C)** *(si ⚑ DOOKU_DUDA)* Dejarlo hablar: "Él también me usó…", y Dooku mira al Canciller → D253 · PIS +3 · PAL -2 · ⚑ DOOKU_PRISIONERO

#### D253 · Obi-Wan en el suelo
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Obi-Wan está inconsciente. "Déjalo, Anakin. No hay tiempo".

- **A)** Cargar a Obi-Wan ★ → D254 · OBI +1
- **B)** Dejarlo → D254 · OBI -3 · PAL +1 *(Obi-Wan despierta y escapa solo)*

#### D254 · La nave partida
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Grievous escapa y la *Mano Invisible* cae partida en dos sobre Coruscant.

- **A)** Pilotar lo que queda de la nave hasta aterrizar ★ → D255 · CLO +1
- **B)** Perseguir a Grievous hasta su cápsula → D255 · OSC +1 · CLO -2 *(escapa igual y el aterrizaje mata a varios)*

#### D255 · La noticia
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Padmé te espera en el Senado: "Anakin, estoy embarazada".

- **A)** "¡Es maravilloso!" ★ → D256 · PAD +2
- **B)** Preocuparte por la Orden: te expulsarán → D256 · PAD -1 · OSC +1
- **C)** Proponerle decírselo al Consejo y dejar la Orden → D256 · PAD +2 · ⚑ ANAKIN_DUDA_ORDEN

## Capítulo 39 · Pesadillas

#### D256 · El sueño
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Sueñas que Padmé muere al dar a luz, igual que soñaste con tu madre antes de perderla.

- **A)** Guardártelo ★ → D257 · OSC +1
- **B)** Contárselo a Padmé → D257 · PAD +1 · ⚑ PADME_SABE_VISIONES
- **C)** *(si ⚑ ANAKIN_SABE_VISION)* Recordar que Ahsoka tuvo una visión de Padmé y logró evitarla → D257 · OSC -1 · AHS +1

#### D257 · Yoda
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Le preguntas a Yoda por visiones de muerte, sin nombrar a Padmé. "Entrénate para dejar ir todo lo que temes perder".

- **A)** Aceptar el consejo, aunque no te alcance ★ → D258 · OSC +1
- **B)** Contarle toda la verdad: Padmé y el bebé → D258 · OSC -2 · ⚑ YODA_SABE_MATRIMONIO
- **C)** *(si ⚑ YODA_SABE_VADER o ⚑ MORTIS_RECUERDA)* Hablarle de Mortis y de la armadura negra → D258 · OSC -1 · PIS +2

#### D258 · Naboo
**Juega:** Padmé · **Fuente:** película *La venganza de los Sith*

Padmé sueña con criar a su hijo en Naboo. *(Si ⚑ PADME_SABE_VISIONES, ella también tiene miedo.)*

- **A)** Pedirle a Anakin que no se preocupe ★ → D259
- **B)** Proponerle irse a Naboo ya → D259 · PAD +1 · ⚑ ANAKIN_DUDA_ORDEN
- **C)** *(si ⚑ PADME_SABE_VISIONES)* Pedirle a Obi-Wan que ayude a Anakin → D259 · OBI +1 · ⚑ OBI_SABE_MATRIMONIO

#### D259 · Obi-Wan pregunta
**Juega:** Obi-Wan

Notas a Anakin distraído y agotado. *(Si ⚑ OBI_SABE_MATRIMONIO, sabes por qué.)*

- **A)** No presionarlo ★ → D260
- **B)** Preguntarle directamente qué le pasa → D260 · OBI +1

#### D260 · El representante
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Palpatine: "Quiero que seas mi representante personal en el Consejo Jedi".

- **A)** Aceptar ★ → D261 · PAL +2
- **B)** Pedir que lo decida el Consejo → D261 · PAL -1 · OBI +1

## Capítulo 40 · El Consejo y la ópera

#### D261 · Sin rango de Maestro
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

El Consejo te acepta, pero sin el rango de Maestro.

- **A)** "¿Qué? ¡Esto es injusto!" ★ → D262 · OSC +1 · OBI -1
- **B)** Aceptarlo con calma → D262 · OBI +1
- **C)** *(si ⚑ MACE_RESPETA)* Mace habla a tu favor; aceptar con respeto → D262 · OBI +1 · OSC -1

#### D262 · Espiar al Canciller
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Obi-Wan te pide informar sobre los movimientos del Canciller.

- **A)** Aceptar a regañadientes ★ → D263 · OBI -1 · PIS +1
- **B)** Negarte: es una traición → D263 · PAL +1 · OBI -2
- **C)** Aceptar de verdad y comprometerte → D263 · PIS +2 · OBI +1
- **D)** *(si ⚑ DOOKU_PRISIONERO)* Visitar antes a Dooku en su celda → D263 · PIS +3 · ⚑ SOSPECHA_PALPATINE

#### D263 · La ópera
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

En la ópera, Palpatine cuenta "la tragedia de Darth Plagueis el Sabio": un Sith capaz de impedir que murieran los que amaba.

- **A)** "¿Es posible aprender ese poder?" ★ → D264 · PAL +2 · OSC +1
- **B)** "Esa es una leyenda Sith" → D264 · PAL -1 · PIS +1
- **C)** *(si ⚑ SIDIOUS_VISTO)* Reconocer la voz del holograma de Mustafar → D264 · PIS +3 · ⚑ SOSPECHA_PALPATINE

#### D264 · Utapau
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Le llevas al Consejo la noticia: Grievous está en Utapau. El Canciller quería que fueras tú; el Consejo manda a Obi-Wan.

- **A)** Aceptarlo ★ → D265
- **B)** Pedir ir con Obi-Wan → D265 · OBI +1 *(el Consejo se niega)*

#### D265 · La despedida
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Obi-Wan parte a Utapau.

- **A)** "Perdóname por ser tan arrogante. Te aprecio, maestro" ★ → D266 · OBI +2
- **B)** Despedirte con frialdad → D266 · OBI -1
- **C)** *(si ⚑ MORTIS_RECUERDA o OBI ≥ 15)* Contarle todo: Padmé, los sueños, el Canciller → D266 · OBI +3 · PIS +1 · ⚑ OBI_SABE_MATRIMONIO

#### D266 · Detener la guerra
**Juega:** Padmé · **Fuente:** película *La venganza de los Sith* (escenas eliminadas)

Padmé, Bail y Mon Mothma reúnen las firmas de dos mil senadores contra el poder del Canciller.

- **A)** Pedirle a Anakin que le pida al Canciller detener la guerra ★ → D267 · PAD -1 *("No me pidas eso")*
- **B)** No meterlo en política → D267 · PAD +1

## Capítulo 41 · El Asedio de Mandalore

#### D267 · Maul
**Juega:** Ahsoka · **Fuente:** TCW 7x10 *The Phantom Apprentice*

En Sundari, Maul le dice a Ahsoka: "Sidious está preparando a Skywalker para ser su nuevo aprendiz. Ayúdame a matarlo antes". *(Si ⚑ AHSOKA_SABE_VADER, Ahsoka recuerda lo que Anakin vio en Mortis.)*

- **A)** Rechazar la alianza y pelear ★ → D268
- **B)** Escucharlo y pedirle pruebas → D268 · PIS +2
- **C)** *(si ⚑ AHSOKA_SABE_VADER)* Creerle de inmediato → D268 · PIS +3 · ⚑ AHSOKA_CREE_MAUL

#### D268 · El duelo
**Juega:** Ahsoka · **Fuente:** TCW 7x10 *The Phantom Apprentice*

Ahsoka y Maul pelean en los andamios del palacio.

- **A)** Capturar a Maul vivo ★ → D269
- **B)** Matarlo → D269 · PIS -1 *(se pierde lo que sabía)*

#### D269 · Avisar
**Juega:** Ahsoka · **Fuente:** TCW 7x11 *Shattered* · ⟡ **Bifurcación mayor**

Ahsoka tiene a Maul preso y sus palabras en la cabeza. Anakin está con el Canciller.

- **A)** Informar al Consejo y preguntar por Anakin ★ → D270 · PIS +1
- **B)** *(si ⚑ AHSOKA_CREE_MAUL o ⚑ AHSOKA_REGRESA)* Llamar a Anakin directo y advertirle → D270 · AHS +3 · ⚑ ADVERTENCIA_AHSOKA
- **C)** Llamar a Padmé → D270 · PAD +1 · PIS +1 · ⚑ PADME_ADVERTIDA

#### D270 · El transporte
**Juega:** Rex · **Fuente:** TCW 7x11 *Shattered*

Rex escolta a Maul a Coruscant. Desde hace días siente un zumbido en la cabeza.

- **A)** Seguir el procedimiento ★ → D271
- **B)** *(si ⚑ FIVES_VIVE o ⚑ CHIP_EXPUESTO)* Pedirle a Kix que le revise el chip ya → D271 · CLO +1 · ⚑ REX_SIN_CHIP

#### D271 · Grievous
**Juega:** Obi-Wan · **Fuente:** película *La venganza de los Sith*

En Utapau enfrentas a Grievous y sus cuatro sables.

- **A)** Pelear y perseguirlo montado en tu varactyl ★ → D272
- **B)** Pedir refuerzos a Anakin → D272 · OBI +1 *(el Consejo no lo deja ir)*

#### D272 · "Tan incivilizado"
**Juega:** Obi-Wan · **Fuente:** película *La venganza de los Sith*

Grievous está en el suelo de la plataforma.

- **A)** Dispararle ★ → D273
- **B)** Capturarlo para interrogarlo → D273 · PIS +2 *(Grievous jura que su amo "está en Coruscant y verá caer a todos")*

## Capítulo 42 · La revelación

#### D273 · El Canciller es un Sith
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith* · ⟡ **Bifurcación mayor**

Le llevas a Palpatine la noticia de Utapau. Te ofrece salvar a Padmé con el lado oscuro y confiesa que es Darth Sidious.

- **A)** Encender el sable sin matarlo: "Te entregaré al Consejo" ★ → D274
- **B)** *(requiere OSC ≥ 35)* Matarlo ahí mismo → D305
- **C)** *(requiere PAD ≥ 25 o ⚑ ANAKIN_DUDA_ORDEN)* Ir directo con Padmé para huir esa misma noche → D309

#### D274 · Mace
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Le cuentas todo a Mace Windu. "Espera en la cámara del Consejo hasta que regresemos".

- **A)** Obedecer ★ → D275
- **B)** *(si ⚑ MACE_RESPETA o ⚑ SOSPECHA_PALPATINE)* Insistir en ir; Mace acepta → D277
- **C)** *(si ⚑ ADVERTENCIA_AHSOKA)* Contarle a Mace lo que dijo Ahsoka de Maul y de los clones → D275 · PIS +2 · ⚑ CONSEJO_SOSPECHA_CLONES

#### D275 · La espera
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Atardece sobre Coruscant. Miras hacia el departamento de Padmé. Si Palpatine muere, se muere con él la única forma de salvarla.

- **A)** Ir a la oficina del Canciller ★ → D277
- **B)** *(requiere OBI ≥ 20 o PIS ≥ 25)* Quedarte y confiar en Mace → D298
- **C)** Ir a ver a Padmé primero → D276

#### D276 · Padmé en la ventana
**Juega:** Padmé · **Rama**

Anakin llega y se lo cuenta todo.

- **A)** Pedirle que vaya a ayudar a Mace → D277 · PAD +2 · OSC -2
- **B)** *(requiere PAD ≥ 25)* Pedirle que huyan esa noche → D309

#### D277 · El duelo en la oficina
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith* · ⟡ **Bifurcación mayor**

Mace tiene a Sidious acorralado contra la ventana. "Es demasiado peligroso dejarlo vivo". *(Si llegaste con Mace, viste todo el duelo.)*

- **A)** Cortarle la mano a Mace ★ → D278 · OSC +5
- **B)** *(requiere OBI ≥ 20 o PIS ≥ 25 o PAL ≤ 12)* Ayudar a Mace a arrestarlo → D298 · ⚑ SIDIOUS_ARRESTADO
- **C)** *(requiere OBI ≥ 20 o PIS ≥ 25 o PAL ≤ 12)* Dejar que Mace lo mate → D298 · OSC +1 · ⚑ SIDIOUS_MUERTO

#### D278 · Arrodillarse
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Mace cae por la ventana. Sidious te tiende la mano: "Haz lo que debas para salvarla".

- **A)** Arrodillarte ★ → D279 · OSC +3 · PAL +3
- **B)** *(si ⚑ MORTIS_RECUERDA o AHS ≥ 55)* Recordar la armadura negra, o la voz de Ahsoka, y negarte → D296
- **C)** *(requiere OSC ≥ 45)* Fingir lealtad para matarlo cuando baje la guardia → D305 · OSC +2

#### D279 · Darth Vader
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

"De ahora en adelante serás Darth Vader". Sidious te ordena ir al Templo Jedi. *(Si vienes del exilio, Sidious te recibe igual: sabía que volverías.)*

- **A)** "¿Qué quiere que haga, mi maestro?" ★ → D281
- **B)** Pedirle que perdone a Obi-Wan y a Ahsoka → D280

#### D280 · "Perdónalos"
**Juega:** Anakin · **Rama**

"Si quieres salvarlos, primero demuéstrame que puedes soltarlos".

- **A)** Obedecer → D281 · OSC +2
- **B)** *(requiere OBI ≥ 20 o AHS ≥ 50)* Dudar y salir de la oficina → D296

## Capítulo 43 · Orden 66

#### D281 · Ejecuten la Orden 66
**Juega:** Rex · **Fuente:** TCW 7x11 *Shattered*

En el crucero sobre Mandalore, Rex recibe la orden. Le arde la cabeza. *(Si ⚑ FIVES_VIVE y ⚑ FIVES_SIN_CHIP, Fives está a bordo y le grita que resista.)*

- **A)** Resistir el chip lo justo para decirle a Ahsoka: "Busca a Fives" ★ → D282
- **B)** *(si ⚑ REX_SIN_CHIP o ⚑ 501_SIN_CHIP)* Negarse a la orden y proteger a Ahsoka → D282 · CLO +3 · ⚑ REX_LIBRE

#### D282 · Maul suelto
**Juega:** Ahsoka · **Fuente:** TCW 7x11 *Shattered*

Los clones van por Ahsoka. Maul está en una celda.

- **A)** Liberar a Maul como distracción ★ → D283
- **B)** Pelear sola sin soltarlo → D283 · CLO -2

#### D283 · El chip de Rex
**Juega:** Ahsoka · **Fuente:** TCW 7x12 *Victory and Death*

Ahsoka atrapa a Rex. La pista de Fives era el chip.

- **A)** Quitarle el chip y fingir sus muertes ★ → D284
- **B)** *(si ⚑ REX_LIBRE)* Rex ya es libre: salvar a más clones → D284 · CLO +2

#### D284 · Kaller
**Juega:** Caleb Dume · **Fuente:** cómic *Kanan: The Last Padawan* y *The Bad Batch* 1x01

El padawan Caleb Dume ve a sus clones disparar contra su maestra, Depa Billaba. "¡Corre, Caleb!" *(Si ⚑ CONSEJO_SOSPECHA_CLONES, el Consejo había alertado a Depa.)*

- **A)** Correr, como ordena Depa ★ → D285
- **B)** *(si ⚑ CONSEJO_SOSPECHA_CLONES)* Pelear junto a Depa, que ya esperaba la traición → D285 · ⚑ JEDI_PREPARADOS

#### D285 · El Templo
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Los iniciados se esconden en la cámara del Consejo. "Maestro Skywalker, son demasiados. ¿Qué hacemos?".

- **A)** Cumplir la orden ★ → D286 · OSC +5
- **B)** *(requiere OSC ≤ 32)* No poder hacerlo y dejarlos escapar → D296

## Capítulo 44 · Mustafar

#### D286 · El humo del Templo
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Padmé vio el humo desde su ventana. Le dices que los Jedi intentaron derrocar a la República.

- **A)** Sostener la mentira ★ → D287 · PAD -1
- **B)** Contarle la verdad → D288

#### D287 · El Consejo Separatista
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

En Mustafar te esperan los líderes separatistas.

- **A)** Ejecutarlos a todos ★ → D289 · OSC +3
- **B)** Tomar preso a Nute Gunray para cerrar la guerra en un tribunal → D289 · OSC +1 · PIS +1

#### D288 · La verdad
**Juega:** Padmé · **Rama**

Padmé escucha lo que Anakin hizo en el Templo.

- **A)** Pedirle que se vaya; Anakin parte a Mustafar → D287 · PAD -3
- **B)** Rogarle que se vaya con ella ahora → D291 · PAD +1 *(la escena de la plataforma ocurre en su departamento)*

#### D289 · El holograma
**Juega:** Obi-Wan · **Fuente:** película *La venganza de los Sith*

En el Templo, Obi-Wan y Yoda ven la grabación: Anakin matando iniciados y arrodillado ante Sidious. "Al joven Skywalker destruir debemos".

- **A)** "Mándame contra el Emperador; no mataré a Anakin". Yoda insiste ★ → D290
- **B)** Aceptar la misión de inmediato → D290 · OBI -2
- **C)** *(si ⚑ OBI_SABE_MATRIMONIO o ⚑ OBI_SABE_VADER)* Ir directo con Padmé: sabes que Anakin la buscará → D290 · OBI +1

#### D290 · Ir a Mustafar
**Juega:** Padmé · **Fuente:** película *La venganza de los Sith*

Obi-Wan te contó lo que hizo Anakin. Sabes dónde está.

- **A)** Ir a Mustafar ★ → D291
- **B)** *(requiere PAD ≤ 10)* Quedarse en Coruscant y mandarle un mensaje → D294
- **C)** *(si ⚑ PADME_ADVERTIDA)* Esconderse con Bail Organa: Ahsoka se lo advirtió → D294 · PAD -2

#### D291 · La plataforma
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Padmé te ruega: "Ven conmigo. Deja todo esto atrás".

- **A)** "Juntos derrocaremos al Emperador y gobernaremos la galaxia" ★ → D292
- **B)** *(requiere PAD ≥ 25)* Dejarlo todo e irte con ella → D309

#### D292 · Obi-Wan en la rampa
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Obi-Wan sale de la nave. "¡Mentirosa! ¡Lo trajiste para matarme!".

- **A)** Estrangular a Padmé con la Fuerza ★ → D293 · PAD -5 · OSC +3
- **B)** *(requiere PAD ≥ 25 o ⚑ PADME_SABE_VISIONES)* Contenerte: "Sube a la nave, Padmé" → D293 · PAD +1 · ⚑ PADME_A_SALVO

#### D293 · La posición alta
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Duelan sobre la lava. Obi-Wan salta a la orilla: "Se acabó, Anakin. Tengo la posición alta".

- **A)** "Subestimas mi poder", y saltar ★ → D295
- **B)** *(requiere PAL ≥ 31)* Retirarte y volver con Sidious → D294
- **C)** *(requiere OBI ≥ 15)* Bajar el sable: "Ayúdame, maestro" → D296

#### D294 · Vader entero
**Juega:** Anakin · **Rama**

Vuelves a Coruscant sin quemaduras y sin armadura. *(Si ⚑ PADME_A_SALVO, o si Padmé no fue a Mustafar, sigue viva.)*

- **A)** Buscar a Padmé y llevarla contigo "para protegerla" → FINAL 2 · PAD -3
- **B)** Dejar que se vaya con Obi-Wan → FINAL 2 · PAD +2

#### D295 · El traje
**Juega:** Anakin · **Fuente:** película *La venganza de los Sith*

Despiertas dentro de una armadura negra. "Lord Vader, ¿me escucha?". Preguntas por Padmé. "Parece que en tu ira la mataste". *(Si ⚑ PADME_A_SALVO, Sidious miente: Padmé vive.)*

- **A)** Gritar y destrozar la sala con la Fuerza ★ → FINAL 1
- **B)** *(si ⚑ MORTIS_RECUERDA)* Reconocer la armadura de la visión, callar y jurar que algún día lo destruirás → FINAL 1

## Línea de la luz

#### D296 · Algo se rompe
**Juega:** Anakin · **Rama** · ⟡ **Línea de la luz**

Venías de la oscuridad y algo te frenó: un recuerdo, una voz, una mirada. Sidious lo siente.

- **A)** Enfrentar a Sidious ahora → D297
- **B)** *(requiere PAD ≥ 25)* Huir con Padmé → D309

#### D297 · Contra Sidious
**Juega:** Anakin · **Rama**

Sidious te espera en la cámara del Senado: "Tu traición era inevitable".

- **A)** Pelear solo → D298 · OSC +2 · ⚑ SIDIOUS_MUERTO
- **B)** Pelear junto a Yoda, que llega al Senado → D298 · OSC -1 · ⚑ SIDIOUS_MUERTO
- **C)** Ofrecerle tu vida a cambio de la de Padmé → FP5

#### D298 · La última transmisión
**Juega:** Anakin · **Rama**

Sidious cayó, a manos de Mace, de Yoda o tuyas, pero antes alcanzó a transmitir: "Ejecuten la Orden 66". *(Si ⚑ SIDIOUS_ARRESTADO, sigue vivo y encadenado. Si la orden ya se estaba cumpliendo, cortarla salva a los que quedan.)*

- **A)** Correr al Templo → D299
- **B)** *(requiere PIS ≥ 25 o ⚑ CONSEJO_SOSPECHA_CLONES)* Cortar la señal en la red de mando del ejército → D300 · ⚑ ORDEN66_DETENIDA
- **C)** Ir por Padmé → D302 · PAD +2

#### D299 · Los clones en el Templo
**Juega:** Anakin · **Rama**

Los clones de la Guardia de Coruscant entran al Templo.

- **A)** Pelear junto a los Jedi → D300 · CLO -3
- **B)** *(si ⚑ 501_SIN_CHIP o ⚑ REX_LIBRE)* Ordenar al 501.° que defienda el Templo → D300 · CLO +3 · ⚑ TEMPLO_SALVADO
- **C)** Sacar a los iniciados por los túneles → D300 · ⚑ INICIADOS_A_SALVO

#### D300 · Rex
**Juega:** Rex · **Rama**

Sobre Mandalore, Rex siente el zumbido. *(Si ⚑ ORDEN66_DETENIDA, la orden llegó cortada y los clones dudan.)*

- **A)** Resistir y avisarle a Ahsoka → D301 · CLO +1
- **B)** *(si ⚑ REX_SIN_CHIP o ⚑ ORDEN66_DETENIDA)* Proteger a Ahsoka contra su propia compañía → D301 · CLO +2 · ⚑ REX_LIBRE

#### D301 · Utapau
**Juega:** Obi-Wan · **Rama**

El comandante Cody recibe la orden. *(Si ⚑ ORDEN66_DETENIDA, Cody duda con el blaster en la mano.)*

- **A)** Notar la duda de Cody y hablarle → D302 · OBI +1
- **B)** Caer al abismo con tu varactyl y esconderte → D302

#### D302 · El Senado sin Canciller
**Juega:** Padmé · **Rama**

Palpatine cayó. *(Si ⚑ SIDIOUS_MUERTO, está muerto; si ⚑ SIDIOUS_ARRESTADO, espera juicio.)* El Senado está en caos y los separatistas se quedaron sin líder.

- **A)** Proponer devolver los poderes de emergencia y negociar la paz → D303 · PAD +1
- **B)** Proponer a Bail Organa como canciller interino → D303 · PIS +1

#### D303 · La decisión de Anakin
**Juega:** Anakin · **Rama**

La guerra termina. El Consejo sabe lo que hiciste por la República y lo cerca que estuviste de destruirla. *(Si ⚑ YODA_SABE_MATRIMONIO, Yoda ya sabe lo de Padmé.)*

- **A)** Quedarte en la Orden y ayudar a reformarla → D304 · OBI +2
- **B)** Dejar la Orden y vivir con Padmé a la vista de todos → D304 · PAD +2
- **C)** *(si ⚑ YODA_SABE_MATRIMONIO)* Pedirle a Yoda que la Orden acepte a un Jedi casado → D304 · OBI +1 · PAD +1

#### D304 · Los gemelos
**Juega:** Padmé · **Rama**

Nacen Luke y Leia. Padmé vive.

- **A)** *(si ⚑ ORDEN66_DETENIDA o ⚑ TEMPLO_SALVADO)* Presentarles los niños a Obi-Wan, Ahsoka y Rex → FINAL 4
- **B)** *(sin ⚑ ORDEN66_DETENIDA ni ⚑ TEMPLO_SALVADO)* Esconderse con los niños mientras los Jedi sobrevivientes se reagrupan → FINAL 5

## Línea del emperador

#### D305 · El trono vacío
**Juega:** Anakin · **Rama** · ⟡ **Línea del emperador**

Sidious está muerto por tu mano. *(Si llegaste fingiendo lealtad, la Orden 66 ya se cumplió y lo mataste mientras dormía.)* En su escritorio están sus holocrones y los códigos de mando del ejército clon.

- **A)** Usar la Orden 66 contra los Jedi antes de que te juzguen → D306 · OSC +5
- **B)** *(requiere OBI ≥ 20)* Entregarte al Consejo y contar la verdad → D302 · OSC -2 · ⚑ SIDIOUS_MUERTO · ⚑ ORDEN66_DETENIDA *(solo si vienes de D273: la orden nunca se dio)*

#### D306 · La Orden 66, por tu mano
**Juega:** Anakin · **Rama**

Los clones obedecen el código del Canciller, sin importar quién lo use.

- **A)** Encabezar tú mismo el ataque al Templo → D307 · OSC +3
- **B)** Ordenar que perdonen a Obi-Wan y a Ahsoka → D307 · OBI +1 · AHS +1

#### D307 · Padmé
**Juega:** Padmé · **Rama**

Padmé sabe lo que hizo Anakin: mató al Canciller, tomó el ejército y lo usó contra los Jedi.

- **A)** Quedarse a su lado → FINAL 3
- **B)** Denunciarlo ante el Senado → D308

#### D308 · La senadora y el emperador
**Juega:** Anakin · **Rama**

Padmé te denunció ante toda la galaxia.

- **A)** Arrestarla "por su seguridad" → FINAL 3 · PAD -5
- **B)** *(requiere PAD ≥ 25)* Renunciar al poder por ella y desaparecer → D309

## Línea del exilio

#### D309 · La huida
**Juega:** Anakin · **Rama** · ⟡ **Línea del exilio**

Dejas todo atrás con Padmé. *(Si llegas aquí antes del Acto VI, la guerra sigue sin ti durante meses.)*

- **A)** Despedirte de Obi-Wan → D310 · OBI +2
- **B)** Irte sin decirle a nadie → D310

#### D310 · La llamada
**Juega:** Anakin · **Rama**

Palpatine te encuentra por holograma: "Puedo salvar a Padmé. Solo yo puedo".

- **A)** Cortar la comunicación → D311
- **B)** Escucharlo y volver a Coruscant → D279

#### D311 · La noticia
**Juega:** Padmé · **Rama**

Las noticias: los Jedi "traicionaron" a la República y Palpatine se proclamó emperador.

- **A)** Pedirle a Anakin que vuelva a ayudar → D296
- **B)** Pedirle que se queden escondidos → D312

#### D312 · Los gemelos
**Juega:** Padmé · **Rama**

Nacen Luke y Leia en un mundo apartado.

- **A)** Criarlos juntos, escondidos → FINAL 6
- **B)** Separarlos para despistar a Sidious: Luke con Obi-Wan y Leia con Bail → FINAL 6

# FINALES

*Cada final tiene variantes según las banderas que el jugador prendió en el camino. Las variantes no son fichas de decisión: son párrafos distintos del epílogo.*

## Finales principales

### FINAL 1 · Lord Vader *(canon)*
**Se llega por:** D295.

Anakin Skywalker muere en Mustafar y Darth Vader se levanta dentro de la armadura. En Polis Massa, Padmé da a luz a Luke y Leia y muere. Obi-Wan lleva a Luke a Tatooine, Bail Organa adopta a Leia y Yoda se exilia en Dagobah. Meses después, en Mustafar, Vader sangra un cristal kyber para forjar su sable rojo y empieza a buscar el poder sobre la muerte que su maestro le prometió (*Master of Evil*, 2025).

**Variantes:**
- *(si eligió D295 B)* Vader recuerda la armadura de Mortis. Sabe que este era el futuro que juró evitar y guarda en silencio una deuda con Sidious que tardará veinte años en cobrar.
- *(si ⚑ PADME_A_SALVO)* Sidious le miente a Vader: Padmé sobrevive escondida con los gemelos y la galaxia la cree muerta.
- *(si ⚑ JEDI_PREPARADOS)* Más Jedi sobreviven a la Orden 66. Depa Billaba vive y se esconde con Caleb.
- *(si ⚑ REX_LIBRE)* Rex y Ahsoka sacan a una parte del 332.° del crucero antes de que caiga.
- *(si ⚑ CRISTAL_REPUBLICA)* El gran cristal de Utapau ya está en manos del Imperio y el proyecto de la superarma se adelanta años.

### FINAL 2 · Vader sin máscara
**Se llega por:** D294.

Anakin vuelve de Mustafar sin quemaduras y sin armadura: es el aprendiz más poderoso que Sidious tuvo jamás y, por eso mismo, el más peligroso para él. El Imperio nace con un Vader de carne y hueso a su lado.

**Variantes:**
- *(si eligió D294 A)* Padmé vive en el palacio imperial, prisionera "por su seguridad". Los gemelos nacen bajo la mirada de Sidious.
- *(si eligió D294 B)* Padmé huye con Obi-Wan. Vader dedica los años siguientes a buscar a su esposa y a sus hijos.
- *(si ⚑ CRISTAL_REPUBLICA)* El proyecto de la superarma se adelanta años.

### FINAL 3 · Emperador Skywalker
**Se llega por:** D307 A o D308 A.

Anakin mató a Sidious y usó su arma secreta, la Orden 66, para eliminar a los Jedi antes de que lo juzgaran. Se proclama protector de la galaxia: no habrá más guerras porque nadie podrá desafiarlo.

**Variantes:**
- *(si eligió D307 A)* Padmé gobierna a su lado, convencida de que puede contenerlo.
- *(si eligió D308 A)* Padmé es prisionera y los gemelos crecen en el palacio sin conocer a su madre.
- *(si eligió D306 B)* Obi-Wan y Ahsoka sobreviven y encabezan la primera rebelión contra el emperador Skywalker.
- *(si ⚑ CRISTAL_REPUBLICA)* Anakin termina la superarma "para que nunca vuelva a haber otra guerra".

### FINAL 4 · El Elegido
**Se llega por:** D304 A *(requiere ⚑ ORDEN66_DETENIDA o ⚑ TEMPLO_SALVADO)*.

Sidious cae y su última orden no se cumple, o el Templo resiste. La guerra termina con la República herida pero viva. Anakin trae el equilibrio a la Fuerza, como decía la profecía, pero no como nadie lo imaginó: eligiendo a las personas por encima del poder.

**Variantes:**
- *(según D303)* Anakin ayuda a reformar la Orden; o la deja y vive con Padmé a la vista de todos; o es el primer Jedi casado con la bendición de Yoda.
- *(si ⚑ INICIADOS_A_SALVO)* Los iniciados del Templo crecen para ser la nueva generación de la Orden.
- *(si ⚑ REX_LIBRE)* Rex encabeza el retiro de los chips de todos los clones.

### FINAL 5 · La luz que resiste
**Se llega por:** D304 B.

Sidious cae, pero la Orden 66 alcanza a cumplirse. Miles de Jedi mueren y la República sobrevive desangrada y sin confianza en nadie. Anakin, Padmé y los sobrevivientes tienen que reconstruirlo todo.

**Variantes:**
- *(si ⚑ JEDI_PREPARADOS)* Muchos Jedi esperaban la traición y sobreviven.
- *(si ⚑ INICIADOS_A_SALVO)* Los iniciados del Templo escaparon por los túneles.
- *(si ⚑ REX_LIBRE)* El 501.° de Rex se vuelve la guardia de los Jedi sobrevivientes.

### FINAL 6 · El exilio
**Se llega por:** D312.

Anakin nunca se convierte en Darth Vader, pero tampoco detiene a Sidious. Desde un mundo apartado ve caer a la República y a la Orden. Es el Elegido que eligió no elegir.

**Variantes:**
- *(si eligió D312 A)* Luke y Leia crecen juntos, con sus dos padres, sin saber quiénes son.
- *(si eligió D312 B)* Los gemelos crecen separados, como en el canon, mientras Anakin y Padmé se esconden lejos de ellos.
- *(si llegó desde D197 C)* Anakin dejó la Orden con Ahsoka antes del final de la guerra; Sidious tuvo que buscar otro aprendiz y la guerra se alargó.

## Finales prematuros

Son derrotas que cortan la partida antes de tiempo. Sirven para que algunas decisiones extremas tengan consecuencias reales.

### FP1 · La deuda de los Hutt
**Se llega por:** D011 C. Rotta muere en Teth. Jabba se alía con los separatistas, la República pierde las rutas del Borde Exterior y el Consejo le quita el mando a Anakin.

### FP2 · El Hijo de Mortis
**Se llega por:** D109 B o D115 B. Anakin se queda en Mortis para siempre: como guardián que reemplaza al Padre (D109) o como aliado del Hijo (D115). En la galaxia, nadie vuelve a saber de él.

### FP3 · Sangre de mi maestro
**Se llega por:** D149 B. Anakin mata a Rako Hardeen, que era Obi-Wan disfrazado. Lo expulsan de la Orden y lo encarcelan; Palpatine lo indulta y lo toma como aprendiz dos años antes de lo previsto.

### FP4 · El juicio de Skywalker
**Se llega por:** D194 B. Barriss muere antes de confesar. Ahsoka es condenada por el atentado al Templo y a Anakin lo expulsan por asesinato.

### FP5 · El precio
**Se llega por:** D297 C. Sidious acepta la vida de Anakin a cambio de la de Padmé, y cumple solo la mitad del trato.

# APÉNDICE A — Banderas

Las 79 banderas del guion. Una bandera es un sí/no que se prende con una decisión y se revisa más adelante para abrir opciones o cambiar una escena. Esta tabla sirve también como lista de variables cuando se programe el juego.

| Bandera | Qué significa | Se prende en | Se revisa en |
|---|---|---|---|
| `501_SIN_CHIP` | Los clones del 501.° ya no tienen el chip inhibidor | D208, D244 | D281, D299 |
| `ADVERTENCIA_AHSOKA` | Ahsoka le advirtió a Anakin lo que dijo Maul | D269 | D274 |
| `AHSOKA_A_PRUEBA` | Anakin aceptó a Ahsoka de mala gana | D003 | D007 |
| `AHSOKA_CREE_MAUL` | Ahsoka cree la advertencia de Maul sobre Anakin | D267 | D269 |
| `AHSOKA_CULPA` | Ahsoka carga con la pérdida del Escuadrón Azul | D043 | D171 |
| `AHSOKA_DUDA_ORDEN` | Ahsoka piensa en dejar la Orden (se lo prometió a Lux) | D172 | D196 |
| `AHSOKA_LLEVA_ROTTA` | Ahsoka cargó a Rotta por el desierto | D016 | D017, D018 |
| `AHSOKA_OSCURA` | El Hijo de Mortis corrompió a Ahsoka | D110 | D111 |
| `AHSOKA_REGRESA` | Ahsoka volvió a la Orden después del juicio | D196 | D199, D246, D249, D269 |
| `AHSOKA_SABE` | Ahsoka sabe del matrimonio de Anakin y Padmé | D058 | D094 |
| `AHSOKA_SABE_VADER` | Ahsoka sabe lo que Anakin vio en Mortis | D117 | D267 |
| `AHSOKA_SOSPECHA` | Ahsoka sospecha lo de Padmé | D023, D058, D101 | D058 |
| `AHSOKA_TEMERARIA` | Ahsoka se volvió temeraria en combate | D005, D035 | D043 |
| `ANAKIN_DUDA_ORDEN` | Anakin ha dicho en voz alta que podría dejar la Orden | D051, D071, D164, D191, D255, D258 | D197, D273 |
| `ANAKIN_EN_KAMINO` | Anakin acompañó a Fives a Kamino | D200 | D203 |
| `ANAKIN_EN_MANDALORE` | Anakin fue con Obi-Wan a rescatar a Satine | D175 | D176 |
| `ANAKIN_SABE_VISION` | Anakin sabe que Ahsoka tuvo una visión sobre Padmé | D094 | D097, D256 |
| `ANAKIN_SOSPECHA_HARDEEN` | Obi-Wan le dejó a Anakin una pista de que seguía vivo | D147 | D149, D152 |
| `BANE_CAPTURADO` | Anakin capturó a Cad Bane en el Senado | D056 | D059 |
| `BARRISS_AMIGA` | Ahsoka y Barriss son amigas cercanas | D073, D076, D078 | D194 |
| `BARRISS_VIGILADA` | Anakin conoce las dudas de Barriss sobre la Orden | D078 | D187, D193 |
| `BOKATAN_ALIADA` | Obi-Wan le prometió ayuda a Bo-Katan | D179 | D248 |
| `CHIP_EXPUESTO` | El Consejo Jedi sabe que el chip de los clones es peligroso | D208 | D218, D244, D270 |
| `CIVILES_MUERTOS` | Murieron civiles twi'lek en Ryloth | D046 | D048 |
| `CLOVIS_RESENTIDO` | Clovis le guarda rencor a Anakin | D069, D070 | D210 |
| `CONSEJO_SOSPECHA_CLONES` | El Consejo sospecha que los clones pueden volverse contra los Jedi | D218, D274 | D284, D298 |
| `CONSEJO_VIGILA` | El Consejo desconfía de Anakin y lo vigila | D065, D224 | D146 |
| `CRISTAL_REPUBLICA` | La República se quedó con el gran cristal kyber de Utapau | D235 | FINAL 1, FINAL 2, FINAL 3 |
| `DOOKU_DUDA` | Dooku duda de Sidious y buscó contacto con la Orden | D183 | D231, D251, D252 |
| `DOOKU_MUERTO_TEMPRANO` | Quinlan Vos mató a Dooku antes de *La venganza de los Sith* | D231 | D233, D251 |
| `DOOKU_PRISIONERO` | Dooku está preso de la República | D231, D252 | D233, D251, D262 |
| `ECHO_SALVADO` | Rex salvó a Echo en la Ciudadela | D122 | D241 |
| `FIVES_EN_KAMINO` | Fives se quedó como instructor en Kamino | D092 | D201 |
| `FIVES_SIN_CHIP` | Fives se quitó el chip | D202 | D281 |
| `FIVES_VIVE` | Fives sobrevivió al almacén | D207 | D208, D244, D270, D281 |
| `HEVY_VIVE` | Hevy sobrevivió en Rishi | D040 | D090 |
| `HONDO_DEUDA` | Hondo le debe un favor a la República | D087 | D169 |
| `INICIADOS_A_SALVO` | Los iniciados del Templo escaparon por los túneles | D299 | FINAL 4, FINAL 5 |
| `INVESTIGACION_SECRETA` | Obi-Wan le ocultó al Canciller lo de Tyranus | D217 | D218 |
| `JEDI_PREPARADOS` | Algunos Jedi esperaban la traición de los clones | D284 | FINAL 1, FINAL 5 |
| `KRELL_PRESO` | Krell está preso y se le puede interrogar | D134 | D135, D216 |
| `LEY_APROBADA` | Se aprobó la ley bancaria del Canciller | D100 | D215 |
| `MACE_RESPETA` | Mace Windu respeta a Anakin | D086, D088 | D261, D274 |
| `MAUL_MENSAJE` | Maul mandó a los Jedi un mensaje anónimo sobre Sidious | D181 | D216 |
| `MORTIS_RECUERDA` | Anakin conserva el recuerdo de la visión de Mortis | D116 | D117, D225, D257, D265, D278, D295 |
| `MUESTRA_GUSANOS` | Obi-Wan guardó una muestra de los gusanos de Geonosis | D075 | D077 |
| `OBI_CONFIESA_SATINE` | Obi-Wan le confesó a Anakin lo que sintió por Satine | D081 | D084 |
| `OBI_SABE_MATRIMONIO` | Obi-Wan sabe del matrimonio | D084, D155, D178, D258, D265 | D259, D289 |
| `OBI_SABE_VADER` | Obi-Wan sabe lo que Anakin vio en Mortis | D117 | D289 |
| `OBI_SATINE` | Obi-Wan admitió que sigue queriendo a Satine o la escondió | D080, D083 | D084 |
| `ORDEN66_DETENIDA` | La Orden 66 se cortó o nunca se dio | D298, D305 | D300, D301, D304, FINAL 4 |
| `PADME_ADVERTIDA` | Ahsoka le advirtió a Padmé lo que dijo Maul | D269 | D290 |
| `PADME_A_SALVO` | Anakin no estranguló a Padmé en Mustafar | D292 | D294, D295, FINAL 1 |
| `PADME_DUDA_RUTA` | Padmé sospecha de la ruta que la llevó a la Malevolencia | D029 | D032 |
| `PADME_HERIDA` | Padmé salió herida (Ziro o Aurra Sing) | D020, D095 | D023, D097 |
| `PADME_SABE_VISIONES` | Padmé sabe de las pesadillas de Anakin | D256 | D258, D292 |
| `PLO_MUERTO` | Plo Koon murió por el ataque de la Malevolencia | D025 | D087, D216 |
| `QUINLAN_LUZ` | Quinlan Vos rechazó el lado oscuro | D229 | D231 |
| `R2_PERDIDO` | R2-D2 se perdió para siempre | D033 | D037, D085 |
| `REX_ALERTA` | Anakin le advirtió a Rex sobre Krell | D127 | D131 |
| `REX_DESOBEDECE` | Rex desobedeció a Krell | D128 | D131 |
| `REX_LIBRE` | Rex resistió la Orden 66 | D281, D300 | D283, D299, FINAL 1, FINAL 4, FINAL 5 |
| `REX_SIN_CHIP` | Rex se quitó el chip antes de la Orden 66 | D270 | D281, D300 |
| `ROTTA_GRAVE` | Rotta llega muy enfermo con Jabba | D009 | D022 |
| `SABLE_RECUPERADO` | Anakin recuperó su sable durante la crisis de rehenes | D054 | D056 |
| `SATINE_VIVE` | Satine sobrevivió a Maul | D176 | D249 |
| `SAW_LIDER` | Saw dirige a los rebeldes de Onderon | D166 | D168 |
| `SIDIOUS_ARRESTADO` | Sidious está arrestado | D277 | D298, D302 |
| `SIDIOUS_MUERTO` | Sidious está muerto | D277, D297, D305 | D302 |
| `SIDIOUS_VISTO` | Anakin oyó la voz de Sidious en Mustafar | D063 | D263 |
| `SOSPECHA_PALPATINE` | Anakin sospecha del Canciller | D262, D263 | D274 |
| `TAMBOR_EJECUTADO` | Cham Syndulla ejecutó a Wat Tambor | D049 | D242 |
| `TARKIN_ALIADO` | Tarkin y Anakin se respetan | D119, D120 | D189 |
| `TEMPLO_SALVADO` | El 501.° defendió el Templo | D299 | D304, FINAL 4 |
| `VENTRESS_INFORMANTE` | Ventress le contó a Obi-Wan que Dooku tiene un maestro | D102 | D158, D216 |
| `YODA_SABE_MATRIMONIO` | Yoda sabe del matrimonio | D257 | D303 |
| `YODA_SABE_VADER` | Yoda sabe lo que Anakin vio en Mortis | D225 | D257 |
| `YODA_VIO_ANAKIN` | Yoda preguntó por el futuro de Anakin | D222 | D225 |
| `ZIRO_ESCAPA` | Ziro borró las pruebas y sigue libre | D021 | D022, D052 |

# APÉNDICE B — Fuentes canónicas

Todo lo marcado con ★ sale de estas obras, que forman parte del canon oficial de Lucasfilm (no de *Legends*). La cronología se revisó contra las líneas de tiempo canónicas de Wookieepedia el 2026-11-09.

**Películas**
- *Star Wars: The Clone Wars* (2008) — Acto I
- *Star Wars: Episodio III – La venganza de los Sith* (2005) — Acto VI

**Series**
- *Star Wars: The Clone Wars*, temporadas 1 a 7 (2008–2020) — columna principal de todo el juego
- *The Clone Wars Legacy*: arco *Crystal Crisis on Utapau* (story reels, 2014) — D234–D236
- *Star Wars: The Bad Batch*, 1x01 *Aftermath* (2021) — D284

**Novelas**
- *Dark Disciple*, Christie Golden (2015) — D228–D233
- *Thrawn: Alliances*, Timothy Zahn (2018), capítulos ambientados en las Guerras Clon — D237–D240
- *Master of Evil*, Adam Christopher (2025) — epílogo del Final 1

**Cómics**
- *Darth Maul: Son of Dathomir* (2014) — D181–D183
- *Kanan: The Last Padawan* (2015) — D284

**Revisadas y no usadas** (obras de la época que no cambian la historia de Anakin): *Hyperspace Stories: Tides of Terror* (2025–2026), *Jar Jar* (2026), *Hyperspace Stories: Grievous* (2026), *Brotherhood* y *Queen's Hope* (2022, ocurren antes de Christophsis), *Catalyst* (2016, el proyecto de la Estrella de la Muerte; solo se menciona en las variantes con ⚑ CRISTAL_REPUBLICA).

**Licencias del guion.** Las escenas de rama son invención del juego. Algunas fichas canónicas agregan detalles que no aparecen en pantalla para que la decisión tenga sentido: la pregunta de Anakin a Obi-Wan sobre Satine (D081), el comentario de Tech sobre los chips (D244), el mensaje privado del Canciller (D008) y la ruta del yate de Padmé (D029), entre otros. El canon se mantiene porque la opción ★ siempre lleva al resultado oficial.
