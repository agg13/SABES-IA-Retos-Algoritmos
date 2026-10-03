"""Visualizador de BFS, DFS y A* en una cuadrícula editable.

Ejecutar desde una terminal:

    python busqueda_visual.py

El programa utiliza únicamente la biblioteca estándar de Python. Tkinter debe
estar disponible en la instalación de Python.
"""

from collections import deque
from dataclasses import dataclass
import heapq
import itertools
import tkinter as tk
from tkinter import ttk
from typing import Dict, Iterable, List, Optional, Set, Tuple


Posicion = Tuple[int, int]


@dataclass(frozen=True)
class Paso:
    """Información necesaria para dibujar una iteración."""

    actual: Posicion
    frontera: Tuple[Posicion, ...]
    visitados: frozenset[Posicion]


@dataclass(frozen=True)
class Resultado:
    algoritmo: str
    camino: Tuple[Posicion, ...]
    pasos: Tuple[Paso, ...]

    @property
    def encontrado(self) -> bool:
        return bool(self.camino)

    @property
    def costo(self) -> Optional[int]:
        return len(self.camino) - 1 if self.camino else None

    @property
    def expandidos(self) -> int:
        return len(self.pasos)


def vecinos(
    posicion: Posicion,
    filas: int,
    columnas: int,
    paredes: Set[Posicion],
) -> List[Posicion]:
    """Movimientos válidos en orden: arriba, derecha, abajo, izquierda."""
    fila, columna = posicion
    candidatos = [
        (fila - 1, columna),
        (fila, columna + 1),
        (fila + 1, columna),
        (fila, columna - 1),
    ]
    return [
        (f, c)
        for f, c in candidatos
        if 0 <= f < filas
        and 0 <= c < columnas
        and (f, c) not in paredes
    ]


def reconstruir_camino(
    padres: Dict[Posicion, Optional[Posicion]], meta: Posicion
) -> Tuple[Posicion, ...]:
    camino: List[Posicion] = []
    actual: Optional[Posicion] = meta
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]
    camino.reverse()
    return tuple(camino)


def buscar_bfs(
    filas: int,
    columnas: int,
    paredes: Set[Posicion],
    inicio: Posicion,
    meta: Posicion,
) -> Resultado:
    """BFS usa una cola FIFO y encuentra rutas mínimas con costo uniforme."""
    frontera = deque([inicio])
    descubiertos = {inicio}
    visitados: Set[Posicion] = set()
    padres: Dict[Posicion, Optional[Posicion]] = {inicio: None}
    pasos: List[Paso] = []

    while frontera:
        actual = frontera.popleft()
        visitados.add(actual)

        if actual != meta:
            for vecino in vecinos(actual, filas, columnas, paredes):
                if vecino not in descubiertos:
                    descubiertos.add(vecino)
                    padres[vecino] = actual
                    frontera.append(vecino)

        pasos.append(Paso(actual, tuple(frontera), frozenset(visitados)))
        if actual == meta:
            return Resultado(
                "BFS", reconstruir_camino(padres, meta), tuple(pasos)
            )

    return Resultado("BFS", tuple(), tuple(pasos))


def buscar_dfs(
    filas: int,
    columnas: int,
    paredes: Set[Posicion],
    inicio: Posicion,
    meta: Posicion,
) -> Resultado:
    """DFS usa una pila LIFO y profundiza antes de cambiar de rama."""
    frontera: List[Posicion] = [inicio]
    descubiertos = {inicio}
    visitados: Set[Posicion] = set()
    padres: Dict[Posicion, Optional[Posicion]] = {inicio: None}
    pasos: List[Paso] = []

    while frontera:
        actual = frontera.pop()
        visitados.add(actual)

        if actual != meta:
            # Se invierte para que "arriba" sea la primera opción extraída.
            for vecino in reversed(vecinos(actual, filas, columnas, paredes)):
                if vecino not in descubiertos:
                    descubiertos.add(vecino)
                    padres[vecino] = actual
                    frontera.append(vecino)

        pasos.append(Paso(actual, tuple(frontera), frozenset(visitados)))
        if actual == meta:
            return Resultado(
                "DFS", reconstruir_camino(padres, meta), tuple(pasos)
            )

    return Resultado("DFS", tuple(), tuple(pasos))


def distancia_manhattan(origen: Posicion, destino: Posicion) -> int:
    return abs(origen[0] - destino[0]) + abs(origen[1] - destino[1])


