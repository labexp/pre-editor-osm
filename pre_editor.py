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


def mostrar_esquema(ruta_esquema):
    with open(ruta_esquema) as esquema:
        data = json.load(esquema)
        del data['nombre-esquema']  # evitar recorrer la hilera 'bekuo'
        # imprimir cada uno de los nodos
        for nodo in data.keys():
            print('{0}Nodo encontrado{0} \n{1}'.format("-"*10, nodo))
            llaves = data[nodo]
            # imprimir cada llave del esquema con su valor
            for i, llave in enumerate(llaves):
                valor = llaves[llave]
                print('Llave Nº{0} \'{1}:{2}\''.format(i+1, llave, valor))


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
    Basado en un waypoint indica que se debe crear un nodo con ciertas etiquetas
    en una coordenada especifica.

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


if __name__ == "__main__":
    # mostrar waypoints del gpx de entrada
    archivo_gpx = open(args.gpx, 'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
    mostrar_esquema(args.esquema)
