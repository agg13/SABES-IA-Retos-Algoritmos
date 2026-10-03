"""K-Means aplicado a la segmentación de una imagen por color.

La ruta puede cambiarse temporalmente en RUTA_IMAGEN. Las imágenes disponibles
se encuentran en la carpeta ``images`` junto a este programa.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


CARPETA_CODIGO = Path(__file__).resolve().parent
RUTA_IMAGEN = CARPETA_CODIGO / "images" / "oso.jpg"
NUMERO_CLUSTERS = 5
MAXIMO_PIXELES_ENTRENAMIENTO = 50_000
SEMILLA = 7


def cargar_imagen(ruta: Path) -> np.ndarray:
    """Carga una imagen JPG y garantiza una matriz RGB uint8."""
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


def segmentar_imagen(
    imagen: np.ndarray,
    numero_clusters: int,
    maximo_entrenamiento: int = MAXIMO_PIXELES_ENTRENAMIENTO,
):
    """Ajusta K-Means con píxeles RGB y reconstruye la imagen segmentada."""
    alto, ancho, canales = imagen.shape
    pixeles = imagen.reshape(-1, canales).astype(float)

    # Para que el ejercicio sea ágil, el modelo puede ajustarse con una muestra
    # de píxeles y luego predecir la etiqueta de todos los píxeles de la imagen.
    rng = np.random.default_rng(SEMILLA)
    if len(pixeles) > maximo_entrenamiento:
        indices = rng.choice(
            len(pixeles), size=maximo_entrenamiento, replace=False
        )
        pixeles_entrenamiento = pixeles[indices]
    else:
        pixeles_entrenamiento = pixeles

    modelo = KMeans(
        n_clusters=numero_clusters,
        n_init=10,
        random_state=SEMILLA,
    )
    modelo.fit(pixeles_entrenamiento)

    etiquetas = modelo.predict(pixeles)
    centroides = modelo.cluster_centers_
    segmentada = centroides[etiquetas].reshape(alto, ancho, canales)
    segmentada = np.clip(segmentada, 0, 255).astype(np.uint8)
    return segmentada, pixeles, etiquetas, centroides


def graficar_imagenes(
    original: np.ndarray, segmentada: np.ndarray, nombre: str
) -> None:
    figura, ejes = plt.subplots(1, 2, figsize=(12, 5))
    ejes[0].imshow(original)
    ejes[0].set_title(f"Imagen original: {nombre}")
    ejes[0].axis("off")

    ejes[1].imshow(segmentada)
    ejes[1].set_title(f"Segmentación K-Means, K={NUMERO_CLUSTERS}")
    ejes[1].axis("off")
    figura.tight_layout()


def graficar_nube_rgb(
    pixeles: np.ndarray,
    etiquetas: np.ndarray,
    centroides: np.ndarray,
    cantidad_muestra: int = 4_000,
) -> None:
    """Muestra los grupos creados dentro del espacio tridimensional RGB."""
    rng = np.random.default_rng(SEMILLA)
    cantidad = min(cantidad_muestra, len(pixeles))
    indices = rng.choice(len(pixeles), size=cantidad, replace=False)
    muestra = pixeles[indices]
    colores = centroides[etiquetas[indices]] / 255.0

    figura = plt.figure(figsize=(10, 7))
    eje = figura.add_subplot(111, projection="3d")
    eje.scatter(
        muestra[:, 0],
        muestra[:, 1],
        muestra[:, 2],
        c=colores,
        s=8,
        alpha=0.5,
    )
    eje.scatter(
        centroides[:, 0],
        centroides[:, 1],
        centroides[:, 2],
        c="black",
        marker="X",
        s=190,
        label="Centroides",
    )
    eje.set_xlabel("Rojo")
    eje.set_ylabel("Verde")
    eje.set_zlabel("Azul")
    eje.set_title("Clústeres de píxeles en el espacio RGB")
    eje.legend()
    figura.tight_layout()


def main() -> None:
    imagen = cargar_imagen(RUTA_IMAGEN)
    segmentada, pixeles, etiquetas, centroides = segmentar_imagen(
        imagen, NUMERO_CLUSTERS
    )

    print("Imagen:", RUTA_IMAGEN)
    print("Forma:", imagen.shape)
    print("Cantidad de píxeles:", len(pixeles))
    print("Centroides RGB encontrados:")
    print(np.round(centroides, 1))

    graficar_imagenes(imagen, segmentada, RUTA_IMAGEN.name)
    graficar_nube_rgb(pixeles, etiquetas, centroides)
    plt.show()


if __name__ == "__main__":
    main()

