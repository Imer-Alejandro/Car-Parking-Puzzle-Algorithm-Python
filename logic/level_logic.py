from logic.estados import State
from logic.veiculos import Vehicle

class Nivel:
    def __init__(self, nombre_archivo, ancho_celda=50):
        self.nombre_archivo = nombre_archivo
        self.ancho_celda = ancho_celda
        self.elementos = {}
        self.filas = 0
        self.columnas = 0

    def leer_desde_txt(self):
        with open(self.nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        self.filas = len(lineas)
        self.columnas = len(lineas[0].strip())
        self.elementos.clear()

        for y, linea in enumerate(lineas):
            for x, caracter in enumerate(linea.strip()):
                if caracter != '.':
                    self.crear_elemento(caracter, x, y)

    def crear_elemento(self, letra, x, y):
        if letra not in self.elementos:
            self.elementos[letra] = []
        self.elementos[letra].append((x, y))

    def determinar_orientacion(self, elemento):
        posiciones = self.elementos[elemento]
        if len(posiciones) == 1:
            return 'obstáculo'
        elif len(set(x for x, y in posiciones)) == 1:
            return 'vertical'
        else:
            return 'horizontal'

    def obtener_estado_juego(self):
        # Crear diccionario de vehículos a partir de elementos
        vehicles = {letra: Vehicle(letra, posiciones) for letra, posiciones in self.elementos.items()}
        # Convertir el tablero en una matriz para el estado inicial
        board = [['.' for _ in range(self.columnas)] for _ in range(self.filas)]
        for letra, posiciones in self.elementos.items():
            for x, y in posiciones:
                board[y][x] = letra
        return State(vehicles, board)

    def es_meta(self, estado):
        # La condición de meta es que el vehículo 'A' esté en la última columna
        for x, y in estado.vehicles['A'].positions:
            if x == self.columnas - 1:
                return True
        return False
