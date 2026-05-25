# Campus Routing - UdeM

Sistema de rutas eficientes para el campus universitario, desarrollado como práctica de algoritmos de grafos.

---

## Descripción del proyecto

La aplicación modela el campus de la UdeM como un **grafo no dirigido y ponderado**, donde cada lugar relevante del campus es un **vértice** y cada camino entre ellos es una **arista** con múltiples atributos:

| Atributo | Descripción |
|---|---|
| Distancia | Longitud del camino en metros |
| Tiempo | Tiempo estimado de recorrido en minutos |
| Congestión | Nivel de tráfico (1=baja, 2=media, 3=alta) |
| Accesibilidad | Si permite tránsito de personas con movilidad reducida |
| Estado | `disponible`, `bloqueado` o `mantenimiento` |

### Funcionalidades

1. **Búsqueda de ruta entre dos lugares** usando **Dijkstra** con 4 criterios seleccionables:
   - Ruta más corta por distancia
   - Ruta más rápida por tiempo
   - Ruta con menor congestión
   - Ruta accesible para personas con movilidad reducida

2. **Recorrido turístico del campus** usando el **Árbol de Expansión Mínima (Prim)**, que visita todos los lugares con la menor distancia total posible.

3. El sistema **ignora automáticamente** caminos bloqueados o en mantenimiento.

4. Se muestra la **ruta reconstruida**, el **costo total** y una **explicación** de por qué se eligió esa ruta.

---

## Estructura del proyecto

```
proyecto-grafos/
├── main.py                     # Punto de entrada con menú interactivo
├── algoritmos/
│   ├── dijkstra.py             # Dijkstra con criterios múltiples
│   └── prim.py                 # MST con Prim para recorrido turístico
├── datos/
│   └── campus.py               # Definición de los 16 vértices y 25 caminos
├── modelos/
│   ├── vertice.py              # Clase Vertice
│   ├── arista.py               # Clase Arista con todos sus atributos
│   └── grafo.py                # Clase Grafo (lista de adyacencia)
├── utils/
│   └── helpers.py              # Utilidades de visualización e input
└── README.md
```

---

## Cómo ejecutar el proyecto

### Requisitos

- Python **3.10 o superior** (no requiere librerías externas)

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/campus-routing.git
cd campus-routing

# 2. Ejecuta el programa
python main.py
```

### Navegación del menú

```
[1] Buscar ruta entre dos lugares    → pide origen, destino y criterio
[2] Ver recorrido turístico (MST)    → recorrido óptimo por todo el campus
[3] Ver todos los lugares            → lista de vértices con su ID y tipo
[4] Ver todos los caminos            → lista de aristas con todos sus atributos
[0] Salir
```

---

## Lugares del campus (vértices)

| ID | Nombre | Tipo |
|---|---|---|
| POR | Portería Principal | Acceso |
| B1 | Bloque 1 - Administrativo | Bloque académico |
| B2 | Bloque 2 - Ciencias Básicas | Bloque académico |
| B3 | Bloque 3 - Humanidades | Bloque académico |
| B4 | Bloque 4 - Ingeniería | Bloque académico |
| LIB | Biblioteca Central | Biblioteca |
| KIO | Kiosko | Cafetería |
| LAB | Laboratorios | Laboratorio |
| TEA | Teatro Universitario | Teatro |
| ENF | Enfermería | Salud |
| DEP | Zona Deportiva | Deporte |
| PAR | Parqueadero Principal | Parqueadero |
| PAR2 | Parqueadero Secundario | Parqueadero |
| ADM | Oficinas Administrativas | Administrativo |
| CAP | Capilla / Auditorio | Auditorio |
| INV | Centro de Investigación | Laboratorio |

---

## Supuestos asumidos

1. El grafo es **no dirigido**: todos los caminos son transitables en ambas direcciones con el mismo costo.
2. Los caminos con estado `bloqueado` o `mantenimiento` son **completamente ignorados** por ambos algoritmos.
3. Para el criterio de **accesibilidad**, los caminos no accesibles reciben peso infinito y quedan excluidos de la búsqueda.
4. El **MST de Prim** parte siempre desde la Portería Principal (`POR`) y no aplica restricciones de accesibilidad, ya que los visitantes no tienen movilidad reducida.
5. El recorrido turístico muestra el orden de visita mediante un **DFS sobre el MST**, lo que garantiza no repetir lugares.
6. Los niveles de congestión, distancias y tiempos son **valores ilustrativos** basados en un campus universitario típico.
7. Se asume que el campus está suficientemente conectado; si un camino queda aislado por bloqueos, el sistema informa que no hay ruta disponible.

---

## Autor

Luisa Fernanda Espinal Montoya 