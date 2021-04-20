import json
import argparse
import gpxpy
import overpy

# Manejar entradas
parser = argparse.ArgumentParser(
    prog='Pre-editor OSM',
    description='Analizar trazas capturadas antes de editarlas en OSM')

parser.add_argument('--gpx', '-g', metavar='', required=True,
                    help="ruta a lo(s) archivo(s) gpx a analizar")
parser.add_argument('--esquema', '-e', metavar='',
                    required=True, help="ruta del esquema de mapeo")
parser.add_argument('--rango', '-r', metavar='', required=False,
                    default=20, type=int,
                    help='radio en metros de la circunferencia donde' +
                    'se descargarán los elementos de OSM')
parser.add_argument('--debug', '-d', metavar='', required=False, default=False,
                    type=bool, help='mostrar mensajes de depuración')

args = parser.parse_args()


def parsear_esquema() -> dict:
    """
    Se encarga de convertir la ruta del esquema de entrada al programa
    a un diccionario de datos.

    Devuelve un diccionario correspondiente al esquema de mapeo.json
    """
    with open(args.esquema) as archivo_esquema:
        esquema_parseado = json.load(archivo_esquema)

    return esquema_parseado


def descargar_nodos_en_rango(lat: float, lon: float,
                             debug=False) -> [overpy.Node]:
    """
    A partir de un punto (lat, lon) dado como argumento, descarga
    todos los nodos que se encuentren a una distancia de 'rango'
    metros.

    Devuelve una lista de objetos overpy.Node.
    """
    api = overpy.Overpass()

    # Consulta descarga nodos, pero si se cambia "node"
    # por "nwr" descarga vías y relaciones.
    consulta = "node(around:%s, %s, %s); out;" % (args.rango, lat, lon)
    descarga_nodos = api.query(consulta)
    if debug:
        mostrar_nodos_descargados(descarga_nodos)
    return descarga_nodos


def mostrar_nodos_descargados(nodos_descargados: [overpy.Node],
                              mostrar_etiquetas=True) -> None:
    """
    Dada una lista de objetos overpy.Node los imprime en un
    formato como el siguiente:

    [TAB]https://osm.org/node/-ID del nodo-
    [TAB][TAB]etiqueta1 => valor1
    [TAB][TAB]etiqueta2 => valor2
    ...
    [TAB][TAB]etiquetaN => valorN
    """
    debug_preambulo = "DEBUG (mostrar_nodos_descargados): "
    url = "https://osm.org/node/"
    print('{0} Se descargaron {1} nodos.'.
          format(debug_preambulo, len(nodos_descargados.nodes)))
    for nodo in nodos_descargados.nodes:
        print('{:>10}{}'.format(url, nodo.id))
        if mostrar_etiquetas:
            for llave, valor in nodo.tags.items():
                print('{:>10} => {:>10}'.format(llave, valor))


def imprimir_encabezado_traza(ruta_gpx: str) -> None:
    """
    Muestra en pantalla un encabezado correspondiente a un
    informe de una ruta de traza gpx brindada y
    la ruta del esquema enviada por terminal.

    No devuelve ningun valor.
    """
    msj = "Informe \n{0}\n\nAnalizando la ruta {1} con el esquema de mapeo {2}"
    print(msj.format("="*8, ruta_gpx, args.esquema))


def imprimir_encabezado_waypoint(nombre: str,
                                 latitud: float,
                                 longitud: float) -> None:
    """
    Muestra en pantalla un encabezado correspondiente
    a un informe del análisis de un waypoint.

    No devuelve ningun valor.
    """
    msj = "\n\nAnalizando el waypoint con nombre '{0}' ubicado en ({1},{2})."
    print(msj.format(nombre, latitud, longitud))


def imprimir_crear(latitud: float, longitud: float,
                   etiquetas_nuevas: dict) -> None:
    """
    Basado en una latitud y longitud indica que se debe crear un
    nodo con ciertas etiquetas en esa coordenada especifica.

    No devuelve ningun valor.
    """
    msj = ("[CREAR] Se debe añadir un nuevo nodo en ({0}, {1})"
           " con las etiquetas:\n{2}")
    print(msj.format(latitud, longitud, json.dumps(
        etiquetas_nuevas, indent=4)[1:-1]))


