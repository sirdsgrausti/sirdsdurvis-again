from entity import Entity
import random
import pygame
####### BROKEN BROKEN DO NOT VIEW

# deprecated enemy object i learned from a tutorial but need to rework






































class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 28, 28, "red")  # red thing placeeholer
        self.image = pygame.image.load("enemy.png")
        self.vx = random.choice([-1, 1]) # This Thing makes the enemy go randomly left or right, but the update() makes it work
        self.speed = 1

    def update(self, tiles):
        # Move left or right
        self.rect.x += self.vx * self.speed

        # flip direction when hitting a wall
        for t in tiles:
            if self.rect.colliderect(t.rect):
                self.rect.x -= self.vx * self.speed
                self.vx *= -1
                break
