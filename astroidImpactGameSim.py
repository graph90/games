import pygame
import sys
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
MOON_COLOR = (150, 150, 150)
ASTEROID_COLOR = (255, 0, 0)
MOON_RADIUS = 50
ASTEROID_RADIUS = 10
ASTEROID_SPEED = 3

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Impact Simulator")
clock = pygame.time.Clock()

def calculate_orbit_position(center_x, center_y, distance, angle):
    x = int(center_x + distance * math.cos(angle))
    y = int(center_y + distance * math.sin(angle))
    return x, y

running = True
moon_x, moon_y = WIDTH // 2, HEIGHT // 2
asteroid_x, asteroid_y = WIDTH // 4, HEIGHT // 4

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    moon_angle = pygame.time.get_ticks() * 0.01
    moon_x, moon_y = calculate_orbit_position(WIDTH // 2, HEIGHT // 2, MOON_RADIUS, moon_angle)

    asteroid_x += ASTEROID_SPEED

    distance = math.sqrt((asteroid_x - moon_x)**2 + (asteroid_y - moon_y)**2)
    if distance < MOON_RADIUS + ASTEROID_RADIUS:
        print("Asteroid impacted the Moon!")
        running = False

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, MOON_COLOR, (moon_x, moon_y), MOON_RADIUS)
    pygame.draw.circle(screen, ASTEROID_COLOR, (int(asteroid_x), int(asteroid_y)), ASTEROID_RADIUS)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
