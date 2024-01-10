import sys
import pygame
from pickle import dump, load

colors = {
    "yellow": (255, 255, 51),
    "white": (255, 255, 255),
    "light gray": (105, 105, 105),
    "silver": (207, 207, 207),
    "red": (255, 69, 0),
    "black": (0, 0, 0),
    "timberwolf": (216, 219, 199),
    "bittersweet": (254, 95, 85)
}

class fonts:

    def __init__(self):
        self.font = pygame.font.SysFont("Orbitron Regular", 28)
        self.spfont = pygame.font.SysFont("Exo 2", 18)
        self.sfont = pygame.font.SysFont("Orbitron Regular", 20)
        self.lfont = pygame.font.SysFont("Orbitron Regular", 40)
        self.xlfont = pygame.font.SysFont("Orbitron Regular", 50)
        self.titlefont = pygame.font.SysFont("Lexend Peta Regular", 76)


        self.fonts = {
            'sm': self.sfont,
            'sm+': self.spfont,
            'm': self.font,
            'l': self.lfont,
            'xl': self.xlfont,
            'title': self.titlefont
        }

class Button:

    def __init__(self, content: str, width: int, height: int, pos: tuple, font_size: str, button: str, func) -> None:
        self.content = content
        self.width = width
        self.height = height
        self.pos = pos
        self.size = font_size
        self.button = button
        self.button_img = pygame.image.load(self.button).convert_alpha()
        self.button_img = pygame.transform.scale(self.button_img, (width, height))
        self.button_rect = self.button_img.get_rect(center = self.pos)
        self.hover = None
        self.fonts = fonts()
        self.font = self.fonts.fonts[self.size].render(self.content, True, colors["white"], None).convert_alpha()
        self.font_rect = self.font.get_rect(center = self.pos)
        self.func = func
        clicked = False

    def draw(self, app):
        app.win.blit(self.button_img, self.button_rect)
        app.win.blit(self.font, self.font_rect)

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.font = self.fonts.fonts[self.size].render(self.content, True, colors["yellow"], None)
        else: self.font = self.fonts.fonts[self.size].render(self.content, True, colors["white"], None)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not(Button.clicked):
                Button.clicked = True
                return self.func()
        if not(pygame.mouse.get_pressed()[0]):
            Button.clicked = False

