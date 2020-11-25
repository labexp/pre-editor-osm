import gpxpy

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
