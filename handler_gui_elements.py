import handler_fonts
import pygame
import os

class UIElement:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = image.get_rect(topleft=(x, y))
        self.home_x = x
        self.home_y = y
        self.default_x = x
        self.default_y = y        
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (new_x, new_y)

class element_button_text (UIElement):
    def __init__(self, text, position, size):
        self.text = text
        self.size = size
        self.position = position
        self.active = True
        self.active_color = (255, 255, 255)  # White
        self.inactive_color = (102, 102, 102)  # #666666
        self.active_text_color = (0, 0, 0)  # Black
        self.inactive_text_color = (204, 204, 204)  # #cccccc
        self.image = pygame.Surface(size)
        
        script_dir = os.path.dirname(__file__)
        font_path = os.path.join(script_dir, 'defaults/default_font_nunito.ttf')
        self.font = handler_fonts.FontHandler().get_font('default', 16)
        
        self.render()
        super().__init__(self.image, position[0], position[1])

    def render(self):
        if self.active:
            self.image.fill(self.active_color)
            text_color = self.active_text_color
        else:
            self.image.fill(self.inactive_color)
            text_color = self.inactive_text_color
        
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.size[0], self.size[1]), 2)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.image.blit(text_surface, text_rect)

    def update_position(self, new_x, new_y):
        super().update_position(new_x, new_y)
        self.render()

    def set_text(self, new_text):
        self.text = new_text
        self.render()

    def set_active(self, is_active):
        if self.active != is_active:
            self.active = is_active
            self.render()

    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

class element_button_image (UIElement):
    def __init__(self, image_path, position, size):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, image_path)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)
        self.hover_image = self.create_hover_image(self.original_image)
        self.image = self.original_image
        super().__init__(self.image, position[0], position[1])
        self.is_hovered = False

    def create_hover_image(self, original):
        hover = original.copy()
        hover.fill((204, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return hover

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.is_hovered = True
                self.image = self.hover_image
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.image = self.original_image

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class element_bar_status (UIElement):
    def __init__(self, x, y, width, height, max_value=100, color=(0, 255, 0), background_color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.color = color
        self.background_color = background_color

    def draw(self, surface, current_value):
        current_value = max(0, min(current_value, self.max_value))
        fill_width = int(self.rect.width * (current_value / self.max_value))
        pygame.draw.rect(surface, self.background_color, self.rect)
        fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.color, fill_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def update_position(self, x, y):
        self.rect.topleft = (x, y)

class element_image (UIElement):
    def __init__(self, image_path, position, size):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, image_path)
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, size)  # Scale the image to the desired size
        self.rect = self.image.get_rect(topleft=position)
        super().__init__(self.image, position[0], position[1])

class element_text_title (UIElement):
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.color = (255, 255, 0)  # Yellow color
        self.font_size = 24

        script_dir = os.path.dirname(__file__)
        font_path = os.path.join(script_dir, 'defaults/default_font_nunito.ttf')
        self.font = handler_fonts.FontHandler().get_font('default', self.font_size)

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.position)

class element_box_color (UIElement):
    def __init__(self, color, position, size):
        self.color = color
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(color)
        super().__init__(self.image, position[0], position[1])

class element_box_text (UIElement):
    def __init__(self, text, position, size, font_size=24, text_color=(0, 0, 0), bg_color=(255, 255, 255)):
        self.text = text
        self.size = size
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.image = pygame.Surface(size)
        self.image.fill(bg_color)

        self.font = handler_fonts.FontHandler().get_font('default', self.font_size)

        self.render()
        super().__init__(self.image, position[0], position[1])

    def render(self):
        self.image.fill(self.bg_color)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.image.blit(text_surface, text_rect)

    def set_text(self, new_text):
        self.text = new_text
        self.render()

