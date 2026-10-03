"""Reto guiado: KNN para clasificar los píxeles RGB de una imagen.

Completa las funciones marcadas con TODO. Las muestras etiquetadas representan
ejemplos de colores conocidos. KNN asignará una clase a cada píxel de la imagen.
"""

from collections import Counter
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np


Vector = Tuple[float, ...]
Ejemplo = Tuple[Vector, str]

CARPETA_CODIGO = Path(__file__).resolve().parent
RUTA_IMAGEN = CARPETA_CODIGO / "images" / "oso.jpg"
K_VECINOS = 3
PASO_MUESTREO = 3


# Ejemplos RGB previamente etiquetados. A diferencia de K-Means, KNN sí recibe
# el significado de cada ejemplo antes de clasificar los datos nuevos.
MUESTRAS_RGB: List[Ejemplo] = [
    ((10, 10, 10), "oscuro"),
    ((35, 30, 28), "oscuro"),
    ((55, 50, 45), "oscuro"),
    ((75, 45, 25), "cafe"),
    ((115, 70, 40), "cafe"),
    ((155, 105, 65), "cafe"),
    ((25, 85, 35), "verde"),
    ((55, 130, 65), "verde"),
    ((95, 165, 95), "verde"),
    ((30, 65, 125), "azul"),
    ((65, 105, 175), "azul"),
    ((105, 155, 215), "azul"),
    ((175, 165, 145), "claro"),
    ((215, 205, 185), "claro"),
    ((245, 240, 225), "claro"),
]


COLORES_SALIDA: Dict[str, Tuple[int, int, int]] = {
    "oscuro": (25, 25, 25),
    "cafe": (145, 85, 45),
    "verde": (45, 170, 75),
    "azul": (55, 105, 220),
    "claro": (235, 225, 205),
}


def cargar_imagen(ruta: Path) -> np.ndarray:
    """Carga una imagen JPG como una matriz RGB uint8."""
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta}\n"
            "Revisa RUTA_IMAGEN y la carpeta images."
        )

    imagen = plt.imread(ruta)
    if imagen.ndim == 2:
        imagen = np.stack([imagen, imagen, imagen], axis=-1)
    if imagen.shape[2] > 3:
        imagen = imagen[:, :, :3]
    if np.issubdtype(imagen.dtype, np.floating):
        imagen = np.clip(imagen * 255, 0, 255)
    return imagen.astype(np.uint8)


def distancia_euclidiana(a: Vector, b: Vector) -> float:
    """Calcula la distancia entre vectores de la misma dimensión."""
    if len(a) != len(b):
        raise ValueError("Los vectores deben tener la misma dimensión")

    # TODO 1:
    # Calcula sqrt(sum((ai-bi)^2)) para todas las características.
    raise NotImplementedError("Completa distancia_euclidiana")


def obtener_vecinos(
    datos: Sequence[Ejemplo], nuevo: Vector, k: int
) -> List[Tuple[float, str, Vector]]:
    """Devuelve los k ejemplos más cercanos ordenados por distancia."""
    if k <= 0:
        raise ValueError("k debe ser mayor que cero")
    if k > len(datos):
        raise ValueError("k no puede ser mayor que la cantidad de ejemplos")

    # TODO 2:
    # 1. Calcula la distancia desde 'nuevo' hasta cada vector RGB.
    # 2. Guarda tuplas (distancia, etiqueta, vector).
    # 3. Ordena por distancia.
    # 4. Devuelve solamente los primeros k elementos.
    raise NotImplementedError("Completa obtener_vecinos")


def predecir_knn(datos: Sequence[Ejemplo], nuevo: Vector, k: int) -> str:
    """Predice la etiqueta mayoritaria entre los vecinos."""
    vecinos = obtener_vecinos(datos, nuevo, k)

    # TODO 3:
    # Cuenta las etiquetas y devuelve la más frecuente.
    # Puedes utilizar Counter.
    raise NotImplementedError("Completa predecir_knn")


def clasificar_imagen(
    imagen: np.ndarray,
    datos: Sequence[Ejemplo],
    k: int,
    paso: int = PASO_MUESTREO,
):
    """Reduce la imagen y clasifica cada píxel mediante la implementación KNN."""
    if paso <= 0:
        raise ValueError("El paso de muestreo debe ser mayor que cero")

    reducida = imagen[::paso, ::paso, :3]
    clasificada = np.zeros_like(reducida)
    etiquetas = np.empty(reducida.shape[:2], dtype=object)
    conteos: Counter[str] = Counter()

    for fila in range(reducida.shape[0]):
        for columna in range(reducida.shape[1]):
            pixel = tuple(float(valor) for valor in reducida[fila, columna])
            etiqueta = predecir_knn(datos, pixel, k)
            clasificada[fila, columna] = COLORES_SALIDA[etiqueta]
            etiquetas[fila, columna] = etiqueta
            conteos[etiqueta] += 1

    return reducida, clasificada, etiquetas, conteos


