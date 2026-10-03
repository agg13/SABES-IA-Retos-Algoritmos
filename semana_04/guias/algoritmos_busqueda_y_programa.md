# Guía básica de algoritmos de búsqueda y del programa visual

## 1. El problema

El programa representa un mundo como una cuadrícula. Cada celda puede ser:

- libre;
- pared;
- posición inicial del robot;
- meta.

Un estado se representa mediante la posición `(fila, columna)`. El robot puede desplazarse arriba, derecha, abajo o izquierda, siempre que permanezca dentro de la cuadrícula y no intente atravesar una pared.

## 2. Conceptos principales

| Concepto | Significado en el programa |
|---|---|
| Estado | Una posición `(fila, columna)` |
| Estado inicial | Celda donde comienza el robot |
| Meta | Celda que debe alcanzar |
| Acción | Movimiento en una de cuatro direcciones |
| Frontera | Estados descubiertos que todavía no se procesan |
| Visitados | Estados que ya fueron procesados |
| Padre | Estado desde el cual se descubrió otro estado |
| Ruta | Secuencia reconstruida desde el inicio hasta la meta |
| Costo | Número de movimientos de la ruta |

## 3. BFS: búsqueda en anchura

BFS utiliza una cola FIFO: el primer elemento que entra es el primero que sale.

```text
insertar inicio en la cola
mientras la cola tenga estados:
    extraer el estado más antiguo
    si es la meta, reconstruir la ruta
    agregar sus vecinos no descubiertos
```

BFS explora por niveles. Cuando todos los movimientos cuestan lo mismo, encuentra una ruta con el menor número de movimientos.

En `busqueda_visual.py`, BFS utiliza `deque`:

```python
frontera = deque([inicio])
actual = frontera.popleft()
frontera.append(vecino)
```

## 4. DFS: búsqueda en profundidad

DFS utiliza una pila LIFO: el último elemento que entra es el primero que sale.

```text
insertar inicio en la pila
mientras la pila tenga estados:
    extraer el estado más reciente
    si es la meta, reconstruir la ruta
    agregar sus vecinos no descubiertos
```

DFS avanza por una rama antes de probar otras. Puede encontrar una solución con pocas expansiones, pero no garantiza la ruta más corta.

En el programa, una lista funciona como pila:

```python
frontera = [inicio]
actual = frontera.pop()
frontera.append(vecino)
```

El orden de los vecinos afecta considerablemente el recorrido de DFS.

## 5. A*: búsqueda informada

A* utiliza una cola de prioridad y evalúa cada estado mediante:

```text
f(n) = g(n) + h(n)
```

- `g(n)`: costo real desde el inicio;
- `h(n)`: estimación de lo que falta hasta la meta;
- `f(n)`: estimación del costo total.

El programa utiliza distancia Manhattan:

```text
h(n) = |fila - fila_meta| + |columna - columna_meta|
```

Esta heurística es adecuada porque no se permiten movimientos diagonales.

## 6. Cómo evita ciclos el programa

Una cuadrícula puede contener regiones cíclicas. Si el algoritmo olvida los estados anteriores, puede regresar continuamente a las mismas posiciones.

El programa conserva un conjunto de estados descubiertos o cerrados:

```python
if vecino not in descubiertos:
    descubiertos.add(vecino)
```

Cada posición se incorpora a la búsqueda de forma controlada. Esto garantiza que una cuadrícula finita no produzca una exploración infinita.

En un robot físico el problema es más complejo: para saber que regresó al mismo estado puede necesitar reconocer la intersección y su orientación.

## 7. Reconstrucción de la ruta

Cuando se descubre un estado se almacena su padre:

```python
padres[vecino] = actual
```

Al encontrar la meta, el programa recorre los padres en sentido inverso hasta llegar al inicio y después invierte la lista.

## 8. Uso de la ventana

Ejecuta:

```powershell
python busqueda_visual.py
```

Controles principales:

- **Pared/libre:** alterna una celda al hacer clic.
- **Colocar robot:** cambia la posición inicial.
- **Colocar meta:** cambia el objetivo.
- **+/- fila o columna:** cambia el tamaño del escenario.
- **Algoritmo:** selecciona BFS, DFS o A*.
- **Pausa:** modifica la velocidad de animación.
- **Iniciar búsqueda:** ejecuta y muestra las iteraciones.

Colores:

| Color | Significado |
|---|---|
| Negro | Pared |
| Azul claro | Visitado |
| Amarillo | Frontera |
| Naranja | Estado actual |
| Verde | Ruta final |
| Azul intenso | Inicio |
| Rojo | Meta |
| Morado | Robot recorriendo la solución |

## 9. Actividad

1. Ejecuta los tres algoritmos con el escenario inicial.
2. Registra el costo y los nodos expandidos.
3. Agrega paredes para crear una ruta larga y otra corta.
4. Construye un ciclo alrededor de una pared interior.
5. Cambia la posición inicial y la meta.
6. Predice el algoritmo que expandirá menos estados.
7. Ejecuta y compara con tu predicción.

## 10. Preguntas

1. ¿Por qué DFS puede producir una ruta más larga que BFS?
2. ¿Qué información adicional utiliza A*?
3. ¿Cuál es la diferencia entre un estado visitado y uno que permanece en la frontera?
4. ¿Qué ocurriría si se eliminara el conjunto de estados descubiertos?
5. ¿Por qué un robot físico necesita algo más que una coordenada para reconocer ciertos estados?

