import pygame
import random

# pygame setup
pygame.init()
width, height = screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('PONG BY KWAZAR374')
icon = pygame.image.load('assets/arts/iconB.png').convert()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True

# background setup
background = pygame.image.load('assets/arts/background_1.png').convert()

# paddles and ball setup
player_surf = pygame.image.load('assets/arts/paddle.png').convert()
player_rect = player_surf.get_rect(midleft=(10, 250))

enemy_surf = pygame.image.load('assets/arts/paddle.png').convert()
enemy_rect = enemy_surf.get_rect(midright=(790, 250))

ball_surf = pygame.image.load('assets/arts/ball.png').convert()
ball_rect = ball_surf.get_rect(center=(200, 200))

# game variables setup:
# paddle
paddle_acceleration = 2
paddle_speed = 0
paddle_speed_limit = 10

# ball
round_active = False
ball_direction = -1 # -1 if ball goes left and 1 if ball goes right
ball_angle = 0 # =========================================
# 1 if ball flies down at a 45-degree angle to the paddle
# 0 if ball flies perpendicular to the paddle
# -1 if ball flies up at a 45-degree angle to the paddle
ball_speed = 8

# game loop
while running:

    #event loop
    for event in pygame.event.get():
        # window actions
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        
    # ball (start procedure)
    if not round_active:
        ball_start_y_pos = random.choice((random.randint(20, 90), random.randint(height-90, height-20)))
        ball_rect.center = (width/2, ball_start_y_pos)
        round_active = True
        ball_direction = -1
        if ball_start_y_pos < height/2:
            ball_angle = 1
        else:
            ball_angle = -1
    
    # ball (movement)
    ball_rect.x += ball_speed * ball_direction
    ball_rect.y += ball_speed * ball_angle
    if ball_rect.x < 0 or ball_rect.x > width:
        round_active = False

    # player movement
    keys_pressed = pygame.key.get_pressed()
    if not (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]):
        paddle_speed = 0
    elif paddle_speed < paddle_speed_limit:
        paddle_speed += paddle_acceleration
    if keys_pressed[pygame.K_w]:
        player_rect.top -= paddle_speed
        if player_rect.top < 0: player_rect.top = 5
    if keys_pressed[pygame.K_s]:
        player_rect.bottom += paddle_speed
        if player_rect.bottom > height: player_rect.bottom = height-5

    # collisions
    # ball with player
    if player_rect.colliderect(ball_rect) == True:
        collision_point = ball_rect.midleft
        ball_direction = 1
        if collision_point[1] - player_rect.topright[1] < 20:
            ball_angle = -1
        elif collision_point[1] - player_rect.topright[1] < 34:
            ball_angle = 0
        else:
            ball_angle = 1
    # ball with walls
    if ball_rect.midbottom[1] <= 0 or ball_rect.midbottom[1] >= height:
        ball_angle *= -1

    # update the screen
    screen.blit(background, (0, 0))
    screen.blit(player_surf, player_rect)
    screen.blit(enemy_surf, enemy_rect)
    screen.blit(ball_surf, ball_rect)

    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)


pygame.quit()