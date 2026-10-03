# Inteligencia Artificial: materiales de clase y proyectos

Bienvenido al repositorio de trabajo de la materia de Inteligencia Artificial.

Aquí encontrarás los programas base, retos, ejemplos, manuales y recursos que utilizaremos durante el curso. Los materiales están organizados por semana y por proyecto para que puedas descargar únicamente lo que necesites y conservar un historial de tus avances.

## ¿Cómo utilizar este repositorio?

1. Consulta primero [`00_instalacion/instalacion_python_y_paquetes.md`](00_instalacion/instalacion_python_y_paquetes.md).
2. Descarga o clona el repositorio en una carpeta fácil de localizar.
3. Crea y activa un entorno virtual de Python.
4. Instala los paquetes indicados en `requirements.txt`.
5. Entra en la carpeta de la semana correspondiente.
6. Lee su `README.md` antes de ejecutar o modificar el código.
7. Conserva una copia de tu trabajo y registra los cambios realizados.

## Estructura inicial

```text
.
├── README.md
├── requirements.txt
├── 00_instalacion/
│   └── instalacion_python_y_paquetes.md
└── semana_04/
    ├── README.md
    ├── codigo/
    │   ├── busqueda_visual.py
    │   ├── kmeans_segmentacion_rgb.py
    │   ├── knn_paso_a_paso.py
    │   └── images/
    │       ├── dos.jpg
    │       ├── lena.jpg
    │       ├── luna.jpg
    │       └── oso.jpg
    └── guias/
        ├── algoritmos_busqueda_y_programa.md
        └── kmeans_knn_comparativa.md
```

La estructura crecerá conforme avancen las semanas. Más adelante aparecerán también los proyectos del robot de laberinto y del SmartBot, así como las actividades de Arduino, lógica difusa, redes neuronales y YOLO.

## Tipos de materiales

- **Ejemplo completo:** programa que puede ejecutarse y estudiarse directamente.
- **Código base:** programa funcional o parcialmente funcional preparado para modificarse en clase.
- **Reto:** archivo con secciones marcadas como `TODO` que deberás completar.
- **Guía:** explicación conceptual y procedimiento de trabajo.
- **Manual:** instrucciones de instalación, conexión o solución de problemas.

## Reglas de trabajo

- Trabaja únicamente sobre una copia propia del código.
- No borres los comentarios `TODO` hasta completar y probar esa sección.
- Ejecuta el programa después de cada cambio pequeño.
- Lee los mensajes de error completos antes de solicitar ayuda.
- No conectes motores o ventiladores directamente a un pin de Arduino; utiliza la etapa de potencia indicada en la guía correspondiente.
- No publiques contraseñas, tokens, datos personales ni credenciales dentro del repositorio.
- Documenta las fuentes externas que utilices.

## Forma de entrega

Cada actividad indicará sus evidencias. Normalmente se solicitarán algunos de los siguientes elementos:

- código fuente modificado;
- capturas o registros de ejecución;
- respuestas a preguntas de análisis;
- explicación breve de los cambios;
- pruebas con entradas diferentes;
- conclusiones y limitaciones observadas.

## Semana 4

La semana 4 conecta la práctica anterior de K-Means con KNN y utiliza un programa visual para introducir los algoritmos de búsqueda.

Comienza en [`semana_04/README.md`](semana_04/README.md).

## Ayuda ante problemas

Antes de pedir ayuda, registra:

1. sistema operativo;
2. versión de Python;
3. comando ejecutado;
4. mensaje de error completo;
5. archivo y línea indicados;
6. cambio realizado antes de que apareciera el problema.

Esto permite reproducir y resolver el error con mayor rapidez.
