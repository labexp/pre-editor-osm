# Mapa actividad bici <img src="https://image.flaticon.com/icons/png/128/3163/3163394.png" width="25" height="25" />

### Descripción     
Este proyecto tiene como objetivo visualizar la movilidad en bicicleta en bicicleta en el cantón de Alajuela por medio de mapas de calor (*heatmaps*).


**Aspectos de implementación**

 Este proyecto se basa en el código del repositorio [gpxheatmap](https://github.com/durian/gpxheatmap), el cual usa las biblioteca `gpxpy` y `folium` (https://python-visualization.github.io/folium/plugins.html). Folium es una bibliioteca de Python3 que permite usar Leaflet, el mapa de calor utiliza como mapa base OSM<img src="https://www.openstreetmap.org/assets/osm_logo_256-ed028f90468224a272961c380ecee0cfb73b8048b34f4b4b204b7f0d1097875d.png" width="15" height="15" />.

 Se añadió `flask` (https://flask.palletsprojects.com/en/1.1.x/) para que el mapa generado se pueda ver en una página web.

**Requerimientos y ejecución**

Las siguientes instrucciones asumen que usted está dentro del directorio del proyecto ya clonado. A la hora de bifurcar (*"forkear"*) el repositorio puede utilizar el siguiente comando para obtener los archivos via *https*.
```
$ git clone <URL repositorio forkeado>
```

Este proyecto requiere `Python3`. Asegúrese que esté instalado en su distribución de Linux.  Si es la primera vez que lo utiliza, debe instalar además el sistema de gestión de paquetes `pip3` directo de la terminal.
```
$ sudo apt install python3-pip
```

Instalar los requerimientos necesarios para la ejecución del programa. Se recomienda utilizar un [entorno virtual](https://python-docs-es.readthedocs.io/es/3.8/library/venv.html), en este proyecto se utilizará el `.venv` como el nombre del entorno virtual.
```
$ pip3 install -r requerimientos.txt
```

Por último el programa es ejecutado.
```
$ python3 movilidad.py
```

El programa buscará las trazas con las cuales generará el mapa de calor en la carpeta `trazas`. Si no cuenta con trazas de movilidad en bicicleta puede  ver el funcionamiento del código usando otras trazas. Por ejemplo [trazas de transporte público.](https://github.com/labexp/trazas-transporte-publico).  El mapa sería así:

<img src="https://raw.githubusercontent.com/wolam/mapa-actividad-bici/master/imagenes-trazas/traza-santabarbar.png" width="500" height="400" />




## Licencia
---
GNU General Public License (GPL) v3.0

##### Autores:
Jaime Gutiérrez Alfaro [**@jamescr**](https://github.com/jamescr)

Wilhelm Carstens [**@wolam**](https://github.com/Wolam)
