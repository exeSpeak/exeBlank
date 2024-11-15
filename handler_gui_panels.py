import handler_gui_elements
import pygame
from pygame.locals import *

class Panels:
    def __init__(self, offset, margin="left"):
        self.elements = []
        self.window_width = 1600
        self.window_height = 900
        self.width = 1600
        self.height = 900
        self.offset = offset
        self.margin = margin
        self.x = self._calculate_x()
        self.y = self._calculate_y()
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((204, 204, 204))
        self.visible = True
        self.set_margin(margin)
        
    def _calculate_x(self):
        if self.margin == "right":
            return self.window_width - self.width
        return 0
        
    def _calculate_y(self):
        if self.margin == "bottom":
            return self.window_height - self.height
        return 0
    
    def set_margin(self, margin):
        """Update panel margin and recalculate position"""
        self.margin = margin
        # Calculate dimensions based on margin type
        if margin in ["left", "right"]:
            self.width = self.offset
            self.height = self.window_height
        else:  # top or bottom
            self.width = self.window_width
            self.height = self.offset
        
        self.x = self._calculate_x()
        self.y = self._calculate_y()
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((204, 204, 204))
        self._update_element_positions()
    
    def _update_element_positions(self):
        """Update all element positions when panel moves"""
        for element in self.elements:
            # Calculate relative position within panel
            rel_x = element.x - (element.default_x - self.x)
            rel_y = element.y - (element.default_y - self.y)
            # Update position
            element.update_position(self.x + rel_x, self.y + rel_y)
            # Update default position
            element.default_x = self.x + rel_x
            element.default_y = self.y + rel_y
    
    def element_add(self, element):
        """Add an element to the panel"""
        # Adjust element position relative to panel
        element.update_position(self.x + element.x, self.y + element.y)
        element.default_x = self.x + element.x
        element.default_y = self.y + element.y
        self.elements.append(element)
    
    def element_remove(self, element):
        """Remove an element from the panel"""
        if element in self.elements:
            self.elements.remove(element)
    
    def hide(self):
        """Hide the panel"""
        self.visible = False
        for element in self.elements:
            element.update_position(element.x + 3000, element.y)
    
    def show(self):
        """Show the panel"""
        self.visible = True
        for element in self.elements:
            element.update_position(element.default_x, element.default_y)
    
    def draw(self, screen):
        """Draw the panel and its elements"""
        if not self.visible:
            return
            
        # Draw panel background
        screen.blit(self.background, (self.x, self.y))
        
        # Draw elements
        for element in self.elements:
            screen.blit(element.image, (element.x, element.y))
    
    def resize(self, width, height):
        """Resize the panel"""
        self.width = width
        self.height = height
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((204, 204, 204))
        # Recalculate position based on margin
        self.x = self._calculate_x()
        self.y = self._calculate_y()
        self._update_element_positions()

# PANEL OBJECTS
class panel_sidebar_left(Panel):
    def __init__(self):
        super().__init__(200, "left")  # 200px wide, full height, left margin
        
class panel_toolbar_top(Panel):
    def __init__(self):
        super().__init__(50, "top")  # Full width, 50px height, top margin
        
class panel_status_bottom(Panel):
    def __init__(self):
        super().__init__(30, "bottom")  # Full width, 30px height, bottom margin
