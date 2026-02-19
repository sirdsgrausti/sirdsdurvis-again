import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.ST_POS = 8
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = 0.35, -0.12
        self.load_frames()
        self.rect = self.idle_frames_right[0].get_rect()
        self.current_frame = 0
        self.last_updated = 0

        self.position = pygame.math.Vector2(self.ST_POS, self.ST_POS)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]

    def draw(self, display, offset_x=0, offset_y=0):
        display.blit(self.current_image, (self.rect.x + offset_x, self.rect.y + offset_y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
        self.set_state()
        self.animate()

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 0.3
        elif self.RIGHT_KEY:
            self.acceleration.x += 0.3

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x
        self.limit_velocity(5)

        self.position.x += self.velocity.x
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y
        if self.velocity.y > 7:
            self.velocity.y = 7

        self.position.y += self.velocity.y
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.velocity.y -= 10
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
            elif self.velocity.x < 0:
                self.position.x = tile.rect.right
            self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)

        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.velocity.y = 0
                self.position.y = tile.rect.top
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h

            self.rect.bottom = self.position.y

    def set_state(self):
        self.state = 'idle'
        if self.velocity.x > 0:
            self.state = 'moving right'
        elif self.velocity.x < 0:
            self.state = 'moving left'

    def animate(self):
        chrspritesheet = Spritesheet('assets/praytellsheet.png')
        gg = chrspritesheet.parse_sprite("pridle.png")
        gg1 = pygame.transform.flip(gg, True, False)

        if self.state == 'moving left':
            self.current_image = gg1
        else:
            self.current_image = gg

    def load_frames(self):
        chrspritesheet = Spritesheet('assets/praytellsheet.png')
        self.idle_frames_right = [chrspritesheet.parse_sprite("pridle.png")]
        self.walking_frames_right = [
            chrspritesheet.parse_sprite("prwalk1.png"),
            chrspritesheet.parse_sprite("prwalk2.png")
        ]
        self.idle_frames_left = [pygame.transform.flip(f, True, False) for f in self.idle_frames_right]
        self.walking_frames_left = [pygame.transform.flip(f, True, False) for f in self.walking_frames_right]
