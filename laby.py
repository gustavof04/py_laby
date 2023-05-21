import pygame
import random
import time

# Dimensões da janela do Laby
WINDOW_WIDTH = 900  # Aumenta a largura
WINDOW_HEIGHT = 900  # Aumenta a altura

# Tamanho dos blocos do labirinto
BLOCK_SIZE = 20

# Paleta de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 223, 0)
TRANSPARENT_RED = (255, 0, 0, 128)

# Inicializa o pygame
pygame.init()

# Cria a janela do jogo
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laby")

# Controla o framerate do Laby
clock = pygame.time.Clock()

# Gera labirintos usando o algoritmo de Prim
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

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

# Desenha o labirinto na janela
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

    # Desenha um caminho no spawn do jogador
    spawn_x, spawn_y = (width - 45, height - 44)
    start_rect = pygame.Rect((spawn_x + 1) * BLOCK_SIZE, (spawn_y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, WHITE, start_rect)

# Desenha o jogador na janela
def draw_player(player_pos):
    x, y = player_pos
    rect = pygame.Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, GREEN, rect)

# Exibe mensagens no meio da tela
def display_message(msg):
    font = pygame.font.Font(None, 70)
    text = font.render(msg, True, GOLD)
    shadow = font.render(msg, True, (100, 100, 100))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
    window.blit(shadow, shadow_rect)
    window.blit(text, text_rect)

# Fim de jogo
def game_over():
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(TRANSPARENT_RED)
    window.blit(overlay, (0, 0))
    display_message("Tempo esgotado! Você perdeu.")

# Recomeça o jogo
def reset_game(width, height):
    maze = generate_maze(width, height)
    player_pos = (width - 45, height - 44)  # Posição inicial do jogador
    return maze, player_pos

# Núcleo principal do Laby
def main():
    width = (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
    height = (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE

    maze, player_pos = reset_game(width, height)

    start_time = time.time()
    countdown_duration = 60
    elapsed_time = 0
    blinking = False
    blink_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Atalhos
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

        elapsed_time = int(time.time() - start_time) # Tempo total de jogo

        remaining_time = max(0, countdown_duration - elapsed_time) # Tempo restante

        # Desenhando o labirinto e o jogador...
        window.fill(BLACK)
        draw_maze(maze, width, height)
        draw_player(player_pos)

        # Exibe o tempo restante + efeito pisca-pisca quando faltar 10 segundos
        if remaining_time <= 10:
            blink_timer += clock.get_rawtime()
            if blink_timer >= 50:
                blinking = not blinking
                blink_timer = 0
            if blinking:
                font = pygame.font.Font(None, 24)
                time_text = font.render("Tempo restante: {} segundos".format(remaining_time), True, RED)
            else:
                font = pygame.font.Font(None, 24)
                time_text = font.render("Tempo restante: {} segundos".format(remaining_time), True, WHITE)
        else:
            font = pygame.font.Font(None, 24)
            time_text = font.render("Tempo restante: {} segundos".format(remaining_time), True, WHITE)

        # Posicionando o tempo restante...
        time_rect = time_text.get_rect(topleft=(3, 3))
        window.blit(time_text, time_rect)

        # Condicional de derrota
        if remaining_time <= 0:
            game_over()
            pygame.display.flip()
            pygame.time.wait(3000)
            maze, player_pos = reset_game(width, height)
            start_time = time.time()

        # Condicional de vitória
        if maze[player_pos[1]][player_pos[0]] == 2:
            display_message("Você escapou do labirinto!")
            pygame.display.flip()
            pygame.time.wait(3000)  # Aguarda 3 segundos
            maze, player_pos = reset_game(width, height)
            start_time = time.time()

        pygame.display.flip() # Atualiza janela
        clock.tick(15) # Limita a 15 fps

if __name__ == '__main__':
    main()
