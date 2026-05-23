class Vertice:
   
    def __init__(self, id: str, nombre: str, tipo: str, descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion

    def __repr__(self):
        return f"Vertice({self.id}: {self.nombre})"

    def __str__(self):
        return f"[{self.id}] {self.nombre} ({self.tipo})"

    def __eq__(self, otro):
        if isinstance(otro, Vertice):
            return self.id == otro.id
        return False

    def __hash__(self):
        return hash(self.id)
