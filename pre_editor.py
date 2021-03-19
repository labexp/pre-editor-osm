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


def descargar_nodos_en_rango(lat, lon):
    """
    A partir de un punto (lat, lon) dado como argumento, descarga todos los nodos que se encuentren
    a una distancia de 'rango' metros.

    Devuelve una lista de objetos overpy.Node.
    """
    api = overpy.Overpass()
    # Consulta descarga nodos, pero si se cambia "node" por "nwr" descarga vías y relaciones.
    consulta = "node(around:%s, %s, %s); out;" % (args.rango, lat, lon)
    resultado = api.query(consulta)
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
    for nodo in resultado.nodes:
        print(prefijo, "https://osm.org/node/" + str(nodo.id))
        if mostrar_etiquetas:
            for etiqueta in nodo.tags:
                print(prefijo*2 + etiqueta, ' = ' + nodo.tags[etiqueta])


def imprimir_encabezado():
    """
    Muestra en pantalla un encabezado correspondiente a un informe de una
    ruta de trazas brindadas y respectivo esquema.

    No devuelve ningun valor.
    """
    msj = "Informe \n{0}\n\nAnalizando la ruta {1} con el esquema de mapeo {2}."
    print(msj.format("="*8, args.gpx, args.esquema))


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
    else:
        imprimir_info(nodo.id)
        
def analizar_traza(ruta_gpx):
    """
    Recibe una ruta a un archivo GPX el cual cada uno de sus waypoints debe ser analizado.

    No devuelve ningún valor
    """
    archivo_gpx = open(args.gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    # parsear esquema antes
    for waypoint in gpx.waypoints:
        nodos_cercanos = descargar_nodos_en_rango(waypoint.lat,waypoint.lon)
        nombre_waypoint = waypoint.name
        etiquetas_esquema = esquema_mapeo_global[nombre_waypoint]
        for nodo in nodos_cercanos:     
            etiquetas_osm = nodo.tags
            estructura_analisis = analizar_etiquetas(etiquetas_osm, etiquetas_esquema)
            imprimir_resultado(nodo,waypoint,estructura_analisis)
              
def analizar_etiquetas(etiquetas_osm: dict, etiquetas_esquema: dict) -> list:
    """
    Segun las etiquetas en osm cercanas y las etiquetas en el esquema de cierto waypoint,
    analiza si las etiquetas de osm se encuentran correctamente mapeadas o viceversa.
    
    Devuelve una estructura una lista con el formato
    [cod_caso,etiquetas_sobrantes||faltantes||necesarias||null]
    """
    total_osm = len(etiquetas_osm)
    total_esquema = len(etiquetas_esquema)

    coincidencias = dict(etiquetas_osm.items() & etiquetas_esquema.items())
    faltantes = dict(etiquetas_osm.items() - etiquetas_esquema.items())
    sobrantes = dict(etiquetas_esquema.items() - etiquetas_osm.items())

    if total_esquema == total_osm and total_osm == len(coincidencias):
        # caso info si etiquetas_osm y etiquetas_esquema son iguales
        return ["INFO", None]
    elif len(faltantes) >= len(coincidencias):
        # caso editar si etiquetas_osm son mas que etiquetas_esquema
        return ["EDITAR",faltantes]
    elif len(coincidencias) == 0:
        # caso crear si etiquetas_osm y etiquetas_esquema no coinciden
        return ["CREAR",etiquetas_esquema]
    elif len(sobrantes) >= len(coincidencias):
        # caso crear si etiquetas_esquema  son mas que etiquetas_osm
        return ["REVISAR",sobrantes]
    

esquema_mapeo_global = parsear_esquema()

if __name__ == "__main__":
    '''
    archivo_gpx = open(args.gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
    mostrar_esquema(args.esquema)
    '''
    etiquetas_osm = {'amenity':'taxi'}
    etiquetas_esquema = {'amenity':'taxi'}
    print(analizar_etiquetas(etiquetas_osm, etiquetas_esquema))
