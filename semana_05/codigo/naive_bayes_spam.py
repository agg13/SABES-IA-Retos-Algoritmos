"""Actividad guiada: clasificador de mensajes con Naive Bayes multinomial.

Completa los tres bloques TODO. El resto del programa carga los datos,
reproduce el ejemplo de pizarra, evalúa el modelo y genera una visualización.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import re
from collections import Counter
from pathlib import Path


RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos" / "mensajes_spam.csv"
CLASES_GRAFICA = ["legitimo", "spam"]

EJEMPLO_PIZARRA = [
    ("gana un premio ahora", "spam"),
    ("reclama tu premio", "spam"),
    ("oferta exclusiva hoy", "spam"),
    ("recibe dinero rapido", "spam"),
    ("nos vemos mañana", "legitimo"),
    ("entrega la tarea mañana", "legitimo"),
    ("reunion de clase hoy", "legitimo"),
    ("puedes traer el material", "legitimo"),
]
MENSAJE_PIZARRA = "premio hoy"


def tokenizar(texto: str) -> list[str]:
    """Convierte un mensaje en una lista sencilla de palabras."""
    return re.findall(r"[a-záéíóúüñ0-9]+", texto.casefold())


def cargar_datos(ruta: Path) -> list[tuple[str, str]]:
    """Carga pares (mensaje, etiqueta) desde un archivo CSV UTF-8."""
    datos: list[tuple[str, str]] = []
    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos.append((fila["mensaje"].strip(), fila["etiqueta"].strip()))
    return datos


def entrenar_naive_bayes(datos: list[tuple[str, str]]) -> dict:
    """Cuenta documentos, palabras y vocabulario para cada clase."""
    # TODO 1:
    # 1. Cuenta cuántos documentos pertenecen a cada clase.
    # 2. Cuenta las apariciones de cada palabra dentro de cada clase.
    # 3. Guarda el total de palabras por clase y el vocabulario completo.
    raise NotImplementedError("Completa TODO 1: entrenar_naive_bayes")


def probabilidad_palabra(palabra: str, clase: str, modelo: dict) -> float:
    """Calcula P(palabra | clase) con suavizado de Laplace."""
    # TODO 2: aplica (conteo + 1) / (total_palabras_clase + tamaño_vocabulario).
    raise NotImplementedError("Completa TODO 2: probabilidad_palabra")


def predecir(mensaje: str, modelo: dict) -> tuple[str, dict, dict]:
    """Calcula los puntajes logarítmicos y las probabilidades normalizadas."""
    # TODO 3:
    # 1. Inicia cada puntaje con log(P(clase)).
    # 2. Suma log(P(palabra | clase)) para cada palabra conocida.
    # 3. Convierte los puntajes en probabilidades y selecciona la mayor.
    raise NotImplementedError("Completa TODO 3: predecir")


def dividir_estratificado(
    datos: list[tuple[str, str]], proporcion_prueba: float = 0.25, semilla: int = 7
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Separa entrenamiento y prueba conservando ejemplos de cada clase."""
    generador = random.Random(semilla)
    por_clase: dict[str, list[tuple[str, str]]] = {}
    for ejemplo in datos:
        por_clase.setdefault(ejemplo[1], []).append(ejemplo)

    entrenamiento: list[tuple[str, str]] = []
    prueba: list[tuple[str, str]] = []
    for ejemplos in por_clase.values():
        generador.shuffle(ejemplos)
        cantidad_prueba = max(1, round(len(ejemplos) * proporcion_prueba))
        prueba.extend(ejemplos[:cantidad_prueba])
        entrenamiento.extend(ejemplos[cantidad_prueba:])

    generador.shuffle(entrenamiento)
    generador.shuffle(prueba)
    return entrenamiento, prueba


def evaluar(modelo: dict, prueba: list[tuple[str, str]]) -> tuple[float, list, list]:
    reales: list[str] = []
    predichas: list[str] = []
    for mensaje, clase_real in prueba:
        clase_predicha, _, _ = predecir(mensaje, modelo)
        reales.append(clase_real)
        predichas.append(clase_predicha)
    aciertos = sum(real == predicha for real, predicha in zip(reales, predichas))
    return aciertos / len(prueba), reales, predichas