class Slider:

    def __init__(self, max: int, min: int, init_value: float, width: int, height: int, pos: tuple, label_pos: str, label_cont: str):
        self.max = max
        self.min = min
        self.init_value = init_value

        self.width = width
        self.height = height
        self.pos = pos
        self.label_pos = label_pos
        self.label_cont = label_cont

        self.slider_left = self.pos[0] - self.width//2
        self.slider_right = self.pos[0] + self.width//2
        self.slider_top = self.pos[1] - self.height//2
        self.slider_bottom = self.pos[1] + self.height//2

        self.positions = {
            "top": (self.slider_left, self.slider_top - self.height - 10)
        }

        self.init_value = self.width * self.init_value
        self.digital_font = pygame.font.SysFont("Digital-7 Mono", self.height - 2)

        self.label_font = None
        self.label_rect = None

        self.slider_rect = pygame.Rect(self.slider_left, self.slider_top, self.width, self.height)
        self.button_rect = pygame.Rect(self.slider_left + self.init_value - 5, self.slider_top - 2, 10, self.height + 4)
        self.slider_outline = pygame.Rect(self.slider_left - 4 , self.slider_top - 4, self.width + 8, self.height + 8)
        self.label_bg = pygame.Rect(self.positions[self.label_pos][0], self.positions[self.label_pos][1], self.width, self.height)
        self.label_bg_outline = pygame.Rect(self.positions[self.label_pos][0] - 4, self.positions[self.label_pos][1] - 4, self.width + 8, self.height + 8)

    def draw(self, app):
        pygame.draw.rect(app.win, colors["black"], self.slider_outline)
        pygame.draw.rect(app.win, colors["white"], self.slider_rect)
        pygame.draw.rect(app.win, colors["silver"], self.button_rect)

    def drag(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.slider_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.button_rect.centerx = mouse_pos[0]

    def get_val(self):
        val = (self.width - (self.slider_right - self.button_rect.centerx))/(self.width - 1) * (self.max-self.min) + self.min
        return round(val, 1)

    def label(self, app):
        self.label_font = self.digital_font.render(str(Slider.get_val(self)) + " " + self.label_cont, True, colors["white"], None).convert_alpha()
        self.label_rect = self.label_font.get_rect(center = self.label_bg.center)
        pygame.draw.rect(app.win, colors["silver"], self.label_bg_outline)
        pygame.draw.rect(app.win, colors["black"], self.label_bg)
        app.win.blit(self.label_font, self.label_rect)

class Textbox:

    def __init__(self, pos:tuple, size: tuple, max_char: int):
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
        self.fonts = fonts()
        self.font = self.fonts.fonts["sm+"]
        self.user_text = ''
        self.max_char = max_char
        self.box = pygame.Rect(self.pos[0] - self.width, self.pos[1] - self.height, self.width, self.height)
        self.box_outline = pygame.Rect(self.pos[0] - self.width - 2, self.pos[1] - self.height - 2, self.width + 4, self.height + 4)
        self.color_active = colors['black']
        self.color_passive = colors['light gray']
        self.color = self.color_passive
        self.active = False

    def text_place(self, win):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        pygame.draw.rect(win, self.color, self.box_outline, 2)
        pygame.draw.rect(win, colors["white"], self.box)
        text = self.font.render(self.user_text, True, colors["black"], None)
        win.blit(text, text.get_rect(topleft = (self.box.x + 5, self.box.y + 5)))

    def event_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box_outline.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.active = False
                else:
                    if len(self.user_text) < self.max_char:
                        self.user_text += event.unicode
        return self.user_text

class Label:

    def __init__(self, content: str, pos: tuple):
        self.content = content
        self.pos = pos

        self.fonts = fonts()

        self.text = self.fonts.fonts["sm"].render(self.content, True, colors["white"], None)
        self.text_rect = self.text.get_rect(topleft = self.pos)

    def label_update(self, app):
        app.win.blit(self.text, self.text_rect)

def loading_screen():
    pygame.init()
    win = pygame.display.set_mode((500, 250))
    pygame.display.set_caption("PhysicsXperience")
    t = 0
    dt = 0.01
    clock = pygame.time.Clock()
    win_size = pygame.display.get_window_size()

    logo_font = pygame.font.SysFont("Above DEMO Regular", 40)
    logo = logo_font.render("PhysicsXperience", True, colors["bittersweet"], None)
    logo_rect = logo.get_rect(center = (win_size[0]//2, win_size[1]//2 - 20))

    width = 0

    icon = pygame.image.load("icon.png").convert()
    pygame.display.set_icon(icon)

    loading_bar = pygame.Rect(win_size[0]//2 - 127, win_size[1]//2 + 24, 254, 24)

    font = pygame.font.SysFont("Exo 2", 20)
    font_text1 = font.render("Initialising Variables...", True, colors["black"], None)
    font_text2 = font.render("Creating Bodies...", True, colors["black"], None)
    font_text3 = font.render("Launching Simulator...", True, colors["black"], None)
    rect1 = font_text1.get_rect(center = (win_size[0]//2, win_size[1]//2 + 70))
    rect2 = font_text2.get_rect(center=(win_size[0]//2, win_size[1]//2 + 70))
    rect3 = font_text3.get_rect(center=(win_size[0]//2, win_size[1]//2 + 70))

    while t < 5:
        clock.tick(100)
        win.fill(colors["timberwolf"])
        pygame.draw.rect(win, colors["black"], loading_bar)
        win.blit(logo, logo_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if t <= 2:
            win.blit(font_text1, rect1)
            width += 0.625
        elif t <= 3:
            win.blit(font_text1, rect1)
        elif t <= 4:
            win.blit(font_text2, rect2)
            width += 1.125
        elif t <= 5:
            win.blit(font_text3, rect3)
            width += 0.125
        elif t >= 5:
            pygame.time.wait(3000)
        bar = pygame.Rect(win_size[0]//2 - 125, win_size[1]//2 + 26, width, 20)
        pygame.draw.rect(win, colors["white"], bar)
        pygame.display.flip()
        t += dt

    pygame.quit()

class login:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((600, 300))
        self.ch = 1

    def main(self):
        clock = pygame.time.Clock()
        win_size = pygame.display.get_window_size()
        pygame.display.set_caption("PhysicsXperience")
        icon = pygame.image.load("icon.png").convert()
        pygame.display.set_icon(icon)

        font = pygame.font.SysFont("Exo 2", 20)
        title_font = pygame.font.SysFont("Exo 2", 50)

        forgot_pass = title_font.render("FORGOT PASSWORD", True, colors["bittersweet"], None)
        forgot_pass_rect = forgot_pass.get_rect(center=(win_size[0] // 2, win_size[1] // 2 - 100))
        sign_in = title_font.render("SIGN IN", True, colors["bittersweet"], None)
        sign_in_rect = sign_in.get_rect(center = (win_size[0]//2, win_size[1]//2 - 100))
        sign_up = title_font.render("SIGN UP", True, colors["bittersweet"], None)
        sign_up_rect = sign_up.get_rect(center=(win_size[0] // 2, win_size[1] // 2 - 100))

        u_lab = font.render("USERNAME", True, colors["black"], None)
        p_lab = font.render("PASSWORD", True, colors["black"], None)
        fp_lab = font.render("NEW PASSWORD", True, colors["black"], None)
        u_lab_rect = u_lab.get_rect(center = (win_size[0]//2 - 180, win_size[1]//2 - 17))
        p_lab_rect = p_lab.get_rect(center = (win_size[0]//2 - 180, win_size[1]//2 + 33))
        fp_lab_rect = p_lab.get_rect(center=(win_size[0] // 2 - 180, win_size[1] // 2 + 33))

        username_t = Textbox((win_size[0]//2 + 250, win_size[1]//2), (300, 30), 16)
        password_t = Textbox((win_size[0]//2 + 250, win_size[1]//2 + 50), (300, 30), 16)

        sign_in_but = Button("Sign in", 52, 20, (win_size[0]//2 + 220, win_size[1]//2 + 50 + 20), 'sm+', "Empty.png", lambda: clicked())
        sign_up_but = Button("Sign up", 52, 20, (win_size[0]//2 + 220, win_size[1]//2 + 50 + 20), 'sm+', "Empty.png", lambda: clicked())
        submit_but = Button("Submit", 75, 30, (win_size[0]//2, win_size[1]//2 + 50 + 20), 'sm+', "button.png", lambda: clicked())
        forgot_pass_but = Button("Forgot password?", 145, 20, (win_size[0]//2 + 180, win_size[1]//2 + 50 + 45), 'sm+', "Empty.png", lambda: clicked())

        def clicked():
            return True

        def check_info_sign_in(username, password):
            with open("log_in.bin", "rb") as f:
                try:
                    while True:
                        rec = load(f)
                        if username == rec[0] and password == rec[1]:
                            return "SUCCESS"
                        elif username == "" or password == "":
                            return "FIELDS CAN'T BE LEFT EMPTY"
                        elif username == rec[0] and password != rec[1]:
                            return "INCORRECT PASSWORD"
                except EOFError:
                    return f"NO ACCOUNT WITH USERNAME '{username}'"

        def check_info_sign_up(username, password):
            usernames = []
            with open("log_in.bin", "ab+") as f:
                f.seek(0)
                try:
                    while True:
                        rec = load(f)
                        usernames += [rec[0]]
                except EOFError:
                    pass
                if username == "" or password == "":
                    return "FIELDS CAN'T BE LEFT EMPTY"
                elif username in usernames:
                    return "ACCOUNT ALREADY EXISTS"
                else:
                    info = (username, password)
                    dump(info, f)
                    return "SUCCESS"

        def check_info_forgot_pass(username, password):
            records = []
            with open("log_in.bin", "rb") as f:
                f.seek(0)
                search = 0
                try:
                    while True:
                        rec = load(f)
                        if username in rec:
                            records += [(username, password)]
                            search = 1
                        else:
                            records += [rec]
                except EOFError:
                    if search == 0:
                        return f"NO ACCOUNT WITH USERNAME '{username}'"
                with open("log_in.bin", "wb") as f:
                    for i in records:
                        dump(i, f)
                return "SUCCESS"

        def forgot_pass_f():
            error_msg = ""
            error = font.render(error_msg, True, colors["black"], None)
            error_rect = error.get_rect(center=(win_size[0] // 2, win_size[1] // 2 + 100))
            while True:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    username = username_t.event_check(event)
                    password = password_t.event_check(event)
                self.win.fill(colors["timberwolf"])
                username_t.text_place(self.win)
                password_t.text_place(self.win)
                self.win.blit(forgot_pass, forgot_pass_rect)
                self.win.blit(u_lab, u_lab_rect)
                self.win.blit(fp_lab, fp_lab_rect)
                sign_in_but.draw(self)
                sign_in_but.check_hover()
                if sign_in_but.check_click():
                    self.ch = 1
                    login.main(self)
                    break
                submit_but.draw(self)
                submit_but.check_hover()
                if submit_but.check_click():
                    msg = check_info_forgot_pass(username, password)
                    if msg == "SUCCESS":
                        return username
                        break
                    else:
                        error_msg = msg
                        error = font.render(error_msg, True, colors["black"], None)
                        error_rect = error.get_rect(center=(win_size[0] // 2, win_size[1] // 2 + 100))
                self.win.blit(error, error_rect)
                pygame.display.flip()

        def sign_in_f():
            error_msg = ""
            error = font.render(error_msg, True, colors["black"], None)
            error_rect = error.get_rect(center = (win_size[0]//2, win_size[1]//2 + 100))
            while True:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    username = username_t.event_check(event)
                    password = password_t.event_check(event)
                self.win.fill(colors["timberwolf"])
                username_t.text_place(self.win)
                password_t.text_place(self.win)
                self.win.blit(sign_in, sign_in_rect)
                self.win.blit(u_lab, u_lab_rect)
                self.win.blit(p_lab, p_lab_rect)
                sign_up_but.draw(self)
                sign_up_but.check_hover()
                if sign_up_but.check_click():
                    self.ch = 0
                    login.main(self)
                    break
                forgot_pass_but.draw(self)
                forgot_pass_but.check_hover()
                if forgot_pass_but.check_click():
                    self.ch = 2
                    login.main(self)
                    break
                submit_but.draw(self)
                submit_but.check_hover()
                if submit_but.check_click():
                    msg = check_info_sign_in(username, password)
                    if msg == "SUCCESS":
                        return username
                        break
                    else:
                        error_msg = msg
                        error = font.render(error_msg, True, colors["black"], None)
                        error_rect = error.get_rect(center = (win_size[0]//2, win_size[1]//2 + 120))
                self.win.blit(error, error_rect)
                pygame.display.flip()

        def sign_up_f():
            error_msg = ""
            error = font.render(error_msg, True, colors["black"], None)
            error_rect = error.get_rect(center=(win_size[0] // 2, win_size[1] // 2 + 100))
            while True:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    username = username_t.event_check(event)
                    password = password_t.event_check(event)
                self.win.fill(colors["timberwolf"])
                username_t.text_place(self.win)
                password_t.text_place(self.win)
                self.win.blit(sign_up, sign_up_rect)
                self.win.blit(u_lab, u_lab_rect)
                self.win.blit(p_lab, p_lab_rect)
                sign_in_but.draw(self)
                sign_in_but.check_hover()
                if sign_in_but.check_click():
                    self.ch = 1
                    login.main(self)
                    break
                submit_but.draw(self)
                submit_but.check_hover()
                if submit_but.check_click():
                    msg = check_info_sign_up(username, password)
                    if msg == "SUCCESS":
                        return username
                        break
                    else:
                        error_msg = msg
                        error = font.render(error_msg, True, colors["black"], None)
                        error_rect = error.get_rect(center=(win_size[0]//2, win_size[1]//2 + 100))
                self.win.blit(error, error_rect)
                pygame.display.flip()

        if self.ch == 0:
            return sign_up_f()
        elif self.ch == 1:
            return sign_in_f()
        elif self.ch == 2:
            return forgot_pass_f()

