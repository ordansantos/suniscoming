
import pygame
import gtk

import Menu
import Game

width = gtk.gdk.screen_width() - 50
height = gtk.gdk.screen_height() - 50

screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

menu = Menu.Menu(screen, width, height)
menu.showMenu()
while True:
    for e in pygame.event.get():
        op = menu.selectMenu(e)
    
    if op == 1:
        menu.loading()
        game = Game.Game(screen, width, height)
        game.run()
        op = 0
