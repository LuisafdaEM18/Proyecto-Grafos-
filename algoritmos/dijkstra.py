import heapq
from modelos.grafo import Grafo


CRITERIOS_VALIDOS = ["distancia", "tiempo", "congestion", "accesibilidad"]

CRITERIOS_DESCRIPCION = {
    "distancia":      "Ruta más corta por distancia (metros)",
    "tiempo":         "Ruta más rápida por tiempo (minutos)",
    "congestion":     "Ruta con menor nivel de congestión",
    "accesibilidad":  "Ruta accesible para personas con movilidad reducida",
}

CRITERIOS_UNIDAD = {
    "distancia":     "metros",
    "tiempo":        "minutos",
    "congestion":    "puntos de congestión",
    "accesibilidad": "metros (solo rutas accesibles)",
}


class ResultadoDijkstra:
    """Encapsula el resultado de ejecutar Dijkstra."""

    def __init__(self, origen: str, destino: str, criterio: str):
        self.origen = origen
        self.destino = destino
        self.criterio = criterio
        self.ruta: list[str] = []          # IDs de los vértices en orden
        self.costo_total: float = 0.0
        self.encontrada: bool = False
        self.distancia_total: float = 0.0
        self.tiempo_total: float = 0.0

    def __bool__(self):
        return self.encontrada


def dijkstra(grafo: Grafo, origen: str, destino: str, criterio: str) -> ResultadoDijkstra:
    """
    Implementación de Dijkstra adaptada para múltiples criterios de búsqueda.

    Reglas:
      - Ignora automáticamente caminos bloqueados o en mantenimiento.
      - Para 'accesibilidad', ignora también caminos no accesibles.
      - Retorna el camino óptimo reconstruido y el costo total.

    Args:
        grafo:    Grafo del campus
        origen:   ID del vértice de partida
        destino:  ID del vértice de llegada
        criterio: Criterio de optimización (distancia/tiempo/congestion/accesibilidad)

    Returns:
        ResultadoDijkstra con la ruta, costo y métricas adicionales
    """
    if criterio not in CRITERIOS_VALIDOS:
        raise ValueError(
            f"Criterio '{criterio}' inválido. Opciones: {', '.join(CRITERIOS_VALIDOS)}"
        )
    if not grafo.existe_vertice(origen):
        raise KeyError(f"El vértice origen '{origen}' no existe en el grafo")
    if not grafo.existe_vertice(destino):
        raise KeyError(f"El vértice destino '{destino}' no existe en el grafo")

    resultado = ResultadoDijkstra(origen, destino, criterio)

    INF = float("inf")

    # distancias[v] = menor costo acumulado desde origen hasta v
    distancias: dict[str, float] = {v: INF for v in grafo.vertices}
    distancias[origen] = 0.0

    # Para reconstruir la ruta: predecesor[v] = vértice desde el que llegamos a v
    predecesor: dict[str, str | None] = {v: None for v in grafo.vertices}

    # Para mostrar métricas adicionales aunque el criterio no sea distancia/tiempo
    dist_acum: dict[str, float] = {v: INF for v in grafo.vertices}
    tiempo_acum: dict[str, float] = {v: INF for v in grafo.vertices}
    dist_acum[origen] = 0.0
    tiempo_acum[origen] = 0.0

    # Min-heap: (costo_acumulado, id_vertice)
    heap: list[tuple[float, str]] = [(0.0, origen)]

    visitados: set[str] = set()

    while heap:
        costo_actual, vertice_actual = heapq.heappop(heap)

        if vertice_actual in visitados:
            continue
        visitados.add(vertice_actual)

        # Si llegamos al destino, terminamos
        if vertice_actual == destino:
            break

        for arista in grafo.obtener_vecinos(vertice_actual, solo_disponibles=True):
            vecino = arista.destino

            if vecino in visitados:
                continue

            # Para accesibilidad, omitir caminos no accesibles
            if criterio == "accesibilidad" and not arista.accesible:
                continue

            peso = arista.peso(criterio)

            # Si el peso es infinito (camino no accesible), ignorar
            if peso == INF:
                continue

            nuevo_costo = costo_actual + peso

            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesor[vecino] = vertice_actual
                dist_acum[vecino] = dist_acum[vertice_actual] + arista.distancia
                tiempo_acum[vecino] = tiempo_acum[vertice_actual] + arista.tiempo
                heapq.heappush(heap, (nuevo_costo, vecino))

    # Verificar si se encontró ruta
    if distancias[destino] == INF:
        resultado.encontrada = False
        return resultado

    # Reconstruir la ruta
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = predecesor[actual]
    ruta.reverse()

    resultado.encontrada = True
    resultado.ruta = ruta
    resultado.costo_total = distancias[destino]
    resultado.distancia_total = dist_acum[destino]
    resultado.tiempo_total = tiempo_acum[destino]

    return resultado


