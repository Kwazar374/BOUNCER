import pygame
import random

# pygame setup
pygame.init()
width, height = screen_size = (800, 800)
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
paddle_speed = paddle_start_speed = 2
paddle_speed_limit = 10
second_paddle_speed = paddle_start_speed

# ball
round_active = False
ball_direction = -1 # -1 if ball goes left and 1 if ball goes right
ball_angle = 0 # =========================================
# 1 if ball flies down at a 45-degree angle to the paddle
# 0 if ball flies perpendicular to the paddle
# -1 if ball flies up at a 45-degree angle to the paddle
ball_speed = 7
ball_simulated = False

# methods
# below method works more precisely when ball_speed is taken into account,
# because collision point depend on speeds of the colliding objects
def calculate_ball_trajectory(ball_cords, ball_dir, ball_ang):
    if ball_ang == 0:
        if ball_dir == -1:
            return (26, ball_cords[1])
        else:
            return (783, ball_cords[1])
    elif ball_dir == 1 and ball_ang == -1:
        if ball_cords[1] + ball_cords[0] < 800:
            ball_cords = (ball_cords[1] + ball_cords[0] - 5, 5)
            ball_ang *= -1
            return calculate_ball_trajectory(ball_cords, ball_dir, ball_ang)
        else:
            return (783, ball_cords[1] - (800 - ball_cords[0]) + 5)
    elif ball_dir == 1 and ball_ang == 1:
        if 800 - ball_cords[1] + ball_cords[0] < 800:
            ball_cords = (800 - ball_cords[1] + ball_cords[0] - 5, 795)
            ball_ang *= -1
            return calculate_ball_trajectory(ball_cords, ball_dir, ball_ang)
        else:
            return (783, ball_cords[1] + (800 - ball_cords[0]) - 5)
    else:
        return 0
    
def simulate_ball_trajectory(ball_rects, ball_dir, ball_ang, ball_sped):
    while ball_rects.right < enemy_rect.left: 
        ball_rects.x += ball_sped * ball_dir
        ball_rects.y += ball_sped * ball_ang
        if ball_rects.midtop[1] <= 0 or ball_rects.midbottom[1] >= height:
            ball_ang *= -1
    return ball_rects.centery
        

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
        ball_start_y_pos = random.choice((random.randint(20, 250), random.randint(height-250, height-20)))
        ball_rect.center = (width/2, ball_start_y_pos)
        round_active = True
        ball_direction = -1
        ball_angle = random.choice((-1, 1))
    
    # ball (movement)
    ball_rect.x += ball_speed * ball_direction
    ball_rect.y += ball_speed * ball_angle
    if ball_rect.x < -100 or ball_rect.x > width+100:
        round_active = False

    # player movement
    keys_pressed = pygame.key.get_pressed()
    if not (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]):
        paddle_speed = paddle_start_speed
    elif paddle_speed < paddle_speed_limit:
        paddle_speed += paddle_acceleration
    if keys_pressed[pygame.K_w]:
        player_rect.top -= paddle_speed
        if player_rect.top < 0: player_rect.top = 5
    if keys_pressed[pygame.K_s]:
        player_rect.bottom += paddle_speed
        if player_rect.bottom > height: player_rect.bottom = height-5

    # enemy movement
    if ball_direction == 1 and not ball_simulated:
        bounce_point  = simulate_ball_trajectory(ball_rect.copy(), ball_direction, ball_angle, ball_speed)
        enemy_rect.centery = bounce_point
        ball_simulated = True

    # collisions
    # ball with player
    if player_rect.colliderect(ball_rect) == True:
        collision_point = ball_rect.midleft
        ball_direction = 1
        if collision_point[1] - player_rect.topright[1] < 33:
            ball_angle = -1
        elif collision_point[1] - player_rect.topright[1] < 47:
            ball_angle = 0
        else:
            ball_angle = 1
    # ball with enemy
    if enemy_rect.colliderect(ball_rect) == True:
        collision_point = ball_rect.midright
        ball_direction = -1
        if collision_point[1] - enemy_rect.topleft[1] < 33:
            ball_angle = -1
        elif collision_point[1] - enemy_rect.topleft[1] < 47:
            ball_angle = 0
        else:
            ball_angle = 1
        ball_simulated = False
    # ball with walls
    if ball_rect.midtop[1] <= 0 or ball_rect.midbottom[1] >= height:
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