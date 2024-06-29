from logic.veiculos import Vehicle

class State:
    def __init__(self, vehicles, board):
        self.vehicles = vehicles  # Diccionario de vehículos
        self.board = board  # Matriz del tablero

    def __hash__(self):
        return hash(tuple(sorted((v.id, tuple(v.positions)) for v in self.vehicles.values())))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def generar_nuevos_estados(self):
        nuevos_estados = []
        for vehiculo in self.vehicles.values():
            for direccion in ['up', 'down', 'left', 'right']:
                nuevo_vehiculo = Vehicle(vehiculo.id, vehiculo.positions[:])
                if nuevo_vehiculo.move(direccion, self.board):
                    nuevos_vehiculos = self.vehicles.copy()
                    nuevos_vehiculos[vehiculo.id] = nuevo_vehiculo
                    nuevos_estados.append(State(nuevos_vehiculos, self.board))
        return nuevos_estados