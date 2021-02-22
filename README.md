# Pre Editor OSM 

### Descripción     
Este proyecto tiene como objetivo validar los datos de un GPX para devolver un informe que indique si la información existe en OSM está correcta, debe ser actualizada o no existe. A esta validación le llamamos pre edición, siendo que es un apoyo previo al proceso de editar el mapa. 

**Bibliotecas utilizadas**

* [gpxpy](https://pypi.org/project/gpxpy/) para la extracción de puntos del gpx.
* [overpy](https://github.com/DinoTools/python-overpy)  para descargar nodos desde OSM.

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
python3 -m venv .venv
```

Iniciar/activar el ambiente virtual para dependendecias posteriores

```
source .venv/bin/activate
```

Sucesivamente se instalan los requerimientos especificados.

```
$ pip3 install -r requerimientos.txt
```

Por último el programa es ejecutado con los argumentos correspondientes.

```
$  python3 pre_editor.py (--gpx|-g ruta_gpx) (--esquema|-e) esquema_mapeo [--rango|-r metros]
```

**Argumentos**

El programa buscará en la carpeta especificada (asignada como `ruta_gpx`) los archivos gpx correspondientes\
para luego analizar los nodos con la ruta del esquema de mapeo (`esquema_mapeo`) brindado.

El `rango` en metros de la circunferencia donde se van a descargar los elementos en OSM es opcional.\
Por defecto se encuentra con un valor de 20.


## Licencia
---
GNU General Public License (GPL) v3.0

##### Autores:
Jaime Gutiérrez Alfaro [**@jamescr**](https://github.com/jamescr)

Wilhelm Carstens [**@wolam**](https://github.com/Wolam)