class element_slider (UIElement):
    def __init__(self, x, y, width, height, min_value, max_value, value):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = value

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        fill_width = int(self.rect.width * (self.value - self.min_value) / (self.max_value - self.min_value))
        fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)

        thumb_width = 20
        thumb_height = 20
        thumb_x = self.rect.left + fill_width - thumb_width // 2
        thumb_y = self.rect.top - thumb_height // 2
        pygame.draw.rect(surface, (0, 0, 0), (thumb_x, thumb_y, thumb_width, thumb_height))
        pygame.draw.circle(surface, (0, 255, 0), (thumb_x + thumb_width // 2, thumb_y + thumb_height // 2), thumb_width // 2)

        text_surface = pygame.font.Font(None, 20).render(str(self.value), True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.left + self.rect.width // 2 - text_surface.get_width() // 2, self.rect.top - text_surface.get_height() // 2))

    def update_position(self, x, y):
        self.rect.topleft = (x, y)

    def update_value(self, value):
        self.value = value

        fill_width = int(self.rect.width * (self.value - self.min_value) / (self.max_value - self.min_value))
        fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
        pygame.draw.rect(self.image, (0, 255, 0), fill_rect)

        thumb_width = 20
        thumb_height = 20
        thumb_x = self.rect.left + fill_width - thumb_width // 2
        thumb_y = self.rect.top - thumb_height // 2
        pygame.draw.rect(self.image, (0, 0, 0), (thumb_x, thumb_y, thumb_width, thumb_height))
        pygame.draw.circle(self.image, (0, 255, 0), (thumb_x + thumb_width // 2, thumb_y + thumb_height // 2), thumb_width // 2)

        text_surface = handler_fonts.FontHandler().get_font('default', 20).render(str(self.value), True, (0, 0, 0))
        self.image.blit(text_surface, (self.rect.left + self.rect.width // 2 - text_surface.get_width() // 2, self.rect.top - text_surface.get_height() // 2))

        self.rect.topleft = (x, y)

        return self.image

    def get_value(self):
        return self.value

class element_viewport (UIElement):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.scroll_x = 0
        self.scroll_y = 0

    def update_position(self, x, y):
        self.rect.topleft = (x, y)

    def update_scroll(self, scroll_x, scroll_y):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y

    def get_scroll(self):
        return self.scroll_x, self.scroll_y

    def get_rect(self):
        return self.rect

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        fill_rect = pygame.Rect(self.rect.left + self.scroll_x, self.rect.top + self.scroll_y, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)

        thumb_width = 20
        thumb_height = 20
        thumb_x = self.rect.left + self.scroll_x - thumb_width // 2
        thumb_y = self.rect.top + self.scroll_y - thumb_height // 2
        pygame.draw.rect(surface, (0, 0, 0), (thumb_x, thumb_y, thumb_width, thumb_height))
        pygame.draw.circle(surface, (0, 255, 0), (thumb_x + thumb_width // 2, thumb_y + thumb_height // 2), thumb_width // 2)

        text_surface = handler_fonts.FontHandler().get_font('default', 20).render(str(self.scroll_x), True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.left + self.rect.width // 2 - text_surface.get_width() // 2, self.rect.top - text_surface.get_height() // 2))

        self.rect.topleft = (x, y)

        return self.image

class element_input_field (UIElement):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.max_length = 20

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surface = handler_fonts.FontHandler().get_font('default', 20).render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.left + 5, self.rect.top + 5))

        self.rect.topleft = (x, y)

        return self.image

class element_toggle (UIElement):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

        self.rect.topleft = (x, y)

        return self.image

class element_menu_bar(UIElement):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.menu_items = {}  # Dictionary to store menu items and their submenus
        self.active_menu = None
        self.font = handler_fonts.FontHandler().get_font('default', 16)
        self.colors = {
            'background': (240, 240, 240),
            'text': (0, 0, 0),
            'hover': (200, 200, 200),
            'active': (180, 180, 180)
        }
        self.item_padding = 10
        self.item_height = 30
        
    def add_menu(self, name, items):
        """Add a menu with its items. Items should be a list of (name, callback) tuples."""
        x = sum(self.font.size(item)[0] + self.item_padding * 2 for item in self.menu_items)
        menu_width = self.font.size(name)[0] + self.item_padding * 2
        menu_rect = pygame.Rect(x, 0, menu_width, self.item_height)
        
        # Calculate dropdown dimensions
        max_item_width = max(self.font.size(item[0])[0] for item in items)
        dropdown_width = max_item_width + self.item_padding * 2
        dropdown_height = len(items) * self.item_height
        
        self.menu_items[name] = {
            'rect': menu_rect,
            'items': items,
            'dropdown_rect': pygame.Rect(x, self.item_height, dropdown_width, dropdown_height)
        }
    
    def draw(self, surface):
        # Draw menu bar background
        pygame.draw.rect(surface, self.colors['background'], self.rect)
        
        # Draw menu items
        x = self.rect.x
        for name, menu in self.menu_items.items():
            item_rect = menu['rect'].copy()
            item_rect.x += x
            
            # Draw menu item background
            if name == self.active_menu:
                color = self.colors['active']
            else:
                color = self.colors['background']
            pygame.draw.rect(surface, color, item_rect)
            
            # Draw menu text
            text = self.font.render(name, True, self.colors['text'])
            text_rect = text.get_rect(center=item_rect.center)
            surface.blit(text, text_rect)
            
            # Draw dropdown if active
            if name == self.active_menu:
                dropdown_rect = menu['dropdown_rect'].copy()
                dropdown_rect.x += x
                pygame.draw.rect(surface, self.colors['background'], dropdown_rect)
                
                # Draw dropdown items
                for i, (item_name, _) in enumerate(menu['items']):
                    item_rect = pygame.Rect(
                        dropdown_rect.x,
                        dropdown_rect.y + i * self.item_height,
                        dropdown_rect.width,
                        self.item_height
                    )
                    text = self.font.render(item_name, True, self.colors['text'])
                    text_rect = text.get_rect(midleft=(item_rect.x + self.item_padding, item_rect.centery))
                    surface.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check main menu items
            for name, menu in self.menu_items.items():
                item_rect = menu['rect']
                if item_rect.collidepoint(mouse_pos):
                    self.active_menu = name if self.active_menu != name else None
                    return True
                    
            # Check dropdown items if a menu is active
            if self.active_menu:
                menu = self.menu_items[self.active_menu]
                dropdown_rect = menu['dropdown_rect']
                if dropdown_rect.collidepoint(mouse_pos):
                    item_index = (mouse_pos[1] - dropdown_rect.y) // self.item_height
                    if 0 <= item_index < len(menu['items']):
                        _, callback = menu['items'][item_index]
                        if callback:
                            callback()
                        self.active_menu = None
                        return True
                        
            # Close dropdown if clicked outside
            self.active_menu = None
        return False

    def update_position(self, x, y):
        self.rect.topleft = (x, y)
        # Update positions of menu items
        current_x = x
        for menu in self.menu_items.values():
            menu['rect'].x = current_x
            menu['dropdown_rect'].x = current_x
            current_x += menu['rect'].width
