# Semana 4: búsqueda visual y transición de K-Means a KNN

## Propósito

Durante esta semana se utilizarán dos ideas de inteligencia artificial:

1. **Búsqueda:** explorar estados para encontrar una ruta hasta una meta.
2. **Clasificación por vecinos:** utilizar ejemplos etiquetados para clasificar un caso nuevo.

La práctica anterior de K-Means servirá como punto de comparación con KNN.

## Resultados de aprendizaje

Al finalizar podrás:

- identificar estado, acción, frontera, visitados y meta;
- explicar por qué registrar estados evita ciclos;
- distinguir BFS, DFS y A*;
- diferenciar K-Means de KNN;
- calcular una distancia euclidiana;
- seleccionar los vecinos más cercanos;
- clasificar un punto mediante votación;
- comparar distintos valores de `k`.

## Archivos

### Guías

- [`guias/algoritmos_busqueda_y_programa.md`](guias/algoritmos_busqueda_y_programa.md)
- [`guias/kmeans_knn_comparativa.md`](guias/kmeans_knn_comparativa.md)

### Código

- [`codigo/busqueda_visual.py`](codigo/busqueda_visual.py): ejemplo completo con ventana interactiva.
- [`codigo/kmeans_segmentacion_rgb.py`](codigo/kmeans_segmentacion_rgb.py): carga una imagen, la segmenta y presenta su nube RGB.
- [`codigo/knn_paso_a_paso.py`](codigo/knn_paso_a_paso.py): carga una imagen, clasifica sus píxeles mediante ejemplos RGB etiquetados y muestra las clases en una nube tridimensional.
- [`codigo/images`](codigo/images): imágenes disponibles para las dos prácticas.

## Orden de trabajo

1. Ejecuta `busqueda_visual.py`.
2. Crea un mapa con al menos un ciclo o una isla interior.
3. Compara BFS, DFS y A*.
4. Lee la guía de búsqueda.
5. Ejecuta `kmeans_segmentacion_rgb.py`.
6. Lee la comparación entre K-Means y KNN.
7. Completa los `TODO` de `knn_paso_a_paso.py`.
8. Cambia la ruta entre `oso.jpg`, `luna.jpg`, `lena.jpg` y `dos.jpg`.
9. Prueba `k = 1`, `k = 3` y `k = 5`.
10. Registra resultados y conclusiones.

## Evidencias sugeridas

- captura del escenario de búsqueda;
- tabla con costo y nodos expandidos de BFS, DFS y A*;
- imagen original y segmentada del recordatorio de K-Means;
- imagen cargada, mapa de clases de color y nube RGB producidos por KNN;
- código con los `TODO` completados;
- predicciones con tres valores diferentes de `k`;
- respuestas a las preguntas de las guías.

## Regla importante

No confundas los dos significados de `K`:

- en K-Means: número de grupos por formar;
- en KNN: número de vecinos que participan en la votación.
