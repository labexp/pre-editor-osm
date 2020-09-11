# Mapa actividad bici <img src="https://image.flaticon.com/icons/png/128/3163/3163394.png" width="25" height="25" />

### Descripción     
Este proyecto tiene como objetivo la visualización de la actividad en bicicleta por el cantón de Alajuela por medio de *heatmaps* (mapas de calor) basados en [gpxheatmap](https://github.com/durian/gpxheatmap). La idea es tratar de localizar las mayor circulación de usuarios en bicicletas la cual emplean principalmente para movilidad como insumo para el diseño de infraestructura.

El código de `movilidad.py` es una adaptación al código de `gpx-locus.py` que busca. En esta se cambian los datos de entrada para usar trazas de rutas de bus que pasan por Alajuela y se centra el mapa de OSM <img src="https://www.openstreetmap.org/assets/osm_logo_256-ed028f90468224a272961c380ecee0cfb73b8048b34f4b4b204b7f0d1097875d.png" width="15" height="15" /> en Alajuela.  Este código usa la biblioteca `gpxpy` y `folium` (https://python-visualization.github.io/folium/plugins.html).  Se añadió `flask` (https://flask.palletsprojects.com/en/1.1.x/) para que el mapa generado se pueda ver en una página web. 

Las trazas son presentadas por medio de un directorio la cual contiene los archivos gpx.
Para temas de pruebas se pueden utilizar las [trazas de transporte público.](https://github.com/labexp/trazas-transporte-publico)

<img src="https://raw.githubusercontent.com/wolam/mapa-actividad-bici/master/imagenes-trazas/traza-santabarbar.png" width="500" height="400" />

**Ejemplo de visualización de la traza en bus_santabarbara_alajuela.**

#### Requerimientos y ejecución
Las siguientes instrucciones asumen que usted está dentro del directorio del proyecto ya clonado. A la hora de forkear el repositorio puede utilizar el siguiente comando para obtener los archivos via *https*.
```
$ git clone <URL repositorio forkeado>
```
Este proyecto requiere `python3`. Asegúrese que esté instalado en su distribución de linux. 
Si es la primera vez que lo utiliza, debe instalar además el sistema de gestión de paquetes `pip3` directo de la terminal.
```
$ sudo apt install python3-pip
```
Sucesivamente debe instalar los requerimientos necesarios para la ejecución del programa.
```
$ pip3 install -r requerimientos.txt
```
Por último el programa es ejecutado.
```
$ python3 movilidad.py
```

Licencia
---
GNU General Public License (GPL) v3.0

##### Autores:
Jaime Gutierrez [**@elotrojames**](github.com/elotrojames)

Wilhelm Carstens [**@wolam**](github.com/wolam)