def construir_matriz_confusion(reales: list[str], predichas: list[str]) -> list[list[int]]:
    matriz = [[0 for _ in CLASES_GRAFICA] for _ in CLASES_GRAFICA]
    indice = {clase: posicion for posicion, clase in enumerate(CLASES_GRAFICA)}
    for real, predicha in zip(reales, predichas):
        matriz[indice[real]][indice[predicha]] += 1
    return matriz


def palabras_indicativas(modelo: dict, cantidad: int = 6) -> tuple[list, list]:
    """Obtiene palabras que favorecen más a cada clase."""
    diferencias = []
    for palabra in modelo["vocabulario"]:
        diferencia = math.log(probabilidad_palabra(palabra, "spam", modelo)) - math.log(
            probabilidad_palabra(palabra, "legitimo", modelo)
        )
        diferencias.append((palabra, diferencia))
    diferencias.sort(key=lambda elemento: elemento[1])
    return diferencias[:cantidad], diferencias[-cantidad:]


def mostrar_calculo_pizarra(modelo: dict, probabilidades: dict, detalles: dict) -> None:
    print("\n=== EJEMPLO DE PIZARRA ===")
    print(f'Mensaje nuevo: "{MENSAJE_PIZARRA}"')
    print(f"Documentos totales: {modelo['total_documentos']}")
    print(f"Palabras diferentes en el vocabulario: {len(modelo['vocabulario'])}")
    print("Vocabulario:", ", ".join(sorted(modelo["vocabulario"])))

    puntajes_sin_normalizar = {}
    for clase in CLASES_GRAFICA[::-1]:
        documentos = modelo["documentos_por_clase"][clase]
        total = modelo["total_documentos"]
        total_palabras = modelo["total_palabras_por_clase"][clase]
        print(f"\nClase {clase.upper()}")
        print(f"Documentos de la clase: {documentos}")
        print(f"Total de palabras de la clase: {total_palabras}")
        print(f"P({clase}) = {documentos}/{total} = {documentos / total:.3f}")
        for palabra in tokenizar(MENSAJE_PIZARRA):
            conteo = modelo["palabras_por_clase"][clase][palabra]
            denominador = total_palabras + len(modelo["vocabulario"])
            print(
                f"P({palabra}|{clase}) = ({conteo}+1)/{denominador} "
                f"= {probabilidad_palabra(palabra, clase, modelo):.5f}"
            )
        puntaje = math.exp(detalles[clase]["puntaje_log"])
        puntajes_sin_normalizar[clase] = puntaje
        print(f"Puntaje sin normalizar: {puntaje:.8f}")
        print(f"Puntaje logarítmico usado por el programa: {detalles[clase]['puntaje_log']:.4f}")

    total_puntajes = sum(puntajes_sin_normalizar.values())
    print("\nNORMALIZACIÓN")
    print(
        "Total de puntajes = "
        f"{puntajes_sin_normalizar['spam']:.8f} + "
        f"{puntajes_sin_normalizar['legitimo']:.8f} = {total_puntajes:.8f}"
    )
    for clase in CLASES_GRAFICA[::-1]:
        print(
            f"P({clase}|mensaje) = {puntajes_sin_normalizar[clase]:.8f} / "
            f"{total_puntajes:.8f} = {probabilidades[clase]:.2%}"
        )


