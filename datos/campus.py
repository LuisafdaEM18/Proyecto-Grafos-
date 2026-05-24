from modelos.vertice import Vertice
from modelos.arista import Arista
from modelos.grafo import Grafo


def construir_campus() -> Grafo:
    """
    Construye y retorna el grafo del campus universitario UdeM.

    Vértices (15 en total):
        B1  - Bloque 1 (Administrativo)
        B2  - Bloque 2 (Ciencias Básicas)
        B3  - Bloque 3 (Humanidades)
        B4  - Bloque 4 (Ingeniería)
        LIB - Biblioteca Central
        KIO - Kiosko
        LAB - Laboratorios 
        TEA - Teatro Universitario
        ENF - Enfermería
        DEP - Zona Deportiva
        PAR - Parqueadero Principal
        PAR2- Parqueadero Secundario
        ADM - Oficinas Administrativas
        CAP - Capilla / Auditorio
        INV - Centro de Investigación
        POR - Portería Principal (entrada)

    Aristas (23 caminos):
        Cada camino tiene: distancia(m), tiempo(min), congestión(1-3), accesible(bool), estado(disponible/bloqueado/mantenimiento)
    """

    grafo = Grafo()
    lugares = [
        Vertice("B1",   "Bloque 1 - Administrativo",      "bloque_academico",  "Sede principal de administración"),
        Vertice("B2",   "Bloque 2 - Ciencias Básicas",    "bloque_academico",  "Matemáticas, física y química"),
        Vertice("B3",   "Bloque 3 - Humanidades",         "bloque_academico",  "Ciencias sociales y arte"),
        Vertice("B4",   "Bloque 4 - Ingeniería",          "bloque_academico",  "Aulas generales y coordinaciones"),
        Vertice("LIB",  "Biblioteca Central",              "biblioteca",        "Colección física y digital"),
        Vertice("KIO",  "Kiosko",                          "kiosko",            "Servicio de snacks y bebidas"),
        Vertice("LAB",  "Laboratorios",                    "laboratorio",       "40 equipos disponibles"),
        Vertice("TEA",  "Teatro Universitario",            "teatro",            "Aforo para 300 personas"),
        Vertice("ENF",  "Enfermería",                      "salud",             "Atención médica básica"),
        Vertice("DEP",  "Zona Deportiva",                  "deporte",           "Canchas y gimnasio"),
        Vertice("PAR",  "Parqueadero Principal",           "parqueadero",       "Capacidad 200 vehículos"),
        Vertice("PAR2", "Parqueadero Secundario",          "parqueadero",       "Capacidad 80 vehículos"),
        Vertice("ADM",  "Oficinas Administrativas",        "administrativo",    "Rectoría y decanaturas"),
        Vertice("CAP",  "Capilla / Auditorio",             "auditorio",         "Eventos académicos y culturales"),
        Vertice("INV",  "Centro de Investigación",         "laboratorio",       "Laboratorios especializados"),
        Vertice("POR",  "Portería Principal",              "acceso",            "Entrada y salida del campus"),
    ]

    for lugar in lugares:
        grafo.agregar_vertice(lugar)
    caminos = [
        # Zona académica central
        Arista("POR",  "PAR",  120, 2.0, 2, True,  "disponible"),
        Arista("POR",  "B4",   180, 3.0, 3, True,  "disponible"),
        Arista("POR",  "ADM",  200, 3.5, 2, True,  "disponible"),
        Arista("PAR",  "B1",   150, 2.5, 2, True,  "disponible"),
        Arista("PAR",  "ENF",  100, 1.5, 1, True,  "disponible"),
        Arista("PAR2", "DEP",   80, 1.5, 1, True,  "disponible"),
        Arista("PAR2", "B3",   160, 2.5, 1, False, "disponible"),   # escaleras, no accesible

        # Bloques entre sí
        Arista("B1",   "B2",    90, 1.5, 2, True,  "disponible"),
        Arista("B1",   "LAB",   60, 1.0, 3, True,  "disponible"),   # alta congestión (muy transitado)
        Arista("B2",   "LIB",  110, 2.0, 2, True,  "disponible"),
        Arista("B2",   "B3",   130, 2.0, 1, True,  "disponible"),
        Arista("B3",   "KIO",   70, 1.0, 3, True,  "disponible"),
        Arista("B3",   "TEA",  200, 3.5, 1, False, "mantenimiento"), # en mantenimiento
        Arista("B4",   "B1",   140, 2.0, 2, True,  "disponible"),
        Arista("B4",   "CAF",  100, 1.5, 3, True,  "disponible"),
        Arista("B4",   "ADM",   80, 1.0, 2, True,  "disponible"),

        # Zona de servicios
        Arista("LIB",  "INV",  170, 3.0, 1, True,  "disponible"),
        Arista("LIB",  "CAP",  140, 2.5, 1, True,  "disponible"),
        Arista("CAF",  "ENF",  150, 2.5, 1, True,  "disponible"),
        Arista("ADM",  "CAP",  120, 2.0, 1, True,  "disponible"),
        Arista("INV",  "LAB",  100, 1.5, 2, True,  "disponible"),
        Arista("DEP",  "ENF",  180, 3.0, 1, True,  "disponible"),
        Arista("DEP",  "CAF",  220, 4.0, 1, True,  "bloqueado"),    # bloqueado por obras
        Arista("PAR",  "PAR2", 300, 5.0, 1, True,  "disponible"),
        Arista("TEA",  "CAP",  160, 3.0, 1, True,  "disponible"),
    ]

    for camino in caminos:
        grafo.agregar_arista(camino)

    return grafo
