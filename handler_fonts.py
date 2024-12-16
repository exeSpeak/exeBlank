import os
import pygame

class FontHandler:
    # CHANGE THESE AS NECESSARY AND THE CODE WILL AUTOMATICALLY LOAD
    font_file_locations = [
        'default/verdana.ttf',
        'default/verdana_bold.ttf', 
        'default/verdana_italic.ttf',
        'default/verdana_bold_italic.ttf'
        ]

    def __init__(self):
        self.fonts = {}
        self.default_font = None
        self._load_default_fonts()
    
    def _load_default_fonts(self):
        """Load all fonts from font_file_locations"""
        script_dir = os.path.dirname(__file__)
        
        # Load all fonts from font_file_locations
        for idx, font_path in enumerate(self.font_file_locations):
            full_path = os.path.join(script_dir, font_path)
            try:
                # Load each font with a numeric identifier
                self.add_font(f'font_{idx}', full_path, sizes=[12, 14, 16, 18, 20, 24, 32, 48])
                
                # First font is also set as default
                if idx == 0:
                    self.add_font('default', full_path, sizes=[12, 14, 16, 18, 20, 24, 32, 48])
                    self.default_font = self.get_font('default', 16)
            except FileNotFoundError:
                print(f"Warning: Font not found at {full_path}")
                if idx == 0:
                    self.default_font = pygame.font.Font(None, 16)  # Fallback to system font
    
    def add_font(self, name, font_path, sizes=None):
        """
        Add a font with multiple sizes to the font collection
        :param name: Name identifier for the font
        :param font_path: Path to the font file
        :param sizes: List of font sizes to pre-load
        """
        if sizes is None:
            sizes = [16]  # Default size if none specified
        
        self.fonts[name] = {
            'path': font_path,
            'sizes': {}
        }
        
        for size in sizes:
            try:
                self.fonts[name]['sizes'][size] = pygame.font.Font(font_path, size)
            except pygame.error as e:
                print(f"Error loading font {name} at size {size}: {e}")
    
    def get_font(self, name='default', size=16):
        """
        Get a font at the specified size
        :param name: Font name
        :param size: Font size
        :return: pygame.font.Font object
        """
        # If font doesn't exist, return default font
        if name not in self.fonts:
            return self.default_font
        
        # If size doesn't exist for this font, create it
        if size not in self.fonts[name]['sizes']:
            try:
                self.fonts[name]['sizes'][size] = pygame.font.Font(self.fonts[name]['path'], size)
            except pygame.error:
                return self.default_font
        
        return self.fonts[name]['sizes'][size]
    
    def render_text(self, text, font_name='default', size=16, color=(0, 0, 0), antialias=True):
        """
        Render text with the specified font
        :param text: Text to render
        :param font_name: Name of the font to use
        :param size: Size of the font
        :param color: Color of the text (RGB tuple)
        :param antialias: Whether to use antialiasing
        :return: Surface with rendered text
        """
        font = self.get_font(font_name, size)
        return font.render(text, antialias, color)

# Create a global font handler instance
font_handler = FontHandler()

def get_font(font_id='default', size=16):
    """
    Get a font by name or index
    Args:
        font_id: Either 'default' or index (0-2) corresponding to font_file_locations
        size: Font size in points
    """
    if isinstance(font_id, int):
        # Use index to get font
        if 0 <= font_id < len(FontHandler.font_file_locations):
            return font_handler.get_font(f'font_{font_id}', size)
    return font_handler.get_font(font_id, size)

def render_text(text, font_id='default', size=16, color=(0, 0, 0), antialias=True):
    """
    Render text with specified font
    Args:
        text: Text to render
        font_id: Either 'default' or index (0-2) corresponding to font_file_locations
        size: Font size in points
        color: Text color (RGB tuple)
        antialias: Whether to use antialiasing
    """
    if isinstance(font_id, int):
        # Use index to get font
        if 0 <= font_id < len(FontHandler.font_file_locations):
            return font_handler.render_text(text, f'font_{font_id}', size, color, antialias)
    return font_handler.render_text(text, font_id, size, color, antialias)