import pygame
from tiles import *
from spritesheet import Spritesheet
from player import Player
from npcs import *

pygame.init()
DISPLAY_W, DISPLAY_H = 1200, 800
canvas = pygame.Surface((1920, 1080))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H), pygame.RESIZABLE)
icon = pygame.image.load("assets/chrisstar.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("HENAGONOMETRY")
running = True
clock = pygame.time.Clock()
pygame.init()
spritesheet = Spritesheet('assets/sprshnew.png')
player = Player()
tile_map = TileMap('mazel.csv', spritesheet)
player.position.x, player.position.y = 80, 80
camera_x = 0
camera_y = 0

while running:  
    canvas.fill((14, 18, 86))
    # it MOVES ! has a CAMERA!!!!
    camera_x = player.rect.centerx - DISPLAY_W // 2
    camera_y = player.rect.centery - DISPLAY_H // 2 # round the division result down insteda of doing crazy stuff       
    player.coins = 0
    player.lives = 12
    hud = HUD("assets/life.png")
    coins = tile_map.coins
    goals = tile_map.goals
    tile_map.draw_map(canvas, offset_x=-camera_x, offset_y=-camera_y)
    player.draw(canvas, offset_x=-camera_x, offset_y=-camera_y) 
    hud.draw_lives(canvas, player.lives)
    hud.draw_coins(canvas, player.coins)
    window.blit(canvas, (0, 0))
    dt = clock.tick(60) * 0.001 * 60
    player.update(dt, tile_map.tiles)

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.LEFT_KEY = False # negated the physics stuff if guy is jum[ping]
            elif event.key == pygame.K_RIGHT:
                player.RIGHT_KEY = False

    if pygame.key.get_pressed()[pygame.K_UP]:
        player.jump() # this tihng was something new put outside the event loop, made today


    pygame.display.update()
