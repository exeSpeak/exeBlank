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

    def element_add (self, UIElement):
        self.elements.append(UIElement)

    def element_remove (self, UIElement):
        self.elements.remove(UIElement)

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
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        

# LAYERS: MAIN MENU
class layer_main_menu_root (Layers):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        
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

# LAYERS: UTILITY
# FADE IN/FADE OUT FUNCTIONALITY LAYER; THIS IS A SIMPLE BLACK SCREEN AND IS NOT THE LOADING SCREEN LAYER
class layer_fades (Layers):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        
        from handler_gui_sizing import get_sizing
        sizing = get_sizing()
        
        # Create a full-screen black overlay
        self.fade_overlay = handler_gui_elements.element_box_color(
            (0, 0, 0),  # Black color
            (0, 0),     # Top-left position
            (sizing.cached_width, sizing.cached_height)  # Full screen size
        )
        self.fade_overlay.set_alpha(0)  # Start fully transparent
        
        self.element_add(self.fade_overlay)
    
    def set_fade_alpha(self, alpha: int):
        """Set the fade overlay transparency (0-100)"""
        self.fade_overlay.set_alpha(alpha)
    
    def get_fade_alpha(self) -> int:
        """Get the current fade overlay transparency (0-100)"""
        return self.fade_overlay.get_alpha()

class layer_loading (Layers):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        
        from handler_gui_sizing import get_sizing
        sizing = get_sizing()
        
        # Create a dark background
        self.background = handler_gui_elements.element_box_color(
            (20, 20, 20),  # Very dark gray
            (0, 0),
            (sizing.cached_width, sizing.cached_height)
        )
        self.element_add(self.background)
        
        # Create loading text
        text_y = sizing.rel_height(40)  # 40% from top
        self.loading_text = handler_gui_elements.element_text_title(
            "Loading...",
            (sizing.center_x(200), text_y)  # Centered horizontally
        )
        self.element_add(self.loading_text)
        
        # Create progress bar
        bar_width = sizing.rel_width(30)   # 30% of screen width
        bar_height = sizing.rel_height(3)   # 3% of screen height
        bar_y = sizing.rel_height(50)       # 50% from top
        self.progress_bar = handler_gui_elements.element_bar_status(
            sizing.center_x(bar_width),     # Centered horizontally
            bar_y,
            bar_width,
            bar_height,
            max_value=100,
            color=(0, 255, 0),             # Green progress
            background_color=(60, 60, 60)   # Darker gray background
        )
        self.element_add(self.progress_bar)
    
    def update_progress(self, progress: float):
        """Update the loading progress (0-100)"""
        # Ensure progress is between 0 and 100
        progress = max(0, min(100, progress))
        # Update progress bar in next draw call
        self.progress = progress
    
    def draw(self, screen):
        """Override draw to handle progress bar separately"""
        # Draw background and text
        screen.blit(self.background.image, (self.background.x + self.x, self.background.y + self.y))
        self.loading_text.draw(screen)
        
        # Draw progress bar with current progress
        if hasattr(self, 'progress'):
            self.progress_bar.draw(screen, self.progress)