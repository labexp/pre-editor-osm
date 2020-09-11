import os
import folium
import gpxpy
from flask import Flask
from folium import plugins

app = Flask(__name__)

AJL_COORDS = (10.0118, -84.2364)


"""
Inicializar un mapa con las coordenadas de Alajuela
a su vez de incluir puntos de una traza 
por medio de un mapa de calor
"""
@app.route('/')
def construir_mapa():
    mapa_folium = folium.Map(location=AJL_COORDS, zoom_start=13)
    archivos_gpx = transcribir_directorio()
    latitudes_longitudes = obtener_latitudes_longitudes(archivos_gpx)
    #insertar en el mapa las longitudes y latitudes con un mapa de calor
    mapa_folium.add_child(plugins.HeatMap(latitudes_longitudes, radius=8))
    return mapa_folium._repr_html_()

# Parsear y obtener todos los gpx dados en un directorio de trazas deseado
def transcribir_directorio(directorio_trazas="trazas-transporte-publico/bus_santabarbara-alajuela"):
    archivos_gpx = []
   # parsed = 0
   # skipped = 0
    #print( "----" )
   # print( directorio_trazas )
    #print( len(sorted(os.listdir( directorio_trazas ))) )
   # print( "----" )
    lista_archivos = sorted(os.listdir( directorio_trazas ))
    for archivo in lista_archivos :
        ruta_archivo = directorio_trazas + "/" + archivo
        if  ruta_archivo.endswith(".gpx"):
         #   print( ruta_archivo )
            archivo_gpx_abierto = open(ruta_archivo, 'r')
            try:
                gpx_parseado = gpxpy.parse(archivo_gpx_abierto)
            except:
                #skipped += 1
                raise NameError( "ERROR TRANSCRIBIENDO ARCHIVO: {}".format(ruta_archivo) )
                #continue
            #parsed += 1
            archivos_gpx.append(gpx_parseado)
            archivo_gpx_abierto.close()
    #print("\tPARSED: ", parsed)
    #print("\tSKIPPED: ", skipped)
    return archivos_gpx

"""
Buscar dentro de los gpxs, las latitudes y longitudes
para poder incluirlas al mapa folium
"""
def obtener_latitudes_longitudes(archivos_gpx):
    latitudes_longitudes=[]
    for gpx in archivos_gpx:
        for traza in gpx.tracks:
            for segmento in traza.segments:
                for punto in segmento.points:
                    latitudes_longitudes.append([ punto.latitude, punto.longitude ])
    #print( "  puntos", len(latitudes_longitudes) )
    return latitudes_longitudes


if __name__ == '__main__':
    app.run(debug=True)
