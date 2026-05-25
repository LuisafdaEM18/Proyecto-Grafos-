from modelos.grafo import Grafo
from modelos.arista import Arista

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    VERDE   = "\033[92m"
    AMARILLO= "\033[93m"
    ROJO    = "\033[91m"
    CYAN    = "\033[96m"
    GRIS    = "\033[90m"
    BLANCO  = "\033[97m"


def titulo(texto: str) -> None:
    borde = "═" * (len(texto) + 4)
    print(f"\n{Color.CYAN}{Color.BOLD}╔{borde}╗")
    print(f"║  {texto}  ║")
    print(f"╚{borde}╝{Color.RESET}\n")


def separador(caracter: str = "─", ancho: int = 60) -> None:
    print(Color.GRIS + caracter * ancho + Color.RESET)


def exito(texto: str) -> None:
    print(f"{Color.VERDE}✔ {texto}{Color.RESET}")


def advertencia(texto: str) -> None:
    print(f"{Color.AMARILLO}⚠ {texto}{Color.RESET}")


def error(texto: str) -> None:
    print(f"{Color.ROJO}✘ {texto}{Color.RESET}")


def mostrar_lista_vertices(grafo: Grafo) -> None:
    print(f"\n{'ID':<6} {'Nombre':<35} {'Tipo':<22}")
    separador()
    for v in grafo.listar_vertices():
        print(f"{Color.CYAN}{v.id:<6}{Color.RESET} {v.nombre:<35} {Color.GRIS}{v.tipo:<22}{Color.RESET}")
    separador()
    print(f"Total: {grafo.total_vertices()} lugares\n")


def mostrar_lista_aristas(grafo: Grafo) -> None:
    aristas = grafo.listar_aristas_unicas()
    print(f"\n{'Origen':<6} {'Destino':<6} {'Dist':>6} {'Tiempo':>7} {'Cong':>5} {'Accesible':>10} {'Estado':<14}")
    separador()
    for a in aristas:
        color_estado = Color.VERDE if a.estado == "disponible" else Color.ROJO
        accesible_txt = "Sí" if a.accesible else "No"
        print(
            f"{a.origen:<6} {a.destino:<6} "
            f"{a.distancia:>5.0f}m {a.tiempo:>6.1f}min "
            f"{a.congestion:>5} {accesible_txt:>10} "
            f"{color_estado}{a.estado:<14}{Color.RESET}"
        )
    separador()
    print(f"Total: {len(aristas)} caminos\n")


def pedir_vertice(grafo: Grafo, mensaje: str) -> str:
    while True:
        valor = input(f"{Color.BOLD}{mensaje}{Color.RESET} ").strip().upper()
        if grafo.existe_vertice(valor):
            return valor
        error(f"'{valor}' no es un ID válido. Intenta de nuevo.")
        print(f"  IDs disponibles: {', '.join(sorted(grafo.vertices.keys()))}")


def pedir_criterio() -> str:
    opciones = {
        "1": "distancia",
        "2": "tiempo",
        "3": "congestion",
        "4": "accesibilidad",
    }
    print(f"\n{Color.BOLD}Selecciona el criterio de búsqueda:{Color.RESET}")
    print("  [1] Ruta más corta por distancia")
    print("  [2] Ruta más rápida por tiempo")
    print("  [3] Ruta con menor congestión")
    print("  [4] Ruta accesible para personas con movilidad reducida")

    while True:
        opcion = input(f"\n{Color.BOLD}Opción (1-4): {Color.RESET}").strip()
        if opcion in opciones:
            return opciones[opcion]
        error("Opción inválida. Elige entre 1 y 4.")


def pedir_confirmacion(mensaje: str) -> bool:
    """Pregunta al usuario sí/no y retorna True si responde afirmativamente."""
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta in ("s", "si", "sí", "y", "yes")