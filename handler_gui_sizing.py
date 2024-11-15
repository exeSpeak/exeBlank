import pygame

class GuiSizing:
    def __init__(self, window_handler):
        self.window_handler = window_handler
        
    def rel_width(self, percentage):
        """Convert percentage of window width to pixels"""
        window_width = self.window_handler.get_window_size()[0]
        return int(window_width * (percentage / 100))
        
    def rel_height(self, percentage):
        """Convert percentage of window height to pixels"""
        window_height = self.window_handler.get_window_size()[1]
        return int(window_height * (percentage / 100))
        
    def rel_pos_x(self, percentage):
        """Convert percentage of window width to x position"""
        window_width = self.window_handler.get_window_size()[0]
        return int(window_width * (percentage / 100))
        
    def rel_pos_y(self, percentage):
        """Convert percentage of window height to y position"""
        window_height = self.window_handler.get_window_size()[1]
        return int(window_height * (percentage / 100))
        
    def rel_size(self, width_percent, height_percent):
        """Convert percentage of window size to (width, height) tuple"""
        return (self.rel_width(width_percent), self.rel_height(height_percent))
        
    def rel_pos(self, x_percent, y_percent):
        """Convert percentage of window position to (x, y) tuple"""
        return (self.rel_pos_x(x_percent), self.rel_pos_y(y_percent))
        
    def center_x(self, width):
        """Get x position to center an element of given width"""
        window_width = self.window_handler.get_window_size()[0]
        return (window_width - width) // 2
        
    def center_y(self, height):
        """Get y position to center an element of given height"""
        window_height = self.window_handler.get_window_size()[1]
        return (window_height - height) // 2
        
    def center_pos(self, width, height):
        """Get (x,y) position to center an element of given size"""
        return (self.center_x(width), self.center_y(height))

# Create a global sizing handler instance that will be initialized in main.py
sizing_handler = None

def init_sizing(window_handler):
    """Initialize the global sizing handler"""
    global sizing_handler
    sizing_handler = GuiSizing(window_handler)
    
def get_sizing():
    """Get the global sizing handler"""
    return sizing_handler
