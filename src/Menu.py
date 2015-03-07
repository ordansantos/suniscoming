# coding: utf-8

import sys
sys.path.append("../")

import pygame
import gtk

class Menu:
    
    def __init__(self, screen, width, height):
        # screen
        self.screen = screen
        self.width = width
        self.height = height
        self.edges = int(self.height / 5)
        
        # background
        self.background = pygame.image.load("../tiles/bg_menu.png").convert()
        gap = self.height - self.background.get_height()
        if gap < 0:
            gap = -gap + self.edges
            self.bg_size = self.background.get_width() - gap, self.height - self.edges
        else:
            self.bg_size = self.background.get_width() + gap, self.height - self.edges
        
        self.background = pygame.transform.scale(self.background, self.bg_size).convert()
        
        # menu
        self.menu = pygame.image.load("../tiles/menu.png").convert_alpha()
        self.menu_pos = int(self.edges / 2) , self.height - self.menu.get_height() - int(self.edges / 2)
    
    def showMenu(self):

        # background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (int(self.width / 2) - int(self.bg_size[0] / 2), int(self.edges / 2)))
        
        # menu
        self.screen.blit(self.menu, (self.menu_pos))
        
        #draw
        pygame.display.flip()
    
    def selectMenu(self, event):
        
        # functions
        def play(mouse_pos):
            if (mouse_pos[0] > (self.menu_pos[0] + 12)) and (mouse_pos[1] > (self.menu_pos[1] + 7)) and (mouse_pos[0] < (self.menu_pos[0] + 68) and (mouse_pos[1]) < (self.menu_pos[1] + 65)):
                return True
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if play(mouse_pos):
                return 1
    
    def loading(self):
        # loading
        self.screen.fill((0, 0, 0))
        loading = pygame.image.load("../tiles/loading.jpeg").convert()
        loading = pygame.transform.scale(loading, (self.width, self.height))
        self.screen.blit(loading, (0,0))
        
        #draw
        pygame.display.flip()
    
if __name__ == '__main__':
    width = gtk.gdk.screen_width() - 50
    height = gtk.gdk.screen_height() - 50
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    menu = Menu(screen, width, height)
    menu.showMenu()
    while True:
        for e in pygame.event.get():
            op = menu.selectMenu(e)
        
        if type(op) == type(0):
            print op
    