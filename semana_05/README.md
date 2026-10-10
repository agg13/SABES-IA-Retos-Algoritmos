# Semana 5: Naive Bayes y clasificación de mensajes

## Propósito

Construir paso a paso un clasificador Naive Bayes multinomial que determine si un mensaje parece `spam` o `legitimo`.

La práctica usa primero los ocho mensajes de la presentación para reproducir el cálculo de pizarra. Después aplica el mismo procedimiento al archivo `datos/mensajes_spam.csv` y muestra:

- distribución de mensajes por clase;
- matriz de confusión;
- probabilidad estimada para un mensaje nuevo;
- palabras que aportan evidencia a cada clase.

> El dataset fue creado para fines didácticos. Es pequeño y sintético; no representa la variedad completa de mensajes reales.

## Archivos

```text
semana_05/
├── README.md
├── codigo/
│   └── naive_bayes_spam.py
├── datos/
│   └── mensajes_spam.csv
├── guia_calculo_manual_naive_bayes.md
└── presentacion/
    ├── naive_bayes_spam.pptx
    └── naive_bayes_spam_detallado_v2.pptx
```

## Actividad

Completa los tres bloques `TODO` del archivo `codigo/naive_bayes_spam.py`:

1. construir los conteos del modelo;
2. calcular `P(palabra | clase)` con suavizado de Laplace;
3. calcular los puntajes logarítmicos y realizar la predicción.

La fórmula utilizada para cada palabra es:

```text
P(palabra | clase) = (conteo + 1) / (total de palabras de la clase + tamaño del vocabulario)
```

Antes de programar, revisa [`guia_calculo_manual_naive_bayes.md`](guia_calculo_manual_naive_bayes.md). La guía explica de dónde salen los 13 y 15 totales de palabras, las 25 palabras del vocabulario, los cuatro conteos utilizados y la normalización final.

## Ejecución

Desde la carpeta `semana_05`:

```powershell
python codigo\naive_bayes_spam.py
```

El programa imprime los cálculos y abre una ventana con cuatro gráficas.

Para probar otro mensaje:

```powershell
python codigo\naive_bayes_spam.py --mensaje "entrega la tarea mañana"
```

Para ejecutar únicamente el caso de la presentación:

```powershell
python codigo\naive_bayes_spam.py --solo-pizarra
```

## Evidencias sugeridas

1. Código con los tres bloques completados.
2. Captura de la visualización.
3. Predicción de cinco mensajes propios.
4. Explicación de un acierto y un error del modelo.
5. Respuesta breve: ¿qué supuesto “ingenuo” realiza Naive Bayes sobre las palabras?