def graficar(
    original: np.ndarray,
    reducida: np.ndarray,
    clasificada: np.ndarray,
    nombre: str,
) -> None:
    figura, ejes = plt.subplots(1, 3, figsize=(15, 5))
    ejes[0].imshow(original)
    ejes[0].set_title(f"Original: {nombre}")
    ejes[1].imshow(reducida)
    ejes[1].set_title(f"Muestra cada {PASO_MUESTREO} píxeles")
    ejes[2].imshow(clasificada)
    ejes[2].set_title(f"Clases KNN, K={K_VECINOS}")
    for eje in ejes:
        eje.axis("off")
    figura.tight_layout()


def graficar_nube_rgb(
    pixeles: np.ndarray,
    etiquetas: np.ndarray,
    datos: Sequence[Ejemplo],
    cantidad_muestra: int = 4_000,
) -> None:
    """Dibuja los píxeles RGB coloreados según la clase predicha por KNN."""
    pixeles_planos = pixeles.reshape(-1, 3).astype(float)
    etiquetas_planas = etiquetas.reshape(-1)

    rng = np.random.default_rng(7)
    cantidad = min(cantidad_muestra, len(pixeles_planos))
    indices = rng.choice(len(pixeles_planos), size=cantidad, replace=False)
    muestra = pixeles_planos[indices]
    clases_muestra = etiquetas_planas[indices]
    colores = np.array(
        [COLORES_SALIDA[clase] for clase in clases_muestra], dtype=float
    ) / 255.0

    figura = plt.figure(figsize=(10, 7))
    eje = figura.add_subplot(111, projection="3d")
    eje.scatter(
        muestra[:, 0],
        muestra[:, 1],
        muestra[:, 2],
        c=colores,
        s=9,
        alpha=0.5,
    )

    # Las X muestran los ejemplos etiquetados que orientan las decisiones.
    clases = sorted({etiqueta for _, etiqueta in datos})
    for clase in clases:
        vectores = np.array(
            [vector for vector, etiqueta in datos if etiqueta == clase],
            dtype=float,
        )
        color = np.array(COLORES_SALIDA[clase], dtype=float) / 255.0
        eje.scatter(
            vectores[:, 0],
            vectores[:, 1],
            vectores[:, 2],
            color=[color],
            edgecolor="black",
            marker="X",
            s=150,
            label=f"muestras: {clase}",
        )

    eje.set_xlabel("Rojo")
    eje.set_ylabel("Verde")
    eje.set_zlabel("Azul")
    eje.set_title("Clases KNN de los píxeles en el espacio RGB")
    eje.legend(loc="upper left", fontsize=8)
    figura.tight_layout()


def main() -> None:
    imagen = cargar_imagen(RUTA_IMAGEN)
    print("Imagen cargada:", RUTA_IMAGEN)
    print("Forma:", imagen.shape)
    print("Muestras RGB etiquetadas:", len(MUESTRAS_RGB))

    try:
        reducida, clasificada, etiquetas, conteos = clasificar_imagen(
            imagen, MUESTRAS_RGB, K_VECINOS
        )
    except NotImplementedError as error:
        print("\nEl reto todavía no está completo:", error)
        print("Busca y resuelve TODO 1, TODO 2 y TODO 3.")
        plt.imshow(imagen)
        plt.title(f"Imagen cargada correctamente: {RUTA_IMAGEN.name}")
        plt.axis("off")
        plt.show()
        return

    print("Cantidad de píxeles por clase:")
    for etiqueta, cantidad in conteos.most_common():
        print(f"  {etiqueta:<8}: {cantidad}")

    graficar(imagen, reducida, clasificada, RUTA_IMAGEN.name)
    graficar_nube_rgb(reducida, etiquetas, MUESTRAS_RGB)
    plt.show()

    # TODO 4:
    # 1. Cambia RUTA_IMAGEN por luna.jpg, lena.jpg o dos.jpg.
    # 2. Prueba k=1 y k=5.
    # 3. Agrega o modifica muestras RGB y explica el cambio obtenido.


if __name__ == "__main__":
    main()
