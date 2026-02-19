import pygame
import random
pygame.init()
pygame.display.set_caption('SIRDSDURVIS')
icon = pygame.image.load("assets/life.png")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE) 

# #### i need:
# something to determine where i want the box (prob on the same spot the whole time/game)
# the box itself (image?)
# func that determines the speaker (chris/stella/questionmark)
# the text storage unit (randomdia.py, stellalogue.py and chrisdia.py)
# the wrapper

class SpeakerBox:
    def __init__(self, x, y, position, chara, ):
        self.x = x
        self.y = y
        self.position = (self.x, self.y) # you cannot do this right?
        self.chara = 1
        

    def chara(chara):
        if chara == 1:
            speaker_icon = pygame.image.load("chrtalksprite.png")
        elif chara == 2:
            speaker_icon = pygame.image.load("steltalksprite.png")
        elif chara == 3:
            speaker_icon = pygame.image.load("questionmarkspr.png")

    
        
