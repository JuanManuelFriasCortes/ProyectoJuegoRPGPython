# Diálogos

Los diálogos de cada ficha, aparte de `Historia.md`. Una ficha sin diálogo se juega con el texto de su ficha como narración. `assets/historia/preparar_historia.py` convierte este archivo en `dialogos.json`.

- Cada ficha empieza con `## D### · Título`.
- Cada línea es `Nombre: lo que dice`. El nombre basta con que sea parte del nombre del personaje (`Rex`, `Obi-Wan`, `Palpatine`). Si el personaje está en la escena, se ilumina y los demás se oscurecen mientras habla.
- `Narra:` es el narrador. Va en cursiva y nadie se ilumina.
- `[entra Nombre]` y `[sale Nombre]` hacen que un personaje aparezca o se vaya, con un fundido, junto con la línea que sigue. Quien tiene un `[entra]` no está en pantalla al empezar la escena.
- Lo de antes del primer `###` se ve antes de la decisión. Debajo de `### A`, `### B`… va la reacción a cada opción.
- Las líneas que empiezan con `>` son notas para quien escribe; el juego no las muestra.

## D002 · Una padawan inesperada

Narra: Christophsis. Los droides se repliegan detrás de su escudo y, por primera vez en horas, los disparos se detienen.
Rex: ¡General! Una lanzadera de la República viene en camino. Aterriza sola.
Obi-Wan: Deben ser los refuerzos que pedimos. Aunque esperaba algo… más grande.
[entra Ahsoka]
Narra: De la lanzadera baja una joven togruta, con la trenza de padawan colgándole del hombro.
Ahsoka: Soy Ahsoka Tano. El Maestro Yoda me envía con un mensaje para el Maestro Skywalker.
Anakin: ¿Para mí? Te equivocaste de Jedi. La padawan nueva es de Obi-Wan.
Ahsoka: No. El Maestro Yoda fue muy claro: voy a ser tu padawan.
Obi-Wan: Parece que el Consejo tiene sentido del humor, Anakin.
Narra: Nunca pediste una padawan. Y menos en medio de una guerra.

### A
Anakin: Está bien, pequeña. Pero aquí nadie te va a llevar de la mano. Si no aguantas el ritmo, te regreso al Templo.
Ahsoka: Tranquilo, Skyguy. Aguanto más de lo que crees.
Anakin: ¿"Skyguy"? …No me llames así.
Rex: Creo que se van a llevar muy bien, señor.

### B
Anakin: Esto tiene que ser un error. Rex, comunícame con el Maestro Yoda.
Ahsoka: ¿Un error? Ni siquiera me has visto pelear.
Obi-Wan: Paciencia, Anakin. Escucha primero lo que el Maestro tiene que decir.

### C
Anakin: Bienvenida a Christophsis, Ahsoka. No es el mejor lugar para empezar, pero aquí estamos juntos.
Ahsoka: ¡Gracias, Maestro! No te voy a decepcionar.
Obi-Wan: Vaya. Eso sí que no lo esperaba de ti.

## D022 · El trono de Jabba

Narra: Palacio de Jabba, Tatooine. Entregas al pequeño Rotta sano y salvo, pero el silencio del salón no suena a gratitud.
Jabba: ¡Jedi! Mi hijo está débil y enfermo… ¡Ustedes se lo llevaron para chantajearme!
Anakin: Nosotros lo rescatamos, Jabba. Fueron los separatistas quienes se lo llevaron.
Ahsoka: ¡Lo cargamos por medio desierto! Y se la pasó babeándome la espalda.
Rotta: ¡Ba-ba! ¡Ba-baaa!
Jabba: ¡Mentiras de Jedi! ¡Guardias, ejecútenlos!
Narra: Los guardias gamorreanos levantan sus hachas. En Coruscant, Padmé busca la prueba que los salvaría… si llega a tiempo.
> la opción C solo aparece si Ziro escapó (⚑ ZIRO_ESCAPA); en este ejemplo no

### A
Anakin: Ahsoka, guarda el sable. Todavía no.
Ahsoka: ¿Todavía no? ¡Nos van a hacer pedacitos!
Anakin: Confía en mí. Solo necesitamos un poco más de tiempo.

### B
Narra: El zumbido de tu sable llena el salón. Los guardias dan un paso atrás.
Anakin: Un paso más y tu palacio se queda sin dueño, Jabba.
Jabba: ¡Jo, jo, jo! El Jedi tiene agallas… Veamos cuánto le duran.
Ahsoka: Maestro… creo que eso no ayudó.

## D252 · "Mátalo"

Narra: La Mano Invisible, sobre Coruscant. Obi-Wan yace inconsciente y tu sable apunta al cuello del Conde Dooku.
Narra: El duelo terminó. Dooku está vencido, a tu merced.
Palpatine: ¡Bien hecho, Anakin! ¡Muy bien hecho!
Narra: Dooku busca los ojos del Canciller. Por primera vez, parece sorprendido.
Palpatine: Ahora… mátalo.
Anakin: No debería. Ya está vencido. Es un prisionero.
Palpatine: Es demasiado peligroso para dejarlo vivir. Mátalo, Anakin. Mátalo ahora.

### A
Narra: Un solo movimiento. El Conde cae sobre el piso del puente.
Anakin: No debí hacerlo. Ese no es el camino de los Jedi.
Palpatine: Era necesario, Anakin. Dooku nunca habría dejado de ser una amenaza.

### B
Anakin: No. Un Jedi no mata a un prisionero vencido. Va a responder ante el Senado.
Palpatine: …Como quieras, Anakin. Espero que no tengas que arrepentirte.
Dooku: Me perdonaste la vida, muchacho. No tienes idea de lo que acabas de hacer.
Narra: La mirada del Canciller se queda fija en el Conde un instante de más.

## D267 · Maul

Narra: Sundari, Mandalore. Entre el humo del asedio, la guardia de Bo-Katan rodea a su prisionero. Pero Maul no parece acorralado.
Maul: Ahsoka Tano. La aprendiz de Skywalker. Te estaba esperando.
Ahsoka: Se acabó, Maul. Ríndete y nadie más tiene que salir herido.
Maul: ¿Rendirme? Hice caer este planeta solo para traerte hasta aquí.
Rex: Comandante, no lo escuche. Está ganando tiempo.
Maul: Sidious está preparando a Skywalker para ser su nuevo aprendiz. Ayúdame a matarlo antes de que sea tarde.
Narra: Algo en su voz te hace dudar. Anakin, siempre tan cerca del Canciller…

### A
Ahsoka: No vine a hacer tratos contigo. ¡Rex, cúbreme!
Rex: ¡A la orden, comandante!
Maul: Entonces lo haremos a la manera difícil.

### B
Ahsoka: Digamos que te creo. ¿Qué pruebas tienes?
Maul: La verdad no se demuestra, niña. Se siente. Y tú ya la sientes.
Rex: Comandante… no me gusta esto.
