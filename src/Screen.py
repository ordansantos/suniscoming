import sys
sys.path.append("../")

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import Walls
import Person
import TextBox
import math

import sys, os, traceback
if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

import PAdLib.occluder as occluder
import PAdLib.shadow as shadow

class Screen:

    CONST_TILE = 16
    CONST_MAX_WH = 7200
    CONST_MAP_PX = 4
    
    def __init__(self, screen, screen_width, screen_height):
        
        self.objectMatrix = [[None for i in xrange(450)] for j in xrange(450)]
        
        # self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen = screen
        
        # screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load(file('../tiles/background.png')).convert()
        self.tile_map = load_pygame('tile_map.tmx')
        Walls.Walls.pushWalls(self.tile_map)    
        self.preLoadTiles()
        
        # shadows
        self.surf_lighting = pygame.Surface((screen_width, screen_height))
        self.shad = shadow.Shadow()
        self.surf_falloff = pygame.image.load("../characters/img/light_falloff100.png").convert()
        radius = 208
        self.shad.set_radius(radius)
        self.surf_falloff = pygame.transform.scale(self.surf_falloff, (radius * 2, radius * 2))
        self.surf_falloff.convert()
        self.mask = self.shad.get_mask()
        self.mask.blit(self.surf_falloff, (0, 0), special_flags=pygame.BLEND_MULT)
        
        # textbox
        self.txt = TextBox.TextBox(screen_width, screen_height)
        
        # lifebar
        self.life = Header(self.screen_width, self.screen_height)
    
    def draw(self, master, sun):
        self.clear(self.getRealPosition(master.getPosition()))
        self.renderPersonsToScreen(master)
        self.renderTilesToScreen(master)
        self.renderPersonsAfter(master)
        self.blitShadow(sun)
        self.txt.drawTextBox()
        self.life.blitLifeBar(master.life)
        pygame.display.flip()
    
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
        
        x, y = 0, 0
        img_x, img_y = mx - self.screen_width / 2, my - self.screen_height / 2
        img_width, img_height = self.screen_width, self.screen_height
        
        if img_x < 0:
            x = 0 - img_x
            img_x = 0
            
        if img_y < 0:
            y = 0 - img_y  
            img_y = 0
            
        if img_x + self.screen_width > self.CONST_MAX_WH:
			img_width -= img_x + self.screen_width - self.CONST_MAX_WH
			
        if img_y + self.screen_height > self.CONST_MAX_WH:
			img_height -= img_y + self.screen_height - self.CONST_MAX_WH
        
        subsurface = self.background.subsurface ((img_x, img_y, img_width, img_height))
        self.screen.blit(subsurface, (x, y))
    
    def blitMaster(self, person):
        x, y = self.screen_width / 2, self.screen_height / 2
        
        img_person = person.getImage()
        self.screen.blit(img_person, (-32 + x, -64 + y))
        
        img_life = person.getLifeBar()
        if person.life != 0:
            self.screen.blit(img_life, (-16 + x, -60 + y))
    
    def blitPerson(self, master, person):
        if (master == person):
            self.blitMaster (master)
        else:    
            x, y = self.getPersonPosition(self.getRealPosition(master.getPosition()), self.getRealPosition(person.getPosition()))
            
            img_person = person.getImage()
            self.screen.blit(img_person, (x, y))
            
            img_life = person.getLifeBar()
            if person.life != 0:
                self.screen.blit(img_life, (16 + x, 4 + y))
            
            img_squirt = person.getBloodSquirt()
            if img_squirt != None:
                self.screen.blit(img_squirt, (x + 8, y + 8))
    
    def blitShadow(self, sun):
        self.surf_lighting.fill(sun.getColor())
        if sun.gray < 160:
            pos = self.shad.get_center_position(self.screen_width / 2, self.screen_height / 2 - 16)
            self.surf_lighting.blit(self.mask, pos, special_flags=pygame.BLEND_MAX)
        self.screen.blit(self.surf_lighting, (0, 0), special_flags=pygame.BLEND_MULT)
    
    def renderTilesToScreen(self, master):
        
        mx, my = self.getRealPosition(master.getPosition())
     
        middlex = self.screen_width / 2
        middley = self.screen_height / 2
        
        inix = (mx - middlex) / 16 * 16 - 32  # -32 margin of error
        iniy = (my - middley) / 16 * 16 - 32
        fimx = mx + middlex + 32  # -32 margin of error
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
                    if (isinstance(self.objectMatrix[xt][yt], tuple)):
                        img_1, img_2 = self.objectMatrix[xt][yt]
                        self.screen.blit (img_1, (self.getObjectPosition((x, y), self.getRealPosition(master.getPosition()))))
                        self.screen.blit (img_2, (self.getObjectPosition((x, y), self.getRealPosition(master.getPosition()))))
                        
                    else:
                        self.screen.blit (self.objectMatrix[xt][yt], (self.getObjectPosition((x, y), self.getRealPosition(master.getPosition()))))

    # Map position
    def preLoadTiles(self):
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if (self.objectMatrix[x][y] != None and not isinstance(self.objectMatrix[x][y], tuple)):
                        self.objectMatrix[x][y] = (self.objectMatrix[x][y], image.convert_alpha())        
                    else:
                        if (self.objectMatrix[x][y] == None):
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
                if (i < 0 or i > Screen.CONST_MAX_WH): continue
                xt = i / Screen.CONST_TILE
                yt = y / Screen.CONST_TILE 
                if (self.objectMatrix[xt][yt] != None):
                    stained = True
            
            self.renderDeathBlood(master, p)
            
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
    
    def renderDeathBlood(self, master, person):
        img_death = person.getDeathBlood()
        if img_death != None:
            if person != master:
                x, y = self.getPersonPosition(self.getRealPosition(master.getPosition()), self.getRealPosition(person.getPosition()))
                self.screen.blit(img_death, (x - 24, y - 16))
            else:
                x, y = self.screen_width / 2, self.screen_height / 2
                self.screen.blit(img_death, (x - 58, y - 80))
                
    def getMousePositionOnMap(self, master, mouse_position):
        mouse_x, mouse_y = mouse_position
        
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        master_x, master_y = master.getPosition()
        
        x = mouse_x - center_x
        y = mouse_y - center_y
        
        x /= Walls.Walls.CONST_MAP_PX
        y /= Walls.Walls.CONST_MAP_PX
        
        
        x = x + master_x
        y = y + master_y
        
        return (x, y)
    

class Header:
    
    def __init__(self, width, height):
        self.src = pygame.display.get_surface()
        self.life_bar = pygame.image.load(file('../characters/img/super_lifebar.png')).convert()
        self.edges = int(width / 15), int(height / 15)
        
        gap = int(width / 1.7) - self.life_bar.get_width()
        if gap < 0:
            gap = -gap + self.edges[0]
            perc = gap * 100 / width
            self.life_size = self.life_bar.get_width() - gap, self.life_bar.get_height() - int(self.life_bar.get_height() * perc / 100)
        else:
            perc = gap * 100 / width
            self.life_size = self.life_bar.get_width() + gap - self.edges[0], self.life_bar.get_height() + int(self.life_bar.get_height() * perc / 100)
        
        self.life_bar = pygame.transform.scale(self.life_bar, self.life_size).convert()
    
    def blitLifeBar(self, life):
        surf = self.life_bar.subsurface(0, 0, int(life * self.life_size[0] / 100), self.life_size[1])
        self.src.blit(surf, (self.edges[0], self.edges[1]))
        
        

    