import pygame
from pygame.locals import *

class MouseHandler:
    def __init__(self):
        """Initialize the mouse handler"""
        self.position = (0, 0)
        self.button_states = {
            1: False,  # Left button
            2: False,  # Middle button
            3: False,  # Right button
            4: False,  # Scroll up
            5: False   # Scroll down
        }
        self.click_handlers = {}
        self.drag_start = None
        self.is_dragging = False
        
    def handle_event(self, event):
        """Process a mouse event"""
        if event.type == MOUSEMOTION:
            self.position = event.pos
            if self.is_dragging:
                self._handle_drag(event.pos)
                
        elif event.type == MOUSEBUTTONDOWN:
            self.button_states[event.button] = True
            if event.button in [1, 2, 3]:  # Regular mouse buttons
                self.drag_start = event.pos
                self._handle_click(event.button, event.pos)
                
        elif event.type == MOUSEBUTTONUP:
            self.button_states[event.button] = False
            if event.button in [1, 2, 3]:  # Regular mouse buttons
                if self.is_dragging:
                    self._handle_drop(event.pos)
                self.is_dragging = False
                self.drag_start = None
                
        elif event.type == MOUSEWHEEL:
            self._handle_scroll(event.y)
    
    def _handle_click(self, button, pos):
        """Handle mouse button click"""
        action = self.click_handlers.get(button)
        if action:
            # Here you would typically call handler_game.processButtonClick(action)
            print(f"Mouse button {button} clicked at {pos}")
    
    def _handle_drag(self, pos):
        """Handle mouse drag"""
        if not self.is_dragging and self.drag_start:
            # Check if we've moved enough to start dragging
            dx = pos[0] - self.drag_start[0]
            dy = pos[1] - self.drag_start[1]
            if abs(dx) > 5 or abs(dy) > 5:  # 5 pixel threshold
                self.is_dragging = True
    
    def _handle_drop(self, pos):
        """Handle mouse drop after drag"""
        print(f"Dropped at {pos}")
    
    def _handle_scroll(self, y):
        """Handle mouse wheel scroll"""
        if y > 0:
            self.button_states[4] = True  # Scroll up
            self.button_states[4] = False
        else:
            self.button_states[5] = True  # Scroll down
            self.button_states[5] = False
    
    def get_position(self):
        """Get current mouse position"""
        return self.position
    
    def is_button_pressed(self, button):
        """Check if a specific button is currently pressed"""
        return self.button_states.get(button, False)
    
    def add_click_handler(self, button, action):
        """Add a new click handler"""
        self.click_handlers[button] = action
    
    def remove_click_handler(self, button):
        """Remove a click handler"""
        if button in self.click_handlers:
            del self.click_handlers[button]
