import pygame
import handler_game

class KeyboardHandler:
    def __init__(self):
        # Dictionary mapping keys to button actions
        self.key_mappings = {
            pygame.K_n: "New Game",  # N key for New Game
            pygame.K_ESCAPE: "Exit",  # ESC key for Exit
            # Add more key mappings here as needed
        }
        
        # For handling key states (useful for held keys)
        self.pressed_keys = set()
    
    def handle_event(self, event):
        """Process keyboard events and trigger corresponding actions"""
        if event.type == pygame.KEYDOWN:
            # Add key to pressed keys set
            self.pressed_keys.add(event.key)
            
            # Check if the pressed key is mapped to an action
            if event.key in self.key_mappings:
                handler_game.processButtonClick(self.key_mappings[event.key])
        
        elif event.type == pygame.KEYUP:
            # Remove key from pressed keys set
            self.pressed_keys.discard(event.key)
    
    def is_key_pressed(self, key):
        """Check if a specific key is currently pressed"""
        return key in self.pressed_keys
    
    # THESE THREE DEFINITIONS ARE FOR RE-MAPPING KEYBINDINGS
    def add_key_mapping(self, key, action):
        """Add or update a key mapping"""
        self.key_mappings[key] = action
    
    def remove_key_mapping(self, key):
        """Remove a key mapping"""
        if key in self.key_mappings:
            del self.key_mappings[key]
    
    def get_key_mappings(self):
        """Get all current key mappings"""
        return self.key_mappings.copy()

