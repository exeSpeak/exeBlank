import handler_gui_elements
import pygame
from pygame.locals import *
from handler_gui_sizing import get_sizing

class Popups:
    def __init__ (self, width_percent=50, height_percent=50):
        self.elements = []
        
        # Get window dimensions from sizing handler
        sizing = get_sizing()
        self.window_width = sizing.cached_width
        self.window_height = sizing.cached_height
        
        # Calculate popup dimensions as percentage of window
        self.width = sizing.rel_width(width_percent)
        self.height = sizing.rel_height(height_percent)
        
        # Calculate position to center the popup
        self.x = (self.window_width - self.width) // 2
        self.y = (self.window_height - self.height) // 2
        
        # Create background surface
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))  # Light gray background
        
        # Add semi-transparent overlay for the rest of the screen
        self.overlay = pygame.Surface((self.window_width, self.window_height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)  # 50% transparency
    
    def element_add (self, element):
        # Adjust element position relative to popup's position
        element.update_position(
            element.x + self.x,
            element.y + self.y
        )
        self.elements.append(element)
    
    def element_remove (self, element):
        self.elements.remove(element)
    
    def hide (self):
        for element in self.elements:
            element.update_position(element.x + 3000, element.y)
    
    def show (self):
        for element in self.elements:
            element.update_position(element.default_x, element.default_y)
    
    def update_position (self, input_newX, input_newY):
        self.x = input_newX
        self.y = input_newY

    def draw (self, screen):
        # Draw darkened overlay
        screen.blit(self.overlay, (0, 0))
        
        # Draw popup background
        screen.blit(self.background, (self.x, self.y))
        
        # Draw elements
        for element in self.elements:
            screen.blit(element.image, (element.x, element.y))

class popup_alert (Popups):
    # NOTE: THE ALERT POPUP AUTOMATICALLY SHOWS ITSELF WHEN IT GETS SENT A MESSAGE
    def __init__(self, title, message):
        super().__init__ (width_percent=40, height_percent=30)
        self.background.fill((0,0,0))
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        self.element_add(handler_gui_elements.element_box_text(
            message,
            (self.x + 10, self.y + 10),
            (self.width - 20, self.height - 20)
        ))
        self.element_add (handler_gui_elements.element_button_text(
            "OKAY",
            (self.x + 10, self.y + self.height - 40),
            (self.width - 20, 30)
        ))
        def updateMessage (input_message):
            message.text = input_message
            self.show()
            self.draw(screen)
            pygame.display.flip()

class popup_gameover (Popups):
    # NOTE: NOTIFY THE USER THAT THE GAME IS OVER
    def __init__(self, title, reason):
        super().__init__ (width_percent=40, height_percent=30)
        self.background.fill((0,0,0))
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        self.element_add(handler_gui_elements.element_box_text(
            "Game Over",
            (self.x + 10, self.y + 10),
            (self.width - 20, self.height - 20)
        ))
        self.element_add(handler_gui_elements.element_box_text(
            reason,
            (self.x + 10, self.y + 40),
            (self.width - 35, self.height - 60)
        ))
        self.element_add (handler_gui_elements.element_button_text(
            "OKAY",
            (self.x + 10, self.y + self.height - 40),
            (self.width - 20, 30)
        ))

class popup_prompt (Popups):
    # NOTE: ASK THE USER A QUESTION AND THEN RECEIVE A "YES" OR "NO" RESPONSE
    def __init__(self, title, inquiry):
        super().__init__ (width_percent=40, height_percent=30)
        self.background.fill((0,0,0))
        self.image = pygame.image.load("default/tg.png").convert_alpha()  # Specify the correct path        
        self.element_add(handler_gui_elements.element_box_text(
            inquiry,
            (self.x + 10, self.y + 10),
            (self.width - 35, self.height - 20)
        ))
        self.element_add (handler_gui_elements.element_button_text(
            "YES",
            (self.x + 10, self.y + self.height - 40),
            (self.width - 20, 30)
        ))
        self.element_add (handler_gui_elements.element_button_text(
            "NO",
            (self.x + 60, self.y + self.height - 40),
            (self.width - 20, 30)
        ))
