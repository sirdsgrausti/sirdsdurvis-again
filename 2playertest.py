import pygame
from tiles import *
from spritesheet import Spritesheet
# from player import Player   unnecessary here - testing the floatier Bot class
from partner import Partner
from hud import HUD
from chrisbot import Bot

class Game:
    def __init__(self):
        pygame.init()
        self.DISPLAY_W, self.DISPLAY_H = 1200, 800
        self.canvas = pygame.Surface((1920, 1080))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.bg = pygame.image.load("lowkeybg.jpg")
        icon = pygame.image.load("chrisstar.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Sirdsdurvis v3")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"    # from the states pf menu, credits, playing
        self.title_font = pygame.font.SysFont("Albertus Nova Black", 100)
        self.menu_font = pygame.font.SysFont("Albertus Nova", 60)
        self.small_font = pygame.font.SysFont("Albertus Nova Thin", 40)

## THE MENU, placed Inconveniently in the Middle as it Always Is :-((((((((((((((((((((((())))))))))))))))))))))) 
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

# THE =(unfinished)credits i placed smack in the middle fo my code!!!! yeah1!!!!!
    def credits(self):
        while self.state == "credits":
            self.canvas.fill("navy")
            bgg = pygame.image.load("loresbg.jpg")
            self.canvas.blit(bgg, (0,0))

            title = self.title_font.render("C R E D I T S", True, "white")
            credit1 = self.small_font.render("Game by Terēze Saule", True, "cornsilk") # because this is my own chaos
            credit2 = self.small_font.render("Supported by DP, KC, and MS", True, "cornsilk") # they each added a line of code or a suggestion
            credit3 = self.small_font.render("Inspired by the work of Chris Cornell", True, "cornsilk") # you know what? don't ask.
            backtext = self.small_font.render("Press ESC to go back", True, "cornsilk")

            self.canvas.blit(title, (self.DISPLAY_W//2 - title.get_width()//2, 150))  # funky centering metho dthing
            self.canvas.blit(credit1, (self.DISPLAY_W//2 - credit1.get_width()//2, 300))
            # self.canvas.blit(credit2, (self.DISPLAY_W//2 - credit2.get_width()//2, 360)) we don't need to use this yet
            self.canvas.blit(credit3, (self.DISPLAY_W//2 - credit3.get_width()//2, 420))
            self.canvas.blit(backtext, (self.DISPLAY_W//2 - backtext.get_width()//2, 600))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    # game loop thing to use!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def play(self):
        spritesheet = Spritesheet('nnnn.png')
        player = Bot()
        partner = Partner()
        tile_map = TileMap("yeurgh.csv", spritesheet)#('branchlev.csv', spritesheet)
        player.position.x = player.position.y = 80
        partner.position.x = partner.position.y = 160
        player.rect.x = player.rect.y = 80
        partner.rect.x = partner.rect.y = 160
        player.coins = 0
        partner.coins = 0
        partner.lives = 12
        player.lives = 12
        hud = HUD("life.png")
        coins = tile_map.coins
        goals = tile_map.goals
        enemies = tile_map.enemies

        camera_x = 0
        camera_y = 0

        while self.state == "playing":
            self.canvas.blit(self.bg, (0,0))

            # camera and draws
            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2

            tile_map.draw_map(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            player.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            partner.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for c in coins:
                c.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for e in enemies:
                e.update(tile_map.tiles)
                e.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for g in goals:
                g.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            # HUD
            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)

            # Update physics
            dt = self.clock.tick(60) * 0.001 * 60
            player.update(dt, tile_map.tiles)
            partner.update(dt, tile_map.tiles)

            # HIT THIS FLOOR< AND YOU"RE DEAD!!!
            if player.rect.top > tile_map.map_height + 200:
                player.lives -= 1
                partner.lives -=1   ###removes a life for each of them
                if player.lives <= 0:
                    self.state = "menu"
                else:
                    player.rect.x = player.rect.y = 80
                    player.position.x = player.position.y = 80
                    partner.rect.x = partner.rect.y = 160
                    partner.position.x = partner.position.y = 160

            # if partner.rect.top > tile_map.map_height + 200:
            #     partner.lives -= 1
            #     player.lives -=1
            #     if player.lives <= 0 and partner.lives <=0:
            #         self.state = "menu"
            #     else:
            #         player.rect.x = player.rect.y = 80
            #         player.position.x = player.position.y = 80

            # KEYSSSS
            for c in coins[:]:
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1
                    partner.coins +=1

                if partner.rect.colliderect(c.rect):
                    coins.remove(c)
                    partner.coins +=1
                    player.coins +=1

            # eenemies that don't really do much except swoop around
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    player.lives -= 1
                    if player.lives <= 0:
                        self.state = "menu"
                    else:
                        player.rect.x = player.rect.y = 80
                if partner.rect.colliderect(e.rect):
                    partner.lives -= 1
                    if partner.lives <= 0:
                        self.state = "menu"
                    else:
                        partner.rect.x = partner.rect.y = 160
                
                    

            # goalpost, of which there are many
            for g in goals:
                if player.rect.colliderect(g.rect):
                    print("Level complete!")
                    self.state = "menu"  #  partner can't win for main, and i didn; t add any goalposts in the csv for this one :-(

            for event in pygame.event.get():
                if event.type == pygame.QUIT:      # main moves with arrows
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

                if event.type == pygame.KEYDOWN:     # partner uses wadsd
                    if event.key == pygame.K_a:
                        partner.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        partner.RIGHT_KEY = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        partner.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        partner.RIGHT_KEY = False
############## why are these out here? don't ask me. i had no idea where to put them
            if pygame.key.get_pressed()[pygame.K_UP]:
                player.jump() # keeping this besause it's nice and itr works so y not

            if pygame.key.get_pressed()[pygame.K_w]:
                partner.jump() # keeping this besause it's nice and itr works so y not

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    # game syates
    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu()
            elif self.state == "credits":
                self.credits()
            elif self.state == "playing":
                self.play()
            else:
                self.running = False

        pygame.quit()

#runs (the other one has a separate file i never use for running lol)
if __name__ == "__main__":
    game = Game()
    game.run()
