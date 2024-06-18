# BY: ©Daniel Burgos Arias
# 2024 
import pygame
import random

# Dimensiones de la ventana y la cuadrícula
WINDOW_SIZE = 400
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Definir clase Individuo
class Individuo:
    generacion_actual = 'A'
    next_id = 1

    def __init__(self, x, y, elemento=None):
        self.id = f"{self.generacion_actual}{self.next_id}"
        self.x = x
        self.y = y
        self.elemento = elemento
        self.en_meta = False
        self.padre = []
        self.probabilidad_derecha = 0
        Individuo.next_id += 1

    def mover(self, grid, otros_individuos):
        if self.en_meta:
            return
        
        # Movimientos posibles: Norte, Sur, Este, Oeste, Noreste, Noroeste, Sureste, Suroeste, No mover
        movimientos = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1), (0, 0)]
        
        # Probabilidad de los movimientos
        probabilidades = [0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.12]
        
        dx, dy = random.choices(movimientos, weights=probabilidades)[0]
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar si el nuevo movimiento está dentro de los límites y no colisiona con otro individuo
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if grid[new_y][new_x] == 0 and not any(ind.x == new_x and ind.y == new_y for ind in otros_individuos):
                self.x = new_x
                self.y = new_y

                # Verificar si alcanzó la meta
                if new_x == GRID_SIZE - 1:
                    self.en_meta = True

# Función para dibujar la cuadrícula inicial
def draw_grid(screen):
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_SIZE, y))

# Función para resaltar la última fila de casillas del lado derecho
def highlight_rightmost_column(screen):
    for y in range(GRID_SIZE):
        pygame.draw.rect(screen, BLUE, ((GRID_SIZE - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Función para dibujar los individuos
def draw_individuals(screen, individuals):
    for individual in individuals:
        color = GREEN if individual.en_meta else RED
        pygame.draw.rect(screen, color, (individual.x * CELL_SIZE, individual.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Función para mover a todos los individuos
def move_individuals(individuals, grid):
    for individual in individuals:
        individual.mover(grid, individuals)

# Función para dibujar información adicional
def draw_info(screen, font, turno, individuos):
    info_surface = pygame.Surface((WINDOW_SIZE // 2, WINDOW_SIZE))
    info_surface.fill(WHITE)
    text_turno = font.render(f"Turno: {turno}", True, BLACK)
    text_individuos = font.render(f"Individuos: {len(individuos)}", True, BLACK)
    info_surface.blit(text_turno, (10, 10))
    info_surface.blit(text_individuos, (10, 40))

    if individuos:
        for idx, ind in enumerate(individuos):
            text_id = font.render(ind.id, True, BLACK)
            info_surface.blit(text_id, (10, 70 + idx * 30))
    else:
        text_no_ganadores = font.render("Sin ganadores en esta generación", True, BLACK)
        info_surface.blit(text_no_ganadores, (10, 70))

    screen.blit(info_surface, (WINDOW_SIZE, 0))

# Función principal de la simulación
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE * 1.5, WINDOW_SIZE))
    pygame.display.set_caption("Algoritmo Genético - Simulación")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Inicialización de la población de individuos (cromosomas)
    population_size = 10
    population = []
    ganadores = []

    for _ in range(population_size):
        x = random.randint(0, GRID_SIZE - 3)
        y = random.randint(0, GRID_SIZE - 1)
        population.append(Individuo(x, y))

    turno = 1
    max_turnos = 9

    running = True
    while running:
        screen.fill(WHITE)

        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        draw_grid(screen)
        highlight_rightmost_column(screen)
        draw_individuals(screen, population)
        draw_info(screen, font, turno, population)
        
        if turno <= max_turnos:
            move_individuals(population, grid)
        else:
            # Mostrar ganadores si los hay
            ganadores = [ind.id for ind in population if ind.en_meta]
            if ganadores:
                print(f"Ganadores: {', '.join(ganadores)}")

            # Eliminar población actual
            population.clear()

            # Generar nueva generación
            Individuo.generacion_actual = chr(ord(Individuo.generacion_actual) + 1)
            for _ in range(population_size):
                # generar 2 
                x = random.randint(0, GRID_SIZE - 3)
                y = random.randint(0, GRID_SIZE - 1)
                population.append(Individuo(x, y))

            # Reiniciar turno
            turno = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(10)  # Controla la velocidad de la simulación (10 movimientos por segundo)
        turno += 1

    pygame.quit()

if __name__ == "__main__":
    main()