from entity import Entity
import pygame
class Goal(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, "green")  
        self.image = pygame.image.load("goalstar.png")
