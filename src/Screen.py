import sys
sys.path.append("../")

import pygame
import pytmx
from pytmx.util_pygame import load_pygame

class Screen:
    a = 1 
    #Matrix = [[0 for x in range(1000)] for x in range(1000)] 
    
    def __init__(self, screen_width, screen_height):
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.t  = load_pygame('tile_map.tmx')
        render_tiles_to_screen(self, (0,0))
        
        pygame.display.flip()
        
    def clear(self):
        pass
  
    def blitPerson(self, p):
        
        img_person = pygame.image.load(p.getPath())
        self.screen.fill((255, 0, 0))
        
        
        render_tiles_to_screen(self, p.getPosition())
        self.screen.blit(img_person, (self.screen_width / 2, self.screen_height / 2))
        pygame.display.update()
        
rect_color = (255, 255, 0)
poly_color = (0, 255, 0)

def render_tiles_to_screen(self, (offx, offy)):
    print offx;
    tmx_data = self.t
    if tmx_data.background_color:
        self.screen.fill(pygame.Color(self.tmx_data.background_color))
    
    # iterate over all the visible layers, then draw them
    # according to the type of layer they are.
    for layer in tmx_data.visible_layers:

        # draw map tile layers
        if isinstance(layer, pytmx.TiledTileLayer):

            # iterate over the tiles in the layer
            for x, y, image in layer.tiles():
                self.screen.blit(image, (x * tmx_data.tilewidth -offx, y * tmx_data.tileheight -offy))

        # draw object layers
        elif isinstance(layer, pytmx.TiledObjectGroup):

            # iterate over all the objects in the layer
            for obj in layer:

                # objects with points are polygons or lines
                if hasattr(obj, 'points'):
                    pygame.draw.lines(self.screen, poly_color,
                            obj.closed, obj.points, 3)

                # some object have an image
                elif obj.image:
                    self.screen.blit(obj.image, (obj.x -offx, obj.y - offy))

                # draw a rect for everything else
                else:
                    pygame.draw.rect(self.screen, rect_color,
                            (obj.x -offx, obj.y - offy, obj.width, obj.height), 3)

        # draw image layers
        elif isinstance(layer, pytmx.TiledImageLayer):
            if layer.image:
                self.screen.blit(layer.image, (0, 0))

    
                
                
                