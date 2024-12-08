import pygame

class GuiSizing:
    def __init__(self, window_handler):
        self.window_handler = window_handler
        # Initialize cached values
        self.cached_width = 0
        self.cached_height = 0
        # Common percentage-based sizes
        self.rel_sizes = {}
        # Update all cached values
        self.update_cache()
    
    def update_cache(self):
        """Update all cached values when window size changes"""
        # Get current window size
        self.cached_width, self.cached_height = self.window_handler.get_window_size()
        
        # Pre-calculate common percentage-based sizes
        # Widths (5% to 100% in steps of 5)
        for i in range(5, 101, 5):
            self.rel_sizes[f'w{i}'] = int(self.cached_width * (i / 100))
            self.rel_sizes[f'h{i}'] = int(self.cached_height * (i / 100))
        
        # Common specific values
        self.rel_sizes['sidebar'] = int(self.cached_width * 0.2)  # 20% width for sidebars
        self.rel_sizes['toolbar'] = int(self.cached_height * 0.05)  # 5% height for toolbar
        self.rel_sizes['statusbar'] = int(self.cached_height * 0.03)  # 3% height for status bar
        self.rel_sizes['button'] = (
            int(self.cached_width * 0.125),  # 12.5% width
            int(self.cached_height * 0.055)   # 5.5% height
        )
        self.rel_sizes['popup'] = (
            int(self.cached_width * 0.4),  # 40% width
            int(self.cached_height * 0.3)  # 30% height
        )
    
    def check_cache(self):
        """Check if window size has changed and update cache if needed"""
        current_size = self.window_handler.get_window_size()
        if (current_size[0] != self.cached_width or 
            current_size[1] != self.cached_height):
            self.update_cache()
    
    def rel_width(self, percentage):
        """Get pre-calculated width or calculate new one"""
        self.check_cache()
        key = f'w{int(percentage)}'
        if key in self.rel_sizes:
            return self.rel_sizes[key]
        return int(self.cached_width * (percentage / 100))
    
    def rel_height(self, percentage):
        """Get pre-calculated height or calculate new one"""
        self.check_cache()
        key = f'h{int(percentage)}'
        if key in self.rel_sizes:
            return self.rel_sizes[key]
        return int(self.cached_height * (percentage / 100))
    
    def rel_pos_x(self, percentage):
        """Get x position based on percentage"""
        self.check_cache()
        return int(self.cached_width * (percentage / 100))
    
    def rel_pos_y(self, percentage):
        """Get y position based on percentage"""
        self.check_cache()
        return int(self.cached_height * (percentage / 100))
    
    def rel_size(self, width_percent, height_percent):
        """Get size tuple based on percentages"""
        return (self.rel_width(width_percent), self.rel_height(height_percent))
    
    def rel_pos(self, x_percent, y_percent):
        """Get position tuple based on percentages"""
        return (self.rel_pos_x(x_percent), self.rel_pos_y(y_percent))
    
    def center_x(self, width):
        """Get centered x position"""
        self.check_cache()
        return (self.cached_width - width) // 2
    
    def center_y(self, height):
        """Get centered y position"""
        self.check_cache()
        return (self.cached_height - height) // 2
    
    def center_pos(self, width, height):
        """Get centered position tuple"""
        return (self.center_x(width), self.center_y(height))
    
    # Common pre-calculated sizes
    def get_sidebar_width(self):
        """Get standard sidebar width (20% of window)"""
        self.check_cache()
        return self.rel_sizes['sidebar']
    
    def get_toolbar_height(self):
        """Get standard toolbar height (5% of window)"""
        self.check_cache()
        return self.rel_sizes['toolbar']
    
    def get_statusbar_height(self):
        """Get standard status bar height (3% of window)"""
        self.check_cache()
        return self.rel_sizes['statusbar']
    
    def get_button_size(self):
        """Get standard button size (12.5% width, 5.5% height)"""
        self.check_cache()
        return self.rel_sizes['button']
    
    def get_popup_size(self):
        """Get standard popup size (40% width, 30% height)"""
        self.check_cache()
        return self.rel_sizes['popup']

# Create a global sizing handler instance that will be initialized in main.py
sizing_handler = None

def init_sizing(window_handler):
    """Initialize the global sizing handler"""
    global sizing_handler
    sizing_handler = GuiSizing(window_handler)
    
def get_sizing():
    """Get the global sizing handler"""
    return sizing_handler
