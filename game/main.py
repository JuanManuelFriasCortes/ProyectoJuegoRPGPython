import pygame
import json
import logica
import os
import random

ANCHO=1280
ALTO=720
FPS=60
ARCHIVO_PARTIDA = "partida_guardada.json"     #AQUI SE GUARDA LA PARTIDA (EN LA RAIZ DEL PROYECTO)


#FUNCION QUE RECIBE TEXTO Y LO PARTE EN RENGLONES PARA QUE QUEPA EN LOS CUADROS DE TEXTO IN GAME
def partir_en_renglones(texto, fuente, ancho_maximo):
    renglones = []
    renglon = ""
    for palabra in texto.split():   #PARTE EL TEXTO Y LO PONE CON ESPACIOS Y LEEMOS CADA PALABRA
        if renglon == "":
            prueba = palabra
        else:
            prueba = renglon + " " + palabra
        if fuente.size(prueba)[0] <= ancho_maximo:  #SE DECIDE CUANTO MIDE LAS PALABRAS DESPLEGADAS EN EL CUADRO Y SI MENOS AL ANCHO CABE
            renglon = prueba
        else:   #SI NO CABE SE GUARDA EN LA LISTA
            renglones.append(renglon)
            renglon = palabra
    if renglon != "":
        renglones.append(renglon)
    return renglones


