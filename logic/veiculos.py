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
        elif self.orientation == 'vertical':
            if direction == 'up':
                new_positions = [(x, y-1) for x, y in self.positions]
            elif direction == 'down':
                new_positions = [(x, y+1) for x, y in self.positions]
        
        if self.is_valid_move(new_positions, board):
            self.positions = new_positions
            return True
        return False

    def is_valid_move(self, new_positions, board):
        for x, y in new_positions:
            if x < 0 or x >= len(board.board[0]) or y < 0 or y >= len(board.board):
                return False
            if board.board[y][x] != '.':
                return False
        return True