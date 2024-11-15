import pygame

class WindowHandler:
    def __init__(self, caption):
        pygame.init()
        info = pygame.display.Info()
        self.display_width = info.current_w
        self.display_height = info.current_h
        self.window_width = self.display_width
        self.window_height = self.display_height - 100
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.set_caption(caption)
        self.menu_bar = None
        self.menu_height = 30  # Default menu bar height

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def get_window(self):
        return self.window

    def update_display(self):
        """Update the display and draw the menu bar if enabled"""
        if self.menu_bar:
            self.menu_bar.draw(self.window)
        pygame.display.update()

    def clear_screen(self, color=(0, 0, 0)):
        self.window.fill(color)

    def handle_events(self):
        """Handle window events including menu interactions"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import main
                main.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                handler_game.create_allLayers()  # Recreate layers with new dimensions
                handler_game.create_allPanels()  # Recreate panels with new dimensions
            elif self.menu_bar:
                self.menu_bar.handle_event(event)
            
            # Return the event so it can be handled by other systems
            return event

    def resize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.update_display()

        self.display_width = width
        self.display_height = height

        return self.display_width, self.display_height

    def get_display_size(self):
        return self.display_width, self.display_height

    def get_window_size(self):
        return self.window_width, self.window_height

    def get_display_center(self):
        return self.display_width // 2, self.display_height // 2

    def get_window_center(self):
        return self.window_width // 2, self.window_height // 2

    def set_titlebar(self, show_titlebar=True):
        if show_titlebar:
            pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        else:
            pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE | pygame.NOFRAME)

    def set_menu_bar(self, show_menu=True):
        """Enable or disable the menu bar"""
        if show_menu and not self.menu_bar:
            from handler_gui_elements import element_menu_bar
            self.menu_bar = element_menu_bar(0, 0, self.window_width, self.menu_height)
        elif not show_menu:
            self.menu_bar = None
        return self.menu_bar

    def add_menu(self, name, items):
        """Add a menu to the menu bar with specified items"""
        if self.menu_bar:
            self.menu_bar.add_menu(name, items)


# Example usage:
# window_handler = WindowHandler("Match 3 Game")
# window_handler.get_window()
