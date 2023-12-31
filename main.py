import pygame
import random
import math

from pygame import mixer

# pygame setup
pygame.init()
width, height = screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('BOUNCER BY KWAZAR374')
icon = pygame.image.load('assets/arts/iconB.png').convert()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True

# SFX
bounce_sfx = mixer.Sound('assets/music/bounce_sfx.ogg')

# font setup
score_font = pygame.font.Font('assets/fonts/bit5x3.ttf', 120)
bounce_counter_font = pygame.font.Font('assets/fonts/bit5x3.ttf', 20)
game_menu_font = pygame.font.Font('assets/fonts/bit5x3.ttf', 60)
main_menu_font_p = pygame.font.Font('assets/fonts/bit5x5.ttf', 50)
main_menu_font_h = pygame.font.Font('assets/fonts/bit5x5.ttf', 140)
credits_font = pygame.font.Font('assets/fonts/bit5x5.ttf', 30)
credits_font_2 = pygame.font.Font('assets/fonts/bit5x5.ttf', 15)
credits_header_font = pygame.font.Font('assets/fonts/bit5x5.ttf', 70)
pause_font = pygame.font.Font('assets/fonts/bit5x5.ttf', 13)

# background setup
background = pygame.image.load('assets/arts/background_1.png').convert()

# paddles and ball setup
player_surf = pygame.image.load('assets/arts/player_paddle.png').convert()
player_rect = player_surf.get_rect(midright=(21, height/2))

enemy_surf = pygame.image.load('assets/arts/enemy_paddle.png').convert()
enemy_rect = enemy_surf.get_rect(midleft=(779, height/2))

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

# pause setup
pause_surf = pygame.image.load('assets/arts/pause_button.png').convert()
pause_rect = pause_surf.get_rect(topright=(795, 5))
show_pause_button = True

# sfx_on and sfx_off buttons setup
sfx_on_surf = pygame.image.load('assets/arts/sfx_on.png').convert()
sfx_on_surf = pygame.transform.scale_by(sfx_on_surf, (3, 3))
sfx_off_surf = pygame.image.load('assets/arts/sfx_off.png').convert()
sfx_off_surf = pygame.transform.scale_by(sfx_off_surf, (3, 3))
sfx_off_rect = sfx_on_rect = sfx_on_surf.get_rect(center=(765, 40))

sfx_active = True

# game restart setup
game_restart = True

# menu variables setup:
main_menu_active = False

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

