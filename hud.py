import pygame

class HUD:
    def __init__(self, life_icon_path):
        self.life_img = pygame.image.load(life_icon_path)
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
