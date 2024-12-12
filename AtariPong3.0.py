import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Configuración de la paleta y la pelota
paddle_width, paddle_height = 10, 100
ball_size = 15

# Posiciones iniciales
left_paddle = pygame.Rect(30, (HEIGHT - paddle_height) // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 30 - paddle_width, (HEIGHT - paddle_height) // 2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_size, ball_size)

# Velocidades
ball_speed_x, ball_speed_y = 5, 5
paddle_speed = 10

# Marcador
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)

# Estado del juego
game_started = False

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            game_started = True

    # Dibujo pantalla
    screen.fill(BLACK)

    if not game_started:
        # Dibujo pantalla de inicio
        play_text = font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(play_text, play_rect)
        pygame.draw.rect(screen, GREEN, (play_rect.left - 20, play_rect.top - 20, play_rect.width + 40, play_rect.height + 40), 2)
    else:
        # Movimiento de las palas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # Movimiento de la pelota
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Colisiones con las paredes
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x = -ball_speed_x

        # Reinicio pelota si sale de la pantalla
        if ball.left <= 0:
            right_score += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball_speed_x = -ball_speed_x
        if ball.right >= WIDTH:
            left_score += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball_speed_x = -ball_speed_x

        # Verificar si algún jugador ha alcanzado los 10 puntos
        if left_score == 10 or right_score == 10:
            game_started = False
            winner_text = font.render("Game Over", True, WHITE)
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(winner_text, winner_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Dibujo pantalla
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Marcador
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width(), 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
