import os
import argparse
import gpxpy

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
        print('Waypoint Encontrado {0} -> ({1},{2})'.
              format(waypoint.name, waypoint.latitude, waypoint.longitude))

if __name__ == "__main__":
    # mostrar waypoints del gpx de entrada
    archivo_gpx = open(args.gpx,'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
