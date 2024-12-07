import pygame
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum, auto
import numpy as np

class AnimationState(Enum):
    IDLE = auto()
    WALK = auto()
    RUN = auto()
    JUMP = auto()
    FALL = auto()
    ATTACK = auto()
    HURT = auto()
    DIE = auto()

@dataclass
class AnimationData:
    frames: List[pygame.Surface]
    frame_duration: float
    loop: bool = True
    current_frame: int = 0
    timer: float = 0.0
    is_finished: bool = False

class SpriteAnimation:
    def __init__(self):
        self.animations: Dict[AnimationState, AnimationData] = {}
        self.current_state: AnimationState = AnimationState.IDLE
        self.flip_x: bool = False
        self.flip_y: bool = False
        
    def add_animation(self, 
                     state: AnimationState,
                     frames: List[pygame.Surface],
                     frame_duration: float,
                     loop: bool = True) -> None:
        """Add a new animation state with its frames"""
        self.animations[state] = AnimationData(
            frames=frames,
            frame_duration=frame_duration,
            loop=loop
        )
        
    def set_state(self, state: AnimationState) -> None:
        """Change the current animation state"""
        if state != self.current_state and state in self.animations:
            self.current_state = state
            self.animations[state].current_frame = 0
            self.animations[state].timer = 0.0
            self.animations[state].is_finished = False
            
    def update(self, delta_time: float) -> None:
        """Update the current animation"""
        if self.current_state not in self.animations:
            return
            
        anim = self.animations[self.current_state]
        if anim.is_finished and not anim.loop:
            return
            
        anim.timer += delta_time
        if anim.timer >= anim.frame_duration:
            anim.timer = 0
            anim.current_frame = (anim.current_frame + 1) % len(anim.frames)
            if not anim.loop and anim.current_frame == 0:
                anim.is_finished = True
                anim.current_frame = len(anim.frames) - 1
                
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get the current frame of the animation"""
        if self.current_state in self.animations:
            anim = self.animations[self.current_state]
            frame = anim.frames[anim.current_frame]
            if self.flip_x or self.flip_y:
                return pygame.transform.flip(frame, self.flip_x, self.flip_y)
            return frame
        return None
        
    def is_animation_finished(self) -> bool:
        """Check if the current animation has finished"""
        if self.current_state in self.animations:
            return self.animations[self.current_state].is_finished
        return True

class SpriteSheet:
    def __init__(self, sprite_sheet: pygame.Surface, sprite_width: int, sprite_height: int):
        self.sheet = sprite_sheet
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        
    def get_sprite(self, x: int, y: int) -> pygame.Surface:
        """Get a single sprite from the sheet at the specified grid position"""
        sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), 
                   (x * self.sprite_width, 
                    y * self.sprite_height, 
                    self.sprite_width, 
                    self.sprite_height))
        return sprite
        
    def get_row(self, row: int, num_frames: int) -> List[pygame.Surface]:
        """Get a row of sprites from the sheet"""
        return [self.get_sprite(x, row) for x in range(num_frames)]
        
    def get_animation_frames(self, start_pos: Tuple[int, int], 
                           num_frames: int, 
                           direction: str = 'horizontal') -> List[pygame.Surface]:
        """Get a sequence of animation frames starting from a position"""
        frames = []
        x, y = start_pos
        
        for i in range(num_frames):
            frames.append(self.get_sprite(x, y))
            if direction == 'horizontal':
                x += 1
            else:  # vertical
                y += 1
                
        return frames

class ColorEffect:
    @staticmethod
    def tint_surface(surface: pygame.Surface, 
                     color: Union[Tuple[int, int, int], pygame.Color],
                     intensity: float = 0.5) -> pygame.Surface:
        """
        Tint a surface with a color
        
        Args:
            surface: Surface to tint
            color: RGB color tuple or pygame.Color
            intensity: Tint intensity (0.0 to 1.0)
        """
        intensity = max(0.0, min(1.0, intensity))
        tinted = surface.copy()
        tinted.fill(color + (0,), special_flags=pygame.BLEND_RGBA_MULT)
        
        if intensity < 1.0:
            # Blend between original and tinted based on intensity
            original = surface.copy()
            tinted.set_alpha(int(255 * intensity))
            original.blit(tinted, (0, 0))
            return original
        return tinted
        
    @staticmethod
    def replace_color(surface: pygame.Surface,
                     old_color: Union[Tuple[int, int, int], pygame.Color],
                     new_color: Union[Tuple[int, int, int], pygame.Color],
                     threshold: int = 5) -> pygame.Surface:
        """
        Replace a specific color in the surface with another color
        
        Args:
            surface: Surface to modify
            old_color: Color to replace
            new_color: New color
            threshold: Color matching threshold (0-255)
        """
        modified = surface.copy()
        arr = pygame.surfarray.pixels3d(modified)
        
        # Convert colors to numpy arrays for efficient comparison
        old = np.array(old_color)
        new = np.array(new_color)
        
        # Find pixels within threshold of old_color
        mask = np.all(np.abs(arr - old) <= threshold, axis=2)
        
        # Replace matching pixels
        arr[mask] = new
        
        del arr  # Release surface lock
        return modified
        
    @staticmethod
    def adjust_brightness(surface: pygame.Surface, 
                         factor: float) -> pygame.Surface:
        """
        Adjust the brightness of a surface
        
        Args:
            surface: Surface to modify
            factor: Brightness factor (0.0 to 2.0, 1.0 is original)
        """
        factor = max(0.0, min(2.0, factor))
        modified = surface.copy()
        arr = pygame.surfarray.pixels3d(modified)
        
        # Adjust RGB values while preserving alpha
        arr = np.clip(arr * factor, 0, 255).astype(np.uint8)
        
        del arr
        return modified
        
    @staticmethod
    def colorize(surface: pygame.Surface,
                 hue: float,
                 saturation: float = 1.0,
                 value: float = 1.0) -> pygame.Surface:
        """
        Colorize a surface using HSV color space
        
        Args:
            surface: Surface to colorize
            hue: Hue value (0.0 to 1.0)
            saturation: Saturation value (0.0 to 1.0)
            value: Value/brightness (0.0 to 1.0)
        """
        modified = surface.copy()
        arr = pygame.surfarray.pixels3d(modified)
        
        # Convert to float for calculations
        arr_float = arr.astype(np.float32) / 255.0
        
        # Convert RGB to HSV
        max_val = np.max(arr_float, axis=2)
        min_val = np.min(arr_float, axis=2)
        diff = max_val - min_val
        
        # Calculate new HSV values
        new_hue = hue
        new_sat = np.where(max_val == 0, 0, diff / max_val) * saturation
        new_val = max_val * value
        
        # Convert back to RGB
        h_i = (new_hue * 6).astype(np.int32)
        f = (new_hue * 6) - h_i
        p = new_val * (1 - new_sat)
        q = new_val * (1 - f * new_sat)
        t = new_val * (1 - (1 - f) * new_sat)
        
        # Create RGB array based on hue sector
        rgb = np.zeros_like(arr_float)
        
        # Hue sector 0
        mask = h_i % 6 == 0
        rgb[mask] = np.dstack((new_val[mask], t[mask], p[mask]))
        
        # Hue sector 1
        mask = h_i % 6 == 1
        rgb[mask] = np.dstack((q[mask], new_val[mask], p[mask]))
        
        # Hue sector 2
        mask = h_i % 6 == 2
        rgb[mask] = np.dstack((p[mask], new_val[mask], t[mask]))
        
        # Hue sector 3
        mask = h_i % 6 == 3
        rgb[mask] = np.dstack((p[mask], q[mask], new_val[mask]))
        
        # Hue sector 4
        mask = h_i % 6 == 4
        rgb[mask] = np.dstack((t[mask], p[mask], new_val[mask]))
        
        # Hue sector 5
        mask = h_i % 6 == 5
        rgb[mask] = np.dstack((new_val[mask], p[mask], q[mask]))
        
        # Convert back to 0-255 range
        arr[:] = (rgb * 255).astype(np.uint8)
        
        del arr
        return modified

class SpriteHandler:
    def __init__(self):
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.sheet_cache: Dict[str, SpriteSheet] = {}
        
    def get_sprite(self, sprite_path: str) -> Optional[pygame.Surface]:
        """Get a single sprite from cache or load it"""
        if sprite_path in self.sprite_cache:
            return self.sprite_cache[sprite_path]
            
        try:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite_cache[sprite_path] = sprite
            return sprite
        except Exception as e:
            print(f"Error loading sprite {sprite_path}: {e}")
            return None
            
    def get_sprite_sheet(self, 
                        sheet_path: str, 
                        sprite_width: int, 
                        sprite_height: int) -> Optional[SpriteSheet]:
        """Get a sprite sheet from cache or create a new one"""
        cache_key = f"{sheet_path}_{sprite_width}_{sprite_height}"
        if cache_key in self.sheet_cache:
            return self.sheet_cache[cache_key]
            
        sprite_surface = self.get_sprite(sheet_path)
        if sprite_surface:
            sheet = SpriteSheet(sprite_surface, sprite_width, sprite_height)
            self.sheet_cache[cache_key] = sheet
            return sheet
        return None
        
    def create_animation(self,
                        sheet_path: str,
                        sprite_width: int,
                        sprite_height: int,
                        animations_data: Dict[AnimationState, Tuple[Tuple[int, int], int, float, bool]]
                        ) -> Optional[SpriteAnimation]:
        """
        Create a sprite animation from a sprite sheet
        
        Args:
            sheet_path: Path to the sprite sheet image
            sprite_width: Width of each sprite frame
            sprite_height: Height of each sprite frame
            animations_data: Dictionary mapping AnimationState to tuple of:
                           (start_position, num_frames, frame_duration, should_loop)
        """
        sheet = self.get_sprite_sheet(sheet_path, sprite_width, sprite_height)
        if not sheet:
            return None
            
        animation = SpriteAnimation()
        for state, (start_pos, num_frames, duration, loop) in animations_data.items():
            frames = sheet.get_animation_frames(start_pos, num_frames)
            animation.add_animation(state, frames, duration, loop)
            
        return animation
        
    def apply_color_effect(self,
                          sprite: pygame.Surface,
                          effect: str,
                          **kwargs) -> pygame.Surface:
        """
        Apply a color effect to a sprite
        
        Args:
            sprite: Sprite to modify
            effect: Effect type ('tint', 'replace_color', 'brightness', 'colorize')
            **kwargs: Effect-specific parameters
        """
        if effect == 'tint':
            return ColorEffect.tint_surface(
                sprite,
                kwargs.get('color', (255, 255, 255)),
                kwargs.get('intensity', 0.5)
            )
        elif effect == 'replace_color':
            return ColorEffect.replace_color(
                sprite,
                kwargs.get('old_color', (0, 0, 0)),
                kwargs.get('new_color', (255, 255, 255)),
                kwargs.get('threshold', 5)
            )
        elif effect == 'brightness':
            return ColorEffect.adjust_brightness(
                sprite,
                kwargs.get('factor', 1.0)
            )
        elif effect == 'colorize':
            return ColorEffect.colorize(
                sprite,
                kwargs.get('hue', 0.0),
                kwargs.get('saturation', 1.0),
                kwargs.get('value', 1.0)
            )
        return sprite

# Global sprite handler instance
sprite_handler = None

def get_sprite_handler() -> SpriteHandler:
    """Get the global sprite handler instance"""
    global sprite_handler
    if sprite_handler is None:
        sprite_handler = SpriteHandler()
    return sprite_handler
