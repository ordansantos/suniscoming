import sys
sys.path.append("../")

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import Walls

class Screen:

    def __init__(self, screen_width, screen_height):
        
        self.objectMatrix = [[None for i in xrange(7210)] for j in xrange(7210)] 
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load(file('../tiles/background.png')).convert()
        self.tile_map  = load_pygame('tile_map.tmx')
        Walls.Walls.pushWalls(self.tile_map)    
        self.preLoadTiles()
    
    def getObjectPosition(self, (objx, objy), (herox, heroy)):
        x = -herox + objx + (self.screen_width / 2)
        y = -heroy + objy + (self.screen_height / 2)
        return (x, y)
    
    def getPersonPosition(self, master, person):
        x = -32 - master.x + person.x + (self.screen_width / 2)
        y = -64 - master.y + person.y + (self.screen_height / 2)
        return (x, y)
    
    def clear(self, (x, y)):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.background, (-x + self.screen_width / 2, -y + self.screen_height / 2))
    
    def blitMaster(self, person, millis):
        img_person = person.getImage(millis)
        self.screen.blit(img_person, (-32 + self.screen_width / 2, -64 + self.screen_height / 2))
        pygame.display.flip()
    
    def blitPerson(self, master, person, millis):
        img_person = person.getImage(millis)
        self.screen.blit(img_person, self.getPersonPosition(master, person))
        pygame.display.flip()
    
    def draw(self, person, millis):
        self.clear(person.getPosition())
        self.renderTilesToScreen(person.getPosition())
        self.blitMaster(person, millis)
        # millis for to the future

    def renderTilesToScreen(self, heroPosition):
        
        hx, hy = heroPosition
        middlex = self.screen_width / 2
        middley = self.screen_height / 2
        
        inix = (hx - middlex) / 16 * 16 - 32 # -32 margem de erro
        iniy = (hy - middley) / 16 * 16 - 32
        fimx = hx + middlex + 32 # -32 margem de erro
        fimy = hy + middley + 32
        
        if (inix < 0): inix = 0
        if (iniy < 0): iniy = 0
        
        if (fimx > 7200):
            fimx = 7200
            
        if (fimy > 7200):
            fimy = 7200
        
        for i in xrange (inix, fimx, 16):
            for j in xrange (iniy, fimy, 16):
                    #imagem
                    if (self.objectMatrix[i][j] != None):
                        self.screen.blit (self.objectMatrix[i][j], (self.getObjectPosition((i, j), heroPosition)))
     
    def preLoadTiles(self):
        
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    x = x * self.tile_map.tilewidth
                    y = y * self.tile_map.tileheight
                    self.objectMatrix[x][y] = image.convert()
        
        
        
