##########################################################################################
#DO NOT RUN! DO NOT RUN! DO NOT RUN!
##########################################################################################




import pygame
import numpy as np

import pygame
# this took me forever to figure out
# this here window is POINTLESS, DO NOT RUN UNDER ANY CIRCUMSTANCES UNLESS YOU WANT TO BREAK THE GAME!
TILE_SIZE = 8          # size of each tile when rendered on the pointless window

pygame.init()
screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

# # why convert? for faster pixel/colour access
image = pygame.image.load("yeurgh.png").convert()
width, height = image.get_size()

# 0 = seethrough/walkable, 1 = HARD!
game_map = []
for y in range(height):    # my fav part :-) the outer shell makes the thing iterate through the rowas
    row = []
    for x in range(width): ## this makes the thing iterate through columns and make the map a map
        colour = image.get_at((x, y))
        # check if the outline is red (i'll have to change this in case my assets/terrain are stylised)
        if colour.r == 255 and colour.g == 0 and colour.b == 0:
            row.append(1)  # wall
        elif colour.r == 0 and colour.g == 255 and colour.b == 0:
            row.append(2) # grassland colour field thing"
        elif colour.r == 255 and colour.g == 255 and colour.b == 0:
            row.append(3) # key
                        
        elif colour.r == 0 and colour.g == 0 and colour.b == 255:
            row.append(4) # this thing would be an item thing? i still haven; t decided how to render thsoe
        else:
            row.append(0)  # not wall not field
    game_map.append(row)
    np.savetxt('yeurgh.csv', game_map, delimiter=",", fmt='%s')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((16, 18, 84))

    for y, row in enumerate(game_map):         # iterates through the map we made to make a pointless window
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, (0, 120, 130),
                                  (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                pygame.draw.rect(screen, (0, 191, 147),
                                  (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 0: # this I should get rid of honestly, it's just a placehloder while i work on the bg stuff
                pygame.draw.rect(screen, (16, 18, 84),
                                 (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()