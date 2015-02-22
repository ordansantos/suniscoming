import sys
sys.path.append("../")

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import Walls
import Person
import math

import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import PAdLib.occluder as occluder
import PAdLib.shadow as shadow

class Screen:

    CONST_TILE = 16
    CONST_MAX_WH = 7200
    CONST_MAP_PX = 4
    
    def __init__(self, screen_width, screen_height):
        
        self.objectMatrix = [[None for i in xrange(450)] for j in xrange(450)]
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load(file('../tiles/background.png')).convert()
        self.tile_map  = load_pygame('tile_map.tmx')
        Walls.Walls.pushWalls(self.tile_map)    
        self.preLoadTiles()
        
        self.surf_lighting = pygame.Surface((screen_width, screen_height))
        self.shad = shadow.Shadow()
        self.surf_falloff = pygame.image.load("../characters/light_falloff100.png").convert()
    
    def getRealPosition(self, (x, y)):
        return (x * Screen.CONST_MAP_PX, y * Screen.CONST_MAP_PX)
    
    # Use object real position
    def getObjectPosition(self, (objx, objy), (mx, my)):
        x = -mx + objx + (self.screen_width / 2)
        y = -my + objy + (self.screen_height / 2)
        return (x, y)
    
    # Use object real position
    def getPersonPosition(self, (mx, my), (px, py)):
        x = -32 - mx + px + (self.screen_width / 2)
        y = -64 - my + py + (self.screen_height / 2)
        return (x, y)
    
    # Use object real position
    def clear(self, (mx, my)):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (-mx + self.screen_width / 2, -my + self.screen_height / 2))
    
    def blitMaster(self, person):
        img_person = person.getImage()
        self.screen.blit(img_person, (-32 + self.screen_width / 2, -64 + self.screen_height / 2))
        
        img_life = person.getLifeBar()
        self.screen.blit(img_life, (-16 + self.screen_width / 2, -60 + self.screen_height / 2))
        
    def blitPerson(self, master, person):
        if (master == person):
            self.blitMaster (master)
        else:    
            img_person = person.getImage()
            x, y = self.getPersonPosition(self.getRealPosition(master.getPosition()), self.getRealPosition(person.getPosition()))
            self.screen.blit(img_person, (x, y))
            img_life = person.getLifeBar()
            self.screen.blit(img_life, (16 + x, 4 + y))
        
    def draw(self, master, sun):
        self.clear(self.getRealPosition(master.getPosition()))
        self.renderPersonsToScreen(master)
        self.renderTilesToScreen(master)
        self.renderPersonsAfter(master)
        self.blitShadow(master, sun)
        pygame.display.flip()
    
    def blitShadow(self, master, sun):
        self.surf_lighting.fill(sun.getColor())
        if not master.furtive:
            radius = sun.getRadius()
            self.shad.set_radius(radius)
            falloff = pygame.transform.scale(self.surf_falloff, (radius * 2, radius * 2))
            falloff.convert()
            mask = self.shad.get_mask()
            mask.blit(falloff, (0,0), special_flags= pygame.BLEND_MULT)
            pos = self.shad.get_center_position(self.screen_width / 2, self.screen_height / 2 - 16)
            self.surf_lighting.blit(mask, pos, special_flags = pygame.BLEND_MAX)
        self.screen.blit(self.surf_lighting, (0,0), special_flags=pygame.BLEND_MULT)
    
    def renderTilesToScreen(self, master):
        
        mx, my = self.getRealPosition(master.getPosition())
     
        middlex = self.screen_width / 2
        middley = self.screen_height / 2
        
        inix = (mx - middlex) / 16 * 16 - 32 # -32 margin of error
        iniy = (my - middley) / 16 * 16 - 32
        fimx = mx + middlex + 32 # -32 margin of error
        fimy = my + middley + 32
        
        if (inix < 0): inix = 0
        if (iniy < 0): iniy = 0
        
        if (fimx > Screen.CONST_MAX_WH):
            fimx = Screen.CONST_MAX_WH
            
        if (fimy > Screen.CONST_MAX_WH):
            fimy = Screen.CONST_MAX_WH
            
        for y in xrange (iniy, fimy, 16):
            yt = y / Screen.CONST_TILE
            for x in xrange (inix, fimx, 16):
                xt = x / Screen.CONST_TILE
                if (self.objectMatrix[xt][yt] != None):
                    self.screen.blit (self.objectMatrix[xt][yt], (self.getObjectPosition((x, y), self.getRealPosition(master.getPosition() ) ) ) )

    # Map position
    def preLoadTiles(self):
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.objectMatrix[x][y] = image.convert_alpha()        
                    
    def renderPersonsToScreen(self, master):
        
        self.to_render_after = []
        
        person_list = Person.Person.getPersons()
        
        for p in person_list:
            if (not self.personIsOnScreen(master, p)): continue
      
            x, y = self.getRealPosition(p.getPosition())
            # has free legs?
            stained = False
            
            for i in xrange (x - 4, x + 5, 4):
                for j in xrange (y, y + 17, 4):
                    if (i < 0 or j < 0 or i > Screen.CONST_MAX_WH or j > Screen.CONST_MAX_WH): continue
                    xt = i / Screen.CONST_TILE
                    yt = j / Screen.CONST_TILE
                    if (self.objectMatrix[xt][yt] != None):
                        stained = True
            
            if (not stained):
                self.to_render_after.append(p)
            else:
                self.blitPerson(master, p)

        
    def renderPersonsAfter(self, master):
        for p in self.to_render_after:
            self.blitPerson(master, p)
            
            
    def personIsOnScreen(self, master, person):
        
        mx, my = self.getRealPosition(master.getPosition())
        px, py = self.getRealPosition(person.getPosition())
        middlex = self.screen_width / 2
        middley = self.screen_height / 2
        
        if (math.fabs(px - mx) > middlex + 32):
            return False
        if (math.fabs(py - my) > middley + 32):
            return False
        return True
