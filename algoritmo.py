import pygame
import random
# Dimensiones de la ventana y la cuadrícula
WINDOW_SIZE = 800
GRID_SIZE = 100
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (34, 139, 34)

# Definir clase Individuo
class Individuo:
    generacion_actual = 1
    next_id = 1
    def __init__(self, x, y, probabilidad_derecha=0.11, padre_id=None, asesino = False):
        self.id = f"P{padre_id if padre_id else 0}G{Individuo.generacion_actual}ID{Individuo.next_id}"
        self.padre_id = Individuo.next_id
        self.x = x
        self.y = y
        self.asesino = asesino
        self.en_meta = False
        self.pasos = 0
        self.probabilidad_derecha = probabilidad_derecha
        Individuo.next_id += 1

    def mover(self, grid, otros_individuos):
        if self.en_meta:
            return
        # Movimientos posibles: Norte, Sur, Este, Oeste, Noreste, Noroeste, Sureste, Suroeste, No mover
        movimientos = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1), (0, 0)]
        # Probabilidad de los movimientos
        probabilidades = [0.11, 0.11, self.probabilidad_derecha, 0.11, 0.11, 0.11, 0.11, 0.11, 0.12]  
        dx, dy = random.choices(movimientos, weights=probabilidades)[0]
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar si el nuevo movimiento está dentro de los límites y no colisiona con otro individuo
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # Verificar colisión con otro individuo
            collided_individual = next((ind for ind in otros_individuos if ind.x == new_x and ind.y == new_y and ind.id != self.id), None)
            if grid[new_y][new_x] == 0 and not collided_individual:
                self.x = new_x
                self.y = new_y
                self.pasos += 1
                # Verificar si alcanzó la meta
                if new_x == GRID_SIZE - 1:
                    self.en_meta = True
            else:
                #colisión
                if collided_individual: 
                    if self.asesino:
                        otros_individuos.remove(collided_individual)  
                        self.x = new_x
                        self.y = new_y
                        if new_x == GRID_SIZE - 1:
                            self.en_meta = True
                    else:
                        self.pasos += 1 

# Función para dibujar la cuadrícula inicial
def draw_grid(screen):
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_SIZE, y))

# Función para resaltar la última fila de casillas del lado derecho
def highlight_rightmost_column(screen):
    for y in range(GRID_SIZE):
        pygame.draw.rect(screen, RED, ((GRID_SIZE - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Función para dibujar los individuos
def draw_individuals(screen, individuals):
    for individual in individuals:
        color = GREEN if individual.en_meta else BLACK if individual.asesino else BLUE
        pygame.draw.rect(screen, color, (individual.x * CELL_SIZE, individual.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Función para mover a todos los individuos
def move_individuals(individuals, grid):
    for individual in individuals:
        individual.mover(grid, individuals)

# Función para dibujar información adicional
def draw_info(screen, font, turno, individuos):
    info_surface = pygame.Surface((WINDOW_SIZE // 2, WINDOW_SIZE))
    info_surface.fill(WHITE)
    pygame.draw.rect(info_surface, BLACK, info_surface.get_rect(), 2)
    
    text_turno = font.render(f"Turno: {turno}", True, BLACK)
    text_individuos = font.render(f"Individuos: {len(individuos)}", True, BLACK)
    info_surface.blit(text_turno, (10, 10))
    info_surface.blit(text_individuos, (10, 40))

    if individuos:
        for idx, ind in enumerate(individuos):
            text_id = font.render(ind.id, True, DARK_GREEN if ind.en_meta else BLACK)
            info_surface.blit(text_id, (10, 70 + idx * 30))
    screen.blit(info_surface, (WINDOW_SIZE, 0))

# Función para dibujar ganadores y sus pasos
def draw_winners(screen, font, ganadores):
    if ganadores:
        winner_surface = pygame.Surface((WINDOW_SIZE // 2, WINDOW_SIZE))
        winner_surface.fill(WHITE)
        pygame.draw.rect(winner_surface, BLACK, winner_surface.get_rect(), 2)
        
        text_ganadores = font.render("Ganadores:", True, BLACK)
        winner_surface.blit(text_ganadores, (10, 10))

        for idx, ganador in enumerate(ganadores):
            text_ganador = font.render(f"{ganador[0]}: {ganador[1]} pasos, Prob. derecha: {ganador[2]:.2f}", True, DARK_GREEN)
            winner_surface.blit(text_ganador, (10, 40 + idx * 30))
        
        screen.blit(winner_surface, (WINDOW_SIZE, 0))

# Función principal de la simulación
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE * 1.5, WINDOW_SIZE))
    pygame.display.set_caption("Algoritmo Genético - Simulación")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Inicialización de la población de individuos (cromosomas)
    population_size = 500
    population = []
    ganadores = []
    Max_turnos = 2000
    for _ in range(population_size):
        x = random.randint(0, GRID_SIZE - 3)
        y = random.randint(0, GRID_SIZE - 1)
        population.append(Individuo(x, y, probabilidad_derecha=0.11))  # Probabilidad base de 0.11 para la primera generación
    turno = 1

    running = True
    while running:
        screen.fill(WHITE)

        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        draw_grid(screen)
        highlight_rightmost_column(screen)
        draw_individuals(screen, population)
        draw_info(screen, font, turno, population)
        
        # Mover individuos y verificar si todos los puestos de la meta están ocupados
        move_individuals(population, grid)
        ganadores = [(ind.id, ind.pasos, ind.probabilidad_derecha, ind.padre_id) for ind in population if ind.en_meta]

        if len(ganadores) >= GRID_SIZE or all(ind.en_meta for ind in population) or turno == Max_turnos:
            # Ordenar ganadores por número de pasos
            ganadores.sort(key=lambda x: x[1])
            draw_winners(screen, font, ganadores)
            print(f"Ganadores: \n {', '.join([f'{ganador[0]} ({ganador[1]} pasos, P.derecha: {ganador[2]:.2f}) ' for ganador in ganadores])}""\n")
            
            #eliminar al ultimo si son ganadores impares
            print(len(ganadores))
            if not len(ganadores) % 2 == 0:
                ganadores.pop()

            # Crear nueva generación
            Individuo.generacion_actual += 1

            # Eliminar población actual
            population.clear()

            #aumentar proabilidad a la derecha de los ganadores
            for ganador in ganadores:
                ganador[2] + 0.2
            
            Numero_hijos = 0
            Numero_hijos = len(ganadores)
            restantes = population_size - Numero_hijos 

            print(Numero_hijos)
            print(restantes)
            # Generar nueva generación con herencia de probabilidad y padres
            while Numero_hijos > 0:
                for i in range(0,len(ganadores),2):
                    x = random.randint(0, GRID_SIZE - 3)
                    y = random.randint(0, GRID_SIZE - 1)
                    padre1 = ganadores[i]
                    padre2 = ganadores[i+1] 
                    probabilidad_derecha = padre1[2] + padre2[2] /2 # Suma de las probabilidades de los padres
                    padre_id = padre1[3]  # ID del primer padre
                    population.append(Individuo(x, y, probabilidad_derecha, padre_id))
                    Numero_hijos -= 1

            #los no ganadores    
            for i in range(int(restantes)):
                x = random.randint(0, GRID_SIZE - 3)
                y = random.randint(0, GRID_SIZE - 1)
                probabilidad_derecha = 0.11
                padre_id = 0
                asesino = random.random() < 0.1
                population.append(Individuo(x, y, probabilidad_derecha, padre_id, asesino))
            turno = 1
        else:
            turno += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(100)
    pygame.quit()

if __name__ == "__main__":
    main()