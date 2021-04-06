import os
import json
import argparse
import gpxpy
import overpy

# Manejar entradas
parser = argparse.ArgumentParser(
    prog='Pre-editor OSM', description='Analizar trazas capturadas antes de editarlas en OSM')

parser.add_argument('--gpx', '-g', metavar='', required=True,
                    help="ruta a lo(s) archivo(s) gpx a analizar")
parser.add_argument('--esquema', '-e', metavar='',
                    required=True, help="ruta del esquema de mapeo")
parser.add_argument('--rango', '-r', metavar='', required=False, default=20,
                    type=int, help='radio en metros de la circunferencia donde se descargarán los '
                    + 'elementos de OSM')
parser.add_argument('--debug', '-d', metavar='', required=False, default=False,
                    type=bool, help='mostrar mensajes de depuración')

args = parser.parse_args()


def parsear_esquema():
    """
    Se encarga de convertir la ruta del esquema de entrada al programa
    a un diccionario de datos.

    Devuelve un diccionario correspondiente al esquema de mapeo.json
    """
    with open(args.esquema) as archivo_esquema:
        esquema_parseado = json.load(archivo_esquema)

    return esquema_parseado


def mostrar_waypoints(gpx):
    print('{0}Informacion de GPX{0}'.format("-"*10))
    for waypoint in gpx.waypoints:
        print('\nWaypoint Encontrado {0} -> ({1},{2})'.
              format(waypoint.name, waypoint.latitude, waypoint.longitude))

        nodos_alrededor = descargar_nodos_en_rango(waypoint.latitude, waypoint.longitude)
        if nodos_alrededor:
            print('\tNodos encontrados a {0}m del punto ({1},{2})'.format(args.rango,
                  waypoint.latitude, waypoint.longitude))
            mostrar_nodos_descargados(nodos_alrededor)
        else:
            print('\tNo hay nodos cerca del punto.')


def descargar_nodos_en_rango(lat, lon, debug=False):
    """
    A partir de un punto (lat, lon) dado como argumento, descarga todos los nodos que se encuentren
    a una distancia de 'rango' metros.

    Devuelve una lista de objetos overpy.Node.
    """
    api = overpy.Overpass()
    # Consulta descarga nodos, pero si se cambia "node" por "nwr" descarga vías y relaciones.
    consulta = "node(around:%s, %s, %s); out;" % (args.rango, lat, lon)
    resultado = api.query(consulta)
    if debug:
        mostrar_nodos_descargados(resultado)
    return resultado


def mostrar_nodos_descargados(resultado, prefijo="\t", mostrar_etiquetas=True):
    """
    Dada una lista de objetos overpy.Node los imprime en un formato como el siguiente:

    [prefijo]https://osm.org/node/-ID del nodo-
    [prefijo][prefijo]-etiqueta1- = -valor1-
    [prefijo][prefijo]-etiqueta2- = -valor2-
    ...
    [prefijo][prefijo]-etiquetaN- = -valorN-
    """
    debug_preambulo = "DEBUG (mostrar_nodos_descargados): "
    print(debug_preambulo + "Se descargaron " + str(len(resultado.nodes)) + " nodos.")
    for nodo in resultado.nodes:
        print(debug_preambulo + prefijo + "https://osm.org/node/" + str(nodo.id))
        if mostrar_etiquetas:
            for etiqueta in nodo.tags:
                print(debug_preambulo + prefijo*2 + etiqueta, ' = ' + nodo.tags[etiqueta])

def imprimir_encabezado():
    """
    Muestra en pantalla un encabezado correspondiente a un informe de una
    ruta de trazas brindadas y respectivo esquema.

    No devuelve ningun valor.
    """
    msj = "Informe \n{0}\n\nAnalizando la ruta {1} con el esquema de mapeo {2}."
    print(msj.format("="*8, args.gpx, args.esquema))

def imprimir_encabezado_waypoint(wpt_nombre, wpt_lat, wpt_lon):
    """
    Muestra en pantalla un encabezado correspondiente a un informe del análisis de un waypoiont.

    No devuelve ningun valor.
    """
    msj = "\n\nAnalizando el waypoint con nombre '{0}' ubicado en {1},{2}."
    print(msj.format(wpt_nombre, wpt_lat, wpt_lon))


