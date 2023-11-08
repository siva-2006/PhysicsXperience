import pygame
import sys

pygame.init()

class fonts:
    def __init__(self):
        self.font = pygame.font.SysFont("Orbitron Regular", 28)
        self.sfont = pygame.font.SysFont("Orbitron Regular", 20)
        self.lfont = pygame.font.SysFont("Orbitron Regular", 40)
        self.xlfont = pygame.font.SysFont("Orbitron Regular", 50)
        self.titlefont = pygame.font.SysFont("Lexend Peta Regular", 76)


        self.fonts = {
            'sm': self.sfont,
            'm': self.font,
            'l': self.lfont,
            'xl': self.xlfont,
            'title': self.titlefont
        }


class Menu:
    def __init__(self, app, bg="gray") -> None:
        self.app = app
        self.bg = bg
        self.fonts = fonts()
        self.win_size = app.win.get_size()
    def main_menu(self):
        running = True
        button = "button.png"
        title = self.fonts.fonts['title'].render("PHYSICSXPERIENCE", True, "white", None)
        title_rect = title.get_rect(center = (self.win_size[0]//2, 120))
        start = Button("START", 250, 100, (self.win_size[0]//2, 300), 'm', button, lambda: test())
        help = Button("HELP", 250, 100, (self.win_size[0] // 2, 450), 'm', button, lambda: test())
        exit = Button("EXIT", 250, 100, (self.win_size[0] // 2, 600), 'm', button, lambda: quit())
        while running:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
            self.app.win.fill((105, 105, 105))
            start.check_hover()
            help.check_hover()
            exit.check_hover()
            start.check_click()
            help.check_click()
            exit.check_click()
            start.draw(self.app)
            help.draw(self.app)
            exit.draw(self.app)
            app.win.blit(title, title_rect)
            pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()
class Button:
    def __init__(self, content: str, width: int, height: int, pos: tuple, size: str, button: str, func) -> None:
        self.content = content
        self.width = width
        self.height = height
        self.pos = pos
        self.size = size
        self.button = button
        self.button_img = pygame.image.load(self.button).convert_alpha()
        self.button_img = pygame.transform.scale(self.button_img, (width, height))
        self.button_rect = self.button_img.get_rect(center = self.pos)
        self.hover = None
        self.fonts = fonts()
        self.font = self.fonts.fonts[self.size].render(self.content, True, "white", None)
        self.font_rect = self.font.get_rect(center = self.pos)
        self.func = func
        self.clicked = False

    def draw(self, app):
        app.win.blit(self.button_img, self.button_rect)
        app.win.blit(self.font, self.font_rect)

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.font = self.fonts.fonts[self.size].render(self.content, True, (255,255,51), None)
        else: self.font = self.fonts.fonts[self.size].render(self.content, True, "white", None)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                self.func()

        if not(pygame.mouse.get_pressed()[0]):
            self.clicked = False

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])

        # label
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self, app):
        pygame.draw.rect(app.screen, "darkgray", self.container_rect)
        pygame.draw.rect(app.screen, BUTTONSTATES[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self, app):
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)
        app.win.blit(self.text, self.label_rect)

class App:
    def __init__(self):
        self.win = pygame.display.set_mode((1200, 750))
        self.menu = Menu(self)

    def return_menu(self):
        return self.menu

def test():
    print("Working!")

app = App()
menu = app.return_menu()
menu.main_menu()
