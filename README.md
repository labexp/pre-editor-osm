# Pre Editor OSM 

### Descripción     
Este proyecto tiene como objetivo validar los datos de un GPX para devolver un informe que indique si la información existe en OSM está correcta, debe ser actualizada o no existe. A esta validación le llamamos pre edición, siendo que es un apoyo previo al proceso de editar el mapa. 

**Aspectos de implementación**

El proyecto se basa en el uso de la biblioteca `gpxpy` para la extracción de puntos.

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

Por último el programa es ejecutado.

```
$ python3 analizador_gpx.py
```

El programa buscará en la carpeta especificada (asignada como `RUTA` en el archivo py) los puntos de ruta (waypoints) que se encuentran en el gpx y los mostrará en la terminal.


## Licencia
---
GNU General Public License (GPL) v3.0

##### Autores:
Jaime Gutiérrez Alfaro [**@jamescr**](https://github.com/jamescr)

Wilhelm Carstens [**@wolam**](https://github.com/Wolam)