def imprimir_crear(latitud, longitud, etiquetas_nuevas):
    """
    Basado en una latitud y longitudt indica que se debe crear un nodo con ciertas etiquetas
    en esa coordenada especifica.

    No devuelve ningun valor.
    """
    msj = "[CREAR] Se debe añadir un nuevo nodo en ({0}, {1}) con las etiquetas:\n{2}"
    print(msj.format(latitud, longitud, json.dumps(etiquetas_nuevas, indent=4)[1:-1]))


def imprimir_info(id):
    """
    Con base a un identificador de un nodo o vía en Open Street Map,imprime un
    mensaje de que el nodo se encuentra mapeado correctamente.

    No devuelve ningun valor.
    """
    msj = "[INFO] El nodo https://osm.org/node/{} está correctamente mapeado."
    print(msj.format(id))


def imprimir_editar(id, etiquetas_faltantes):
    """
    A partir de un identificador de un nodo, indica por medio de un mensaje que dicho
    nodo debe ser mejorado con las etiquetas de la forma {llave1:valor1...llaveN:valorN}
    encontradas en el esquema de mapeo.

    No devuelve ningun valor.
    """
    msj = "[EDITAR] El nodo https://osm.org/node/{0} debe ser mejorado con las etiquetas:\n{1}"
    print(msj.format(id, json.dumps(etiquetas_faltantes, indent=4)[1:-1]))


def imprimir_revisar(id, etiquetas_sobrantes):
    """
    Indica que cierto nodo con identificador brindado posee mayor cantidad de etiquetas
    a las que corresponde en el esquema de mapeo y por lo tanto debe ser revisado.

    No devuelve ningun valor.
    """
    msj = ("[REVISAR] El nodo https://osm.org/node/{0} tiene más etiquetas que las indicadas "
           "en el esquema de mapeo {1}\nLas etiquetas demás son:\n{2}")
    print(msj.format(id, args.esquema, json.dumps(etiquetas_sobrantes, indent=4)[1:-1]))


def imprimir_resultado(nodo,waypoint,estructura_analisis):
    """
    Recibe una estructura de anális retormada por analizar_etiquetas y los datos del nodo y
    waypoint. Con base a esto decide cuál resultado debe ser impreso.

    No devuelve ningun valor.
    """
    caso = estructura_analisis[0]
    etiquetas_analizadas = estructura_analisis[1]
    if caso == "REVISAR":
        imprimir_revisar(nodo.id,etiquetas_analizadas)
    elif caso == "EDITAR":
        imprimir_editar(nodo.id,etiquetas_analizadas)
    elif caso == "CREAR":
        imprimir_crear(waypoint.latitude,waypoint.longitude,etiquetas_analizadas)
    elif caso == "INFO":
        imprimir_info(nodo.id)
    else:
        print("Nada por hacer")


