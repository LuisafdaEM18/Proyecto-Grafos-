class Arista:

    # Constantes para el estado del camino
    DISPONIBLE = "disponible"
    BLOQUEADO = "bloqueado"
    MANTENIMIENTO = "mantenimiento"

    # Constantes para nivel de congestión
    CONGESTION_BAJA = 1
    CONGESTION_MEDIA = 2
    CONGESTION_ALTA = 3

    def __init__(self, origen: str, destino: str, distancia: float, tiempo: float, congestion: int, accesible: bool, estado: str = "disponible"):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.tiempo = tiempo
        self.congestion = congestion
        self.accesible = accesible
        self.estado = estado

    def esta_disponible(self) -> bool:
        return self.estado == self.DISPONIBLE

    def peso(self, criterio: str) -> float:
        if criterio == "distancia":
            return self.distancia
        elif criterio == "tiempo":
            return self.tiempo
        elif criterio == "congestion":
            return float(self.congestion)
        elif criterio == "accesibilidad":
            return self.distancia if self.accesible else float("inf")
        else:
            raise ValueError(f"Criterio desconocido: '{criterio}'. Use: distancia, tiempo, congestion, accesibilidad")

    def congestion_texto(self) -> str:
        niveles = {
            self.CONGESTION_BAJA: "Baja",
            self.CONGESTION_MEDIA: "Media",
            self.CONGESTION_ALTA: "Alta",
        }
        return niveles.get(self.congestion, "Desconocida")

    def __repr__(self):
        return (
            f"Arista({self.origen} -> {self.destino} | "
            f"dist={self.distancia}m, tiempo={self.tiempo}min, "
            f"congestión={self.congestion_texto()}, "
            f"accesible={'Sí' if self.accesible else 'No'}, "
            f"estado={self.estado})"
        )