import pygame
from tiles import *
from spritesheet import Spritesheet
from player import Player
from npcs import *
from partner import Partner

START_POS_PL = 8
START_POS_PA = 160

# MAYBE fix these too:
    # fix the partner/player/bot thing (a class that gets inherited from >>>>>>> whatever these separate classes are...)
    # improve level generation thing (potentially procedural level generation?)

class Game:
    def __init__(self):
        pygame.init() # this thing gives you basic things (thank you internet forums)
        self.DISPLAY_W, self.DISPLAY_H = 1200, 800
        self.canvas = pygame.Surface((1920, 1080))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)   # placed the pygsame window into a function that can be called
        self.bg = pygame.image.load("assets/lowkeybg.jpg")
        icon = pygame.image.load("assets/chrisstar.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"    # from the states pf menu, credits, lev1, lev2. since we're starting the game, it's the menu thing (start screen)
        self.title_font = pygame.font.SysFont("Albertus Nova Black", 100)
        self.menu_font = pygame.font.SysFont("Cambria", 60)    # i wonder how this'll work on other computers that don't have crazy fonts
        self.small_font = pygame.font.SysFont("Cambria", 40)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("HENAGONOMETRY")
   
    def menu(self):  # construct menu
        # while self.state == "menu":
            self.canvas.fill((0, 0, 0))
            self.canvas.blit(self.bg, (0,0))

            title = self.title_font.render("HENAGONOMETRY", True, "white")
            start_text = self.menu_font.render("Press ENTER to Start", True, "cornsilk")
            credits_text = self.menu_font.render("Press C for Credits", True, "cornsilk")
            quit_text = self.menu_font.render("Press ESC to Quit", True,"cornsilk")

            self.canvas.blit(title, (self.DISPLAY_W//2 - title.get_width()//2, 200))   # these four give us the centered text blocsks
            self.canvas.blit(start_text, (self.DISPLAY_W//2 - start_text.get_width()//2, 390))
            self.canvas.blit(credits_text, (self.DISPLAY_W//2 - credits_text.get_width()//2, 460))
            self.canvas.blit(quit_text, (self.DISPLAY_W//2 - quit_text.get_width()//2, 520))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None         # nullifies the shit and makes u QUIT the game
                if event.type == pygame.KEYDOWN: # keypress
                    if event.key == pygame.K_RETURN:
                        self.state = "lev1"      # enter turns your state into playing, a.k.a, the GAME
                    elif event.key == pygame.K_c:
                        self.state = "credits"      # makes you read boring information
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False        # QUITS your game
                        self.state = None
            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    def credits(self):
        # while self.state == "credits":
            self.canvas.fill("navy")
            self.canvas.blit(self.bg, (0,0))

            title = self.title_font.render("C R E D I T S", True, "white")
            credit1 = self.small_font.render("Game by Terēze Saule", True, "cornsilk") # because this is my own chaos
            credit2 = self.small_font.render("placeholder text", True, "cornsilk") # they each added a line of code or a suggestion
            credit3 = self.small_font.render("Inspired by the work of Chris Cornell", True, "cornsilk") # you know what? don't ask.
            backtext = self.small_font.render("Press C to go back", True, "cornsilk") #### changed it to c to be more intuitive

            self.canvas.blit(title, (self.DISPLAY_W//2 - title.get_width()//2, 150))  # funky centering metho dthing
            self.canvas.blit(credit1, (self.DISPLAY_W//2 - credit1.get_width()//2, 300))
            self.canvas.blit(credit2, (self.DISPLAY_W//2 - credit2.get_width()//2, 360))
            self.canvas.blit(credit3, (self.DISPLAY_W//2 - credit3.get_width()//2, 420))
            self.canvas.blit(backtext, (self.DISPLAY_W//2 - backtext.get_width()//2, 600))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None       # kills you
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.state = "menu"    # returns you

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update() # boring necessity

    def lev1(self):
        spritesheet = Spritesheet('nnnn.png')
        player = Player()
        partner = Partner()
        tile_map = TileMap("branchlev.csv", spritesheet)
        player.position.x = player.position.y = START_POS_PL
        partner.position.x = partner.position.y = START_POS_PA
        player.rect.x = player.rect.y = START_POS_PL
        partner.rect.x = partner.rect.y = START_POS_PA
        player.coins = 0
        partner.coins = 0
        partner.lives = 12
        player.lives = 12
        hud = HUD("assets/life.png")
        coins = tile_map.coins
        goals = tile_map.goals

        camera_x = START_POS_PL
        camera_y = START_POS_PL

        while self.state == "lev1":
            self.canvas.blit(self.bg, (0,0))

            # camera and draws
            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2

            tile_map.draw_map(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            player.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            partner.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for c in coins:
                c.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for g in goals:
                g.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)

            dt = self.clock.tick(60) * 0.001 * 60
            player.update(dt, tile_map.tiles)
            partner.update(dt, tile_map.tiles)

            if player.rect.top > tile_map.map_height + 200:
                player.lives -= 1
                partner.lives -=1
                if player.lives == 0:
                    self.state = "menu"
                else:
                    player.rect.x = player.rect.y = START_POS_PL
                    player.position.x = player.position.y = START_POS_PL
                    partner.rect.x = partner.rect.y = START_POS_PA
                    partner.position.x = partner.position.y = START_POS_PA

            for c in coins[:]: # copies the list and doesn't change the og by using a colon
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1
                    partner.coins +=1

                if partner.rect.colliderect(c.rect):
                    coins.remove(c)
                    partner.coins +=1
                    player.coins +=1

            for g in goals:
                if player.rect.colliderect(g.rect):
                    print("Level complete!")
                    self.state = "lev2"

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
                player.jump() 
            if pygame.key.get_pressed()[pygame.K_w]:
                partner.jump() 

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

##### HUGE LEVEL TWO THING
    def lev2(self): # this thing wil be HUGE
        spritesheet = Spritesheet('nnnn.png')
        player = Player()
        tile_map = TileMap('sliplev.csv', spritesheet)
        player.position.x = player.position.y = START_POS_PL
        player.rect.x = player.rect.y = START_POS_PL
        player.coins = 0
        player.lives = 12
        hud = HUD("assets/life.png")
        coins = tile_map.coins
        goals = tile_map.goals
        camera_x = START_POS_PL
        camera_y = START_POS_PL

        while self.state == "lev2":
            self.canvas.blit(self.bg, (0,0))

            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2

            tile_map.draw_map(self.canvas, offset_x=-camera_x, offset_y=-camera_y)
            player.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for c in coins:
                c.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            for g in goals:
                g.draw(self.canvas, offset_x=-camera_x, offset_y=-camera_y)

            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)

            dt = self.clock.tick(60) * 0.001 * 60
            player.update(dt, tile_map.tiles)

            # HIT THIS< AND YOUŖE DEAD!!! again!!!
            if player.rect.top > tile_map.map_height + 200:
                player.lives -= 1
                if player.lives <= 0:
                    self.state = "lev1"
                else:
                    player.rect.x = player.rect.y = START_POS_PL
                    player.position.x = player.position.y = START_POS_PL

            for c in coins[:]:
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1

            for g in goals:
                if player.rect.colliderect(g.rect):
                    print("done!")
                    self.state = "lev3"
                    # import lev2 ## this is BAD go ahead and FIX IT

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
    def lev3(self):
        import lev2         # i must fix the spritesheets as asap as possible

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu()
            elif self.state == "credits":
                self.credits()
            elif self.state == "lev1":
                self.lev1()
            elif self.state == "lev2":
                self.lev2()
            elif self.state == "lev3":
                self.lev3()
            else:
                self.running = False
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
