from entity import Entity
import pygame
class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, "yellow")  # this is NOT an unnecessary line of code, it gives us sccess to parent class methods
        self.image = pygame.image.load("bigkey.png")
