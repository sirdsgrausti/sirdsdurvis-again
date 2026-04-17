import pygame
import random

# all in one piece to make life less difficult
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface, offset_x=0, offset_y=0):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

class Goal(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32) # This is just an entity with a goal icon thing. like a key but .. different.. 
        self.image = pygame.image.load("assets/goalstar.png")

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.image = pygame.image.load("assets/enemy.png")

class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)  # this is NOT an unnecessary line of code, it gives us sccess to parent class methods
        self.image = pygame.image.load("assets/bigkey.png")

class HUD:
    def __init__(self, life_icon_path):
        self.life_img = pygame.image.load(life_icon_path) # cute little variable that gives us image we put in main.py, i made it customisab;e
        self.life_img = pygame.transform.scale(self.life_img, (32, 32))

    def draw_lives(self, surface, lives):
        x = 10
        for i in range(lives):
            surface.blit(self.life_img, (x, 10))
            x += 32  # spacing

    def draw_coins(self, surface, coins): # oins is a placeholdefr name for the stuff player collects
        font = pygame.font.SysFont("Albertus Nova", 36)
        text = font.render(f"Keys: {coins}", True, "white")
        surface.blit(text, (10, 50))

