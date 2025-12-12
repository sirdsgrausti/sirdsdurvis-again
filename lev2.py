from tiles import *
from spritesheet import Spritesheet
from player import Player
import pygame

import pygame
from tiles import *
from spritesheet import Spritesheet
from player import Player
######################### THIS HAS NO USE EXCEPT FOR BEING A PLACEHOLDER LEVEL/TEST HOW LEVEL SWITCHNG WORKS WITH IMPORTS

pygame.init()
DISPLAY_W, DISPLAY_H = 1200, 800
canvas = pygame.Surface((1920, 1080))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H), pygame.RESIZABLE)
icon = pygame.image.load("chrisstar.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Sirdsdurvis v3")
running = True
clock = pygame.time.Clock()

spritesheet = Spritesheet('sprshnew.png')
player = Player()
tile_map = TileMap('mazel.csv', spritesheet)
player.position.x, player.position.y = 80, 80
camera_x = 0
camera_y = 0
# OK, don;t touch these (basic setup stuff)

while running:   # only runs.. well. while the thing is running (set to True unless you exit)
    canvas.fill((14, 18, 86))

    # it MOVES ! has a CAMERA!!!!
    camera_x = player.rect.centerx - DISPLAY_W // 2
    camera_y = player.rect.centery - DISPLAY_H // 2 # round the division result down insteda of doing crazy stuff

    tile_map.draw_map(canvas, offset_x=-camera_x, offset_y=-camera_y) # draws map 
    player.draw(canvas, offset_x=-camera_x, offset_y=-camera_y) # draws player

    window.blit(canvas, (0, 0))
    dt = clock.tick(60) * 0.001 * 60
    player.update(dt, tile_map.tiles)

    # i got rid of stuff not yet thought through

    for event in pygame.event.get():          # this does things based on what keys are pressed (basically The Point of the for loop)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = True
            # elif event.key == pygame.K_UP:
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = False # negated the physics stuff if guy is jum[ping]
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = False
   
    if pygame.key.get_pressed()[pygame.K_UP]:
        player.jump() # this tihng was something new put outside the event loop, made today


    pygame.display.update()