def graficar_resultados(
    datos: list[tuple[str, str]],
    matriz: list[list[int]],
    mensaje: str,
    probabilidades: dict,
    modelo: dict,
    exactitud: float,
    mostrar: bool,
    guardar: Path | None,
) -> None:
    if not mostrar:
        import matplotlib

        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    conteos = Counter(etiqueta for _, etiqueta in datos)
    legitimas, spam = palabras_indicativas(modelo)
    palabras = [p for p, _ in legitimas] + [p for p, _ in spam]
    valores = [v for _, v in legitimas] + [v for _, v in spam]
    colores = ["#287271" if v < 0 else "#d1495b" for v in valores]

    figura, ejes = plt.subplots(2, 2, figsize=(12, 8))
    figura.suptitle("Naive Bayes: clasificación de mensajes", fontsize=16, fontweight="bold")

    ejes[0, 0].bar(
        CLASES_GRAFICA,
        [conteos[clase] for clase in CLASES_GRAFICA],
        color=["#287271", "#d1495b"],
    )
    ejes[0, 0].set_title("Mensajes disponibles por clase")
    ejes[0, 0].set_ylabel("Cantidad")

    ejes[0, 1].imshow(matriz, cmap="Blues")
    ejes[0, 1].set_title(f"Matriz de confusión · exactitud {exactitud:.1%}")
    ejes[0, 1].set_xticks(range(2), CLASES_GRAFICA)
    ejes[0, 1].set_yticks(range(2), CLASES_GRAFICA)
    ejes[0, 1].set_xlabel("Predicción")
    ejes[0, 1].set_ylabel("Clase real")
    for fila in range(2):
        for columna in range(2):
            ejes[0, 1].text(columna, fila, matriz[fila][columna], ha="center", va="center", fontsize=14)

    clases = list(probabilidades)
    ejes[1, 0].bar(clases, [probabilidades[c] for c in clases], color=["#287271", "#d1495b"])
    ejes[1, 0].set_ylim(0, 1)
    ejes[1, 0].set_title(f'Predicción para: "{mensaje}"')
    ejes[1, 0].set_ylabel("Probabilidad")

    ejes[1, 1].barh(palabras, valores, color=colores)
    ejes[1, 1].axvline(0, color="#333333", linewidth=1)
    ejes[1, 1].set_title("Palabras que favorecen cada clase")
    ejes[1, 1].set_xlabel("Legítimo ← evidencia → Spam")

    figura.tight_layout(rect=(0, 0, 1, 0.95))
    if guardar:
        guardar.parent.mkdir(parents=True, exist_ok=True)
        figura.savefig(guardar, dpi=160, bbox_inches="tight")
        print(f"Gráfica guardada en: {guardar}")
    if mostrar:
        plt.show()
    else:
        plt.close(figura)


def crear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clasificador de spam con Naive Bayes")
    parser.add_argument("--mensaje", default="reclama tu premio exclusivo hoy")
    parser.add_argument("--solo-pizarra", action="store_true")
    parser.add_argument("--sin-ventana", action="store_true")
    parser.add_argument("--guardar", type=Path)
    return parser.parse_args()


def main() -> None:
    argumentos = crear_argumentos()
    try:
        modelo_pizarra = entrenar_naive_bayes(EJEMPLO_PIZARRA)
        prediccion, probabilidades, detalles = predecir(MENSAJE_PIZARRA, modelo_pizarra)
        mostrar_calculo_pizarra(modelo_pizarra, probabilidades, detalles)
        print(f"Predicción del ejemplo: {prediccion.upper()}")

        if argumentos.solo_pizarra:
            return

        datos = cargar_datos(RUTA_DATOS)
        entrenamiento, prueba = dividir_estratificado(datos)
        modelo = entrenar_naive_bayes(entrenamiento)
        exactitud, reales, predichas = evaluar(modelo, prueba)
        prediccion, probabilidades, _ = predecir(argumentos.mensaje, modelo)
        matriz = construir_matriz_confusion(reales, predichas)

        print("\n=== DATASET COMPLETO ===")
        print(f"Datos: {RUTA_DATOS}")
        print(f"Entrenamiento: {len(entrenamiento)} mensajes")
        print(f"Prueba: {len(prueba)} mensajes")
        print(f"Exactitud: {exactitud:.2%}")
        print(f'Mensaje: "{argumentos.mensaje}"')
        print(f"Predicción: {prediccion.upper()}")
        for clase, valor in probabilidades.items():
            print(f"  {clase}: {valor:.2%}")

        graficar_resultados(
            datos,
            matriz,
            argumentos.mensaje,
            probabilidades,
            modelo,
            exactitud,
            mostrar=not argumentos.sin_ventana,
            guardar=argumentos.guardar,
        )
    except NotImplementedError as error:
        print(f"\nActividad pendiente: {error}")
        print("Completa los tres bloques TODO y vuelve a ejecutar el programa.")


if __name__ == "__main__":
    main()
