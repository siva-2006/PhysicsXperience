import pygame
from ui import Button, fonts, colors
import sys
from projectile import vertical_projectile, hori_projectile, projectile

class Menu:

    def __init__(self, username, app) -> None:
        self.app = app
        self.username = username
        self.fonts = fonts()
        self.win_size = app.win.get_size()
        self.vert_projectile = vertical_projectile()
        self.hori_projectile = hori_projectile()
        self.projectile = projectile()

    def main_menu(self):
        running = True
        button = "button.png"
        title = self.fonts.fonts['title'].render("PHYSICSXPERIENCE", True, colors["bittersweet"], None)
        title_rect = title.get_rect(center = (self.win_size[0]//2, 120))
        start = Button("START", 200, 75, (self.win_size[0]//2, 400), 'm', button, lambda: Menu.Start(self))
        exit = Button("EXIT", 200, 75, (self.win_size[0]//2, 500), 'm', button, lambda: quit())
        text = self.fonts.fonts['sm+'].render(f"Logged in as '{self.username}'", True, colors["white"], None)
        text_rect = text.get_rect(topright = (self.win_size[0] - 20, self.win_size[0] - 55))

        while running:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.app.win.fill(colors["timberwolf"])
            start.draw(self.app)
            exit.draw(self.app)

            start.check_hover()
            exit.check_hover()

            start.check_click()
            exit.check_click()

            self.app.win.blit(title, title_rect)
            self.app.win.blit(text, text_rect)

            pygame.display.flip()

    def Start(self):
        running = True
        button = "button.png"
        vert_proj = Button("VERTICAL PROJECTILE", 500, 75, (self.win_size[0] // 2, 150), 'm', button, lambda: self.vert_projectile.main(self.app))
        hor_proj = Button("HORIZONTAL PROJECTILE", 500, 75, (self.win_size[0] // 2, 300), 'm', button, lambda: self.hori_projectile.main(self.app))
        proj = Button("NORMAL PROJECTILE", 500, 75, (self.win_size[0] // 2, 450), 'm', button, lambda: self.projectile.main(self.app))
        back = Button("< BACK", 500, 75, (self.win_size[0] // 2, 600), 'm', button, lambda: True)
        while running:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.app.win.fill(colors["timberwolf"])

            vert_proj.check_hover()
            hor_proj.check_hover()
            proj.check_hover()
            back.check_hover()

            vert_proj.check_click()
            hor_proj.check_click()
            proj.check_click()
            if back.check_click():
                return

            vert_proj.draw(self.app)
            hor_proj.draw(self.app)
            proj.draw(self.app)
            back.draw(self.app)

            pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()