import heapq
from modelos.grafo import Grafo
from modelos.arista import Arista


class ResultadoPrim:
    def __init__(self):
        self.aristas_mst: list[Arista] = []   # Aristas que forman el MST
        self.orden_visita: list[str] = []      # Orden sugerido para el recorrido
        self.distancia_total: float = 0.0
        self.completo: bool = False            # True si conectó todos los vértices


def prim(grafo: Grafo) -> ResultadoPrim:
    """
    Algoritmo de Prim para encontrar el Árbol de Expansión Mínima (MST) del campus.

    Usado para: planear el recorrido de visitantes que quieran visitar TODOS los
    lugares del campus recorriendo la menor distancia posible, sin repetir lugares.

    Supuestos:
      - No se consideran restricciones de accesibilidad (visitantes sin restricciones).
      - Solo se usan caminos disponibles (no bloqueados ni en mantenimiento).
      - El criterio de peso es siempre la DISTANCIA.
      - Se parte desde la Portería Principal ('POR') si existe, o desde el primer vértice.

    Args:
        grafo: Grafo del campus

    Returns:
        ResultadoPrim con las aristas del MST y el orden de visita sugerido
    """
    resultado = ResultadoPrim()

    if grafo.total_vertices() == 0:
        return resultado

    vertices_ids = list(grafo.vertices.keys())

    # Punto de partida: POR (portería) si existe, sino el primero
    inicio = "POR" if "POR" in grafo.vertices else vertices_ids[0]

    INF = float("inf")

    # clave[v] = menor peso de arista que conecta v al MST construido
    clave: dict[str, float] = {v: INF for v in vertices_ids}
    clave[inicio] = 0.0

    # padre[v] = vértice del MST desde el que se conectó v
    padre: dict[str, str | None] = {v: None for v in vertices_ids}

    # arista_padre[v] = la arista completa que conectó v al MST
    arista_padre: dict[str, Arista | None] = {v: None for v in vertices_ids}

    en_mst: set[str] = set()

    # Min-heap: (clave, id_vertice)
    heap: list[tuple[float, str]] = [(0.0, inicio)]

    while heap:
        peso_min, vertice = heapq.heappop(heap)

        if vertice in en_mst:
            continue
        en_mst.add(vertice)

        # Agregar la arista al MST (excepto para el vértice inicial)
        if arista_padre[vertice] is not None:
            resultado.aristas_mst.append(arista_padre[vertice])
            resultado.distancia_total += arista_padre[vertice].distancia

        # Explorar vecinos (solo disponibles, sin restricción de accesibilidad)
        for arista in grafo.obtener_vecinos(vertice, solo_disponibles=True):
            vecino = arista.destino
            if vecino not in en_mst and arista.distancia < clave[vecino]:
                clave[vecino] = arista.distancia
                padre[vecino] = vertice
                arista_padre[vecino] = arista
                heapq.heappush(heap, (arista.distancia, vecino))

    resultado.completo = len(en_mst) == len(vertices_ids)

    # Construir orden de visita haciendo un recorrido DFS sobre el MST
    resultado.orden_visita = _dfs_orden_visita(inicio, resultado.aristas_mst, vertices_ids)

    return resultado


def _dfs_orden_visita(inicio: str, aristas_mst: list[Arista], todos_vertices: list[str]) -> list[str]:
    # Construir lista de adyacencia solo con las aristas del MST
    adyacencia: dict[str, list[str]] = {v: [] for v in todos_vertices}
    for arista in aristas_mst:
        adyacencia[arista.origen].append(arista.destino)
        adyacencia[arista.destino].append(arista.origen)

    visitados: set[str] = set()
    orden: list[str] = []
    pila: list[str] = [inicio]

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        orden.append(actual)
        # Agregar vecinos en orden inverso para mantener consistencia
        for vecino in reversed(adyacencia[actual]):
            if vecino not in visitados:
                pila.append(vecino)

    return orden


def explicar_mst(grafo: Grafo, resultado: ResultadoPrim) -> str:
    """
    Genera una explicación del recorrido del visitante basado en el MST.

    Args:
        grafo:     Grafo del campus
        resultado: Resultado del algoritmo de Prim

    Returns:
        Texto explicativo para mostrar al usuario
    """
    lineas = []

    if not resultado.aristas_mst and not resultado.orden_visita:
        return "No se pudo construir el recorrido. Verifica que el grafo tenga vértices."

    if not resultado.completo:
        lineas.append(
            "⚠ AVISO: No todos los lugares están conectados con caminos disponibles.\n"
            "El recorrido cubre solo los lugares alcanzables desde la entrada.\n"
        )

    lineas.append("=" * 60)
    lineas.append("   RECORRIDO TURÍSTICO DEL CAMPUS (Árbol de Expansión Mínima)")
    lineas.append("=" * 60)
    lineas.append("")
    lineas.append(f"Algoritmo utilizado : Prim (MST por distancia mínima)")
    lineas.append(f"Lugares a visitar   : {len(resultado.orden_visita)}")
    lineas.append(f"Distancia total MST : {resultado.distancia_total:.0f} metros")
    lineas.append("")

    lineas.append("Orden de visita sugerido:")
    for i, vid in enumerate(resultado.orden_visita, 1):
        v = grafo.obtener_vertice(vid)
        lineas.append(f"  {i:>2}. [{v.id:>4}] {v.nombre}")

    lineas.append("")
    lineas.append("Conexiones del árbol de expansión:")
    for arista in resultado.aristas_mst:
        origen_nombre  = grafo.obtener_vertice(arista.origen).nombre
        destino_nombre = grafo.obtener_vertice(arista.destino).nombre
        lineas.append(
            f"  {origen_nombre} → {destino_nombre}  |  {arista.distancia:.0f} m"
        )

    lineas.append("")
    lineas.append("¿Por qué esta ruta?")
    lineas.append(
        "  El Árbol de Expansión Mínima conecta TODOS los lugares del campus "
        "usando el conjunto de caminos con menor distancia total acumulada, "
        "sin formar ciclos. Esto garantiza que los visitantes recorran la menor "
        "cantidad de metros posible para ver todos los lugares, sin repetir ninguno."
    )

    return "\n".join(lineas)