def main_menu():
    global main_menu_active
    global running
    global game_restart

    main_menu_active = True

    main_menu_header_text = main_menu_font_h.render('BOUNCER', False, 'white')
    main_menu_header_rect = main_menu_header_text.get_rect(midleft=(30, 95))

    main_menu_rect = pygame.rect.Rect(30, 195, 20, 260)

    while main_menu_active:

        play_button_text = main_menu_font_p.render('PLAY', False, 'white')
        play_rect_col = 'black'
        play_button_rect = play_button_text.get_rect(midleft=(70, 230))

        credits_button_text = main_menu_font_p.render('CREDITS', False, 'white')
        credits_rect_col = 'black'
        credits_rect = credits_button_text.get_rect(midleft=(70, 310))

        exit_button_text = main_menu_font_p.render('EXIT', False, 'white')
        exit_rect_col = 'black'
        exit_rect = exit_button_text.get_rect(midleft=(70, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_active = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu_active = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    main_menu_active = False
                if credits_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    credits()
                if exit_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    main_menu_active = False
                    running = False

        if main_menu_active:
            if play_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                play_button_text = main_menu_font_p.render('PLAY', False, 'black')
                play_rect_col = 'white'
            play_button_rect_to_display = pygame.Rect.inflate(play_button_rect, 15, 15)
            play_button_rect_to_display = play_button_rect_to_display.move(0, -3)

            if credits_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                credits_button_text = main_menu_font_p.render('CREDITS', False, 'black')
                credits_rect_col = 'white'
            credits_rect_to_display = pygame.Rect.inflate(credits_rect, 15, 15)
            credits_rect_to_display = credits_rect_to_display.move(0, -3)

            if exit_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                exit_button_text = main_menu_font_p.render('EXIT', False, 'black')
                exit_rect_col = 'white'
            exit_rect_to_display = pygame.Rect.inflate(exit_rect, 15, 15)
            exit_rect_to_display = exit_rect_to_display.move(0, -3)

            screen.fill('black')
            pygame.draw.rect(screen, play_rect_col, play_button_rect_to_display)
            pygame.draw.rect(screen, credits_rect_col, credits_rect_to_display)
            pygame.draw.rect(screen, exit_rect_col, exit_rect_to_display)
            pygame.draw.rect(screen, 'white', main_menu_rect)
            screen.blit(main_menu_header_text, main_menu_header_rect)
            screen.blit(play_button_text, play_button_rect)
            screen.blit(credits_button_text, credits_rect)
            screen.blit(exit_button_text, exit_rect)

            pygame.display.update()

def credits():
    credits_active = True
    global running
    global main_menu_active
    global icon

    credits_header_text = credits_header_font.render('Credits', False, 'white')
    credits_header_rect = credits_header_text.get_rect(midleft=(25, 90))

    icon_surf = icon
    icon_rect = icon_surf.get_rect(midleft=(60, 500))

    credits_rect = pygame.rect.Rect(25, 186, 15, 550)

    credits_lines = [
        'Code, Art:     Kwazar374',
        'Fonts:     www.mattlag.com/bitfonts/',
        'Inspiration:   Atari Pong from 1972',
        'SFX:  www.opengameart.org/content/3-ping-pong-sounds-8-bit-style'
    ]

    while credits_active:

        back_button_text = main_menu_font_p.render('BACK', False, 'white')
        back_rect_col = 'black'
        back_button_rect = back_button_text.get_rect(midleft=(60, 700))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_active = False
                running = False
                credits_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    credits_active = False

        if credits_active:  
            screen.fill('black')
            screen.blit(credits_header_text, credits_header_rect)

            if back_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                back_button_text = main_menu_font_p.render('BACK', False, 'black')
                back_rect_col = 'white'
            back_button_rect_to_display = pygame.Rect.inflate(back_button_rect, 15, 15)
            back_button_rect_to_display = back_button_rect_to_display.move(0, -3)
            
            pygame.draw.rect(screen, back_rect_col, back_button_rect_to_display)
            screen.blit(back_button_text, back_button_rect)

            pygame.draw.rect(screen, 'white', credits_rect)

            screen.blit(icon_surf, icon_rect)

            x_coord = 60
            y_coord = 200
            for line in credits_lines:
                if line[0:3] == 'SFX':
                    text = credits_font_2.render(line, False, 'white')
                else:
                    text = credits_font.render(line, False, 'white')
                rect = text.get_rect(midleft=(x_coord, y_coord))
                screen.blit(text, rect)
                if line[0:3] == 'Ins':
                    y_coord += 40
                else:
                    y_coord += 50
            
            pygame.display.update()
       
def game_menu():
    game_menu_active = True
    global running
    global game_paused
    global game_restart
    global sfx_active
    
    while game_menu_active:
        
        restart_button_text = game_menu_font.render('RESTART', False, 'white')
        restart_rect_col = 'black'
        restart_button_rect = restart_button_text.get_rect(midleft=(150, 230))

        exit_to_main_menu_button_text = game_menu_font.render('EXIT TO MAIN MENU', False, 'white')
        exit_to_main_menu_rect_col = 'black'
        exit_to_main_menu_rect = exit_to_main_menu_button_text.get_rect(midleft=(150, 310))

        exit_to_desktop_text = game_menu_font.render('EXIT TO DESKTOP', False, 'white')
        exit_to_desktop_rect_col = 'black'
        exit_to_desktop_rect = exit_to_desktop_text.get_rect(midleft=(150, 400))

        back_button_text = game_menu_font.render('BACK', False, 'white')
        back_rect_col = 'black'
        back_button_rect = back_button_text.get_rect(midleft=(60, 700))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_menu_active = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_menu_active = False
                game_paused = True
                pygame.time.set_timer(pause_event, 700)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    game_menu_active = False
                    game_restart = True
                if exit_to_main_menu_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    game_menu_active = False
                    game_restart = True
                    main_menu()
                if exit_to_desktop_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    game_menu_active = False
                    running = False
                if back_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    game_menu_active = False
                    game_paused = True
                    pygame.time.set_timer(pause_event, 700)
                if sfx_on_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    sfx_active = not sfx_active
        
        if game_menu_active:
            if restart_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                restart_button_text = game_menu_font.render('RESTART', False, 'black')
                restart_rect_col = 'white'
            restart_button_rect_to_display = pygame.Rect.inflate(restart_button_rect, 15, 15)
            restart_button_rect_to_display = restart_button_rect_to_display.move(-5, -3)

            if exit_to_main_menu_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                exit_to_main_menu_button_text = game_menu_font.render('EXIT TO MAIN MENU', False, 'black')
                exit_to_main_menu_rect_col = 'white'
            exit_to_main_menu_rect_to_display = pygame.Rect.inflate(exit_to_main_menu_rect, 15, 15)
            exit_to_main_menu_rect_to_display = exit_to_main_menu_rect_to_display.move(-5, -3)

            if exit_to_desktop_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                exit_to_desktop_text = game_menu_font.render('EXIT TO DESKTOP', False, 'black')
                exit_to_desktop_rect_col = 'white'
            exit_to_desktop_rect_to_display = pygame.Rect.inflate(exit_to_desktop_rect, 15, 15)
            exit_to_desktop_rect_to_display = exit_to_desktop_rect_to_display.move(-5, -3)

            if back_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                back_button_text = game_menu_font.render('BACK', False, 'black')
                back_rect_col = 'white'
            back_button_rect_to_display = pygame.Rect.inflate(back_button_rect, 15, 15)
            back_button_rect_to_display = back_button_rect_to_display.move(0, -3)

            screen.fill('black')
            pygame.draw.rect(screen, restart_rect_col, restart_button_rect_to_display)
            pygame.draw.rect(screen, exit_to_main_menu_rect_col, exit_to_main_menu_rect_to_display)
            pygame.draw.rect(screen, exit_to_desktop_rect_col, exit_to_desktop_rect_to_display)
            pygame.draw.rect(screen, back_rect_col, back_button_rect_to_display)
            screen.blit(restart_button_text, restart_button_rect)
            screen.blit(exit_to_main_menu_button_text, exit_to_main_menu_rect)
            screen.blit(exit_to_desktop_text, exit_to_desktop_rect)
            screen.blit(back_button_text, back_button_rect)
            if sfx_active:
                screen.blit(sfx_on_surf, sfx_on_rect)
            else:
                screen.blit(sfx_off_surf, sfx_off_rect)

            pygame.display.update()

def controls():
    controls_active = True
    global running

    controls_header_text = credits_header_font.render('Controls', False, 'white')
    controls_header_rect = controls_header_text.get_rect(midleft=(25, 90))

    controls_rect = pygame.rect.Rect(25, 186, 15, 550)

    controls_lines = [
        'Paddle Movement:   W, S',
        'Bounce-Boost:  Q or Spacebar',
        'Pause:  P',
        'Game Menu:  ESC'
    ]

    start_button_flash = pygame.USEREVENT + 3
    pygame.time.set_timer(start_button_flash, 350)
    flash_flag = False

    random_text = random.choice(('GOT IT!', 'PLAY!', 'START!'))
    while controls_active:

        start_button_text = main_menu_font_p.render(random_text, False, 'white')
        start_rect_col = 'black'
        start_button_rect = start_button_text.get_rect(midleft=(60, 700))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controls_active = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    controls_active = False
            if event.type == start_button_flash:
                flash_flag = not flash_flag

        if controls_active:  
            screen.fill('black')
            screen.blit(controls_header_text, controls_header_rect)

            if start_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) or flash_flag:
                start_button_text = main_menu_font_p.render(random_text, False, 'black')
                start_rect_col = 'white'
            start_button_rect_to_display = pygame.Rect.inflate(start_button_rect, 15, 15)
            start_button_rect_to_display = start_button_rect_to_display.move(0, -3)
            
            pygame.draw.rect(screen, start_rect_col, start_button_rect_to_display)
            screen.blit(start_button_text, start_button_rect)

            pygame.draw.rect(screen, 'white', controls_rect)

            x_coord = 50
            y_coord = 200
            for line in controls_lines:
                text = credits_font.render(line, False, 'white')
                rect = text.get_rect(midleft=(x_coord, y_coord))
                screen.blit(text, rect)
                y_coord += 50
            
            pygame.display.update()

main_menu()
if running:
    controls()
# game loop
while running:
    # game variables setup:
    if game_restart:
        game_paused = False

        # gamemode
        retro_mode_on = False # not stable

        # score
        player_score = 0
        enemy_score = 0
        color_counter = 100
        last_score_by_player = False

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
        bounce_boost_update_cooldown = 1500  # in milliseconds

        # userevents
        bounce_boost_update = pygame.USEREVENT + 1
        pause_event = pygame.USEREVENT + 2

        # timers
        pygame.time.set_timer(bounce_boost_update, bounce_boost_update_cooldown)

        # bounce boost surface
        right_boost_surf = bounce_boost_frames[17]
        bounce_boost_frame = 0

        game_restart = False

    
    #event loop
    for event in pygame.event.get():
        # window actions
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_menu()
        if event.type == bounce_boost_update:
            if not bounce_boost_ready:
                right_boost_surf = bounce_boost_frames[bounce_boost_frame]
                if bounce_boost_frame < 17:
                    bounce_boost_frame += 1
                else: 
                    bounce_boost_frame = 0
                    bounce_boost_ready = True                  
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_SPACE) and bounce_boost_ready:
            bounce_boost_activated = True
            bounce_boost_used = False
            right_boost_surf = bounce_boost_used_surf
            if ball_speed > 13:
                reaction_time = random.randint(0, 10)
            elif ball_speed > 11:
                reaction_time = random.randint(5, 20)
            else:
                if random.choice((False, False, True)):
                    reaction_time = random.randint(lower_reaction_time-5, upper_reaction_time-32)
                elif random.choice((False, True)):
                    reaction_time = random.randint(lower_reaction_time+5, upper_reaction_time-16)
                else:
                    reaction_time = random.randint(lower_reaction_time+25, upper_reaction_time-8)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            game_paused = not game_paused
            pygame.time.set_timer(pause_event, 700)
            show_pause_button = True
        if event.type == pause_event:
            show_pause_button = not show_pause_button
    if not running:
        break

    if not game_paused:
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
            reaction_time = 30
            ball_speed = ball_starting_speed
            bounce_counter = 0
        
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
                last_score_by_player = False
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
                last_score_by_player = True



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
            if ball_speed < 17:
                ball_speed += 0.15
            bounce_counter += 1
            if sfx_active:
                bounce_sfx.play()
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

            speed_bonus = math.floor(ball_speed - ball_starting_speed) * 8
            if speed_bonus > 30:
                speed_bonus = 30
            if bounce_counter < 8 and last_score_by_player:
                reaction_time = 10
            elif bounce_counter < 6:
                reaction_time = 20
            else:
                if enemy_rect.centery < 300 or enemy_rect.centery > 500:
                    reaction_time = random.randint(math.floor(lower_reaction_time - (speed_bonus+10)/4), upper_reaction_time-random.randint(6, 12)-speed_bonus)
                else:
                    reaction_time = random.randint(math.floor(lower_reaction_time+10 - (speed_bonus+10)/2), upper_reaction_time-speed_bonus)
            if ball_speed < 17:
                ball_speed += 0.15
            bounce_counter += 1
            if sfx_active:
                bounce_sfx.play()
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
    if math.floor(ball_speed-9) == 8:
        bounce_counter_text_color = 'dodgerblue2'
    else:
        bounce_counter_text_color = 'white'
    if bounce_boost_activated:
        pass
    else:
        bounce_counter_text = bounce_counter_font.render("Speed " + str(math.floor(ball_speed-9)), False, bounce_counter_text_color)
    bounce_counter_text_rect = bounce_counter_text.get_rect(midright = (795, 786))

    # level 

    # update the screen
    screen.blit(background, (0, 0))
    if not right_boost_rect.colliderect(ball_rect) and not right_boost_rect.colliderect(player_rect):
        screen.blit(right_boost_surf, right_boost_rect)
    screen.blit(player_surf, player_rect)
    screen.blit(enemy_surf, enemy_rect)
    screen.blit(score_text_left, score_text_left_rect)
    if not bounce_counter_text_rect.colliderect(enemy_rect) and not bounce_counter_text_rect.colliderect(ball_rect):
        screen.blit(bounce_counter_text, bounce_counter_text_rect)
    screen.blit(score_text_right, score_text_right_rect)
    screen.blit(ball_surf, ball_rect)
    if game_paused and show_pause_button:
        screen.blit(pause_surf, pause_rect)
    if game_paused:
        pause_info_text = pause_font.render('(click \'p\' to unpause)', False, 'white')
        pause_info_rect = pause_info_text.get_rect(topright=(760, 15))
        screen.blit(pause_info_text, pause_info_rect)

    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)


pygame.quit()