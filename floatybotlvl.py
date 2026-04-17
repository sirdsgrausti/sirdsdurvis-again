import pygame
from tilemaps.tiles import *
from main import Game
from spritesheet import Spritesheet
from npcs import *
from chrisbot import Bot

class FBLevel(Game):
    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load("assets/lowkeybg.jpg")
        self.state = "playing1"

    def menu(self):
        while self.state == "menu":
            self.canvas.fill((10, 10, 40))
            self.canvas.blit(self.bg, (0,0))
            title = self.title_font.render("S I R D S D U R V I S", True, (255,255,255))
            start_text = self.menu_font.render("Press ENTER to Start", True, "cornsilk")
            credits_text = self.menu_font.render("Press C for Credits", True, "cornsilk")
            quit_text = self.menu_font.render("Press ESC to Quit", True,"cornsilk")
            self.canvas.blit(title, (self.DISPLAY_W//2 - title.get_width()//2, 200))
            self.canvas.blit(start_text, (self.DISPLAY_W//2 - start_text.get_width()//2, 390))
            self.canvas.blit(credits_text, (self.DISPLAY_W//2 - credits_text.get_width()//2, 460))
            self.canvas.blit(quit_text, (self.DISPLAY_W//2 - quit_text.get_width()//2, 520))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = "playing"
                    elif event.key == pygame.K_c:
                        self.state = "credits"
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.state = None
            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()


    def play1(self):
        spritesheet = Spritesheet('nnnn.png')
        player = Bot()
        tile_map = TileMap("tilemaps/yeurgh.csv", spritesheet)#('branchlev.csv', spritesheet)
        player.position.x = player.position.y = 80
        # partner.position.x = partner.position.y = 160
        player.rect.x = player.rect.y = 80
        player.coins = 0
        player.lives = 12
        hud = HUD("assets/life.png")
        coins = tile_map.coins
        goals = tile_map.goals
        # enemies = tile_map.enemies

        camera_x = 0
        camera_y = 0

        while self.state == "playing1":
            self.canvas.blit(self.bg, (0,0))
            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2
            tile_map.draw_map(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            player.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
           
            for c in coins:
                c.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            # for e in enemies:
            #     e.update(tile_map.tiles) # wotdefok
            #     e.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for g in goals:
                g.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)

            dt = self.clock.tick(60) * 0.001 * 60
            player.update(dt, tile_map.tiles)
            
            for c in coins[:]:
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1
            # for e in enemies:
            #     if player.rect.colliderect(e.rect):
            #         player.lives -= 1
            #         if player.lives <= 0:
            #             self.state = "menu"
            #         else:
            #             player.coins -=1

            for g in goals:
                if player.rect.colliderect(g.rect): 
                    print("Level complete!")
                    self.state = "menu"  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:     
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = True
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = True
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = False
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = False

            if pygame.key.get_pressed()[pygame.K_UP]:
                player.jump()

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu()
            elif self.state == "playing1":
                self.play1()
            else:
                self.running = False
        pygame.quit()

if __name__ == "__main__":
    game = FBLevel()
    game.run()