def analizar_traza(ruta_gpx, debug=False):
    """
    Recibe una ruta a un archivo GPX el cual cada uno de sus waypoints debe ser analizado.

    No devuelve ningún valor. Imprime en pantalla los resultados del análisis apoyándose en las
    funciones auxiliares.
    """
    archivo_gpx = open(ruta_gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    # parsear esquema antes
    for waypoint in gpx.waypoints:
        nodos_cercanos = descargar_nodos_en_rango(waypoint.latitude,waypoint.longitude, debug)
        nombre_waypoint = waypoint.name
        imprimir_encabezado_waypoint(nombre_waypoint, waypoint.latitude, waypoint.longitude)
        etiquetas_esquema = esquema_mapeo_global[nombre_waypoint]
        resultados_analisis = list()
        for nodo in nodos_cercanos.nodes:
            etiquetas_osm = nodo.tags
            estructura_analisis = analizar_etiquetas(etiquetas_osm, etiquetas_esquema, debug)
            if estructura_analisis[0] != "NADA":
                resultados_analisis.append(estructura_analisis)
                imprimir_resultado(nodo,waypoint,estructura_analisis)

        if resultados_analisis == []:
            # CREAR
            imprimir_resultado(nodo,waypoint,["CREAR", etiquetas_esquema])

    archivo_gpx.close()


def analizar_etiquetas(etiquetas_osm: dict, etiquetas_esquema: dict,debug=True) -> list:
    """
    Segun las etiquetas en osm cercanas y las etiquetas en el esquema de cierto waypoint,
    si las ambos dicciones son iguales (INFO), si hay al menos una coinciddncia en una etiqueta pero
    hay ḿas etiquetas en el esquema (EDITAR), si hay condicen todas las etiquetas entre ambos
    diccionario pero hay algunas adicionales en OSM (REVISAR). Si ninguno de los tres casos está
    presente entonces se devuelve el código de caso NADA con etiqueta nulas.

    Devuelve una estructura una lista con el formato:

    [codigo_caso, etiquetas]

    etiquetas será una opción entre: etiquetas_sobrantes||faltantes||necesarias||null
    """

    debug_preambulo = "DEBUG (analizar_etiquetas): "

    if debug:
        print("\n\n")
        print(debug_preambulo + "etiquetas_osm: " + str(etiquetas_osm))
        print(debug_preambulo + "etiquetas_esquema: " + str(etiquetas_esquema))
    total_osm = len(etiquetas_osm)
    total_esquema = len(etiquetas_esquema)

    coincidencias = dict(etiquetas_osm.items() & etiquetas_esquema.items())
    # "fsobrantes_en_osm": están en OSM y no en el esquema.
    sobrantes_en_osm = dict(etiquetas_osm.items() - etiquetas_esquema.items())
    # sobrantes_esquema: están en el esquema y no en OSM
    sobrantes_esquema = dict(etiquetas_esquema.items() - etiquetas_osm.items())

    # INFO
    if total_esquema == total_osm and total_osm == len(coincidencias):
        # caso info si etiquetas_osm y etiquetas_esquema son iguales
        if debug:
            print(debug_preambulo + "INFO" + str(None))
        return ["INFO", None]

    # EDITAR
    elif len(coincidencias) >= 1 and len(sobrantes_esquema) >= 1:
        # caso editar si etiquetas_osm son mas que etiquetas_esquema
        if debug:
            print(debug_preambulo + "EDITAR" + str(sobrantes_esquema))
        return ["EDITAR", sobrantes_esquema]

    # REVISAR
    elif len(coincidencias) == total_esquema and len(sobrantes_en_osm) > 0:
        # caso crear si etiquetas_esquema son mas que etiquetas_osm
        if debug:
            print(debug_preambulo + "REVISAR" + str(sobrantes_en_osm))
        return ["REVISAR", sobrantes_en_osm]

    # NADA: candidato a caso de CREAR
    else:
        if debug:
            print(debug_preambulo + "CASO NO CONTEMPLADO")
            print(debug_preambulo + "total_osm: " + str(total_osm))
            print(debug_preambulo + "total_esquema: " + str(total_esquema))
            print(debug_preambulo + "coincidencias " + str(coincidencias))
            print(debug_preambulo + "sobrantes_en_osm: " + str(sobrantes_en_osm))
            print(debug_preambulo + "sobrantes_esquema: " + str(sobrantes_esquema))
        return ["NADA", None]

esquema_mapeo_global = parsear_esquema()

if __name__ == "__main__":
    '''
    archivo_gpx = open(args.gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
    mostrar_esquema(args.esquema)
    '''
    ruta_gpx = args.gpx
    debug = args.debug

    #caso info
    #etiquetas_osm = {'amenity':'taxi'}
    #etiquetas_esquema = {'amenity':'taxi'}
    #print(analizar_etiquetas(etiquetas_osm, etiquetas_esquema))

    # caso editar
    #etiquetas_osm ={'crossing': 'traffic_signals', 'highway': 'traffic_signals', 'traffic_signals': 'crossing'}
    #etiquetas_esquema = {'crossing': 'traffic_signals', 'traffic_signals:sound': 'walk;yes'}
    #print(analizar_etiquetas(etiquetas_osm, etiquetas_esquema))

    # caso revisar
    #etiquetas_osm = {'bench': 'yes', 'bus': 'yes', 'covered': 'yes', 'highway': 'bus_stop', 'name': 'UNADECA', 'public_transport': 'platform', 'shelter': 'yes'}
    #etiquetas_esquema = {'public_transport': 'platform', 'bench': 'yes', 'shelter': 'yes', 'bus': 'yes'}
    #print(analizar_etiquetas(etiquetas_osm, etiquetas_esquema))

    analizar_traza(ruta_gpx, debug)
