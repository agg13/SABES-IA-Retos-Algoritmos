# Instalación de Python y paquetes del repositorio

## Objetivo

Preparar un entorno aislado para ejecutar los ejemplos y retos del curso sin modificar otras instalaciones de Python del equipo.

Las instrucciones principales están escritas para Windows. En otros sistemas cambian principalmente los comandos de activación del entorno virtual.

## 1. Instalar Python

Instala una versión de Python de 64 bits compatible con los paquetes del curso. En los equipos del laboratorio se utilizará la versión que indique el profesor.

Durante la instalación en Windows:

1. activa la opción para agregar Python al `PATH`, si aparece;
2. conserva la instalación de `pip`;
3. termina la instalación;
4. cierra y vuelve a abrir la terminal.

Comprueba la instalación:

```powershell
python --version
```

Si Windows utiliza el lanzador `py`, prueba:

```powershell
py --version
```

No continúes hasta que alguno de estos comandos muestre una versión válida.

## 2. Descargar el repositorio

Puedes descargar el repositorio como archivo ZIP o clonarlo con Git. Guarda la carpeta en una ubicación cuyo nombre puedas identificar fácilmente.

Después abre una terminal dentro de la carpeta que contiene `README.md` y `requirements.txt`.

## 3. Crear un entorno virtual

Con `python`:

```powershell
python -m venv .venv
```

O con el lanzador `py`:

```powershell
py -m venv .venv
```

El entorno virtual separa los paquetes de esta materia de los utilizados por otros proyectos.

## 4. Activar el entorno

### PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Símbolo del sistema de Windows

```bat
.venv\Scripts\activate.bat
```

Si PowerShell no permite activar el entorno, utiliza el Símbolo del sistema. No cambies las políticas de seguridad de todo el equipo sin autorización.

Cuando el entorno está activo, normalmente aparece `(.venv)` al inicio de la línea.

## 5. Actualizar pip

```powershell
python -m pip install --upgrade pip
```

## 6. Instalar los paquetes base

Desde la carpeta donde se encuentra `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Los paquetes iniciales son:

| Paquete | Uso principal |
|---|---|
| NumPy | Arreglos, imágenes y operaciones numéricas |
| Matplotlib | Gráficas y visualización |
| Pillow | Lectura y manejo básico de archivos de imagen |
| scikit-learn | K-Means, KNN y otros algoritmos de aprendizaje automático |
| pandas | Tablas y conjuntos de datos |
| pyserial | Comunicación entre Python y Arduino |

Las prácticas futuras podrán solicitar paquetes adicionales, por ejemplo `scikit-fuzzy`, `opencv-python` o `ultralytics`. Instálalos únicamente cuando la guía de la semana lo indique, porque algunos son grandes y requieren más tiempo.

## 7. Comprobar Tkinter

El programa visual de búsqueda utiliza Tkinter, que normalmente se incluye con Python en Windows.

Ejecuta:

```powershell
python -m tkinter
```

Debe abrirse una ventana pequeña de prueba. Ciérrala para continuar.

Si aparece un error indicando que Tkinter no existe, utiliza una instalación de Python que incluya soporte Tk o solicita apoyo al profesor.

## 8. Comprobar los paquetes

Ejecuta:

```powershell
python -c "import numpy, matplotlib, sklearn, pandas, serial; print('Instalación correcta')"
```

Si aparece `Instalación correcta`, el entorno base está listo.

## 9. Ejecutar un programa

Entra en la carpeta del código de la semana 4:

```powershell
cd semana_04\codigo
```

Ejecuta el programa visual de búsqueda:

```powershell
python busqueda_visual.py
```

Ejecuta el recordatorio de K-Means:

```powershell
python kmeans_segmentacion_rgb.py
```

Ejecuta el reto de KNN:

```powershell
python knn_paso_a_paso.py
```

## 10. Cerrar el entorno virtual

Al terminar:

```powershell
deactivate
```

## Problemas frecuentes

### `python` no se reconoce

Cierra y vuelve a abrir la terminal. Si continúa, prueba `py` o revisa la instalación de Python.

### `No module named ...`

Comprueba que el entorno virtual esté activo y repite:

```powershell
python -m pip install -r requirements.txt
```

### El programa imprime datos, pero no abre una ventana

Verifica Tkinter con:

```powershell
python -m tkinter
```

Ejecuta el archivo completo desde una terminal, no solamente una selección de líneas.

### Las gráficas se cierran inmediatamente

Ejecuta el archivo desde una terminal para poder leer cualquier mensaje de error. No cierres la terminal mientras las gráficas estén abiertas.

### Se instaló el paquete, pero Python no lo encuentra

Puede haberse instalado en otro intérprete. Comprueba:

```powershell
python -m pip --version
python --version
```

Ambos deben apuntar al entorno `.venv` cuando está activado.
