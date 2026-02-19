import pygame
from tiles import *
from spritesheet import Spritesheet
from playernew import Player
from npcs import *
# from partner import Partner

START_POS_PL = (0,0)
START_POS_PA = (8, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.DISPLAY_W, self.DISPLAY_H = 1200, 800
        self.canvas = pygame.Surface((1920, 1080))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.bg = pygame.image.load("assets/lowkeybg.jpg")
        icon = pygame.image.load("assets/chrisstar.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.title_font = pygame.font.SysFont("Albertus Nova Black", 100)
        self.menu_font = pygame.font.SysFont("Cambria", 60)
        self.small_font = pygame.font.SysFont("Cambria", 40)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("HENAGONOMETRY")
   
    def menu(self):
        self.canvas.fill((0, 0, 0))
        self.canvas.blit(self.bg, (0,0))

        title = self.title_font.render("HENAGONOMETRY", True, "white")
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
                    self.state = "lev1"
                elif event.key == pygame.K_c:
                    self.state = "credits"
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.state = None

        self.window.blit(self.canvas, (0, 0))
        pygame.display.update()

    def credits(self):
        self.canvas.fill("navy")
        self.canvas.blit(self.bg, (0,0))

        title = self.title_font.render("C R E D I T S", True, "white")
        credit1 = self.small_font.render("Game by Terēze Saule", True, "cornsilk")
        credit2 = self.small_font.render("placeholder text", True, "cornsilk")
        credit3 = self.small_font.render("Inspired by the work of Chris Cornell", True, "cornsilk")
        backtext = self.small_font.render("Press C to go back", True, "cornsilk")

        self.canvas.blit(title, (self.DISPLAY_W//2 - title.get_width()//2, 150))
        self.canvas.blit(credit1, (self.DISPLAY_W//2 - credit1.get_width()//2, 300))
        self.canvas.blit(credit2, (self.DISPLAY_W//2 - credit2.get_width()//2, 360))
        self.canvas.blit(credit3, (self.DISPLAY_W//2 - credit3.get_width()//2, 420))
        self.canvas.blit(backtext, (self.DISPLAY_W//2 - backtext.get_width()//2, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.state = "menu"

        self.window.blit(self.canvas, (0, 0))
        pygame.display.update()

    def lev1(self):
        spritesheet = Spritesheet('nnnn.png')
        player = Player()
        # partner = Partner()
        tile_map = TileMap("branchlev.csv", spritesheet)

        player.position.x, player.position.y = START_POS_PL
        player.rect.midbottom = START_POS_PL
        player.velocity.xy = (0, 0)

        # partner.position.x, partner.position.y = START_POS_PA
        # partner.rect.midbottom = START_POS_PA
        # partner.velocity.xy = (0, 0)

        player.coins = 0
        # partner.coins = 0
        # partner.lives = 12
        player.lives = 12

        hud = HUD("assets/life.png")
        coins = tile_map.coins
        goals = tile_map.goals

        while self.state == "lev1":
            self.canvas.blit(self.bg, (0,0))

            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2

            tile_map.draw_map(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            player.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            # partner.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for c in coins:
                c.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for g in goals:
                g.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)

            dt = self.clock.tick(60) / 1000

            player.update(dt, tile_map.tiles)
            # partner.update(dt, tile_map.tiles)

            if player.rect.top > tile_map.map_height + 200:
                player.lives -= 1
                # partner.lives -= 1

                if player.lives == 0:
                    self.state = "menu"
                else:
                    player.position.x, player.position.y = START_POS_PL
                    player.rect.midbottom = START_POS_PL
                    player.velocity.xy = (0, 0)

                    # partner.position.x, partner.position.y = START_POS_PA
                    # partner.rect.midbottom = START_POS_PA
                    # partner.velocity.xy = (0, 0)

            for c in coins[:]:
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1
                    # partner.coins += 1

            for g in goals:
                if player.rect.colliderect(g.rect):
                    self.state = "lev2"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = True
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = True
                    # elif event.key == pygame.K_a:
                        # partner.LEFT_KEY = True
                    # elif event.key == pygame.K_d:
                        # partner.RIGHT_KEY = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = False
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = False
                    # elif event.key == pygame.K_a:
                        # partner.LEFT_KEY = False
                    # elif event.key == pygame.K_d:
                        # partner.RIGHT_KEY = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.jump()
            # if keys[pygame.K_w]:
                # partner.jump()

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu()
            elif self.state == "credits":
                self.credits()
            elif self.state == "lev1":
                self.lev1()
            else:
                self.running = False
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
