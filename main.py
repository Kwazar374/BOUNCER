import pygame
import random
import math

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
player_surf = pygame.image.load('assets/arts/player_paddle.png').convert()
player_rect = player_surf.get_rect(midleft=(10, height/2))

enemy_surf = pygame.image.load('assets/arts/enemy_paddle.png').convert()
enemy_rect = enemy_surf.get_rect(midright=(790, height/2))

ball_surf = pygame.image.load('assets/arts/ball.png').convert()
ball_rect = ball_surf.get_rect(center=(200, 200))

# game variables setup:

# gamemode
retro_mode_on = False

# paddle
paddle_acceleration = 2
paddle_speed = paddle_start_speed = 2
paddle_speed_limit = 12

# enemy
enemy_acceleration = 1
enemy_speed = enemy_start_speed = 1
enemy_speed_limit = 12
reaction_counter = 0
if retro_mode_on:
    reaction_time = 58
else:
    reaction_time = 44
random_dest_set = False

# ball
round_active = False
ball_direction = -1 # -1 if ball goes left and 1 if ball goes right
ball_angle = 0 # =========================================
# 1 if ball flies down at a 45-degree angle to the paddle
# (non-retro mode) 0.5 if ball flies down at a 60-degree angle to the paddle
# 0 if ball flies perpendicular to the paddle
# (non-retro mode) -0.5 if ball flies up at a 60-degree angle to the paddle
# -1 if ball flies up at a 45-degree angle to the paddle
ball_speed = 9
ball_simulated = False
last_wall_collision = -1

# methods
    
