
import pygame

import Game
import Menu

pygame.init()

info = pygame.display.Info()

width = info.current_w
height = info.current_h

screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

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
        switch = game.run()
        if switch == 'QUIT':
            break
        op = 0
    
    elif op == 2:
        switch = menu.options()
        if switch == 'QUIT':
            break
        op = 0
    
    elif op == 3:
        break
