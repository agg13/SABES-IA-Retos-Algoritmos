# Cálculo manual de Naive Bayes: `premio hoy`

Esta guía desarrolla exactamente el ejemplo que utiliza el programa. El objetivo es identificar de dónde sale cada número antes de ejecutar el código.

## 1. Datos de entrenamiento

El modelo recibe ocho mensajes cuya clase ya conocemos:

| Número | Mensaje | Clase |
|---:|---|---|
| 1 | `gana un premio ahora` | spam |
| 2 | `reclama tu premio` | spam |
| 3 | `oferta exclusiva hoy` | spam |
| 4 | `recibe dinero rapido` | spam |
| 5 | `nos vemos mañana` | legítimo |
| 6 | `entrega la tarea mañana` | legítimo |
| 7 | `reunion de clase hoy` | legítimo |
| 8 | `puedes traer el material` | legítimo |

Queremos clasificar un mensaje nuevo:

```text
premio hoy
```

## 2. Fórmula de Bayes

Para una clase `C` y un mensaje formado por las palabras `w1` y `w2`:

```text
P(C | w1, w2) = P(w1, w2 | C) × P(C) / P(w1, w2)
```

Naive Bayes supone que las palabras son condicionalmente independientes cuando conocemos la clase:

```text
P(w1, w2 | C) ≈ P(w1 | C) × P(w2 | C)
```

Por lo tanto:

```text
P(C | w1, w2) ∝ P(C) × P(w1 | C) × P(w2 | C)
```

El símbolo `∝` significa “proporcional a”. Primero calculamos un puntaje para cada clase. Al final dividimos cada puntaje entre la suma de todos los puntajes para obtener probabilidades que sumen 1.

## 3. Probabilidades previas

Hay cuatro mensajes spam y cuatro legítimos entre ocho mensajes:

```text
P(spam) = mensajes spam / mensajes totales
P(spam) = 4 / 8 = 0.50

P(legítimo) = mensajes legítimos / mensajes totales
P(legítimo) = 4 / 8 = 0.50
```

Estas probabilidades se llaman **previas** porque se calculan antes de observar las palabras del mensaje nuevo.

## 4. Conteo de palabras por clase

### Palabras de los mensajes spam

```text
gana un premio ahora          → 4 palabras
reclama tu premio             → 3 palabras
oferta exclusiva hoy          → 3 palabras
recibe dinero rapido          → 3 palabras
```

Total:

```text
4 + 3 + 3 + 3 = 13 palabras en la clase spam
```

La palabra `premio` aparece dos veces en spam y `hoy` aparece una vez:

```text
conteo(premio, spam) = 2
conteo(hoy, spam) = 1
```

### Palabras de los mensajes legítimos

```text
nos vemos mañana              → 3 palabras
entrega la tarea mañana       → 4 palabras
reunion de clase hoy          → 4 palabras
puedes traer el material      → 4 palabras
```

Total:

```text
3 + 4 + 4 + 4 = 15 palabras en la clase legítimo
```

La palabra `premio` no aparece en mensajes legítimos y `hoy` aparece una vez:

```text
conteo(premio, legítimo) = 0
conteo(hoy, legítimo) = 1
```

## 5. Tamaño del vocabulario

El vocabulario contiene todas las palabras diferentes de los ocho mensajes:

```text
ahora, clase, de, dinero, el, entrega, exclusiva, gana, hoy,
la, mañana, material, nos, oferta, premio, puedes, rapido,
recibe, reclama, reunion, tarea, traer, tu, un, vemos
```

Hay 25 palabras diferentes:

```text
V = 25
```

Otra forma de comprobarlo:

- los mensajes spam contienen 12 palabras diferentes;
- los mensajes legítimos contienen 14 palabras diferentes;
- `hoy` aparece en las dos clases, por lo que no debe contarse dos veces;
- `12 + 14 - 1 = 25`.

## 6. Suavizado de Laplace

Usamos la fórmula:

```text
P(palabra | clase) = (conteo de la palabra en la clase + 1)
                     / (total de palabras de la clase + V)
```

El `+1` evita obtener probabilidad cero cuando una palabra no apareció en una clase. Si multiplicáramos por cero, se perdería toda la evidencia aportada por las demás palabras.

### Probabilidades dentro de spam

El denominador para spam es:

```text
13 palabras de spam + 25 palabras del vocabulario = 38
```

Entonces:

```text
P(premio | spam) = (2 + 1) / 38 = 3/38 = 0.078947
P(hoy | spam) = (1 + 1) / 38 = 2/38 = 0.052632
```

### Probabilidades dentro de legítimo

El denominador para legítimo es:

```text
15 palabras legítimas + 25 palabras del vocabulario = 40
```

Entonces:

```text
P(premio | legítimo) = (0 + 1) / 40 = 1/40 = 0.025000
P(hoy | legítimo) = (1 + 1) / 40 = 2/40 = 0.050000
```

## 7. Puntajes sin normalizar

### Puntaje de spam

```text
puntaje(spam)
= P(spam) × P(premio | spam) × P(hoy | spam)
= 0.50 × 3/38 × 2/38
= 3/1444
= 0.00207756
```

### Puntaje de legítimo

```text
puntaje(legítimo)
= P(legítimo) × P(premio | legítimo) × P(hoy | legítimo)
= 0.50 × 1/40 × 2/40
= 1/1600
= 0.00062500
```

El puntaje de spam es mayor, pero todavía no son probabilidades que sumen 1.

## 8. Normalización

Primero sumamos los dos puntajes:

```text
total = 0.00207756 + 0.00062500
total = 0.00270256
```

Después dividimos cada puntaje entre el total:

```text
P(spam | "premio hoy")
= 0.00207756 / 0.00270256
= 0.7687
= 76.87 %

P(legítimo | "premio hoy")
= 0.00062500 / 0.00270256
= 0.2313
= 23.13 %
```

La predicción final es:

```text
SPAM
```

## 9. Relación con el código

El programa realiza los mismos pasos:

1. `entrenar_naive_bayes` cuenta documentos, palabras y vocabulario;
2. `probabilidad_palabra` aplica el suavizado de Laplace;
3. `predecir` suma logaritmos en lugar de multiplicar números pequeños;
4. `mostrar_calculo_pizarra` imprime los conteos y resultados del ejemplo.

La suma de logaritmos representa la misma operación que la multiplicación:

```text
log(a × b × c) = log(a) + log(b) + log(c)
```

El uso de logaritmos evita problemas numéricos cuando un mensaje contiene muchas palabras.
