import pygame
from tilemaps.tiles import *
from spritesheet import Spritesheet
from player import Player
from npcs import *
from partner import Partner
from cutscenebutton import SpeakerBox
from cutscene import *
from SpareParts.startsceneblabber import *   

START_POS_PL = (0,0)
START_POS_PA = (8, 0) # they just fall and i ont like it

class MenuNode:
    def __init__(self, text):
        self.text = text
        self.next = None
        self.prev = None

def buildmenu():
    menu = MenuNode("<-   return to menu   ->")
    sound = MenuNode("<-   toggle sound    ->")
    quitn = MenuNode("<-       quit       ->") 

    menu.next = sound
    sound.next = quitn
    quitn.next = menu

    menu.prev = quitn
    sound.prev = menu
    quitn.prev = sound
    return menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.musicon = True
        pygame.mixer.music.load("hallthemoon.wav")  
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1) #loop forevvvs xd
        self.DISPLAY_W, self.DISPLAY_H = 1200, 800
        self.canvas = pygame.Surface((1920, 1080))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.bg = pygame.image.load("assets/lowkeybg.jpg")
        icon = pygame.image.load("assets/chrisstar.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.cutscene = None
        self.state = "menu"
        self.title_font = pygame.font.SysFont("Cambria", 100, True)
        self.menu_font = pygame.font.SysFont("Cambria", 60)
        self.small_font = pygame.font.SysFont("Cambria", 40)
        self.chara_font = pygame.font.SysFont("Cambria", 28)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Salient Falls - Find Stella's keys")
   
    def menu(self):
        self.canvas.fill((0, 0, 0))
        self.canvas.blit(self.bg, (0,0))

        title = self.title_font.render("SALIENT FALLS", True, "white")
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
                    self.cutscene = Cutscene(self, SpeakerBox(100, (self.DISPLAY_H - 220), (self.DISPLAY_W - 200), 180, self.chara_font), STARTTEXT)
                    self.state = "cutscene"
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

        title = self.title_font.render("CREDITS", True, "white")
        credit1 = self.small_font.render("Game code and assets by Terēze Saule", True, "cornsilk")
        credit2 = self.small_font.render("Thanks to Kārlis and Dāvids for being awesome and encouraging", True, "cornsilk")
        credit3 = self.small_font.render("Music by Isaac Hall (free to use)", True, "cornsilk")
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

    def cutsceneloop(self):
        scenebg = pygame.image.load("assets/start.png").convert()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = None
            elif event.type == pygame.KEYDOWN:
                self.cutscene.update(event)
        self.canvas.blit(scenebg, (0, 0))
        if self.cutscene:
            self.cutscene.draw(self.canvas)
        self.window.blit(self.canvas, (0, 0))
        pygame.display.update()

    def lev1(self):
        spritesheet = Spritesheet('nnnn.png')
        player = Player()
        partner = Partner()
        tile_map = TileMap("tilemaps/newlev.csv", spritesheet)

        dialogue = SpeakerBox(100, (self.DISPLAY_H - 220), (self.DISPLAY_W - 200), 180, self.chara_font)
        dialactive = False

        pauseimg = pygame.image.load("assets/pausescreen.png")
        paused = False
        current = buildmenu()

        player.position.x, player.position.y = START_POS_PL
        player.rect.midbottom = START_POS_PL
        player.velocity.xy = (0, 0)

        partner.position.x, partner.position.y = START_POS_PA
        partner.rect.midbottom = START_POS_PA
        partner.velocity.xy = (0, 0)

        player.coins = 0
        partner.coins = 0
        partner.lives = 12
        player.lives = 12

        hud = HUD("assets/life.png")
        coins = tile_map.coins
        goals = tile_map.goals
        enemies = tile_map.enemies
        annoying = [AnnoyingEnemy(300, 800), AnnoyingEnemy(600, 700), AnnoyingEnemy(1000,1200), AnnoyingEnemy(2000,1700)]
        while self.state == "lev1":
            self.canvas.blit(self.bg, (0,0))

            camera_x = player.rect.centerx - self.DISPLAY_W // 2
            camera_y = player.rect.centery - self.DISPLAY_H // 2

            tile_map.draw_map(self.canvas, -camera_x, -camera_y)    # just realised howd dumb the offset variables were roflmao
            player.draw(self.canvas, -camera_x, -camera_y)
            partner.draw(self.canvas, -camera_x, -camera_y)

            for a in annoying:
                a.draw(self.canvas, -camera_x, -camera_y)

            for c in coins:
                c.draw(self.canvas, -camera_x, -camera_y)

            for g in goals:
                g.draw(self.canvas, -camera_x, -camera_y)
            
            for e in enemies:
                e.draw(self.canvas, -camera_x, -camera_y)

            hud.draw_lives(self.canvas, player.lives)
            hud.draw_coins(self.canvas, player.coins)
            
            if dialactive:
                dialogue.draw(self.canvas)
            
            dt = self.clock.tick(60) / 1000

            player.update(dt, tile_map.tiles)
            partner.update(dt, tile_map.tiles)

            if player.rect.top > tile_map.map_height + 200:
                player.lives -= 1
                partner.lives -= 1

                if player.lives == 0:
                    self.state = "menu"
                else:
                    player.position.x, player.position.y = START_POS_PL
                    player.rect.midbottom = START_POS_PL
                    player.velocity.xy = (0, 0)

                    partner.position.x, partner.position.y = START_POS_PA
                    partner.rect.midbottom = START_POS_PA
                    partner.velocity.xy = (0, 0)

            for c in coins[:]:
                if player.rect.colliderect(c.rect) or partner.rect.colliderect(c.rect):
                    coins.remove(c)
                    player.coins += 1
                    # partner.coins += 1

            for g in goals:
                if player.rect.colliderect(g.rect):
                    self.cutscene = Cutscene(self, SpeakerBox(100, (self.DISPLAY_H - 220), (self.DISPLAY_W - 200), 180, self.chara_font), ENDTEXT)
                    self.state = "endscene"

            for e in enemies:
                if player.rect.colliderect(e.rect):
                    if not hasattr(player, "cooldown"): # look at this new funny thing i found on stackexchange and w3schools!!! xD ha satter. has attribute.
                        player.cooldown = 0

                    if player.cooldown <= 0:
                        if player.coins > 0:
                            player.coins -= 1
                        player.cooldown = 300  # frames
                        if player.coins == 0:
                            player.position.x, player.position.y = START_POS_PL
                            player.rect.midbottom = START_POS_PL

                    # if player.coins > 0:
                    #     player.coins -= 1
                    #     break  # prevent succcccking out all his keys/coins/whatevs in one frame

            if hasattr(player, "cooldown") and player.cooldown > 0:
                player.cooldown -= 1

            for a in annoying:
                a.update(dt, player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif paused:
                        if event.key == pygame.K_RIGHT:
                            current = current.next
                        elif event.key == pygame.K_LEFT:
                            current = current.prev
                        elif event.key == pygame.K_RETURN:
                            if "return to menu" in current.text:
                                self.state = "menu"
                                paused = False
                            elif "quit" in current.text:
                                self.running = False
                                self.state = None
                                # paused = False
                            elif "toggle sound" in current.text:
                                if self.musicon:
                                    pygame.mixer.music.pause()
                                    self.musicon = False
                                else:
                                    pygame.mixer.music.unpause()
                                    self.musicon = True
                                # self.musicon = not self.musicon

                    else:
                        if event.key == pygame.K_LEFT:
                            player.LEFT_KEY = True
                        elif event.key == pygame.K_RIGHT:
                            player.RIGHT_KEY = True
                        elif event.key == pygame.K_a:
                            partner.LEFT_KEY = True
                        elif event.key == pygame.K_d:
                            partner.RIGHT_KEY = True

                    if event.key == pygame.K_e:
                        import SpareParts.stellalogue
                        dialactive = not dialactive # i love NOT,,xd
                        dialogue.speakerchoice(1)
                        bub = "post1"
                        dialogue.textset(SpareParts.stellalogue.stellaspeech[bub]) # had stuff planned but didnt do it bcs dialogue is not really necessary here

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = False
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = False
                    elif event.key == pygame.K_a:
                        partner.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        partner.RIGHT_KEY = False

            keys = pygame.key.get_pressed()         # still as weird and clunky as it was in january. how nice!
            if keys[pygame.K_UP]:
                player.jump()
            if keys[pygame.K_w]:
                partner.jump()

            # if not paused:
            #     keys = pygame.key.get_pressed()
            #     if keys[pygame.K_UP]:             # if i get rid of this, he can still jump in SloMo :-) not a bug. feature.
            #         player.jump()
            #     if keys[pygame.K_w]:
            #         partner.jump()

            if paused:
                self.canvas.blit(pauseimg, (0, 0))
                text = self.menu_font.render(current.text, True, "cornsilk")
                self.canvas.blit(text, (self.DISPLAY_W//2 - text.get_width()//2, 350))
                

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
            elif self.state == "cutscene" or self.state == "endscene":
                self.cutsceneloop()
            # elif self.state == "endscene":
            #     self.cutsceneloop()
            else:
                self.running = False
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
