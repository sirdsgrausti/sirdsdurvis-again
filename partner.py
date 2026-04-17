import pygame
from spritesheet import Spritesheet
from player import Player

class Partner(Player):   # yeyeyeye finally stopped being scared of super().__init__()!! evem though i used it before like half a semester ago
    def __init__(self):
        super().__init__()
        self.ST_POS = 16
        # self.is_jumping, self.on_ground = False, False

    def jump(self):
        if self.on_ground:
            self.velocity.y -= 11
            self.on_ground = False

    def animate(self):
        chrspritesheet = Spritesheet('assets/stellasheet.png')
        rightface = chrspritesheet.parse_sprite("stidle.png")
        leftface = pygame.transform.flip(rightface, True, False)  # still have no clue why this is so dumb

        if self.state == 'moving left':
            self.current_image = leftface
        else:
            self.current_image = rightface

    def load_frames(self):
        chrspritesheet = Spritesheet('assets/stellasheet.png')
        self.idle_frames_right = [chrspritesheet.parse_sprite("stidle.png")]
        self.walking_frames_right = [
            chrspritesheet.parse_sprite("stwalk1.png"),
            chrspritesheet.parse_sprite("stwalk2.png")
        ]
        self.idle_frames_left = [pygame.transform.flip(f, True, False) for f in self.idle_frames_right]
        self.walking_frames_left = [pygame.transform.flip(f, True, False) for f in self.walking_frames_right]
    