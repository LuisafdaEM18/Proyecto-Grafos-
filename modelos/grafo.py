from modelos.vertice import Vertice
from modelos.arista import Arista


class Grafo:

    def __init__(self):
        self.vertices: dict[str, Vertice] = {}
        self.adyacencia: dict[str, list[Arista]] = {}


    def agregar_vertice(self, vertice: Vertice) -> None:
        if vertice.id in self.vertices:
            raise ValueError(f"Ya existe un vértice con ID '{vertice.id}'")
        self.vertices[vertice.id] = vertice
        self.adyacencia[vertice.id] = []

    def agregar_arista(self, arista: Arista) -> None:
        if arista.origen not in self.vertices:
            raise ValueError(f"Vértice origen '{arista.origen}' no existe en el grafo")
        if arista.destino not in self.vertices:
            raise ValueError(f"Vértice destino '{arista.destino}' no existe en el grafo")

        self.adyacencia[arista.origen].append(arista)

        arista_inversa = Arista(
            origen=arista.destino,
            destino=arista.origen,
            distancia=arista.distancia,
            tiempo=arista.tiempo,
            congestion=arista.congestion,
            accesible=arista.accesible,
            estado=arista.estado,
        )
        self.adyacencia[arista.destino].append(arista_inversa)

    def obtener_vertice(self, id: str) -> Vertice:
        if id not in self.vertices:
            raise KeyError(f"No existe el vértice '{id}'")
        return self.vertices[id]

    def obtener_vecinos(self, id: str, solo_disponibles: bool = True) -> list[Arista]:
        aristas = self.adyacencia.get(id, [])
        if solo_disponibles:
            aristas = [a for a in aristas if a.esta_disponible()]
        return aristas

    def existe_vertice(self, id: str) -> bool:
        return id in self.vertices

    def total_vertices(self) -> int:
        return len(self.vertices)

    def total_aristas(self) -> int:
        return sum(len(v) for v in self.adyacencia.values()) // 2

    def listar_vertices(self) -> list[Vertice]:
        return list(self.vertices.values())

    def listar_aristas_unicas(self) -> list[Arista]:
        vistas = set()
        resultado = []
        for aristas in self.adyacencia.values():
            for a in aristas:
                clave = tuple(sorted([a.origen, a.destino]))
                if clave not in vistas:
                    vistas.add(clave)
                    resultado.append(a)
        return resultado

    def __repr__(self):
        return f"Grafo(vértices={self.total_vertices()}, aristas={self.total_aristas()})"