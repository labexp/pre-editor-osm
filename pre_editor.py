import os
import logging
import argparse
import gpxpy

# Manejar entradas
parser = argparse.ArgumentParser(
    prog='Pre-editor OSM', description='Analizar trazas capturadas y compararlas con OSM.')


parser.add_argument('ruta_trazas',help="ruta a lo(s) arhivo(s) gpx a analizar")
parser.add_argument('esquema_mapeo',help="ruta del esquema para analizar gpx")
parser.add_argument('--rango', '-r', metavar='',required=False,default=20,
                    type=int, help='radio en metros de la circunferencia donde se descargarán los elementos de OSM.')

args = parser.parse_args()
print(args)

RUTA = '../trazas-transporte-publico/bus_alajuela-giralda/2546300.gpx'
def mostrar_waypoints(gpx):
    print('{0}Informacion de GPX{0}'.format("-"*10))
    for waypoint in gpx.waypoints:
        print('Waypoint Encontrado {0} -> ({1},{2})'.
              format(waypoint.name, waypoint.latitude, waypoint.longitude))


if __name__ == "__main__":
    archivo_gpx = open(RUTA,'r')
    gpx = gpxpy.parse(archivo_gpx)
    archivo_gpx.close()
    mostrar_waypoints(gpx)
