import pygame, csv, os
from npcs import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def draw(self, surface, offset_x=0, offset_y=0):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_width, self.map_height = 0, 0
        self.map_surface = pygame.Surface((1, 1))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, offset_x=0, offset_y=0):
        for tile in self.tiles:
            tile.draw(surface, offset_x, offset_y)

    def load_map(self):
        if self.tiles:
            max_x = max(tile.rect.right for tile in self.tiles)
            max_y = max(tile.rect.bottom for tile in self.tiles)
            self.map_width, self.map_height = max_x, max_y

    def read_csv(self, filename):
        map_data = [] # this reads the csv and turn the stuff there into a list to use later
        with open(os.path.join(filename)) as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                map_data.append(list(row))
        return map_data

    def load_tiles(self, filename):
        tiles = []             # BEIDZOT ATRADU MASĪVUS YAY
        self.coins = [] 
        self.goals = []
        self.enemies = []
        map_data = self.read_csv(filename) # turns into a list
        y = 0
        for row in map_data:
            x = 0
            for tile in row:
                tx = x * self.tile_size
                ty = y * self.tile_size
                if tile == '1':  
                    tiles.append(Tile('grass.png', tx, ty, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('grass2.png', tx, ty, self.spritesheet))  # lietosim APPEND!! galā pieliek to ko redz no iekavam
                elif tile == '3':
                    self.coins.append(Coin(tx + 6, ty + 6)) # these are different becuase theyŗe overlaid on the map
                elif tile == '4':
                    self.goals.append(Goal(tx, ty))
                elif tile == '5':
                    self.enemies.append(Enemy(tx, ty))
                x += 1
            y += 1

        self.map_width, self.map_height = x * self.tile_size, y * self.tile_size
        return tiles
