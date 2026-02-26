import pygame
import random
# #### i need:
# something to determine where i want the box (prob on the same spot the whole time/game)
# the box itself (image?)
# func that determines the speaker (chris/stella/questionmark)
# the text storage unit (randomdia.py, stellalogue.py and chrisdia.py)
# the wrapper

class SpeakerBox:
    def __init__(self, x, y, width, height, font):
        self.x = x
        self.y = y
        self.position = (self.x, self.y) # you cannot do this right?
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.padding = 20
        self.lspacing = 5
        self.chara = None
        self.icon = None
        self.text = ""
        self.box = pygame.image.load("assets/input.png")

    def speakerchoice(self, chara):
        if chara == 1:
        #     self.icon = pygame.image.load("chrtalksprite.png").convert_alpha()   blocked out while assets arent done. lazy lazy me.
        # elif chara == 2:
        #     self.icon = pygame.image.load("steltalksprite.png").convert_alpha()
        # elif chara == 3:
            self.icon = pygame.image.load("assets/qmarktalk.png").convert_alpha()

        self.chara = chara

    def textset(self, text):
        self.text = text

    def draw(self, screen):
        if self.box != None:
            screen.blit(self.box, self.rect)
        else:
            pygame.draw.rect(screen, (20, 20, 20), self.rect)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        text_x = self.rect.x + self.padding
        text_y = self.rect.y + self.padding

        if self.icon:
            screen.blit(self.icon, (text_x, text_y))
            text_x += self.icon.get_width() + 10

        self.wraptext(screen, self.text, text_x, text_y)

    def wraptext(self, screen, text, x, y):

        maxw = self.rect.width - (x - self.rect.x) - self.padding
        words = text.split(" ")

        lines = []
        current = "" 

        for w in words:
            test = current + w + " "
            width = self.font.size(test)[0]
            if width < maxw:
                current = test
            else:
                lines.append(current)
                current = w + " "

        lines.append(current)

        for i, line in enumerate(lines):
            textsurf = self.font.render(line, True, "white")
            screen.blit(textsurf, (x, y + i * (self.font.get_height() + self.lspacing)))


    
        
