# K-Means y KNN: explicación básica y comparación

## 1. Punto de partida: segmentación con K-Means

En la práctica anterior una imagen RGB se convirtió en una colección de píxeles. Cada píxel se representó como un punto con tres características:

```text
(rojo, verde, azul)
```

K-Means agrupó esos puntos por semejanza de color. Después se reconstruyó la imagen sustituyendo cada píxel por el color de su centroide.

También se dibujó una nube tridimensional RGB para observar los grupos creados.

## 2. ¿Qué hace K-Means?

K-Means es un algoritmo de aprendizaje no supervisado. Recibe datos sin clases conocidas y trata de formar `K` grupos.

Proceso básico:

1. seleccionar `K` centroides iniciales;
2. asignar cada punto al centroide más cercano;
3. recalcular cada centroide usando la media de su grupo;
4. repetir la asignación y actualización;
5. terminar cuando los centroides dejan de cambiar significativamente.

Resultado:

- centroide de cada grupo;
- etiqueta de clúster para cada dato.

Las etiquetas `0`, `1`, `2`, etc. no representan clases conocidas previamente. Son identificadores de los grupos descubiertos.

## 3. ¿Qué hace KNN?

KNN es un algoritmo de aprendizaje supervisado. Recibe ejemplos que ya tienen una etiqueta y utiliza los vecinos más cercanos para clasificar un dato nuevo.

Proceso básico:

1. recibir un punto nuevo;
2. calcular su distancia respecto a los ejemplos conocidos;
3. ordenar las distancias;
4. elegir los `K` vecinos más cercanos;
5. contar sus etiquetas;
6. asignar la etiqueta con mayor número de votos.

KNN no calcula centroides y normalmente no construye un modelo matemático durante una fase de entrenamiento. Conserva los ejemplos para consultarlos al predecir.

En el código de esta semana cada píxel también es un vector RGB, pero ahora existen muestras previamente etiquetadas:

```text
(10, 10, 10)    → oscuro
(115, 70, 40)   → café
(55, 130, 65)   → verde
(65, 105, 175)  → azul
(215, 205, 185) → claro
```

KNN compara cada píxel de la imagen con estas muestras y le asigna una clase conocida. El resultado es un mapa de categorías de color, no un conjunto de clústeres anónimos.

El programa también muestra una nube tridimensional RGB. Cada punto representa un píxel y se colorea según la clase predicha. Las muestras etiquetadas aparecen como marcadores `X` grandes. Esto permite comparar visualmente:

- los centroides descubiertos automáticamente por K-Means;
- los ejemplos etiquetados que orientan las decisiones de KNN.

## 4. Distancia euclidiana

Para dos puntos de dos dimensiones:

```text
A = (a1, a2)
B = (b1, b2)
```

La distancia es:

```text
d(A, B) = sqrt((a1 - b1)² + (a2 - b2)²)
```

Ejemplo:

```text
A = (2, 3)
B = (5, 7)

d = sqrt((2 - 5)² + (3 - 7)²)
d = sqrt(9 + 16)
d = 5
```

## 5. Comparación

| Característica | K-Means | KNN |
|---|---|---|
| Tipo de aprendizaje | No supervisado | Supervisado |
| ¿Existen etiquetas conocidas? | No | Sí |
| Significado de `K` | Número de clústeres | Número de vecinos |
| Operación central | Asignar al centroide más cercano | Votar entre vecinos cercanos |
| Resultado | Grupos descubiertos | Clase predicha |
| Almacenamiento | Centroides y asignaciones | Ejemplos de entrenamiento |
| Uso anterior o actual | Segmentación de una imagen | Clasificación supervisada de los píxeles de una imagen |

## 6. Importancia de la escala

Supón que un dato utiliza:

- peso entre 0 y 1000 gramos;
- color entre 0 y 10.

La diferencia de peso puede dominar la distancia aunque el color sea importante. Por ello es frecuente escalar o normalizar las variables antes de aplicar KNN o K-Means.

En el reto inicial se utilizan características con rangos semejantes para concentrarse primero en el algoritmo.

## 7. Elegir el valor de K en KNN

- `K = 1`: muy sensible al ejemplo más cercano y al ruido.
- `K` pequeño: decisiones locales y fronteras irregulares.
- `K` grande: decisiones más estables, pero puede ignorar grupos pequeños.
- `K` par: aumenta la posibilidad de empate cuando existen dos clases.

No existe un valor universal. Debe compararse mediante datos de validación.

## 8. Archivos de la semana

Las dos prácticas cargan por defecto:

```text
codigo/images/oso.jpg
```

La ruta se encuentra en la constante `RUTA_IMAGEN`. Puede cambiarse por `luna.jpg`, `lena.jpg` o `dos.jpg`.

Ejecuta K-Means:

```powershell
python codigo\kmeans_segmentacion_rgb.py
```

Después completa KNN:

```powershell
python codigo\knn_paso_a_paso.py
```

## 9. Reto KNN

Completa en `knn_paso_a_paso.py`:

1. la distancia euclidiana entre vectores RGB;
2. la selección de muestras vecinas;
3. la votación de clases de color;
4. la clasificación de los píxeles de la imagen;
5. la interpretación de la nube tridimensional RGB;
6. las pruebas con diferentes imágenes y valores de `k`.

## 10. Preguntas

1. ¿Por qué las etiquetas de K-Means no son clases verdaderas?
2. ¿Qué necesita KNN que K-Means no necesita?
3. ¿Qué sucede si se utiliza `k = 1`?
4. ¿Por qué conviene utilizar un número impar de vecinos con dos clases?
5. ¿Cómo puede afectar la escala de las características?
6. ¿Qué diferencia observas entre los colores descubiertos por K-Means y las clases definidas previamente para KNN?