#FUNCION QUE CARGA LA FICHA DEL JSON Y DEVUELVE LOS DATOS PARA USARLOS EN EL JUEGO
def cargar_ficha(clave):
    ficha = historia["fichas"][clave]   #BUSCA LA FICHA EN EL JSON (POR EJEMPLO "D001")
    pygame.display.set_caption(clave + " · " + ficha["titulo"])  #PONE EL NUMERO Y TITULO DE LA FICHA EN LA BARRA DE LA VENTANA

    #CARGA LA HOJA CON LOS 144 CUADROS DEL FONDO ANIMADO Y LOS RECORTA EN UNA LISTA, ESTO AYUDA A AHORRAR RAM
    hoja = pygame.image.load("assets/escenarios/animados_60/" + ficha["fondo"] + ".png").convert()
    cuadros = []
    for t in range(144):
        x = (t % 12) * 320     #COLUMNA DEL CUADRO EN LA HOJA
        y = (t // 12) * 180    #FILA DEL CUADRO EN LA HOJA
        cuadros.append(hoja.subsurface((x, y, 320, 180)))

    #CARGA LOS PERSONAJES DE LA FICHA (NORMAL O HOLOGRAMA), LOS ESCALA Y LOS GIRA SI ESTAN EN EL SUELO
    personajes = []
    for p in ficha["personajes"]:
        carpeta = "assets/personajes/sprites_1x/"
        if p["holograma"]:
            carpeta = "assets/personajes/sprites_holograma/"
        imagen = pygame.image.load(carpeta + p["clave"] + ".png").convert_alpha()
        imagen = pygame.transform.scale(imagen, (40 * p["escala"], 56 * p["escala"]))
        if p["girado"]:
            imagen = pygame.transform.rotate(imagen, 90)    #PARA CUANDO ESTAN EN EL SUELO
        #LA VERSION APAGADA, PARA CUANDO HABLA OTRO (LOS HOLOGRAMAS SE QUEDAN IGUAL)
        apagada = imagen
        if not p["holograma"]:
            apagada = pygame.image.load("assets/personajes/sprites_apagados/" + p["clave"] + ".png").convert_alpha()
            apagada = pygame.transform.scale(apagada, (40 * p["escala"], 56 * p["escala"]))
            if p["girado"]:
                apagada = pygame.transform.rotate(apagada, 90)
        #SE GUARDA CADA PERSONAJE CON SUS DOS IMAGENES Y SU POSICION EN PANTALLA
        personajes.append({"clave": p["clave"], "imagen": imagen, "apagada": apagada, "posicion": (p["izquierda"], p["arriba"])})

    #SE CALCULAN LOS RENGLONES DEL TEXTO PARA QUE QUEPA EN EL CUADRO DE TEXTO
    texto = ficha["texto"]
    for nota in ficha["notas"]:
        if logica.cumple(nota["requiere"], estado):
            texto = texto + " " + nota["texto"]
    
    #QUIENES ESTAN EN LA FICHA
    todos = []
    for p in ficha["personajes"]:
        todos.append(p["clave"])

    #ARMA LA LISTA DE LINEAS: EL DIALOGO SI LA FICHA TIENE, SI NO, EL TEXTO DE LA FICHA COMO NARRACION.
    #CADA LINEA GUARDA QUIEN HABLA ("clave") Y QUIENES ESTAN EN ESCENA EN ESE MOMENTO ("presentes")
    lineas = []
    if clave in dialogos:
        presentes = list(todos)     #COPIA DE LA LISTA, PARA NO MODIFICAR "todos"
        for linea in dialogos[clave]["antes"]:      #QUIEN TIENE UN "entra" NO ESTA AL PRINCIPIO
            if linea["tipo"] == "entra" and linea["clave"] in presentes:
                presentes.remove(linea["clave"])
        for linea in dialogos[clave]["antes"]:
            if linea["tipo"] == "entra":        #APARECE A MEDIA ESCENA
                presentes.append(linea["clave"])
            elif linea["tipo"] == "sale":       #SE VA A MEDIA ESCENA
                if linea["clave"] in presentes:
                    presentes.remove(linea["clave"])
            else:                               #"dice" O "narra": UNA LINEA QUE SE MUESTRA
                lineas.append({"quien": linea["quien"], "clave": linea["clave"], "presentes": list(presentes),
                               "renglones": partir_en_renglones(linea["texto"], fuente, caja.width - 48), "largo": len(linea["texto"])})   #"largo": CUANTAS LETRAS TIENE LA LINEA
    else:
        lineas.append({"quien": "", "clave": None, "presentes": todos,
                       "renglones": partir_en_renglones(texto, fuente, caja.width - 48), "largo": len(texto)})

    #SE GUARDAN LAS OPCIONES QUE EL JUGADOR PUEDE VER (POR AHORA SOLO LAS QUE NO TIENEN REQUISITO)
    opciones = logica.opciones_visibles(ficha, estado)

    #DEVUELVE TODOO LO QUE SE NECESITA PARA DIBUJAR LA FICHA
    return ficha, cuadros, personajes, lineas, opciones


#FUNCION QUE ARMA LAS LINEAS QUE SE MUESTRAN DESPUES DE ELEGIR: LA REACCION DEL DIALOGO Y EL RESULTADO DE LA OPCION
def lineas_de_reaccion(clave, opcion):
    todos = []      #EN LAS REACCIONES ESTAN TODOS LOS DE LA FICHA
    for p in historia["fichas"][clave]["personajes"]:
        todos.append(p["clave"])
    lineas = []
    if clave in dialogos and opcion["letra"] in dialogos[clave]["reacciones"]:
        for linea in dialogos[clave]["reacciones"][opcion["letra"]]:
            if linea["tipo"] == "dice" or linea["tipo"] == "narra":
                lineas.append({"quien": linea["quien"], "clave": linea["clave"], "presentes": todos,
                               "renglones": partir_en_renglones(linea["texto"], fuente, caja.width - 48), "largo": len(linea["texto"])})
    if opcion["resultado"] != "" and logica.cumple(opcion["resultado_requiere"], estado):   #LA CONSECUENCIA ("99 muere.") COMO NARRACION
        lineas.append({"quien": "", "clave": None, "presentes": todos,
                       "renglones": partir_en_renglones(opcion["resultado"], fuente, caja.width - 48), "largo": len(opcion["resultado"])})
    return lineas

#FUNCION QUE CAMBIA LA MUSICA SOLO SI ES OTRA CANCION. DEVUELVE LA QUE QUEDO SONANDO
def poner_musica(nombre, actual):
    if nombre == actual:        #ES LA MISMA: QUE SIGA SONANDO SIN CORTARSE
        return actual
    ruta = "assets/musica/pistas/" + nombre + ".ogg"
    if not os.path.exists(ruta):    #SI NO ESTA EL ARCHIVO, SE QUEDA SIN MUSICA PERO EL JUEGO SIGUE
        pygame.mixer.music.stop()
        return nombre
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, fade_ms=1500)   #-1 = EN BUCLE; fade_ms = ENTRA SUAVE EN 1.5 SEGUNDOS
    return nombre


