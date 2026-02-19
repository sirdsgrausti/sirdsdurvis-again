import pygame
## whyš this thing have so many comments? from the last programming test where i was expecting to explain every thing i had done.
class Bot(pygame.sprite.Sprite): # player class inherits sprite properties
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # init for the thing to know it's a spite
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False # trackers for the state og the sprite/if he touches the grund
        self.gravity, self.friction = 0.35, -0.12 # physics
        self.image = pygame.image.load("assets/chrisstar.png")
        self.rect = self.image.get_rect()
        # self.rect.midbottom = (8, 8)# we don't need this
        self.current_frame = 0           # this is for animation - tracks which frame it is
        self.last_updated = 0
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0, self.gravity) #


    def draw(self, display, offset_x=0, offset_y=0): # thing makes the camera work by blitting with offsets
        display.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)       
        self.vertical_movement(dt)   # updates each variable
        self.checkCollisionsy(tiles) # tiles == all the blocks to hit
# move
    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:      # this code is oooooold. these key variables were to save me a headache i guess?
            self.acceleration.x -= 0.3
        elif self.RIGHT_KEY:        # this stuff is based on physics mainly
            self.acceleration.x += 0.3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt  # more physics
        self.limit_velocity(5)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7  # vertical movement
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel): # so he doesn't spin out of control
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel)) # max = maximum value
        if abs(self.velocity.x) < 0.01: self.velocity.x = 0  # abs = absolute value

    def jump(self):
        if self.on_ground: 
            self.is_jumping = True
            self.velocity.y -= 17    # defines the jumping state & velocity ""pulling him down"""
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                hits.append(tile)                   # tests if the guy collides with the tiles iterating through them
        return hits # gives the guyš hit list back to the function i guess

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)      # uses the previous code to check collision in x direction
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:
                self.position.x = tile.rect.right  # matches the x so that they don'tphase through the wall
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1    # uses get hits to get the collisoin in y
        collisions = self.get_hits(tiles)
        for tile in collisions: # each tile in the gethits list is used to check collisions (many tiles. very many.)
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False     # but this needs him to fall smootjly
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h # same as x but with more physics for natural looking falls
                self.rect.bottom = self.position.y
