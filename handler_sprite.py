import pygame

class SpriteHandler:
    def __init__(self):
        self.sprite_cache = {}  # Cache to store loaded sprites
        
    def get_sprite(self, sprite_name: str) -> pygame.Surface:
        """
        Get a sprite based on the provided sprite name
        Args:
            sprite_name (str): Path or name of the sprite to load
        Returns:
            pygame.Surface: The loaded sprite surface
        """
        # Check if sprite is already in cache
        if sprite_name in self.sprite_cache:
            return self.sprite_cache[sprite_name]
            
        try:
            # Load the sprite
            sprite = pygame.image.load(sprite_name).convert_alpha()
            # Store in cache for future use
            self.sprite_cache[sprite_name] = sprite
            return sprite
        except Exception as e:
            print(f"Error loading sprite {sprite_name}: {e}")
            # Return a default/placeholder sprite or None
            return None