#FUNCION QUE ARMA LAS OPCIONES DEL MENU DE TITULO: "Continuar" SOLO APARECE SI HAY PARTIDA GUARDADA
def opciones_del_menu():
    if os.path.exists(ARCHIVO_PARTIDA):
        return ["Continuar", "Nueva partida", "Salir"]
    return ["Nueva partida", "Salir"]


#BLOQUE QUE INICIA LA INTERFAZ
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.SCALED)    #SCALED: EN PANTALLA COMPLETA AGRANDA TODO SIN MOVER LAS POSICIONES
pygame.display.set_caption("Star Wars: La Guerra de los Clones")
reloj = pygame.time.Clock()


#CARGA TODOS LOS DATOS DE LA HISTORIA DESDE EL ARCHIVO JSON
with open("assets/historia/historia.json", encoding="utf-8") as archivo:    #ABRE EL ARCHIVO Y LO CIERRA CUANDO LO DEJE DE USAR
    historia = json.load(archivo)


#CARGA LOS DIALOGOS ESCRITOS (SOLO ALGUNAS FICHAS LOS TIENEN)
with open("assets/historia/dialogos.json", encoding="utf-8") as archivo:
    dialogos = json.load(archivo)

#CARGA LOS SONIDOS: LAS VOCES DE CADA PERSONAJE AL ESCRIBIR Y LOS DEL CURSOR
with open("assets/sonidos/sonidos.json", encoding="utf-8") as archivo:
    sonidos = json.load(archivo)

voces = {}      #CADA VOZ CON SUS 6 VARIANTES YA CARGADAS: {"anakin": [sonido1, sonido2, ...], ...}
for nombre_voz in sonidos["voces"]:
    voces[nombre_voz] = []
    for archivo_voz in sonidos["voces"][nombre_voz]:
        voces[nombre_voz].append(pygame.mixer.Sound("assets/sonidos/" + archivo_voz))
sonido_cursor = pygame.mixer.Sound("assets/sonidos/" + sonidos["ui"]["cursor"])
sonido_confirmar = pygame.mixer.Sound("assets/sonidos/" + sonidos["ui"]["confirmar"])

estado = logica.nuevo_estado(historia)   #CREA LA PARTIDA NUEVA: MEDIDORES, BANDERAS Y ELECCIONES DEL JUGADOR


#PONEMOS LA FUENTE PARA LOS TEXTOS Y EL RECUADRO DONDE VAN
fuente = pygame.font.SysFont("arial", 30)
caja = pygame.Rect(20, 472, 1240, 232)


#NOMBRE DE LA FICHA Y EL TITULO DE LA HISTORIA EN LA PESTAÑA DE PANTALLA
fuente_nombre = pygame.font.SysFont("arial", 22, bold=True)
fuente_titulo = pygame.font.SysFont("arial", 80, bold=True)     #PARA EL TITULO DEL MENU

#CAPA NEGRA SEMITRANSPARENTE PARA OSCURECER EL FONDO DEL MENU
sombra = pygame.Surface((ANCHO, ALTO))
sombra.fill((0, 0, 0))
sombra.set_alpha(150)   #0 = INVISIBLE, 255 = NEGRO TOTAL


ficha_actual = estado["ficha"]   #LA FICHA CON LA QUE EMPIEZA EL JUEGO
ficha, cuadros, personajes, lineas, opciones = cargar_ficha(ficha_actual)
musica_actual = poner_musica("menu", "")   #EN EL MENU SUENA EL TEMA PRINCIPAL
cuadro_actual = 0
modo = "titulo"     #EL JUEGO EMPIEZA EN EL MENU DE TITULO
opciones_menu = opciones_del_menu()
seleccion_menu = 0
ver_medidores = False   #CON F1 SE MUESTRAN LOS MEDIDORES (PARA PROBAR)
seleccion = 0
linea_actual = 0    #LA LINEA DEL DIALOGO QUE SE ESTA MOSTRANDO
letras = 0          #CUANTAS LETRAS DE LA LINEA YA SE VEN (MAQUINA DE ESCRIBIR)