def simulate_ball_trajectory(ball_rects, ball_dir, ball_ang, ball_sped):
    if retro_mode_on:
        while ball_rects.right < enemy_rect.left: 
            ball_rects.x += ball_sped * ball_dir
            ball_rects.y += ball_sped * ball_ang
            if ball_rects.midtop[1] <= 0 or ball_rects.midbottom[1] >= height:
                ball_ang *= -1
        return ball_rects.centery
    else:
        last_wall_collision_counter = 20
        while ball_rects.right < enemy_rect.left:
            last_wall_collision_counter += 1
            if ball_ang in (-1, 1):
                ball_rects.x += (ball_sped * math.sqrt(2) / 2) * ball_dir
                ball_rects.y += (ball_sped * math.sqrt(2) / 2) * ball_ang
            elif ball_ang == 0:
                ball_rects.x += ball_sped * ball_dir
            elif ball_ang in (-0.5, 0.5):
                ball_rects.x += (ball_sped * math.sqrt(3) / 2) * ball_dir
                ball_rects.y += (ball_sped / 2) * int(ball_ang/0.5)
            if ball_rects.midtop[1] <= 0 or ball_rects.midbottom[1] >= height:
                if retro_mode_on:
                    ball_ang *= -1
                elif last_wall_collision_counter > 20:
                    # in some specific cases wall-ball collision procedure was called several times 
                    # in short time intervals and it was resulting in ball glitches
                    ball_ang *= -1
                    last_wall_collision_counter = 0
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
        reaction_counter = 0
        first_bounce = True
        ball_simulated = False
        ball_direction = -1
        ball_angle = random.choice((-1, 1))
    
    # ball (movement)
    if retro_mode_on:
        ball_rect.x += ball_speed * ball_direction
        ball_rect.y += ball_speed * ball_angle
        if ball_rect.x < -100 or ball_rect.x > width+100:
            round_active = False
    else:
        if ball_angle in (-1, 1):
            ball_rect.x += (ball_speed * math.sqrt(2) / 2) * ball_direction
            ball_rect.y += (ball_speed * math.sqrt(2) / 2) * ball_angle
        elif ball_angle == 0:
            ball_rect.x += ball_speed * ball_direction
        elif ball_angle in (-0.5, 0.5):
            ball_rect.x += (ball_speed * math.sqrt(3) / 2) * ball_direction
            ball_rect.y += (ball_speed / 2) * int(ball_angle/0.5)
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
        if player_rect.top < -5: player_rect.top = -5
    if keys_pressed[pygame.K_s]:
        player_rect.bottom += paddle_speed
        if player_rect.bottom > height+5: player_rect.bottom = height+5

    # enemy movement
    if ball_direction == 1:
        if reaction_counter > reaction_time:
            if not ball_simulated:
                bounce_point  = simulate_ball_trajectory(ball_rect.copy(), ball_direction, ball_angle, ball_speed)
                enemy_dest = bounce_point + random.choice((-20, 0, 20))
                if enemy_dest + enemy_rect.height//2 > height - 5:
                    enemy_dest -= enemy_dest + enemy_rect.height//2 - height + 5
                elif enemy_dest - enemy_rect.height//2 < 5:
                    enemy_dest += enemy_rect.height//2 - enemy_dest + 5
                ball_simulated = True

            if enemy_dest == enemy_rect.centery:
                enemy_speed = enemy_start_speed
            else:
                if enemy_speed < enemy_speed_limit:
                    enemy_speed += enemy_acceleration
                if abs(enemy_dest - enemy_rect.centery) < enemy_speed:
                    enemy_speed = enemy_start_speed
                else:
                    if enemy_dest < enemy_rect.centery:
                        enemy_rect.centery -= enemy_speed
                    elif enemy_dest > enemy_rect.centery:
                        enemy_rect.centery += enemy_speed
        else:
            reaction_counter += 1
    elif first_bounce:
        enemy_dest = height/2
        if enemy_dest == enemy_rect.centery:
            enemy_speed = enemy_start_speed
        else:
            if enemy_speed < enemy_speed_limit:
                enemy_speed += enemy_acceleration
            if abs(enemy_dest - enemy_rect.centery) < enemy_speed:
                enemy_speed = enemy_start_speed
            else:
                if enemy_dest < enemy_rect.centery:
                    enemy_rect.centery -= enemy_speed
                elif enemy_dest > enemy_rect.centery:
                    enemy_rect.centery += enemy_speed
    else:
        if not random_dest_set:
            enemy_dest = random.choice((0, 1))
            if enemy_rect.centery > 3 * height/4 and enemy_dest == 1:
                enemy_dest = random.randint(300, 600)
            elif enemy_rect.centery < height/4 and enemy_dest == 1:
                enemy_dest = random.randint(200, 500)
            else:
                enemy_dest = 0
            random_dest_set = True
        if enemy_dest != 0:
            if enemy_dest == enemy_rect.centery:
                enemy_speed = enemy_start_speed
            else:
                if enemy_speed < enemy_speed_limit:
                    enemy_speed += enemy_acceleration
                if abs(enemy_dest - enemy_rect.centery) < enemy_speed:
                    enemy_speed = enemy_start_speed
                else:
                    if enemy_dest < enemy_rect.centery:
                        enemy_rect.centery -= enemy_speed
                    elif enemy_dest > enemy_rect.centery:
                        enemy_rect.centery += enemy_speed
                

        

    # collisions
    # ball with player
    if player_rect.colliderect(ball_rect) == True:
        if retro_mode_on:
            collision_point = ball_rect.midleft
            ball_direction = 1
            if collision_point[1] - player_rect.topright[1] < 30:
                ball_angle = -1
            elif collision_point[1] - player_rect.topright[1] < 50:
                ball_angle = 0
            else:
                ball_angle = 1
        else:
            collision_point = ball_rect.midleft
            ball_direction = 1
            if collision_point[1] - player_rect.topright[1] < 30:
                ball_angle = -0.5
            elif collision_point[1] - player_rect.topright[1] < 50:
                ball_angle = 0
            else:
                ball_angle = 0.5
        first_bounce = False
    # ball with enemy
    if enemy_rect.colliderect(ball_rect) == True:
        random_dest_set = False
        if retro_mode_on:
            collision_point = ball_rect.midright
            ball_direction = -1
            if collision_point[1] - enemy_rect.topleft[1] < 23:
                ball_angle = -1
            elif collision_point[1] - enemy_rect.topleft[1] < 47:
                ball_angle = 0
            else:
                ball_angle = 1
        else:
            collision_point = ball_rect.midright
            ball_direction = -1
            if collision_point[1] - enemy_rect.topleft[1] < 23:
                ball_angle = -0.5
            elif collision_point[1] - enemy_rect.topleft[1] < 47:
                ball_angle = 0
            else:
                ball_angle = 0.5
        ball_simulated = False
        reaction_counter = 0
    # ball with walls
    if ball_rect.midtop[1] <= 0 or ball_rect.midbottom[1] >= height:
        if retro_mode_on:
            ball_angle *= -1
        else:
            # in some specific cases wall-ball collision procedure was called several times 
            # in short time intervals and it was resulting in ball glitches
            if last_wall_collision == -1 or pygame.time.get_ticks() - last_wall_collision > 20:
                ball_angle *= -1
                last_wall_collision = pygame.time.get_ticks()


    # update the screen
    screen.blit(background, (0, 0))
    screen.blit(player_surf, player_rect)
    screen.blit(enemy_surf, enemy_rect)
    screen.blit(ball_surf, ball_rect)

    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)


pygame.quit()