def buscar_a_estrella(
    filas: int,
    columnas: int,
    paredes: Set[Posicion],
    inicio: Posicion,
    meta: Posicion,
) -> Resultado:
    """A* prioriza el valor f(n) = g(n) + h(n)."""
    contador = itertools.count()
    costos: Dict[Posicion, int] = {inicio: 0}
    padres: Dict[Posicion, Optional[Posicion]] = {inicio: None}
    cerrados: Set[Posicion] = set()
    abiertos: Set[Posicion] = {inicio}
    pasos: List[Paso] = []
    prioridad_inicial = distancia_manhattan(inicio, meta)
    frontera = [(prioridad_inicial, 0, next(contador), inicio)]

    while frontera:
        _, costo_extraido, _, actual = heapq.heappop(frontera)

        # El heap puede conservar una entrada antigua de un estado actualizado.
        if actual in cerrados or costo_extraido != costos.get(actual):
            continue

        abiertos.discard(actual)
        cerrados.add(actual)

        if actual != meta:
            for vecino in vecinos(actual, filas, columnas, paredes):
                if vecino in cerrados:
                    continue
                nuevo_costo = costos[actual] + 1
                if nuevo_costo < costos.get(vecino, float("inf")):
                    costos[vecino] = nuevo_costo
                    padres[vecino] = actual
                    prioridad = nuevo_costo + distancia_manhattan(vecino, meta)
                    heapq.heappush(
                        frontera,
                        (prioridad, nuevo_costo, next(contador), vecino),
                    )
                    abiertos.add(vecino)

        frontera_visible = tuple(
            sorted(
                abiertos,
                key=lambda p: (costos[p] + distancia_manhattan(p, meta), p),
            )
        )
        pasos.append(Paso(actual, frontera_visible, frozenset(cerrados)))

        if actual == meta:
            return Resultado(
                "A*", reconstruir_camino(padres, meta), tuple(pasos)
            )

    return Resultado("A*", tuple(), tuple(pasos))


def paredes_ejemplo() -> Set[Posicion]:
    return {
        (0, 0), (0, 5), (0, 8),
        (1, 1), (1, 6),
        (2, 0), (2, 6),
        (3, 2), (3, 5),
        (4, 1), (4, 5), (4, 6), (4, 7),
        (5, 8),
        (6, 1), (6, 3),
        (7, 1), (7, 6), (7, 9),
    }