#BLOQUE PARA CAPTURAR EL TECLADO, SE ACTUALIZA LA PANTALLA
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            if modo == "titulo":    #EN EL MENU, ESC CIERRA EL JUEGO
                jugando = False
            else:                   #JUGANDO, ESC REGRESA AL MENU (LA PARTIDA QUEDA GUARDADA EN LA ULTIMA FICHA)
                modo = "titulo"
                opciones_menu = opciones_del_menu()
                seleccion_menu = 0
                musica_actual = poner_musica("menu", musica_actual)
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()      #PANTALLA COMPLETA / VENTANA
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
            ver_medidores = not ver_medidores       #MUESTRA U OCULTA LOS MEDIDORES
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            pasar = False   #SE VUELVE True CUANDO YA HAY QUE IR A LA SIGUIENTE FICHA
            if modo == "texto" or modo == "reaccion":
                if letras < lineas[linea_actual]["largo"]:   #SI TODAVIA SE ESTA ESCRIBIENDO, LA COMPLETA DE GOLPE
                    letras = lineas[linea_actual]["largo"]
                elif linea_actual < len(lineas) - 1:          #SI YA ESTABA COMPLETA Y QUEDAN LINEAS, PASA A LA SIGUIENTE
                    linea_actual += 1
                    letras = 0
                elif modo == "texto":                         #TERMINO EL TEXTO: MUESTRA LAS OPCIONES
                    modo = "opciones"
                else:                                         #TERMINO LA REACCION: TOCA LA SIGUIENTE FICHA
                    pasar = True
            elif modo == "final":   #EN LA PANTALLA DEL FINAL, ENTER REGRESA AL MENU
                modo = "titulo"
                opciones_menu = opciones_del_menu()
                seleccion_menu = 0
                musica_actual = poner_musica("menu", musica_actual)
            elif modo == "titulo":
                sonido_confirmar.play()
                elegido = opciones_menu[seleccion_menu]
                if elegido == "Salir":
                    jugando = False
                elif elegido == "Nueva partida":
                    estado = logica.nuevo_estado(historia)     #PARTIDA DESDE CERO
                    pasar = True                               #CARGA estado["ficha"] CON EL MISMO CODIGO DE SIEMPRE
                else:   #"Continuar"
                    estado = logica.cargar_partida(ARCHIVO_PARTIDA)
                    pasar = True
            elif modo == "opciones":
                sonido_confirmar.play()     #LAS DOS NOTAS AL ELEGIR
                elegida = opciones[seleccion]
                logica.elegir(elegida, ficha_actual, estado)
                lineas = lineas_de_reaccion(ficha_actual, elegida)
                if len(lineas) > 0:     #SI HAY REACCION (O RESULTADO), SE MUESTRA ANTES DE PASAR DE FICHA
                    modo = "reaccion"
                    linea_actual = 0
                    letras = 0
                else:                   #SI NO, PASA DIRECTO
                    pasar = True

            if pasar:   #CARGA LA SIGUIENTE FICHA O LA PANTALLA DEL FINAL
                ficha_actual = estado["ficha"]
                if ficha_actual in historia["fichas"]:
                    ficha, cuadros, personajes, lineas, opciones = cargar_ficha(ficha_actual)
                    musica_actual = poner_musica(ficha["musica"], musica_actual)   #CAMBIA LA CANCION SI LA FICHA TIENE OTRA
                    modo = "texto"
                    seleccion = 0
                    linea_actual = 0    #LA FICHA NUEVA EMPIEZA EN SU PRIMERA LINEA
                    letras = 0
                    logica.guardar_partida(estado, ARCHIVO_PARTIDA)     #GUARDA LA PARTIDA AL LLEGAR A CADA FICHA
                else:   #SI NO ES UNA FICHA, ES UN FINAL ("FINAL 1", "FP3"...)
                    if os.path.exists(ARCHIVO_PARTIDA):    #LA PARTIDA TERMINO: SE BORRA EL GUARDADO
                        os.remove(ARCHIVO_PARTIDA)
                    #BUSCA EL FINAL EN EL JSON
                    final = historia["finales"][ficha_actual]
                    musica_actual = poner_musica(final["musica"], musica_actual)   #LA CANCION DEL FINAL
                    #ARMA EL TEXTO DEL FINAL: EL TEXTO BASE MAS LAS VARIANTES QUE SE CUMPLAN SEGUN LA PARTIDA
                    texto_final = final["texto"]
                    for variante in final["variantes"]:
                        if logica.cumple(variante["requiere"], estado):
                            texto_final = texto_final + " " + variante["texto"]
                    #PARTE EL TEXTO DEL FINAL EN RENGLONES (MAS ANCHOS, OCUPA CASI TODA LA PANTALLA)
                    renglones_final = partir_en_renglones(texto_final, fuente, 1100)
                    modo = "final"  #CAMBIA A LA PANTALLA DEL FINAL

        if evento.type == pygame.KEYDOWN and modo == "titulo":     #FLECHAS EN EL MENU
            if evento.key == pygame.K_DOWN:
                seleccion_menu = (seleccion_menu + 1) % len(opciones_menu)
                sonido_cursor.play()
            if evento.key == pygame.K_UP:
                seleccion_menu = (seleccion_menu - 1) % len(opciones_menu)
                sonido_cursor.play()
        if evento.type == pygame.KEYDOWN and modo == "opciones":
            if evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(opciones)
                sonido_cursor.play()     #CLIC AL MOVER LA FLECHA
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(opciones)
                sonido_cursor.play()

    fondo = pygame.transform.scale(cuadros[cuadro_actual], (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))    #PONE EL FONDO DE PANTALLA
    #IMPRIME LOS PERSONAJES: SOLO LOS QUE ESTAN EN ESCENA, Y APAGADOS SI HABLA OTRO
    for p in personajes:
        if modo == "texto" or modo == "reaccion":
            linea = lineas[linea_actual]
            if p["clave"] not in linea["presentes"]:    #TODAVIA NO ENTRA O YA SE FUE
                continue
            if linea["clave"] is not None and linea["clave"] != p["clave"]:    #HABLA OTRO: SE DIBUJA APAGADO
                pantalla.blit(p["apagada"], p["posicion"])
                continue
        pantalla.blit(p["imagen"], p["posicion"])

    #EN EL TEXTO LA PESTAÑA DICE QUIEN HABLA; EN LAS OPCIONES, QUIEN JUEGA. EL NARRADOR NO LLEVA PESTAÑA
    if modo == "texto" or modo == "reaccion":
        nombre_pestana = lineas[linea_actual]["quien"]
    else:
        nombre_pestana = ficha["juega"]
    if nombre_pestana != "":
        nombre = fuente_nombre.render(nombre_pestana.upper(), False, (255, 214, 102))
        pestana = pygame.Rect(caja.x + 12, caja.y - 34, nombre.get_width() + 32, 36)     #IMPRIME EL NOMBRE EN LA PESTAÑA DE TEXTO (ANAKIN, AHSOKA, ETC...)
        pygame.draw.rect(pantalla, (10, 14, 34), pestana)
        pygame.draw.rect(pantalla, (122, 200, 255), pestana, 3)
        pantalla.blit(nombre, (pestana.x + 16, pestana.y + 6))
    pygame.draw.rect(pantalla, (10, 14, 34), caja)  #IMPRIME EL RECUADRO DE TEXTO
    pygame.draw.rect(pantalla, (122, 200, 255), caja, 3)

    if modo == "texto" or modo == "reaccion": #PARA CUANDO SOLO SE IMPRIME TEXTO EN LOS RECUADROS
        y = caja.y + 24
        restantes = letras      #LETRAS QUE QUEDAN POR MOSTRAR, SE VAN REPARTIENDO ENTRE LOS RENGLONES
        for renglon in lineas[linea_actual]["renglones"]:    #LOS RENGLONES DE LA LINEA ACTUAL
            if restantes > 0:
                imagen_texto = fuente.render(renglon[:restantes], False, (236, 240, 250))   #SOLO LAS LETRAS QUE YA TOCA VER
                pantalla.blit(imagen_texto, (caja.x + 24, y))
            restantes -= len(renglon)
            y += 36
    else:   #PARA CUANDO SE IMPRIMEN OPCIONES DE TEXTO EN LOS RECUADROS
        pregunta = fuente.render("¿Qué haces?", False, (196, 206, 232))
        pantalla.blit(pregunta, (caja.x + 24, caja.y + 20))
        y = caja.y + 64
        for i, opcion in enumerate(opciones):
            color = (236, 240, 250)
            marca = "   "
            if i == seleccion:  #AYUDA A IDENTIFICAR CUAL OPCION ESTA SELECCIONADA, SE PINTA DE OTRO COLOR Y SE LE PONE UNA MARCA
                color = (255, 214, 102)
                marca = "► "
            texto_opcion = fuente.render(marca + opcion["letra"] + ") " + opcion["texto"], False, color)
            pantalla.blit(texto_opcion, (caja.x + 24, y))
            y += 36
    cuadro_actual = (cuadro_actual + 1) % 144   #AVANZA LOS 144 CUADROS DE LA ANIMACION DE LAS IMAGENES
    if modo == "texto" or modo == "reaccion":
        linea = lineas[linea_actual]
        if letras < linea["largo"]:     #SOLO MIENTRAS SE ESTA ESCRIBIENDO
            letras += 1     #CADA VUELTA SE VE UNA LETRA MAS (60 POR SEGUNDO)
            if letras % sonidos["cada_letras"] == 1:    #CADA 4 LETRAS SUENA LA VOZ DE QUIEN HABLA
                if linea["clave"] is None:
                    voz = sonidos["narrador"]
                else:
                    voz = sonidos["personajes"].get(linea["clave"], sonidos["por_defecto"])
                random.choice(voces[voz]).play()     #UNA DE LAS 6 VARIANTES, AL AZAR

    #PANTALLA DEL FINAL: SE DIBUJA ENCIMA DE TODOo LO DEMAS
    if modo == "final":
        pantalla.fill((4, 6, 14))   #PINTA TODA LA PANTALLA CASI NEGRA Y TAPA EL FONDO Y LOS PERSONAJES

        #TITULO DEL FINAL EN AMARILLO (POR EJEMPLO "FINAL 1 · Lord Vader")
        titulo_final = fuente_nombre.render(ficha_actual + " · " + final["nombre"], False, (255, 214, 102))
        pantalla.blit(titulo_final, (90, 120))

        #TEXTO DEL FINAL RENGLON POR RENGLON
        y = 180
        for renglon in renglones_final:
            imagen_texto = fuente.render(renglon, False, (236, 240, 250))
            pantalla.blit(imagen_texto, (90, y))
            y += 40

        #AVISO ABAJO PARA QUE EL JUGADOR SEPA COMO SALIR
        aviso = fuente_nombre.render("Enter para salir", False, (150, 170, 210))
        pantalla.blit(aviso, (90, 640))

    #MENU DE TITULO: EL FONDO ANIMADO OSCURECIDO, EL TITULO Y LAS OPCIONES AL CENTRO
    if modo == "titulo":
        pantalla.blit(fondo, (0, 0))    #TAPA LO QUE SE DIBUJO ANTES (PERSONAJES Y CUADRO)
        pantalla.blit(sombra, (0, 0))
        titulo = fuente_titulo.render("STAR WARS", False, (255, 214, 102))
        pantalla.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 140))    #CENTRADO: (ANCHO DE PANTALLA - ANCHO DEL TEXTO) / 2
        subtitulo = fuente.render("La Guerra de los Clones", False, (236, 240, 250))
        pantalla.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 240))
        y = 360
        for i, texto_menu in enumerate(opciones_menu):
            color = (236, 240, 250)
            marca = ""
            if i == seleccion_menu:
                color = (255, 214, 102)
                marca = "► "
            imagen_menu = fuente.render(marca + texto_menu, False, color)
            pantalla.blit(imagen_menu, ((ANCHO - imagen_menu.get_width()) // 2, y))
            y += 50
        ayuda = fuente_nombre.render("↑↓ elegir · Enter aceptar · F11 pantalla completa · Esc salir", False, (150, 170, 210))
        pantalla.blit(ayuda, ((ANCHO - ayuda.get_width()) // 2, 640))

    #MEDIDORES EN PANTALLA (F1), PARA PROBAR EL JUEGO
    if ver_medidores and modo != "titulo":
        texto_medidores = ""
        for clave_medidor in estado["medidores"]:
            texto_medidores = texto_medidores + clave_medidor + " " + str(estado["medidores"][clave_medidor]) + "   "
        texto_medidores = texto_medidores + "Banderas: " + str(len(estado["banderas"]))
        imagen_medidores = fuente_nombre.render(texto_medidores, False, (255, 214, 102))
        pygame.draw.rect(pantalla, (10, 14, 34), (10, 10, imagen_medidores.get_width() + 20, 36))
        pantalla.blit(imagen_medidores, (20, 16))

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()