class Vehicle:
    def __init__(self, id, positions):
        self.id = id
        self.positions = positions
        self.orientation = self.determinar_orientacion()

    def determinar_orientacion(self):
        if len(self.positions) == 1:
            return 'obstáculo'
        elif len(set(x for x, y in self.positions)) == 1:
            return 'vertical'
        else:
            return 'horizontal'

    def move(self, direction, board):
        new_positions = []
        if self.orientation == 'horizontal':
            if direction == 'left':
                new_positions = [(x-1, y) for x, y in self.positions]
            elif direction == 'right':
                new_positions = [(x+1, y) for x, y in self.positions]
            else:
                print(f"Movimiento inválido para {self.id} hacia {direction}: {self.positions}")
                return False  # Movimiento inválido para orientación horizontal
        elif self.orientation == 'vertical':
            if direction == 'up':
                new_positions = [(x, y-1) for x, y in self.positions]
            elif direction == 'down':
                new_positions = [(x, y+1) for x, y in self.positions]
            else:
                print(f"Movimiento inválido para {self.id} hacia {direction}: {self.positions}")
                return False  # Movimiento inválido para orientación vertical

        if self.is_valid_move(new_positions, board):
            self.positions = new_positions
            print(f"Movimiento válido para {self.id} hacia {direction}: {new_positions}")
            return True
        print(f"Movimiento inválido para {self.id} hacia {direction}: {new_positions}")
        return False

    def is_valid_move(self, new_positions, board):
        rows, cols = len(board), len(board[0])
        for x, y in new_positions:
            if x < 0 or x >= cols or y < 0 or y >= rows or (board[y][x] != '.' and board[y][x] != '0' and (x, y) not in self.positions):
                return False
        return True
