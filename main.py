import pygame
import sys

from algoritmos.DFS import dfs_solve
from logic.estados import State
from logic.veiculos import Vehicle
from logic.level_logic import Nivel

pygame.init()

# Variables globales para Pygame
ANCHO, ALTO = 1000, 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
GRIS = (169, 169, 169)

# Función para dibujar el tablero centrado en la pantalla con Pygame
def dibujar_tablero(tablero, pantalla):
    pantalla.fill(BLANCO)

    # Calcular el ancho y alto total del tablero en píxeles
    ancho_tablero = tablero.columnas * tablero.ancho_celda
    alto_tablero = tablero.filas * tablero.ancho_celda

    # Calcular la posición inicial para centrar el tablero
    x_inicial = (ANCHO - ancho_tablero) // 2
    y_inicial = (ALTO - alto_tablero) // 2

    for row in range(tablero.filas):
        for col in range(tablero.columnas):
            rect = pygame.Rect(x_inicial + col * tablero.ancho_celda, 
                               y_inicial + row * tablero.ancho_celda,
                               tablero.ancho_celda, tablero.ancho_celda)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

    for letra, posiciones in tablero.elementos.items():
        color = ROJO if letra == 'A' else VERDE if letra == '0'  else GRIS if letra == 'B' else AZUL

        for pos in posiciones:
            x, y = pos
            orientacion = tablero.determinar_orientacion(letra)

            rect_elemento = pygame.Rect(x_inicial + x * tablero.ancho_celda, 
                                        y_inicial + y * tablero.ancho_celda,
                                        tablero.ancho_celda, tablero.ancho_celda)
            
            pygame.draw.rect(pantalla, color, rect_elemento)
            font = pygame.font.Font(None, 36)
            texto = font.render(letra, True, BLANCO)
            pantalla.blit(texto, (rect_elemento.x + 10, rect_elemento.y + 5))

    pygame.display.flip()



def es_estado_meta(estado_actual, estado_meta):
    return estado_actual == estado_meta

def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Juego de Tablero')

    tablero = Nivel('nivel.txt')
    tablero.leer_desde_txt()

#implementacion de DFS a medias comentado aqui abajo 

    # vehicles = {letra: Vehicle(letra, posiciones) for letra, posiciones in tablero.elementos.items()}
    # estado_inicial = State(vehicles, tablero.obtener_estado_juego())

    # # Encontrar la posición del '0'
    # posicion_meta = tablero.elementos['0'][0]

    # # Definir el estado objetivo con 'A' en la posición del '0'
    # vehicles_meta = {letra: Vehicle(letra, posiciones) for letra, posiciones in tablero.elementos.items()}
    # vehicles_meta['A'] = Vehicle('A', [posicion_meta])

    # estado_meta = State(vehicles_meta, tablero.obtener_estado_juego())

    # solucion = dfs_solve(estado_inicial, lambda estado: es_estado_meta(estado, estado_meta))

    # if solucion:
    #     print("Solución encontrada:")
    #     for state in solucion:
    #         print("Estado del tablero:")
    #         for fila in state.board:
    #             print("".join(fila))
    #         print()
    # else:
    #     print("No se encontró solución.")

    

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        dibujar_tablero(tablero, pantalla)
        pygame.time.delay(100)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()