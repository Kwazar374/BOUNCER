import pygame

# pygame setup
pygame.init()
width, height = screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('PONG BY KWAZAR374')
icon = pygame.image.load('assets/arts/iconB.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True

# background setup
background = pygame.image.load('assets/arts/background_1.png')

# paddles and ball setup
player_surf = pygame.image.load('assets/arts/paddle.png').convert()
player_rect = player_surf.get_rect(midleft=(10, 250))

enemy_surf = pygame.image.load('assets/arts/paddle.png').convert()
enemy_rect = enemy_surf.get_rect(midright=(790, 250))

ball_surf = pygame.image.load('assets/arts/ball.png').convert()
ball_rect = ball_surf.get_rect(center=(200, 200))

# game variables setup:
paddle_acceleration = 3
paddle_speed = 0

# game loop
while running:

    #event loop
    for event in pygame.event.get():
        # window actions
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        

    # player movement
    keys_pressed = pygame.key.get_pressed()
    if not (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]):
        paddle_speed = 0
    elif paddle_speed < 15:
        paddle_speed += paddle_acceleration
    if keys_pressed[pygame.K_w]:
        player_rect.top -= paddle_speed
        if player_rect.top < 0: player_rect.top = 5
    if keys_pressed[pygame.K_s]:
        player_rect.bottom += paddle_speed
        if player_rect.bottom > height: player_rect.bottom = height-5

    print(player_rect.top, player_rect.bottom)
    

    # update the screen
    screen.blit(background, (0, 0))
    screen.blit(player_surf, player_rect)
    screen.blit(enemy_surf, enemy_rect)
    screen.blit(ball_surf, ball_rect)

    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)


pygame.quit()