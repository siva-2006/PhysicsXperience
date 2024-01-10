import sys
import pygame
from ui import Button, Slider, Label
from math import *
class vertical_projectile:

    def __init__(self) -> None:
        self.dt = 0.01

        self.win_size = pygame.display.get_window_size()
        self.start = False
        self.disable_button = False
        self.disable_slider = False

        self.x = self.win_size[0] // 2
        self.y = 0
        vertical_projectile.coor_return(self)

        self.ball = pygame.image.load("ball.png").convert_alpha()
        self.ball = pygame.transform.scale(self.ball, (20, 20))
        self.bg = pygame.image.load("background.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, self.win_size)

        self.ball_rect = self.ball.get_rect(center = (self.win_size[0]//2, self.win_size[1] - 160))
        self.ground_rect = pygame.Rect(0, self.win_size[1] - 150, self.win_size[0], 150)

        self.vel_slider = Slider(30, 5, 0.5, 300, 30, (self.ground_rect.centerx - 200, self.ground_rect.centery + 20), "top", "m/s")
        self.g_slider = Slider(17, 7, 0.28, 200, 30, (self.ground_rect.centerx + 420, self.ground_rect.centery + 20), "top", "m/s^2")

        self.reset_label = Label("Press 'R' to reset", (10, 10))
        self.escape_label = Label("Press 'Q' to quit", (10, 40))
        self.vels_label = Label("Velocity : ", (self.ground_rect.centerx - 475, self.ground_rect.centery - 15))
        self.gs_label = Label("Acceleration due to g : ", (self.ground_rect.centerx + 60, self.ground_rect.centery - 15))
        self.sim_label = Label("Simulation Under Progress...", (self.ground_rect.topleft[0] + 10, self.ground_rect.topleft[1] - 50))

        self.play_button = Button("", 50, 50, self.ground_rect.center,"sm", "play-button.png", lambda : vertical_projectile.pause(self))

    def update_pos(self):
        if self.start == True:
            self.y += self.vel_c
            if self.y <= 0:
                self.y = 0
                self.vel_c = 0
                self.vel = 0
            self.vel_c += self.g
            self.vel = self.vel_c/self.dt
        vertical_projectile.coor_return(self)
        self.ball_rect.center = (self.win_size[0]//2, self.y_c)

    def draw_proj(self, app):
        app.win.blit(self.ball, self.ball_rect)

    def reset(self, app):
        vertical_projectile.__init__(self)
        vertical_projectile.main(self, app)

    def value_get(self):
        if self.disable_slider == False:
            self.vel_s = self.vel_slider.get_val()
            self.g_s = self.g_slider.get_val()
            self.vel = self.vel_s
            self.g = -self.g_s * self.dt ** 2
            self.vel_c = self.vel * self.dt

    def check_stop(self):
        if self.ground_rect.colliderect(self.ball_rect):
            self.start = False
            self.disable_button = True
            self.vel_c = 0
            self.vel = 0

    def coor_return(self):
        self.y_c = self.win_size[1] - 160 - self.y*9

    def run(self, app):
        self.vel_slider.draw(app)
        self.g_slider.draw(app)
        self.vel_slider.get_val()
        self.g_slider.get_val()
        self.vel_slider.label(app)
        self.g_slider.label(app)
        self.vels_label.label_update(app)
        self.gs_label.label_update(app)
        if self.disable_slider == False:
            self.vel_slider.drag()
            self.g_slider.drag()
        else:
            self.sim_label.label_update(app)
        self.play_button.draw(app)
        self.play_button.check_click()
        self.y_label = Label(f"Y - pos : {round(self.y, 2)} m", (self.win_size[0] - 250, 10))
        self.vel_label = Label(f"Velocity : {round(self.vel, 2)} m/s", (self.win_size[0] - 250, 40))
        self.reset_label.label_update(app)
        self.escape_label.label_update(app)
        self.y_label.label_update(app)
        self.vel_label.label_update(app)

    def pause(self):
        if self.start == False and self.disable_button == False:
            self.start = True
        else:
            self.start = False

    def main(self, app):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(100)

            if self.start == False:
                vertical_projectile.value_get(self)
            else:
                self.disable_slider = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                vertical_projectile.reset(self, app)
            if keys[pygame.K_q]:
                return
            app.win.blit(self.bg, (0,0))
            vertical_projectile.check_stop(self)
            vertical_projectile.update_pos(self)
            vertical_projectile.draw_proj(self, app)
            vertical_projectile.run(self, app)
            pygame.display.flip()

class hori_projectile:

    def __init__(self):
        self.dt = 0.01
        self.g = -9.8

        self.win_size = pygame.display.get_window_size()
        self.start = False
        self.disable_button = False

        self.ball = pygame.image.load("ball.png")
        self.ball = pygame.transform.scale(self.ball, (20, 20))
        self.bg = pygame.image.load("background.jpg")
        self.bg = pygame.transform.scale(self.bg, self.win_size)

        self.ground_rect = pygame.Rect(0, self.win_size[1] - 150, self.win_size[0], 150)

        self.vel = 0
        self.vely = 0

        self.x = 0
        self.y = 0
        hori_projectile.coor_return(self)

        self.ball_rect = self.ball.get_rect(center=(self.x_c, self.y_c))
        self.play_button = Button("", 50, 50, self.ground_rect.center, "sm", "play-button.png", lambda: hori_projectile.pause(self))

        self.vel_slider = Slider(37, 0, 0.5, 250, 30, (self.ground_rect.centerx - 200, self.ground_rect.centery + 15), "top", "m/s")
        self.h_slider = Slider(60, 0, 0, 300, 30, (self.ground_rect.centerx + 300, self.ground_rect.centery + 15) ,"top", "m")

        self.reset_label = Label("Press 'R' to reset", (10, 10))
        self.escape_label = Label("Press 'Q' to quit", (10, 40))
        self.h_label = Label("Height : ", (self.ground_rect.centerx + 50, self.ground_rect.centery - 15))
        self.vels_label = Label("Velocity : ", (self.ground_rect.centerx - 450, self.ground_rect.centery - 15))
        self.sim_label = Label("Simulation Under Progress...", (self.ground_rect.topleft[0] + 10, self.ground_rect.topleft[1] - 50))

    def coor_return(self):
        self.x_c = self.x*9 + 10
        self.y_c = self.win_size[1] - self.y*9 - 160

    def update_pos(self):
        if self.start == True:
            if self.y + self.vely * self.dt >= 0:
                self.x += self.vel * self.dt
                self.y += self.vely * self.dt
            else:
                self.y = 0
                self.vely = 0
                self.vel = 0
                self.start = False
                self.disable_button = True
            self.vely += self.g * self.dt
        hori_projectile.coor_return(self)
        self.ball_rect.center = (self.x_c, self.y_c)

    def pause(self):
        if self.disable_button == False:
            if self.start == False: self.start = True
            else: self.start = False

    def draw_proj(self, app):
        app.win.blit(self.ball, self.ball_rect)

    def reset(self, app):
        hori_projectile.__init__(self)
        hori_projectile.main(self, app)

    def get_value(self):
        self.vel = self.vel_slider.get_val()
        self.y = self.h_slider.get_val()

    def main(self, app):
        clock = pygame.time.Clock()
        while self.start == False:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                hori_projectile.reset(self, app)
            if keys[pygame.K_q]:
                return

            app.win.blit(self.bg, (0, 0))
            hori_projectile.update_pos(self)
            hori_projectile.draw_proj(self, app)
            self.vel_slider.draw(app)
            self.vel_slider.label(app)
            self.vel_slider.drag()
            self.h_slider.draw(app)
            self.h_slider.label(app)
            self.h_slider.drag()
            self.play_button.draw(app)
            self.play_button.check_click()
            self.x_label = Label(f"X - pos : {round(self.x, 2)} m", (self.win_size[0] - 260, 10))
            self.y_label = Label(f"Y - pos : {round(self.y, 2)} m", (self.win_size[0] - 260, 40))
            self.vel_label = Label(f"Y Velocity : {round(self.vely, 2)} m/s", (self.win_size[0] - 260, 70))
            self.x_label.label_update(app)
            self.y_label.label_update(app)
            self.vel_label.label_update(app)
            self.reset_label.label_update(app)
            self.escape_label.label_update(app)
            self.h_label.label_update(app)
            self.vels_label.label_update(app)
            hori_projectile.get_value(self)
            hori_projectile.coor_return(self)
            pygame.display.flip()

        running = True

        hori_projectile.get_value(self)

        while running:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                hori_projectile.reset(self, app)
            if keys[pygame.K_q]:
                return

            app.win.blit(self.bg, (0, 0))
            hori_projectile.update_pos(self)
            hori_projectile.draw_proj(self, app)
            self.vel_slider.draw(app)
            self.vel_slider.label(app)
            self.h_slider.draw(app)
            self.h_slider.label(app)
            self.play_button.draw(app)
            self.play_button.check_click()
            self.x_label = Label(f"X - pos : {round(self.x, 2)} m", (self.win_size[0] - 260, 10))
            self.y_label = Label(f"Y - pos : {round(self.y, 2)} m", (self.win_size[0] - 260, 40))
            self.vel_label = Label(f"Y Velocity : {round(self.vely, 2)} m/s", (self.win_size[0] - 260, 70))
            self.x_label.label_update(app)
            self.y_label.label_update(app)
            self.vel_label.label_update(app)
            self.reset_label.label_update(app)
            self.escape_label.label_update(app)
            self.h_label.label_update(app)
            self.vels_label.label_update(app)
            self.sim_label.label_update(app)
            pygame.display.flip()


class projectile:

    def __init__(self):
        self.dt = 0.01
        self.g = -9.8

        self.win_size = pygame.display.get_window_size()
        self.start = False
        self.disable_button = False

        self.ball = pygame.image.load("ball.png")
        self.ball = pygame.transform.scale(self.ball, (20, 20))
        self.bg = pygame.image.load("background.jpg")
        self.bg = pygame.transform.scale(self.bg, self.win_size)

        self.ground_rect = pygame.Rect(0, self.win_size[1] - 150, self.win_size[0], 150)

        self.velx = 0
        self.vely = 0
        self.vel = 0
        self.angle = 0

        self.x = 0
        self.y = 0
        projectile.coor_return(self)

        self.ball_rect = self.ball.get_rect(center=(self.x_c, self.y_c))

        self.play_button = Button("", 50, 50, self.ground_rect.center, "sm", "play-button.png", lambda: projectile.pause(self))

        self.vel_slider = Slider(35, 0, 0.5, 250, 30, (self.ground_rect.centerx - 200, self.ground_rect.centery + 15), "top", "m/s")
        self.ang_slider = Slider(90, 0, 0, 360, 30, (self.ground_rect.centerx + 330, self.ground_rect.centery + 15), "top", "deg")

        self.reset_label = Label("Press 'R' to reset", (10, 10))
        self.escape_label = Label("Press 'Q' to quit", (10, 40))
        self.ang_label = Label("Angle : ", (self.ground_rect.centerx + 50, self.ground_rect.centery - 15))
        self.vels_label = Label("Velocity : ", (self.ground_rect.centerx - 450, self.ground_rect.centery - 15))
        self.sim_label = Label("Simulation Under Progress...", (self.ground_rect.topleft[0] + 10, self.ground_rect.topleft[1] - 50))

    def coor_return(self):
            self.x_c = self.x * 9 + 10
            self.y_c = self.win_size[1] - self.y * 9 - 160

    def pause(self):
        if self.disable_button == False:
            if self.start == False: self.start = True
            else: self.start = False

    def update_pos(self):
        if self.start == True:
            if self.y + self.vely * self.dt >= 0:
                self.x += self.velx * self.dt
                self.y += self.vely * self.dt
            else:
                self.y = 0
                self.vely = 0
                self.velx = 0
                self.vel = 0
                self.start = False
                self.disable_button = True
            self.vely += self.g * self.dt
        hori_projectile.coor_return(self)
        self.ball_rect.center = (self.x_c, self.y_c)

    def draw_proj(self, app):
        app.win.blit(self.ball, self.ball_rect)

    def reset(self, app):
        projectile.__init__(self)
        projectile.main(self, app)

    def get_value(self):
        self.vel = self.vel_slider.get_val()
        self.angle = self.ang_slider.get_val()
        self.velx = cos(radians(self.angle)) * self.vel
        self.vely = sin(radians(self.angle)) * self.vel

    def main(self, app):
        clock = pygame.time.Clock()
        while self.start == False:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                projectile.reset(self, app)
            if keys[pygame.K_q]:
                return

            app.win.blit(self.bg, (0, 0))
            app.win.blit(self.bg, (0, 0))
            projectile.update_pos(self)
            projectile.draw_proj(self, app)
            self.vel_slider.draw(app)
            self.vel_slider.label(app)
            self.vel_slider.drag()
            self.ang_slider.draw(app)
            self.ang_slider.label(app)
            self.ang_slider.drag()
            self.play_button.draw(app)
            self.play_button.check_click()
            self.x_label = Label(f"X - pos : {round(self.x, 2)} m", (self.win_size[0] - 260, 10))
            self.y_label = Label(f"Y - pos : {round(self.y, 2)} m", (self.win_size[0] - 260, 40))
            self.velx_label = Label(f"X Velocity : {round(self.velx, 2)} m/s", (self.win_size[0] - 260, 70))
            self.vely_label = Label(f"Y Velocity : {round(self.vely, 2)} m/s", (self.win_size[0] - 260, 100))
            self.vel_label = Label(f"Velocity : {round(self.vel, 2)} m/s", (self.win_size[0] - 260, 130))
            self.x_label.label_update(app)
            self.y_label.label_update(app)
            self.velx_label.label_update(app)
            self.vely_label.label_update(app)
            self.vel_label.label_update(app)
            self.reset_label.label_update(app)
            self.escape_label.label_update(app)
            self.ang_label.label_update(app)
            self.vels_label.label_update(app)
            projectile.get_value(self)
            projectile.coor_return(self)
            pygame.display.flip()

        running = True

        projectile.get_value(self)

        while running:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                projectile.reset(self, app)
            if keys[pygame.K_q]:
                return

            app.win.blit(self.bg, (0, 0))
            projectile.update_pos(self)
            projectile.draw_proj(self, app)
            self.vel_slider.draw(app)
            self.vel_slider.label(app)
            self.ang_slider.draw(app)
            self.ang_slider.label(app)
            self.play_button.draw(app)
            self.play_button.check_click()
            self.x_label = Label(f"X - pos : {round(self.x, 2)} m", (self.win_size[0] - 260, 10))
            self.y_label = Label(f"Y - pos : {round(self.y, 2)} m", (self.win_size[0] - 260, 40))
            self.velx_label = Label(f"X Velocity : {round(self.velx, 2)} m/s", (self.win_size[0] - 260, 70))
            self.vely_label = Label(f"Y Velocity : {round(self.vely, 2)} m/s", (self.win_size[0] - 260, 100))
            self.vel_label = Label(f"Velocity : {round(self.vel, 2)} m/s", (self.win_size[0] - 260, 130))
            self.x_label.label_update(app)
            self.y_label.label_update(app)
            self.velx_label.label_update(app)
            self.vely_label.label_update(app)
            self.vel_label.label_update(app)
            self.reset_label.label_update(app)
            self.escape_label.label_update(app)
            self.ang_label.label_update(app)
            self.vels_label.label_update(app)
            self.sim_label.label_update(app)
            pygame.display.flip()