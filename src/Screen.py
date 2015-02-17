import sys
sys.path.append("../")

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import Walls

class Screen:

    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load(file('../tiles/background.png')).convert()
        self.tile_map  = load_pygame('tile_map.tmx')
        Walls.Walls.pushWalls(self.tile_map)    
    
    def getScreenPosition(self, (objx, objy), (herox, heroy)):
        x = -herox + objx + (self.screen_width / 2)
        y = -heroy + objy + (self.screen_height / 2)
        return (x, y)
    
    def clear(self, (x, y)):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.background, (-x + self.screen_width / 2, -y + self.screen_height / 2))
        
    def blitPerson(self, p, millis):
        img_person = p.getImage(millis)
        self.screen.blit(img_person, (-16 + self.screen_width / 2, -48 + self.screen_height / 2))
        
    def draw(self, position):
        self.render_tiles_to_screen(position)
        pygame.display.flip()

    def render_tiles_to_screen(self, heroPosition):
        
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    x = x * self.tile_map.tilewidth
                    y = y * self.tile_map.tileheight
                    self.screen.blit(image, (self.getScreenPosition((x, y), heroPosition)))


            
            
