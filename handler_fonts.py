import os
from pygame import font
font.init()

class FontHandler:
    # HARDCODED BELOW; THIS IS FOR REFERENCE
    # font_file_locations = [
    #    'trajan_regular.ttf',
    #    'verdana.ttf',
    #    'verdana_bold.ttf', 
    #    'verdana_italic.ttf',
    #    'verdana_bold_italic.ttf'
    #    ]

    def __init__(self):
        self.fonts_loaded = {}
        self.font_directory = "fonts"
        self.__load_all_fonts()
    
    def __load_all_fonts(self):
        self.fonts_loaded['default'] = font.Font("fonts/trajan_regular.ttf", 16)
        self.fonts_loaded['trajan24'] = font.Font("fonts/trajan_regular.ttf", 24)
        self.fonts_loaded['trajan32'] = font.Font("fonts/trajan_regular.ttf", 32)
        self.fonts_loaded['trajan48'] = font.Font("fonts/trajan_regular.ttf", 48)
        self.fonts_loaded['verdana16'] = font.Font("fonts/verdana.ttf", 16)
        self.fonts_loaded['verdanaBold16'] = font.Font("fonts/verdana_bold.ttf", 16)
        self.fonts_loaded['verdanaItalic16'] = font.Font("fonts/verdana_italic.ttf", 16)
        self.fonts_loaded['verdanaBoldItalic16'] = font.Font("fonts/verdana_bold_italic.ttf", 16)
    
    def get_font(self, name='default'):
        if name not in self.fonts_loaded:
            raise ValueError(f"Font '{name}' not found.")
        return self.fonts_loaded[name]
    
    def render_text(self, text, font_name='default', size=16, color=(0, 0, 0), antialias=True):
        temp_font = self.get_font(font_name)
        return temp_font.render(text, antialias, color)
    
# Create a global font handler instance
font_handler = FontHandler()

def get_font(font_id='default'):
    return font_handler.get_font(font_id)

def render_text(text, font_id='default', color=(0, 0, 0), antialias=True):
    return font_handler.render_text(text, font_id, color, antialias)
