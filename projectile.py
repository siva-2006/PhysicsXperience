import pygame
from math import *

win = pygame.display.set_mode((1200,790))
ICON = pygame.image.load('Untitled design.png').convert()
pygame.display.set_icon(ICON)
run = True

win_size = pygame.display.get_window_size()

pygame.init()
if pygame.get_init():
    print("PYGAME INITIALISED SUCCESSFULLY...")


#Class for the vertical_projectile object

class vertical_projectile:

    def __init__(self, vel, g, win):
        self.dt = 0.001
        self.g = -g * (self.dt)**2
        self.vel = vel * self.dt
        self.x = win_size[0]//2
        self.y = 0
        self.win = win

    def update_pos(self):
        self.y += self.vel
        self.vel += self.g
        return self.y

    def update_screen(self, y):
        cent = (self.x, coor_return(0, y)[1])
        self.win.fill((64, 64, 64))
        pygame.draw.circle(self.win, "white", cent, 20)
        pygame.draw.circle(self.win, "black", cent, 22, 2)
        pygame.display.update()
def coor_return(x, y):
    x_c = x*4
    y_c = win_size[1] - 150 - y*4
    return x_c, y_c

obj = vertical_projectile(50, 9.8, win)
clock = pygame.time.Clock()

while run:
    clock.tick(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pos = obj.update_pos()
    print(pos)
    obj.update_screen(pos)

pygame.quit()