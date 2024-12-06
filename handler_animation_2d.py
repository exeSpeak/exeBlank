import pygame
import math
from enum import Enum, auto
from typing import Tuple, Optional, Dict, Callable
from handler_gui_sizing import get_sizing

class EaseType(Enum):
    LINEAR = auto()
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_IN_OUT = auto()
    BOUNCE = auto()
    ELASTIC = auto()

class Animation:
    def __init__(self, 
                 sprite: pygame.sprite.Sprite,
                 start_pos: Tuple[float, float],
                 end_pos: Tuple[float, float],
                 duration: float,
                 ease_type: EaseType = EaseType.LINEAR):
        self.sprite = sprite
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.ease_type = ease_type
        self.elapsed_time = 0
        self.is_complete = False

class AnimationManager:
    def __init__(self):
        self.animations: Dict[int, Animation] = {}
        self.next_animation_id = 0
        
    def create_animation(self,
                        sprite: pygame.sprite.Sprite,
                        end_pos_percent: Tuple[float, float],
                        duration: float,
                        ease_type: EaseType = EaseType.LINEAR) -> int:
        """Creates a new animation for a sprite to move to a relative screen position"""
        sizing = get_sizing()
        start_pos = sprite.rect.topleft
        end_pos = sizing.rel_pos(end_pos_percent[0], end_pos_percent[1])
        
        animation = Animation(sprite, start_pos, end_pos, duration, ease_type)
        animation_id = self.next_animation_id
        self.animations[animation_id] = animation
        self.next_animation_id += 1
        return animation_id

    def update(self, delta_time: float) -> None:
        """Updates all active animations"""
        completed_animations = []
        
        for animation_id, animation in self.animations.items():
            if animation.is_complete:
                completed_animations.append(animation_id)
                continue
                
            animation.elapsed_time += delta_time
            progress = min(animation.elapsed_time / animation.duration, 1.0)
            
            # Apply easing function
            eased_progress = self._apply_easing(progress, animation.ease_type)
            
            # Calculate new position
            new_x = animation.start_pos[0] + (animation.end_pos[0] - animation.start_pos[0]) * eased_progress
            new_y = animation.start_pos[1] + (animation.end_pos[1] - animation.start_pos[1]) * eased_progress
            
            # Update sprite position
            animation.sprite.rect.topleft = (new_x, new_y)
            
            if progress >= 1.0:
                animation.is_complete = True
                
        # Remove completed animations
        for animation_id in completed_animations:
            del self.animations[animation_id]

    def _apply_easing(self, t: float, ease_type: EaseType) -> float:
        """Applies easing function to the progress value"""
        if ease_type == EaseType.LINEAR:
            return t
        elif ease_type == EaseType.EASE_IN:
            return t * t
        elif ease_type == EaseType.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif ease_type == EaseType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - pow(-2 * t + 2, 2) / 2
        elif ease_type == EaseType.BOUNCE:
            if t < 1 / 2.75:
                return 7.5625 * t * t
            elif t < 2 / 2.75:
                t -= 1.5 / 2.75
                return 7.5625 * t * t + 0.75
            elif t < 2.5 / 2.75:
                t -= 2.25 / 2.75
                return 7.5625 * t * t + 0.9375
            else:
                t -= 2.625 / 2.75
                return 7.5625 * t * t + 0.984375
        elif ease_type == EaseType.ELASTIC:
            if t == 0 or t == 1:
                return t
            t = t * 2
            if t < 1:
                return -0.5 * pow(2, 10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)
            return 0.5 * pow(2, -10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi) + 1

    def cancel_animation(self, animation_id: int) -> bool:
        """Cancels an animation by its ID"""
        if animation_id in self.animations:
            del self.animations[animation_id]
            return True
        return False

    def is_animating(self, animation_id: int) -> bool:
        """Checks if an animation is still running"""
        return animation_id in self.animations

# Global animation manager instance
animation_manager = None

def get_animation_manager() -> AnimationManager:
    """Get the global animation manager instance"""
    global animation_manager
    if animation_manager is None:
        animation_manager = AnimationManager()
    return animation_manager