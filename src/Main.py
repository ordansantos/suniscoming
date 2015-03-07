
import pygame
import gtk

import Menu
import Game

width = 800 # gtk.gdk.screen_width() - 50
height = 600 # gtk.gdk.screen_height() - 50

screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

menu = Menu.Menu(screen, width, height)

while True:
    menu.showMenu()

    # close window
    if pygame.event.peek(pygame.QUIT):
        pygame.quit()
        break
    
    # handle events
    for e in pygame.event.get():
        op = menu.selectMenu(e)
    
    if op == 1:
        menu.loading()
        game = Game.Game(screen, width, height)
        game.run()
        # for now
        break
    
    elif op == 2:
        r = menu.options()
        if r == 'stop':
            break
        op = 0
    
