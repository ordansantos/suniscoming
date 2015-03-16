# coding: utf-8

import pygame
from pygame.locals import *

import sys
import Game
import Person
import cPickle
from Menu import Menu, Text

def selectMenu():
    
    global screen, width, height, index
    
    def _size(mouse_pos):
        if mouse_pos[0] > size_pos[0] and mouse_pos[1] > size_pos[1] and mouse_pos[0] < size_pos[0] + size[0] and mouse_pos[1] < size_pos[1] + size[1]:
            return True
        return False
    
    menus = [unicode('Jogar', 'utf8'), unicode('Opções', 'utf8'), unicode('Sobre', 'utf8'), unicode('Sair', 'utf8')]
    menu = Text(menus, int(height[index] / 15))
    
    size_pic = pygame.image.load('../tiles/menu/img/full_white.png').convert_alpha()
    
    while True:
        
        # background
        background = pygame.image.load("../tiles/menu/img/fog.jpg").convert()
        bg_size = Menu.getSizeByHeight(height[index], background.get_width(), background.get_height())
        bg_size = bg_size[0], bg_size[1]
        background = pygame.transform.scale(background, bg_size).convert()
        
        # blit background
        screen.fill((0, 0, 0))
        screen.blit(background, (int(width[index] / 2) - int(bg_size[0] / 2), int(height[index] / 2) - int(bg_size[1] / 2)))
        
        # blit game name
        menu.blitAvulseText('Sun is coming', -1, int(height[index]/8), font='../tiles/menu/fonts/Toxia_FRE.ttf', font_size=int(height[index]/5), color=(255, 0, 0))
        
        # blit menu
        menu.show_horizontal((int(width[index] / 15), height[index] - int(height[index] / 15) * 2))
        
        # blit size
        size = int(height[index] / 15), int(height[index] / 15)
        size_pos = width[index] - size[0] * 1.5, height[index] - size[0] * 1.5
        size_pic = pygame.transform.scale(size_pic, size).convert_alpha()
        screen.blit(size_pic, size_pos)
        
        # draw
        pygame.display.flip()
        
        # close game
        if pygame.event.peek(pygame.QUIT):
            return 4
        
        mouse_pos = pygame.mouse.get_pos()
        if _size(mouse_pos):
            if index == 1:
                size_pic = pygame.image.load('../tiles/menu/img/small_red.png').convert_alpha()
            else:
                size_pic = pygame.image.load('../tiles/menu/img/full_red.png').convert_alpha()
        else:
            if index == 1:
                size_pic = pygame.image.load('../tiles/menu/img/small_white.png').convert_alpha()
            else:
                size_pic = pygame.image.load('../tiles/menu/img/full_white.png').convert_alpha()
        
        for e in pygame.event.get():
            # button clicked
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i in xrange(len(menus)):
                    if menu.isMouseInMenu(i):
                        return i
                # size
                if _size(mouse_pos):
                    if index == 0:
                        index = 1
                        screen = pygame.display.set_mode((width[index], height[index]), FULLSCREEN | HWSURFACE | DOUBLEBUF)
                    else:
                        index = 0
                        screen = pygame.display.set_mode((width[index], height[index]), HWSURFACE | DOUBLEBUF)

# begin main
pygame.init()

info = pygame.display.Info()

width = [800, info.current_w]
height = [600, info.current_h]

index = 0

screen = pygame.display.set_mode((width[index], height[index]), HWSURFACE | DOUBLEBUF)

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

master_name = 'Ordan Santos'
master_image = '../characters/sprites/ordan.png'

clock = pygame.time.Clock()

while True:
    
    clock.tick(10)
    
    op = 0
    
    op = selectMenu()
    
    if op == 0:
        Person.Person.restartPerson()
        Menu.loading(width[index], height[index])
        game = Game.Game(screen, width[index], height[index], master_name, master_image)
        switch = game.run()
        if switch == 'QUIT':
            pygame.quit()
            break
    
    elif op == 1:
        switch = Menu.options(width[index], height[index])
        if switch[0] == 'QUIT':
            pygame.quit()
            break
        elif switch[0] == 'MASTER':
            master_image = switch[1]
            # master_name = switch[2]
    
    elif op == 2:
        switch = Menu.about(width[index], height[index])
        if switch[0] == 'QUIT':
            pygame.quit()
            break
    
    elif op == 3:
        pygame.quit()
        break