def imprimir_info(argumentos_imprimir: (int, dict, float, float)) -> None:
    """
    Con base a los argumentos de imprimir, obtiene
    el indentificador de un nodo o vía en Open Street Map e
    imprime un mensaje de que el nodo se encuentra
    mapeado correctamente.

    No devuelve ningun valor.
    """
    id = argumentos_imprimir[0]
    msj = ("[INFO] El nodo https://osm.org/node/{}"
           " está correctamente mapeado.")
    print(msj.format(id))


def imprimir_editar(argumentos_imprimir: (int, dict, float, float)) -> None:
    """
    A partir de los argumentos de imprimir, obtiene las
    etiquetas faltantes y el identificador de nodo
    para indicar en pantalla que debe ser mejorado con las
    etiquetas de la forma {llave1:valor1...llaveN:valorN}
    encontradas en el esquema de mapeo.

    No devuelve ningun valor.
    """
    id, etiquetas_faltantes, _, _ = argumentos_imprimir
    msj = ("[EDITAR] El nodo https://osm.org/node/{0}"
           "debe ser mejorado con las etiquetas:\n{1}")
    print(msj.format(id, json.dumps(etiquetas_faltantes, indent=4)[1:-1]))


def imprimir_revisar(argumentos_imprimir: (int, dict, float, float)) -> None:
    """

    Según los argumentos de imprimir, consigue las
    etiquetas  sobrantes y el identificador de nodo
    para imprimir en pantalla que el nodo cuenta con una
    mayor cantidad de etiquetas a las que corresponde en el
    esquema de mapeo y por lo tanto debe ser revisado.

    No devuelve ningun valor.
    """
    id, etiquetas_sobrantes, _, _ = argumentos_imprimir
    msj = ("[REVISAR] El nodo https://osm.org/node/{0}"
           "tiene más etiquetas que las indicadas en el"
           "esquema de mapeo {1}\nLas etiquetas demás son:\n{2}")
    print(msj.format(id, args.esquema, json.dumps(
        etiquetas_sobrantes, indent=4)[1:-1]))


def imprimir_resultado(resultado: (callable, dict), id: int,
                       latitud: float, longitud: float) -> None:
    """
    Recibe un resultado retornado de la forma
    (funcion_imprimir, etiquetas_analizadas),
    un identificador y la latitud y longitud del waypoint.

    Con base a esto decide cuál funcion debe ser llamada
    para imprimir el resultado.

    No devuelve ningun valor.
    """
    funcion_imprimir, etiquetas_analizadas = resultado
    argumentos_imprimir = (id, etiquetas_analizadas, latitud, longitud)
    funcion_imprimir(argumentos_imprimir)


