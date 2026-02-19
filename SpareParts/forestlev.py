
# NOT something important - only the setup for a new levelš background









import pygame
from player import Player
# setups and Fluff. DON'T TOUCH THESE!!!!!!!!!!!!!!!!!
pygame.init()
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("III: Summer Stench")
icon = pygame.image.load("assets/life.png")
pygame.display.set_icon(icon)

tree = pygame.image.load("assets/fetterforestfrag.png")
surface = pygame.Surface((screen.get_width(), screen.get_height())) # needed for displaying fonts and images

#creatures
player = Player()

while running:
##################################### DO NOT LOOK AT THIS; THIS IS NOT YET FINISHED #####################################################################
    screen.fill((16, 18, 89))
    trx = -300
    while trx < 2000: #blitting the trees for the opening cutscene
        trx = trx + 110
        screen.blit(tree, (trx, 0))

    gry = 450
    grx = -300
    grx2 = -300


#########################################################################################################
    for event in pygame.event.get():   # NO TOUCHING!!!!!!!!!
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse

    pygame.display.flip() ## DO NOT TOUCH!



dt = clock.tick(60) / 1000 
pygame.display.quit()