class Aplicacion:
    COLORES = {
        "libre": "#FFFFFF",
        "pared": "#20242A",
        "visitado": "#9ED8FF",
        "frontera": "#FFD166",
        "actual": "#F77F00",
        "ruta": "#8AC926",
        "inicio": "#4361EE",
        "meta": "#E63946",
        "robot": "#7209B7",
    }

    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Búsqueda visual: BFS, DFS y A*")
        self.raiz.minsize(800, 640)

        self.filas = 8
        self.columnas = 10
        self.paredes = paredes_ejemplo()
        self.inicio = (7, 0)
        self.meta = (0, 9)
        self.tamano = 48
        self.animando = False
        self.paso: Optional[Paso] = None
        self.ruta: Tuple[Posicion, ...] = tuple()
        self.robot: Optional[Posicion] = None

        self.modo = tk.StringVar(value="pared")
        self.algoritmo = tk.StringVar(value="BFS")
        self.pausa = tk.IntVar(value=140)
        self.estado = tk.StringVar()

        self._crear_interfaz()
        self._ajustar_canvas()
        self._dibujar()
        self._mensaje("Edita el escenario o inicia una búsqueda.")

    def _crear_interfaz(self) -> None:
        principal = ttk.Frame(self.raiz, padding=10)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="BFS, DFS y A* en una cuadrícula",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        edicion = ttk.LabelFrame(principal, text="Edición", padding=8)
        edicion.pack(fill="x")
        for texto, valor in (
            ("Pared / libre", "pared"),
            ("Colocar robot", "inicio"),
            ("Colocar meta", "meta"),
        ):
            ttk.Radiobutton(
                edicion, text=texto, value=valor, variable=self.modo
            ).pack(side="left", padx=4)

        ttk.Button(edicion, text="− fila", command=lambda: self._redimensionar(-1, 0)).pack(side="left", padx=(15, 2))
        ttk.Button(edicion, text="+ fila", command=lambda: self._redimensionar(1, 0)).pack(side="left", padx=2)
        ttk.Button(edicion, text="− columna", command=lambda: self._redimensionar(0, -1)).pack(side="left", padx=2)
        ttk.Button(edicion, text="+ columna", command=lambda: self._redimensionar(0, 1)).pack(side="left", padx=2)
        ttk.Button(edicion, text="Limpiar paredes", command=self._limpiar_paredes).pack(side="left", padx=8)
        ttk.Button(edicion, text="Restaurar", command=self._restaurar).pack(side="left", padx=2)

        contenedor = ttk.Frame(principal)
        contenedor.pack(fill="both", expand=True, pady=8)
        self.canvas = tk.Canvas(contenedor, background="#E9ECEF")
        barra_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.canvas.xview)
        barra_y = ttk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=barra_x.set, yscrollcommand=barra_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        self.canvas.bind("<Button-1>", self._clic)

        controles = ttk.LabelFrame(principal, text="Búsqueda", padding=8)
        controles.pack(fill="x")
        ttk.Label(controles, text="Algoritmo:").pack(side="left")
        ttk.Combobox(
            controles,
            values=("BFS", "DFS", "A*"),
            textvariable=self.algoritmo,
            state="readonly",
            width=6,
        ).pack(side="left", padx=5)
        ttk.Label(controles, text="Pausa:").pack(side="left", padx=(15, 0))
        ttk.Scale(
            controles,
            from_=30,
            to=600,
            variable=self.pausa,
            orient="horizontal",
            length=170,
        ).pack(side="left", padx=5)
        self.boton_iniciar = ttk.Button(
            controles, text="▶ Iniciar", command=self._iniciar
        )
        self.boton_iniciar.pack(side="left", padx=15)

        ttk.Label(principal, textvariable=self.estado, justify="left").pack(
            fill="x", pady=(7, 0)
        )

    def _mensaje(self, texto: str) -> None:
        self.estado.set(
            f"Tamaño: {self.filas} × {self.columnas} | "
            f"Inicio: {self.inicio} | Meta: {self.meta} | "
            f"Paredes: {len(self.paredes)}\n{texto}"
        )

    def _ajustar_canvas(self) -> None:
        self.canvas.configure(
            scrollregion=(0, 0, self.columnas * self.tamano, self.filas * self.tamano)
        )

    def _dibujar(self) -> None:
        self.canvas.delete("all")
        visitados = set(self.paso.visitados) if self.paso else set()
        frontera = set(self.paso.frontera) if self.paso else set()
        actual = self.paso.actual if self.paso else None

        for fila in range(self.filas):
            for columna in range(self.columnas):
                posicion = (fila, columna)
                color = self.COLORES["libre"]
                texto = ""
                texto_color = "#111111"

                if posicion in self.paredes:
                    color = self.COLORES["pared"]
                elif posicion in visitados:
                    color = self.COLORES["visitado"]
                if posicion in frontera:
                    color = self.COLORES["frontera"]
                if posicion == actual:
                    color = self.COLORES["actual"]
                if posicion in self.ruta:
                    color = self.COLORES["ruta"]
                if posicion == self.inicio:
                    color, texto, texto_color = self.COLORES["inicio"], "I", "white"
                if posicion == self.meta:
                    color, texto, texto_color = self.COLORES["meta"], "M", "white"
                if posicion == self.robot:
                    color, texto, texto_color = self.COLORES["robot"], "R", "white"

                x0, y0 = columna * self.tamano, fila * self.tamano
                x1, y1 = x0 + self.tamano, y0 + self.tamano
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=color, outline="#6C757D"
                )
                if texto:
                    self.canvas.create_text(
                        (x0 + x1) / 2,
                        (y0 + y1) / 2,
                        text=texto,
                        fill=texto_color,
                        font=("Segoe UI", 13, "bold"),
                    )

    def _limpiar_visualizacion(self) -> None:
        self.paso = None
        self.ruta = tuple()
        self.robot = None

    def _clic(self, evento) -> None:
        if self.animando:
            return
        columna = int(self.canvas.canvasx(evento.x) // self.tamano)
        fila = int(self.canvas.canvasy(evento.y) // self.tamano)
        posicion = (fila, columna)
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return

        mensaje = "Escenario actualizado."
        if self.modo.get() == "pared":
            if posicion in {self.inicio, self.meta}:
                mensaje = "El inicio y la meta no pueden ser paredes."
            elif posicion in self.paredes:
                self.paredes.remove(posicion)
            else:
                self.paredes.add(posicion)
        elif self.modo.get() == "inicio":
            if posicion in self.paredes or posicion == self.meta:
                mensaje = "Selecciona una celda libre diferente de la meta."
            else:
                self.inicio = posicion
        elif self.modo.get() == "meta":
            if posicion in self.paredes or posicion == self.inicio:
                mensaje = "Selecciona una celda libre diferente del inicio."
            else:
                self.meta = posicion

        self._limpiar_visualizacion()
        self._dibujar()
        self._mensaje(mensaje)

    def _primera_libre(self, excluir: Posicion) -> Posicion:
        for fila in range(self.filas):
            for columna in range(self.columnas):
                posicion = (fila, columna)
                if posicion not in self.paredes and posicion != excluir:
                    return posicion
        raise RuntimeError("No quedan suficientes celdas libres.")

    def _redimensionar(self, cambio_fila: int, cambio_columna: int) -> None:
        if self.animando:
            return
        nuevas_filas = self.filas + cambio_fila
        nuevas_columnas = self.columnas + cambio_columna
        if not (2 <= nuevas_filas <= 20 and 2 <= nuevas_columnas <= 20):
            self._mensaje("El tamaño permitido va de 2 × 2 a 20 × 20.")
            return

        self.filas, self.columnas = nuevas_filas, nuevas_columnas
        self.paredes = {
            p for p in self.paredes
            if 0 <= p[0] < self.filas and 0 <= p[1] < self.columnas
        }
        while self.filas * self.columnas - len(self.paredes) < 2:
            self.paredes.pop()

        if not (0 <= self.inicio[0] < self.filas and 0 <= self.inicio[1] < self.columnas):
            self.inicio = self._primera_libre(self.meta)
        if not (0 <= self.meta[0] < self.filas and 0 <= self.meta[1] < self.columnas):
            self.meta = self._primera_libre(self.inicio)

        self._limpiar_visualizacion()
        self._ajustar_canvas()
        self._dibujar()
        self._mensaje("Tamaño modificado.")

    def _limpiar_paredes(self) -> None:
        if self.animando:
            return
        self.paredes.clear()
        self._limpiar_visualizacion()
        self._dibujar()
        self._mensaje("Se eliminaron las paredes.")

    def _restaurar(self) -> None:
        if self.animando:
            return
        self.filas, self.columnas = 8, 10
        self.paredes = paredes_ejemplo()
        self.inicio, self.meta = (7, 0), (0, 9)
        self._limpiar_visualizacion()
        self._ajustar_canvas()
        self._dibujar()
        self._mensaje("Se restauró el escenario inicial.")

    def _iniciar(self) -> None:
        if self.animando:
            return
        funciones = {
            "BFS": buscar_bfs,
            "DFS": buscar_dfs,
            "A*": buscar_a_estrella,
        }
        resultado = funciones[self.algoritmo.get()](
            self.filas, self.columnas, self.paredes, self.inicio, self.meta
        )
        self.animando = True
        self.boton_iniciar.configure(state="disabled")
        self._limpiar_visualizacion()
        self._animar_busqueda(resultado, 0)

    def _animar_busqueda(self, resultado: Resultado, indice: int) -> None:
        if indice < len(resultado.pasos):
            self.paso = resultado.pasos[indice]
            self._dibujar()
            self._mensaje(
                f"{resultado.algoritmo} | iteración {indice + 1}/"
                f"{len(resultado.pasos)} | actual={self.paso.actual} | "
                f"frontera={len(self.paso.frontera)} | "
                f"visitados={len(self.paso.visitados)}"
            )
            self.raiz.after(
                max(20, int(self.pausa.get())),
                lambda: self._animar_busqueda(resultado, indice + 1),
            )
            return

        if resultado.encontrado:
            self.ruta = resultado.camino
            self._animar_robot(resultado, 0)
        else:
            self._terminar(resultado, "No existe una ruta hasta la meta.")

    def _animar_robot(self, resultado: Resultado, indice: int) -> None:
        if indice < len(resultado.camino):
            self.robot = resultado.camino[indice]
            self._dibujar()
            self._mensaje(
                f"{resultado.algoritmo} | movimiento {indice}/"
                f"{resultado.costo} | expandidos={resultado.expandidos}"
            )
            self.raiz.after(
                max(80, int(self.pausa.get())),
                lambda: self._animar_robot(resultado, indice + 1),
            )
            return
        self._terminar(
            resultado,
            f"Ruta terminada: costo={resultado.costo}, "
            f"nodos expandidos={resultado.expandidos}.",
        )

    def _terminar(self, resultado: Resultado, mensaje: str) -> None:
        self.animando = False
        self.boton_iniciar.configure(state="normal")
        self._mensaje(f"{resultado.algoritmo}: {mensaje}")


def main() -> None:
    raiz = tk.Tk()
    Aplicacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()