def analizar_traza(ruta_gpx: str, debug=False) -> None:
    """
    Recibe una ruta a un archivo GPX el cual cada uno de sus
    waypoints debe ser analizado.

    Imprime en pantalla los resultados del análisis apoyándose en las
    en los argumentos recibidos por el análisis de etiquetas.

    No devuelve ningún valor.
    """

    imprimir_encabezado_traza(ruta_gpx)

    # Parsear el gpx
    archivo_gpx = open(ruta_gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()

    for waypoint in gpx.waypoints:

        # Obtener los atributos del waypoint
        latitud = waypoint.latitude
        longitud = waypoint.longitude
        nombre = waypoint.name

        # Mostrar informacion del waypoint
        nodos_cercanos = descargar_nodos_en_rango(latitud, longitud, debug)
        imprimir_encabezado_waypoint(nombre, latitud, longitud)

        # Se asume que las etiquetas del waypoint no se encuentran en OSM
        nodo_es_nuevo = True

        # Si no hay etiquetas en el esquema con ese nombre se omite
        etiquetas_esquema = esquema.get(nombre)
        if etiquetas_esquema is not None:
            for nodo in nodos_cercanos.nodes:
                etiquetas_osm = nodo.tags
                resultado = analizar_etiquetas(
                    etiquetas_osm, etiquetas_esquema, debug)

                # Si el resultado fue un caso esperado quiere decir que
                # las etiquetas analizadas ya estaban en OSM
                if resultado is not None:
                    nodo_es_nuevo = False
                    imprimir_resultado(resultado, nodo.id, latitud, longitud)

            if nodo_es_nuevo:
                imprimir_crear(latitud, longitud, etiquetas_esquema)


def analizar_etiquetas(etiquetas_osm: dict, etiquetas_esquema: dict,
                       debug=True) -> (callable, dict):
    """
    Segun las etiquetas en osm cercanas y las etiquetas en el
    esquema de cierto waypoint, determina cual es la funcion
    que se debe llamar para mostrar en pantalla las etiquetas
    analizadas

    Si las ambos dicciones son iguales (INFO),

    Si hay al menos una coincidencia en una etiqueta pero
    hay ḿas etiquetas en el esquema (EDITAR)

    Si hay condicen todas las etiquetas entre ambos
    diccionarios pero hay algunas adicionales en OSM (REVISAR)

    Si ninguno de los tres casos está presente entonces se
    devuelve un resultado vacio

    Devuelve una tupla de resultado con el formato:

    (funcion_imprimir, etiquetas)

    etiquetas será una opción entre:
    etiquetas_sobrantes||faltantes||necesarias||None

    funcion_imprimir será una opción entre imprimir_:
    info||editar||revisar||None
    """

    debug_preambulo = "DEBUG (analizar_etiquetas): "

    if debug:
        print('\n\n {0} etiquetas_osm: {1} etiquetas_esquema{2}'
              .format(debug_preambulo, etiquetas_osm, etiquetas_esquema))
    total_osm = len(etiquetas_osm)
    total_esquema = len(etiquetas_esquema)

    coincidencias = dict(etiquetas_osm.items() & etiquetas_esquema.items())
    # sobrantes_en_osm: están en OSM y no en el esquema.
    sobrantes_en_osm = dict(etiquetas_osm.items() - etiquetas_esquema.items())
    # sobrantes_esquema: están en el esquema y no en OSM
    sobrantes_esquema = dict(etiquetas_esquema.items() - etiquetas_osm.items())

    # INFO
    if total_esquema == total_osm and total_osm == len(coincidencias):
        # caso info si etiquetas_osm y etiquetas_esquema son iguales
        if debug:
            print('{0} INFO (None)'.format(debug_preambulo))
        return (imprimir_info, None)

    # EDITAR
    elif len(coincidencias) >= 1 and len(sobrantes_esquema) >= 1:
        # caso editar si etiquetas_osm son mas que etiquetas_esquema
        if debug:
            print('{0} EDITAR {1}'.format(debug_preambulo, sobrantes_esquema))
        return (imprimir_editar, sobrantes_esquema)

    # REVISAR
    elif len(coincidencias) == total_esquema and len(sobrantes_en_osm) > 0:
        # caso crear si etiquetas_esquema son mas que etiquetas_osm
        if debug:
            print('{0} REVISAR {1}'.format(debug_preambulo, sobrantes_en_osm))
        return (imprimir_revisar, sobrantes_en_osm)

    # NADA: candidato a caso de CREAR
    else:
        if debug:
            msj = ("{0} CASO NO CONTEMPLADO\n"
                   "{0} total_osm: {1}\n"
                   "{0} total_esquema: {2}\n"
                   "{0} coincidencias: {3}\n"
                   "{0} sobrantes_osm: {4}\n"
                   "{0} sobrantes_esquema: {5}\n")
            print(msj.format(debug_preambulo, total_osm, total_esquema,
                             coincidencias, sobrantes_en_osm,
                             sobrantes_esquema))
        return None


esquema = parsear_esquema()

if __name__ == "__main__":
    ruta_gpx = args.gpx
    debug = args.debug
    analizar_traza(ruta_gpx, debug)
