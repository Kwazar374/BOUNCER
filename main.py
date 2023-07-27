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

# font setup
score_font = pygame.font.Font('assets/fonts/bit5x3.ttf', 120)

# background setup
background = pygame.image.load('assets/arts/background_1.png').convert()

# paddles and ball setup
player_surf = pygame.image.load('assets/arts/player_paddle.png').convert()
player_rect = player_surf.get_rect(midleft=(10, height/2))

enemy_surf = pygame.image.load('assets/arts/enemy_paddle.png').convert()
enemy_rect = enemy_surf.get_rect(midright=(790, height/2))

ball_surf = pygame.image.load('assets/arts/ball.png').convert()
ball_rect = ball_surf.get_rect(center=(200, 200))

# bounce boost setup (1/2)
right_boost_surf = pygame.image.load('assets/arts/boost_right.png').convert()
right_boost_rect = right_boost_surf.get_rect(center=(20, 783))
bounce_boost_frames = []
for i in range(1, 18):
    bounce_boost_frames.append(pygame.image.load(f'assets/arts/circle_animation/{i}.png'))
bounce_boost_frames.append(right_boost_surf)
bounce_boost_used_surf = pygame.image.load('assets/arts/boost_right_used.png')
bounce_boost_frame = 0

# game variables setup:


# gamemode
retro_mode_on = False # not stable

# score
player_score = 0
enemy_score = 0
color_counter = 100

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
    upper_reaction_time = 62
    lower_reaction_time = 48
else:
    upper_reaction_time = 52
    lower_reaction_time = 10
reaction_time = lower_reaction_time
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
ball_starting_speed = 10
ball_speed = ball_starting_speed
ball_simulated = False
last_wall_collision = -1

# bounce boost setup (2/2)
bounce_boost_ready = True
bounce_boost_activated = False
bounce_boost_used = True
bounce_boost_value = 3
bounce_boost_update_cooldown = 400  # in milliseconds

# userevents
bounce_boost_update = pygame.USEREVENT + 1

# timers
pygame.time.set_timer(bounce_boost_update, bounce_boost_update_cooldown)

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
        if event.type == bounce_boost_update:
            if not bounce_boost_ready:
                right_boost_surf = bounce_boost_frames[bounce_boost_frame]
                if bounce_boost_frame < 17:
                    bounce_boost_frame += 1
                else: 
                    bounce_boost_frame = 0
                    bounce_boost_ready = True                  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q and bounce_boost_ready:
            bounce_boost_activated = True
            bounce_boost_used = False
            right_boost_surf = bounce_boost_used_surf
            if random.choice((False, False, True)):
                reaction_time = random.randint(lower_reaction_time-5, upper_reaction_time-32)
            elif random.choice((False, True)):
                reaction_time = random.randint(lower_reaction_time+5, upper_reaction_time-16)
            else:
                reaction_time = random.randint(lower_reaction_time+25, upper_reaction_time-8)

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
        if bounce_boost_activated and bounce_boost_used:
            ball_speed -= bounce_boost_value
            bounce_boost_activated = False
        reaction_time = random.randint(lower_reaction_time, upper_reaction_time-10)
    
    # ball (movement)
    if retro_mode_on:
        ball_rect.x += ball_speed * ball_direction
        ball_rect.y += ball_speed * ball_angle
        if ball_rect.x < -100:
            round_active = False
            if not first_bounce: enemy_score += 1
        elif ball_rect.x > width+100:
            round_active = False
            player_score += 1
    else:
        if ball_angle in (-1, 1):
            ball_rect.x += (ball_speed * math.sqrt(2) / 2) * ball_direction
            ball_rect.y += (ball_speed * math.sqrt(2) / 2) * ball_angle
        elif ball_angle == 0:
            ball_rect.x += ball_speed * ball_direction
        elif ball_angle in (-0.5, 0.5):
            ball_rect.x += (ball_speed * math.sqrt(3) / 2) * ball_direction
            ball_rect.y += (ball_speed / 2) * int(ball_angle/0.5)
        if ball_rect.x < -100:
            round_active = False
            if not first_bounce: enemy_score += 1
        elif ball_rect.x > width+100:
            round_active = False
            player_score += 1



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
            enemy_dest = random.choice((0, 1, 1))
            if enemy_rect.centery > 3 * height/4 and enemy_dest == 1:
                enemy_dest = random.randint(450, 650)
            elif enemy_rect.centery < height/4 and enemy_dest == 1:
                enemy_dest = random.randint(150, 350)
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
        if bounce_boost_activated:
            ball_speed += bounce_boost_value
            bounce_boost_used = True
            bounce_boost_ready = False
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
        if bounce_boost_activated and bounce_boost_used:
            bounce_boost_activated = False
            ball_speed -= bounce_boost_value
        if enemy_rect.centery < 300 or enemy_rect.centery > 500:
            reaction_time = random.randint(lower_reaction_time, upper_reaction_time-random.randint(6, 12))
        else:
            reaction_time = random.randint(lower_reaction_time+10, upper_reaction_time)
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

    # score
    if ball_rect.top < 250:
        color = f'grey{color_counter}'
        if color_counter > 10:
            color_counter -= 2
    elif ball_rect.top > 350:
        if color_counter < 100:
            color_counter += 2
        color = f'grey{color_counter}'
    score_text_left = score_font.render(str(player_score), False, color)
    score_text_left_rect = score_text_left.get_rect(midright = (380, 100))
    score_text_right = score_font.render(str(enemy_score), False, color)
    score_text_right_rect = score_text_right.get_rect(midleft = (440, 100))
    

    # update the screen
    screen.blit(background, (0, 0))
    screen.blit(player_surf, player_rect)
    screen.blit(enemy_surf, enemy_rect)
    screen.blit(score_text_left, score_text_left_rect)
    screen.blit(score_text_right, score_text_right_rect)
    screen.blit(right_boost_surf, right_boost_rect)
    screen.blit(ball_surf, ball_rect)

    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)


pygame.quit()