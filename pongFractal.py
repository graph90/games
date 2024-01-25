import pygame
import sys
import random
import math

pygame.init()

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 130
MIN_BALL_SIZE, MAX_BALL_SIZE = 20, 40
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPARK_SIZE = 3
SPARK_SPEED = 10
SPARK_COUNT = 20

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Pong Fractal")

WIDTH, HEIGHT = pygame.display.get_surface().get_size()

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
balls = [{'rect': pygame.Rect(WIDTH // 2 - MIN_BALL_SIZE // 2, HEIGHT // 2 - MIN_BALL_SIZE // 2, MIN_BALL_SIZE, MIN_BALL_SIZE),'speed': [5, 5],'size': MIN_BALL_SIZE}]

sparks = []

fractal_frames = 30
fractal_frame_count = 0

trail_length = 15
trails = []

elapsed_time = 0
new_ball_timer = 0

def generate_sparks(position):
    for _ in range(SPARK_COUNT):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, SPARK_SPEED)
        sparks.append([position[0], position[1], math.cos(angle) * speed, math.sin(angle) * speed])

def show_start_menu():
    font_title = pygame.font.Font(None, 100)
    font_prompt = pygame.font.Font(None, 74)

    title_text = font_title.render("Pong Fractal", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    prompt_text = font_prompt.render("Press Space to Start", True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(title_text, title_rect)
    screen.blit(prompt_text, prompt_rect)

def show_pause_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Paused - Press P to Resume", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_flaming_trail(positions, size):
    for pos in positions:
        flame_size = size + random.randint(-5, 5)
        flame_color = (255, random.randint(50, 150), 0)
        pygame.draw.ellipse(screen, flame_color, (pos[0] - flame_size // 2, pos[1] - flame_size // 2, flame_size, flame_size), 2)

start_menu_active = True
pause_menu_active = False
clock = pygame.time.Clock()

while True:
    dt = clock.tick(FPS) / 1000
    elapsed_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif event.key == pygame.K_SPACE and start_menu_active:
                start_menu_active = False
                for ball in balls:
                    ball['speed'] = [5, 5]
            elif event.key == pygame.K_p and not start_menu_active:
                pause_menu_active = not pause_menu_active
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_m and not start_menu_active:
                start_menu_active = True

    if start_menu_active:
        show_start_menu()
    elif pause_menu_active:
        show_pause_menu()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= 7
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += 7

        if balls and opponent_paddle.centery < balls[0]['rect'].centery and opponent_paddle.bottom < HEIGHT:
            opponent_paddle.y += 5
        elif balls and opponent_paddle.centery > balls[0]['rect'].centery and opponent_paddle.top > 0:
            opponent_paddle.y -= 5

        for ball in balls:
            ball['rect'].x += ball['speed'][0]
            ball['rect'].y += ball['speed'][1]

            if ball['rect'].top <= 0 or ball['rect'].bottom >= HEIGHT:
                ball['speed'][1] = -ball['speed'][1]

            if ball['rect'].colliderect(player_paddle):
                ball['speed'][0] = -ball['speed'][0]
                generate_sparks([player_paddle.right, ball['rect'].centery])
                fractal_frame_count = 0
                ball['size'] = MAX_BALL_SIZE
            elif ball['rect'].colliderect(opponent_paddle):
                ball['speed'][0] = -ball['speed'][0]
                generate_sparks([opponent_paddle.left - SPARK_SIZE, ball['rect'].centery])
                fractal_frame_count = 0
                ball['size'] = MAX_BALL_SIZE
            else:
                ball['size'] = MIN_BALL_SIZE

            if ball['rect'].left <= 0 or ball['rect'].right >= WIDTH:
                ball['speed'] = [5, 5]
                ball['rect'].x = WIDTH // 2 - ball['size'] // 2
                ball['rect'].y = HEIGHT // 2 - ball['size'] // 2

            sparks = [[x + dx, y + dy, dx, dy] for x, y, dx, dy in sparks]
            sparks = [spark for spark in sparks if 0 <= spark[0] <= WIDTH and 0 <= spark[1] <= HEIGHT]

            trails.append((ball['rect'].x, ball['rect'].y))
            if len(trails) > trail_length:
                trails.pop(0)

        screen.fill(BLACK)

        draw_flaming_trail(trails, ball['size'])

        for ball in balls:
            if fractal_frame_count < fractal_frames:
                fractal_factor = math.sin((fractal_frame_count / fractal_frames) * math.pi) ** 2
                fractal_size = ball['size'] * fractal_factor
                fractal_rect = pygame.Rect(ball['rect'].x - (fractal_size - ball['size']) / 2, ball['rect'].y - (fractal_size - ball['size']) / 2, fractal_size, fractal_size)
                pygame.draw.rect(screen, WHITE, fractal_rect)
                fractal_frame_count += 1
            else:
                pygame.draw.ellipse(screen, WHITE, ball['rect'])

        pygame.draw.rect(screen, (100, 100, 255), player_paddle, border_radius=5)
        pygame.draw.rect(screen, (255, 100, 100), opponent_paddle, border_radius=5)

        for spark in sparks:
            pygame.draw.circle(screen, WHITE, (int(spark[0]), int(spark[1])), SPARK_SIZE)

        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        pygame.display.flip()

        new_ball_timer += dt
        if new_ball_timer >= 30:
            new_ball_timer = 0
            new_ball = {'rect': pygame.Rect(WIDTH // 2 - MIN_BALL_SIZE // 2, HEIGHT // 2 - MIN_BALL_SIZE // 2, MIN_BALL_SIZE, MIN_BALL_SIZE),'speed': [5, 5],'size': MIN_BALL_SIZE}
balls.append(new_ball)
