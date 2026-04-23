import pygame
from cutscenebutton import *

class Cutscene:
    def __init__(self, game, speakerbox, data):
        self.game = game
        self.speakerbox = speakerbox
        self.data = data
        self.current = "start"
        self.load()

    def load(self):
        node = self.data[self.current] # is it really a node? linked list crap
        self.speakerbox.speakerchoice(2)
        self.speakerbox.textset(node["text"])

    def update(self, event):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RETURN]:
            nextkey = self.data[self.current]["next"]
            if nextkey is None:
                self.game.state = "lev1"  
            else:
                self.current = nextkey
                self.load()
        if keys[pygame.K_ESCAPE]:
            self.game.state = None
            self.game.running = False

    def draw(self, surface):
        self.speakerbox.draw(surface)