import json


#FUNCION QUE CREA EL ESTADO DE UNA PARTIDA NUEVA: TODOO LO QUE EL JUEGO RECUERDA DEL JUGADOR
def nuevo_estado(historia):
    estado = {
        "ficha": historia["inicio"],
        "medidores": dict(historia["medidores"]),   #SE COPIA LOS MEDIDORES DEL JSON PARA QUE EL JUEGO LOS USE Y LOS MODIFIQUE
        "banderas": [],
        "elecciones": [],
    }
    return estado


#FUNCION QUE REVISA UNA SOLA PIEZA DEL REQUISITO, POR EJEMPLO "OSC >= 35" O "MORTIS_RECUERDA"
def cumple_pieza(pieza, estado):
    partes = pieza.split()  #SEPARA LA PIEZA EN PARTES, POR EJEMPLO ["OSC", ">=", "35"]
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


#FUNCION QUE REVISA EL REQUISITO COMPLETO DE UNA OPCION
def cumple(requisito, estado):
    if requisito == "":
        return True
    for alternativa in requisito.split(" o "):  #PARA LAS OPCIONES QUE SOLO APARECEN SI UN REQUISITO SE CUMPLE POR EJEMPLO "PAD >= 25 o MORTIS_RECUERDA"
        todas = True
        for pieza in alternativa.split(" y "):  #SI ALGUNO DE LOS REQUIAITOS NO SE CUMPLE NO MUESTRA LA OPCION, POR EJEMPLO "PAD >= 25 y MORTIS_RECUERDA"
            if not cumple_pieza(pieza, estado):
                todas = False
        if todas:
            return True
    return False


#FUNCION QUE APLICA LOS EFECTOS DE UNA OPCION AL ESTADO DEL JUGADOR
def aplicar(efectos, estado):
    for efecto in efectos:  #UNA ACCION PUEDE TENER VARIOS EFECTOS, POR EJEMPLO "OSC -1", "PAL -1", "DOOKU_PRISIONERO"
        partes = efecto.split()
        if partes[0] == "quita":
            if partes[1] in estado["banderas"]:
                estado["banderas"].remove(partes[1])
        elif len(partes) == 2:
            estado["medidores"][partes[0]] += int(partes[1])
        else:
            if efecto not in estado["banderas"]:
                estado["banderas"].append(efecto)


#FUNCION QUE DEVUELVE SOLO LAS OPCIONES QUE EL JUGADOR PUEDE VER EN ESTA FICHA
def opciones_visibles(ficha, estado):
    visibles = []
    for opcion in ficha["opciones"]:
        if cumple(opcion["requiere"], estado):
            visibles.append(opcion)
    return visibles


#FUNCION QUE REGISTRA LA DECISION, APLICA SUS EFECTOS Y DICE A QUE FICHA SIGUE
def elegir(opcion, clave_ficha, estado):
    estado["elecciones"].append(clave_ficha + " " + opcion["letra"])
    aplicar(opcion["efectos"], estado)
    for extra in opcion["efectos_si"]:
        if cumple(extra["requiere"], estado):
            aplicar(extra["efectos"], estado)
    estado["ficha"] = opcion["siguiente"]



#FUNCION QUE GUARDA LA PARTIDA EN UN ARCHIVO (EL ESTADO ES UN DICCIONARIO, ASI QUE SE ESCRIBE TAL CUAL COMO JSON)
def guardar_partida(estado, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estado, archivo, ensure_ascii=False, indent=1)


#FUNCION QUE LEE LA PARTIDA GUARDADA Y LA DEVUELVE COMO DICCIONARIO
def cargar_partida(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)

#PARA CORRER EL PROGRAMA DE FORMA INDEPENDIENTE Y PROBAR EL ESTADO NUEVO
if __name__ == "__main__":
    import json
    with open("assets/historia/historia.json", encoding="utf-8") as archivo:
        historia = json.load(archivo)
    estado = nuevo_estado(historia)
    print(estado)

    #PRUEBAS DE cumple (DEBEN SALIR: True, False, True, False, True, False)
    print(cumple("", estado))
    print(cumple("OSC >= 35", estado))
    estado["medidores"]["OSC"] = 40
    print(cumple("OSC >= 35", estado))
    print(cumple("PAD >= 25 o MORTIS_RECUERDA", estado))
    estado["banderas"].append("MORTIS_RECUERDA")
    print(cumple("PAD >= 25 o MORTIS_RECUERDA", estado))
    print(cumple("AHS >= 35 y sin AHSOKA_DUDA_ORDEN", estado))

    #PRUEBAS DE aplicar (DEBEN SALIR: 45 3 ['MORTIS_RECUERDA', 'PLO_MUERTO'] Y DESPUES ['MORTIS_RECUERDA'])
    aplicar(["OSC +5", "PAD -2", "PLO_MUERTO"], estado)
    print(estado["medidores"]["OSC"], estado["medidores"]["PAD"], estado["banderas"])
    aplicar(["quita PLO_MUERTO"], estado)
    print(estado["banderas"])