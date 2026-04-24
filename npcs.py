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
        super().__init__(x, y, 32, 32) 
        self.image = pygame.image.load("assets/goalstar.png")

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.image = pygame.image.load("assets/enemy.png")  # easy enemy lol

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

class AnnoyingEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cell_size = 12
        self.image = pygame.image.load("assets/whitemodule.png").convert_alpha()

        self.grid = [[0 for ugh in range(5)] for ugh in range(5)] #thank my coding teachers for the beauty that is 2d arrays
        self.timer = 0
        self.changeinterval = 1000 # time in milliseconds feels funny
        self.rect = pygame.Rect(self.x, self.y, 5*self.cell_size, 5*self.cell_size)
        self.mix()

    def mix(self):
        for r in range(5):
            for c in range(5):
                self.grid[r][c] = random.choice([0, 1])

    def update(self, dt, player):
        self.timer += dt * 1000
        if self.timer >= self.changeinterval:
            self.timer = 0
            self.mix()

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        dist = (dx*dx + dy*dy) ** 0.5     # weird way to get sqrt without importing math. pythagoras!!
        if dist != 0: # dont divide by zero 
            dx /= dist
            dy /= dist    # it follows the player, doesnt accelerate, division normaliseds my thing bcs thes are vectors
        speed = 0.5

        self.x += dx * speed
        self.y += dy * speed

        # # self.x += random.randint(-1, 1)  # i made it annoying
        # # self.y += random.randint(-1, 1)
        self.rect.topleft = (self.x, self.y)

        for r in range(5):
            for c in range(5):  # even more annoying xD
                if self.grid[r][c] == 1:
                    px = self.x + c*5
                    py = self.y + r*5
                    particlerect = pygame.Rect(px, py, self.cell_size, self.cell_size)
                    if particlerect.colliderect(player.rect):
                        if player.coins > 0: # i put the mechanic in here because cross-file stuff is AWFUL imo
                            player.coins -= 1
                        return  # prevent succcccking out all his keys/coins/whatevs in one frame

    def draw(self, surface, offset_x=0, offset_y=0):
        for r in range(5):
            for c in range(5):
                if self.grid[r][c] == 1:
                    px = self.x + r * self.cell_size + offset_x
                    py = self.y + c * self.cell_size + offset_y #legibilitys sake made me change ii and iii to r and c
                    surface.blit(self.image, (px, py))