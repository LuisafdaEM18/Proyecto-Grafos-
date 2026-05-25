from datos.campus import construir_campus
from algoritmos.dijkstra import dijkstra, explicar_resultado
from algoritmos.prim import prim, explicar_mst
from utils.helpers import (
    titulo, separador, exito, advertencia, error,
    mostrar_lista_vertices, mostrar_lista_aristas,
    pedir_vertice, pedir_criterio, pedir_confirmacion,
    Color,
)


def menu_principal() -> str:
    print(f"\n{Color.BOLD}¿Qué deseas hacer?{Color.RESET}")
    print("  [1] Buscar ruta entre dos lugares")
    print("  [2] Ver recorrido turístico del campus (MST)")
    print("  [3] Ver todos los lugares del campus")
    print("  [4] Ver todos los caminos del campus")
    print("  [0] Salir")

    while True:
        opcion = input(f"\n{Color.BOLD}Opción: {Color.RESET}").strip()
        if opcion in ("0", "1", "2", "3", "4"):
            return opcion
        error("Opción no válida.")


def flujo_dijkstra(grafo) -> None:
   
    titulo("BUSCAR RUTA ENTRE DOS LUGARES")

    print("Ingresa los IDs de los lugares (puedes ver la lista completa en la opción 3).\n")

    origen  = pedir_vertice(grafo, "Lugar de origen  (ID):")
    destino = pedir_vertice(grafo, "Lugar de destino (ID):")

    if origen == destino:
        advertencia("El origen y el destino son el mismo lugar.")
        return

    criterio = pedir_criterio()

    print(f"\n{Color.GRIS}Calculando ruta...{Color.RESET}")
    resultado = dijkstra(grafo, origen, destino, criterio)

    separador("═")
    print(explicar_resultado(grafo, resultado))
    separador("═")

    if resultado.encontrada:
        exito("Ruta encontrada exitosamente.")
    else:
        error("No se encontró ninguna ruta con los parámetros indicados.")


def flujo_mst(grafo) -> None:
    titulo("RECORRIDO TURÍSTICO DEL CAMPUS")

    print("Este recorrido visita TODOS los lugares del campus con la menor")
    print("distancia total posible, sin restricciones de accesibilidad.\n")

    print(f"{Color.GRIS}Calculando árbol de expansión mínima (Prim)...{Color.RESET}\n")
    resultado = prim(grafo)

    separador("═")
    print(explicar_mst(grafo, resultado))
    separador("═")

    if resultado.completo:
        exito("Recorrido completo: cubre todos los lugares del campus.")
    else:
        advertencia("Algunos lugares no son alcanzables con los caminos disponibles.")


def main() -> None:
    titulo("CAMPUS ROUTING - UdeM")
    print("Cargando el mapa del campus...")

    grafo = construir_campus()
    exito(f"Mapa cargado: {grafo.total_vertices()} lugares, {grafo.total_aristas()} caminos.\n")

    while True:
        opcion = menu_principal()

        if opcion == "1":
            flujo_dijkstra(grafo)

        elif opcion == "2":
            flujo_mst(grafo)

        elif opcion == "3":
            titulo("LUGARES DEL CAMPUS")
            mostrar_lista_vertices(grafo)

        elif opcion == "4":
            titulo("CAMINOS DEL CAMPUS")
            mostrar_lista_aristas(grafo)

        elif opcion == "0":
            print(f"\n{Color.CYAN}¡Hasta luego!{Color.RESET}\n")
            break

        input(f"\n{Color.GRIS}Presiona Enter para continuar...{Color.RESET}")


if __name__ == "__main__":
    main()