def explicar_resultado(grafo: Grafo, resultado: ResultadoDijkstra) -> str:
    """
    Genera una explicación en lenguaje natural de por qué se seleccionó la ruta.

    Args:
        grafo:     Grafo del campus
        resultado: Resultado del algoritmo Dijkstra

    Returns:
        Texto explicativo para mostrar al usuario
    """
    if not resultado.encontrada:
        return (
            f"No se encontró una ruta entre '{resultado.origen}' y '{resultado.destino}' "
            f"con el criterio '{resultado.criterio}'.\n"
            "Esto puede deberse a que todos los caminos disponibles están bloqueados, "
            "en mantenimiento, o no son accesibles según el criterio seleccionado."
        )

    criterio = resultado.criterio
    unidad = CRITERIOS_UNIDAD[criterio]
    pasos = " → ".join(
        grafo.obtener_vertice(v).nombre for v in resultado.ruta
    )

    lineas = [
        f"Criterio aplicado : {CRITERIOS_DESCRIPCION[criterio]}",
        f"Ruta encontrada   : {pasos}",
        f"Costo total       : {resultado.costo_total:.1f} {unidad}",
    ]

    if criterio != "distancia":
        lineas.append(f"Distancia total   : {resultado.distancia_total:.0f} metros")
    if criterio != "tiempo":
        lineas.append(f"Tiempo estimado   : {resultado.tiempo_total:.1f} minutos")

    lineas.append("")
    lineas.append("¿Por qué esta ruta?")

    if criterio == "distancia":
        lineas.append(
            f"  Dijkstra evaluó todos los caminos disponibles y encontró que esta "
            f"secuencia de {len(resultado.ruta) - 1} tramos suma {resultado.costo_total:.0f} m, "
            f"la menor distancia posible entre los dos puntos."
        )
    elif criterio == "tiempo":
        lineas.append(
            f"  El algoritmo priorizó los tramos con menor tiempo de recorrido. "
            f"Esta ruta tarda aproximadamente {resultado.costo_total:.1f} minutos, "
            f"menos que cualquier otra combinación de caminos disponibles."
        )
    elif criterio == "congestion":
        lineas.append(
            f"  Se eligieron tramos con nivel de congestión más bajo, evitando "
            f"caminos muy transitados. El índice de congestión acumulado es "
            f"{resultado.costo_total:.0f} puntos (1=baja, 2=media, 3=alta por tramo)."
        )
    elif criterio == "accesibilidad":
        lineas.append(
            f"  Solo se consideraron caminos marcados como accesibles para "
            f"personas con movilidad reducida (rampas, superficies planas). "
            f"La ruta recorre {resultado.distancia_total:.0f} m sin barreras arquitectónicas."
        )

    # Advertir si algún tramo tiene congestión alta
    for i in range(len(resultado.ruta) - 1):
        origen_id = resultado.ruta[i]
        destino_id = resultado.ruta[i + 1]
        for arista in grafo.obtener_vecinos(origen_id):
            if arista.destino == destino_id and arista.congestion == 3:
                v_nombre = grafo.obtener_vertice(destino_id).nombre
                lineas.append(
                    f"  ⚠ Tramo hacia '{v_nombre}' tiene congestión ALTA en este momento."
                )

    return "\n".join(lineas)
