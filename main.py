import pygame

pygame.init()

winx, winy = 1200, 600

win = pygame.display.set_mode((winx, winy))

b_img = pygame.image.load("Physicsxperience.png")

pygame.display.set_caption("First Simulation")

running = True
class ball:
    def __init__(self, rad, x, y, vely, velx, g, ax, ay, image):
        self.rad = rad
        self.x = x
        self.y = y
        self.respawn_coor = (self.x,self.y)
        self.vely = vely
        self.velx = velx
        self.g = g
        self.ax = ax
        self.ay = ay
        self.image = image
        self.texture = pygame.image.load(image)
    def drawer(self):
        win.blit(self.texture, (self.x - self.rad, self.y - self.rad))

    def friction(self):
        if self.y + self.vely >= winy - 2*self.rad:
            self.velx -= 0.1 * self.velx

    def gravity(self):
        if not (self.y + self.vely >= winy - self.rad):
            self.vely += self.g

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velx -= self.ax
        if keys[pygame.K_RIGHT]:
            self.velx += self.ax
        if keys[pygame.K_UP]:
            self.vely -= self.ay
        if keys[pygame.K_DOWN]:
            self.vely += self.ay
        if keys[pygame.K_r]:
            self.x, self.y = self.respawn_coor
            self.velx, self.vely = 0,0

        self.y += self.vely
        self.x += self.velx

        self.gravity()

        self.friction()

        if not(self.y + self.vely >= self.rad):
            self.vely = - self.vely * 0.9

        elif not(self.y + self.vely <= winy - self.rad):
            self.vely = - self.vely * 0.9

        if not (self.x + self.velx >= self.rad):
            self.velx = - self.velx * 0.6

        elif not (self.x + self.velx <= winx - self.rad):
            self.velx = - self.velx * 0.6

        self.x += self.velx
        self.y += self.vely

b1 = ball(25, 100, 70, 0, 10, 0.67,  0.5, 1.5, "ball.webp")

clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.blit(b_img, (0,0))
    b1.drawer()
    b1.gravity()
    b1.movement()
    pygame.display.update()
pygame.quit()
