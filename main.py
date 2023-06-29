import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('PONG BY KWAZAR374')
icon = pygame.image.load('assets/arts/iconB.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
running = True

# background setup
background = pygame.image.load('assets/arts/background_1.png')

# game loop
while running:

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    # update the screen
    screen.blit(background, (0, 0))
    pygame.display.update()
    
    # limit FPS to 60
    clock.tick(60)

pygame.quit()