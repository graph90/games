import pygame,sys
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
maze = [
    "WWWWWWWWWWWW",
    "W          W",
    "W   WWWWW  W",
    "W   W      W",
    "W   W  W   W",
    "W   W  W   W",
    "W   W  W   W",
    "W   W  W   W",
    "W   W     GW",
    "WWWWWWWWWWWW",
]
player_x, player_y = 1, 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and maze[player_y - 1][player_x] == " ":
        player_y -= 1
    if keys[pygame.K_DOWN] and maze[player_y + 1][player_x] == " ":
        player_y += 1
    if keys[pygame.K_LEFT] and maze[player_y][player_x - 1] == " ":
        player_x -= 1
    if keys[pygame.K_RIGHT] and maze[player_y][player_x + 1] == " ":
        player_x += 1
    screen.fill(black)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "W":
                pygame.draw.rect(screen, white, (x * 60, y * 60, 60, 60))
            elif cell == "G":
                pygame.draw.rect(screen, green, (x * 60, y * 60, 60, 60))
            elif cell == " ":
                pygame.draw.rect(screen, black, (x * 60, y * 60, 60, 60))

    pygame.draw.rect(screen, red, (player_x * 60, player_y * 60, 60, 60))
    pygame.display.flip()
