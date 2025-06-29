import pygame
from menu import Menu
from ui import loading_screen, login

class APP:

    def __init__(self):
        loading_screen()
        log = login()
        self.username = log.main()
        pygame.quit()
        pygame.init()
        self.win = pygame.display.set_mode((1200, 725))
        self.win_size = pygame.display.get_window_size()
        pygame.display.set_caption("PhysicsXperience")
        icon = pygame.image.load("icon.png").convert()
        pygame.display.set_icon(icon)

    def menu(self):
        menu = Menu(self.username, self)
        menu.main_menu()

if __name__ == "__main__":
    with open("log_in.bin", "ab"):
        pass
    app = APP()
    app.menu()