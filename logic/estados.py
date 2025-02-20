from logic.veiculos import Vehicle

class State:
    def __init__(self, vehicles, board):
        self.vehicles = vehicles  # Diccionario de vehículos
        self.board = board  # Matriz del tablero
        self.cost = 0  # Costo acumulado para llegar a este estado

    def __hash__(self):
        return hash(tuple(sorted((v.id, tuple(v.positions)) for v in self.vehicles.values())))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def generar_nuevos_estados(self):
        nuevos_estados = []

        for vehiculo in self.vehicles.values():
            if vehiculo.id in ['0', 'B']:  # Saltar vehículos '0' y 'B'
                continue

            direcciones = ['left', 'right'] if vehiculo.orientation == 'horizontal' else ['up', 'down']
            
            for direccion in direcciones:
                nuevo_vehiculo = Vehicle(vehiculo.id, vehiculo.positions[:])
                if nuevo_vehiculo.move(direccion, self.board):
                    nuevos_vehiculos = self.vehicles.copy()
                    nuevos_vehiculos[vehiculo.id] = nuevo_vehiculo
                    nuevo_estado = State(nuevos_vehiculos, self.actualizar_board(nuevos_vehiculos))
                    nuevo_estado.cost = self.cost + 1  # Aumentar el costo acumulado
                    nuevos_estados.append((nuevo_estado, f"{vehiculo.id}-{direccion[0].upper()}"))

        return nuevos_estados

    def actualizar_board(self, vehicles):
        board = [['.' for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        for v in vehicles.values():
            for x, y in v.positions:
                board[y][x] = v.id
        return board
