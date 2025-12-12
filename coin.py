from entity import Entity
import pygame
class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, "yellow")  # this is a really unncecessary line of code
        self.image = pygame.image.load("bigkey.png")
