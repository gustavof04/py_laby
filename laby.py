import pygame
import random

# Dimensões da janela do jogo
WINDOW_WIDTH = 900  # Aumenta a largura da janela
WINDOW_HEIGHT = 900  # Aumenta a altura da janela

# Tamanho dos blocos do labirinto
BLOCK_SIZE = 20

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicializa o pygame
pygame.init()

# Cria a janela do jogo
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laby")

clock = pygame.time.Clock()

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    # Gera um labirinto usando o algoritmo de Prim
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        
        directions = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]
        random.shuffle(directions)
        
        found = False
        for new_x, new_y in directions:
            if 0 <= new_x < width and 0 <= new_y < height and maze[new_y][new_x] == 1:
                maze[new_y][new_x] = 0
                maze[(y + new_y) // 2][(x + new_x) // 2] = 0
                stack.append((new_x, new_y))
                found = True
                break

        if not found:
            stack.pop()

    # Define a posição de chegada do labirinto
    maze[height - 2][width - 1] = 2

    return maze

def draw_maze(maze, width, height):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if cell == 1:
                pygame.draw.rect(window, BLACK, rect)
            elif cell == 2:
                pygame.draw.rect(window, RED, rect)
            else:
                pygame.draw.rect(window, WHITE, rect)

    # Desenha um quadrado branco na posição inicial (spawn) do jogador
    spawn_x, spawn_y = (width - 45, height - 44)
    start_rect = pygame.Rect((spawn_x + 1) * BLOCK_SIZE, (spawn_y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, WHITE, start_rect)

def draw_player(player_pos):
    x, y = player_pos
    rect = pygame.Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, GREEN, rect)

def main():
    width = (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
    height = (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE

    maze = generate_maze(width, height)

    player_pos = (width - 45, height - 44)  # Posição inicial do jogador

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_pos = (player_pos[0], player_pos[1] - 1)
            if maze[new_pos[1]][new_pos[0]] in [0, 2]:
                player_pos = new_pos
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_pos = (player_pos[0], player_pos[1] + 1)
            if maze[new_pos[1]][new_pos[0]] in [0, 2]:
                player_pos = new_pos
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_pos = (player_pos[0] - 1, player_pos[1])
            if maze[new_pos[1]][new_pos[0]] in [0, 2]:
                player_pos = new_pos
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_pos = (player_pos[0] + 1, player_pos[1])
            if maze[new_pos[1]][new_pos[0]] in [0, 2]:
                player_pos = new_pos

        window.fill(BLACK)
        draw_maze(maze, width, height)
        draw_player(player_pos)

        if maze[player_pos[1]][player_pos[0]] == 2:
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(15)

if __name__ == '__main__':
    main()
