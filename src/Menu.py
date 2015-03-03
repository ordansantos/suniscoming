# coding: utf-8

import sys
sys.path.append("../")

import pygame
import gtk

class Menu:
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.menu_pos = width / 2 + 392, height - 205
    
    def showMenu(self):
        # background
        self.screen.fill((0, 0, 0))
        background = pygame.image.load("../tiles/menu.png").convert()
        self.screen.blit(background, (self.width / 2 - 392, self.height / 2 - 343))
        
        # menu
        menu = pygame.image.load("../tiles/opcoes.png").convert()
        self.screen.blit(menu, (self.menu_pos))
        
        #draw
        pygame.display.flip()
    
    def selectMenu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.play(mouse_pos):
                return 1
    
    def play(self, mouse_pos):
        if (mouse_pos[0] > (self.menu_pos[0] + 12)) and (mouse_pos[1] > (self.menu_pos[1] + 7)) and (mouse_pos[0] < (self.menu_pos[0] + 68) and (mouse_pos[1]) < (self.menu_pos[1] + 65)):
            return True
        return False
    
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
    