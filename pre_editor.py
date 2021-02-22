import os
import argparse
import gpxpy
import overpy

# Manejar entradas
parser = argparse.ArgumentParser(
    prog='Pre-editor OSM', description='Analizar trazas capturadas antes de editarlas en OSM')

parser.add_argument('--gpx', '-g',metavar='', required=True,
                    help="ruta a lo(s) archivo(s) gpx a analizar")
parser.add_argument('--esquema', '-e', metavar='', required=True, help="ruta del esquema de mapeo")
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
                print(prefijo*2 +  etiqueta, ' = ' + nodo.tags[etiqueta])


if __name__ == "__main__":
    # mostrar waypoints del gpx de entrada
    archivo_gpx = open(args.gpx,'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
