import handler_gui_elements
import pygame
from pygame.locals import *

class Layers:
    def __init__(self):
        self.elements = []
        self.window_width = 1600
        self.window_height = 900
        self.x = 0
        self.y = 0
        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill((204,204,204))

    def element_add (self, element):
        self.elements.append(element)

    def element_remove (self, element):
        self.elements.append(element)

    def hide (self):
        for element in self.elements:
            element.update_position(element.x + 3000, element.y)

    def show(self):
        for element in self.elements:
            element.update_position(element.default_x, element.default_y)

    def draw(self, screen):
        for element in self.elements:
            screen.blit(element.image, (element.x + self.x, element.y + self.y))

# LAYERS: GAMEPLAY-SPECIFIC
class layer_game (Layers):
    def __init__(self):
        super().__init__()

# LAYERS: MAIN MENU
class layer_main_menu_root (Layers):
    def __init__(self):
        super().__init__()
        
        from handler_gui_sizing import get_sizing
        sizing = get_sizing()
        
        # Calculate button size as percentage of window
        button_width = sizing.rel_width(12.5)  # 12.5% of window width
        button_height = sizing.rel_height(5.5)  # 5.5% of window height
        
        # Position buttons in center, with some spacing
        new_game_y = sizing.rel_height(45)  # 45% down from top
        exit_y = sizing.rel_height(55)      # 55% down from top
        
        # Center buttons horizontally
        button_x = sizing.center_x(button_width)
        
        self.element_add(handler_gui_elements.element_button_text(
            "New Game",
            (button_x, new_game_y),
            (button_width, button_height)
        ))
        
        self.element_add(handler_gui_elements.element_button_text(
            "Exit",
            (button_x, exit_y),
            (button_width, button_height)
        ))
