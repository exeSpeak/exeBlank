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

class RotationType(Enum):
    CLOCKWISE = auto()
    COUNTERCLOCKWISE = auto()
    SHORTEST_PATH = auto()

class Animation:
    def __init__(self, 
                 sprite: pygame.sprite.Sprite,
                 start_pos: Tuple[float, float],
                 end_pos: Tuple[float, float],
                 duration: float,
                 ease_type: EaseType = EaseType.LINEAR,
                 start_angle: float = 0,
                 end_angle: float = 0,
                 rotation_type: RotationType = RotationType.SHORTEST_PATH,
                 rotation_center: Optional[Tuple[float, float]] = None,
                 on_complete: Optional[Callable[[int], None]] = None,
                 on_cancel: Optional[Callable[[int], None]] = None,
                 on_pause: Optional[Callable[[int], None]] = None,
                 on_resume: Optional[Callable[[int], None]] = None):
        self.sprite = sprite
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.ease_type = ease_type
        self.elapsed_time = 0
        self.is_complete = False
        self.is_paused = False
        
        # Store the last state before pausing
        self.pause_state = {
            'position': None,
            'angle': None,
            'progress': 0.0
        }
        
        # Rotation properties
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.rotation_type = rotation_type
        self.rotation_center = rotation_center
        self.current_angle = start_angle
        
        # Store original image for rotation
        self.original_image = sprite.image
        
        # Callback functions
        self.on_complete = on_complete
        self.on_cancel = on_cancel
        self.on_pause = on_pause
        self.on_resume = on_resume
        
        # Calculate rotation direction and total angle
        self._calculate_rotation_path()
    
    def _calculate_rotation_path(self):
        """Calculate the optimal rotation path based on rotation type"""
        if self.rotation_type == RotationType.CLOCKWISE:
            if self.end_angle < self.start_angle:
                self.total_angle = 360 - (self.start_angle - self.end_angle)
            else:
                self.total_angle = self.end_angle - self.start_angle
        elif self.rotation_type == RotationType.COUNTERCLOCKWISE:
            if self.end_angle > self.start_angle:
                self.total_angle = -(360 - (self.end_angle - self.start_angle))
            else:
                self.total_angle = -(self.start_angle - self.end_angle)
        else:  # SHORTEST_PATH
            diff = (self.end_angle - self.start_angle) % 360
            if diff <= 180:
                self.total_angle = diff
            else:
                self.total_angle = diff - 360

class AnimationManager:
    def __init__(self):
        self.animations: Dict[int, Animation] = {}
        self.next_animation_id = 0
        
    def create_animation(self,
                        sprite: pygame.sprite.Sprite,
                        end_pos_percent: Tuple[float, float],
                        duration: float,
                        ease_type: EaseType = EaseType.LINEAR,
                        start_angle: float = 0,
                        end_angle: float = 0,
                        rotation_type: RotationType = RotationType.SHORTEST_PATH,
                        rotation_center: Optional[Tuple[float, float]] = None,
                        on_complete: Optional[Callable[[int], None]] = None,
                        on_cancel: Optional[Callable[[int], None]] = None,
                        on_pause: Optional[Callable[[int], None]] = None,
                        on_resume: Optional[Callable[[int], None]] = None) -> int:
        """Creates a new animation for a sprite with optional rotation
        
        Args:
            sprite: The sprite to animate
            end_pos_percent: Target position as percentage of screen size
            duration: Animation duration in seconds
            ease_type: Type of easing to apply
            start_angle: Starting rotation angle in degrees
            end_angle: Ending rotation angle in degrees
            rotation_type: Direction of rotation
            rotation_center: Center point for rotation (defaults to sprite center)
            on_complete: Callback when animation completes normally
            on_cancel: Callback when animation is cancelled
            on_pause: Callback when animation is paused
            on_resume: Callback when animation is resumed
        """
        sizing = get_sizing()
        start_pos = sprite.rect.topleft
        end_pos = sizing.rel_pos(end_pos_percent[0], end_pos_percent[1])
        
        animation = Animation(
            sprite, start_pos, end_pos, duration, ease_type,
            start_angle, end_angle, rotation_type, rotation_center,
            on_complete, on_cancel, on_pause, on_resume
        )
        animation_id = self.next_animation_id
        self.animations[animation_id] = animation
        self.next_animation_id += 1
        return animation_id

    def create_rotation(self,
                       sprite: pygame.sprite.Sprite,
                       end_angle: float,
                       duration: float,
                       rotation_type: RotationType = RotationType.SHORTEST_PATH,
                       ease_type: EaseType = EaseType.LINEAR,
                       rotation_center: Optional[Tuple[float, float]] = None,
                       on_complete: Optional[Callable[[int], None]] = None,
                       on_cancel: Optional[Callable[[int], None]] = None,
                       on_pause: Optional[Callable[[int], None]] = None,
                       on_resume: Optional[Callable[[int], None]] = None) -> int:
        """Creates a pure rotation animation without position change
        
        Args:
            sprite: The sprite to rotate
            end_angle: Target angle in degrees
            duration: Animation duration in seconds
            rotation_type: Direction of rotation
            ease_type: Type of easing to apply
            rotation_center: Center point for rotation (defaults to sprite center)
            on_complete: Callback when animation completes normally
            on_cancel: Callback when animation is cancelled
            on_pause: Callback when animation is paused
            on_resume: Callback when animation is resumed
        """
        start_pos = sprite.rect.topleft
        current_angle = getattr(sprite, 'rotation', 0)
        
        animation = Animation(
            sprite, start_pos, start_pos, duration, ease_type,
            current_angle, end_angle, rotation_type, rotation_center,
            on_complete, on_cancel, on_pause, on_resume
        )
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
                
            if animation.is_paused:
                continue
                
            animation.elapsed_time += delta_time
            progress = min(animation.elapsed_time / animation.duration, 1.0)
            
            # Apply easing function
            eased_progress = self._apply_easing(progress, animation.ease_type)
            
            # Calculate new position
            new_x = animation.start_pos[0] + (animation.end_pos[0] - animation.start_pos[0]) * eased_progress
            new_y = animation.start_pos[1] + (animation.end_pos[1] - animation.start_pos[1]) * eased_progress
            
            # Store current state for pause functionality
            animation.pause_state['position'] = (new_x, new_y)
            animation.pause_state['progress'] = progress
            
            # Calculate new rotation angle
            if animation.total_angle != 0:
                new_angle = animation.start_angle + (animation.total_angle * eased_progress)
                new_angle = new_angle % 360
                
                # Store current angle for pause functionality
                animation.pause_state['angle'] = new_angle
                
                # Perform rotation
                if animation.rotation_center is None:
                    # Use sprite center as rotation point
                    center = animation.sprite.rect.center
                else:
                    center = animation.rotation_center
                
                # Rotate the original image
                rotated_image = pygame.transform.rotate(animation.original_image, -new_angle)
                
                # Get the new rect and maintain the center position
                old_center = animation.sprite.rect.center
                animation.sprite.image = rotated_image
                animation.sprite.rect = animation.sprite.image.get_rect()
                animation.sprite.rect.center = old_center
                
                # Store current angle for reference
                animation.current_angle = new_angle
                setattr(animation.sprite, 'rotation', new_angle)
            
            # Update sprite position
            animation.sprite.rect.topleft = (new_x, new_y)
            
            if progress >= 1.0:
                animation.is_complete = True
                if animation.on_complete:
                    try:
                        animation.on_complete(animation_id)
                    except Exception as e:
                        print(f"Error in animation completion callback: {e}")
                
        # Remove completed animations
        for animation_id in completed_animations:
            del self.animations[animation_id]

    def pause_animation(self, animation_id: int) -> bool:
        """Pauses an animation, preserving its current state
        
        Args:
            animation_id: ID of the animation to pause
            
        Returns:
            bool: True if animation was found and paused, False otherwise
        """
        if animation_id in self.animations:
            animation = self.animations[animation_id]
            if not animation.is_paused and not animation.is_complete:
                animation.is_paused = True
                if animation.on_pause:
                    try:
                        animation.on_pause(animation_id)
                    except Exception as e:
                        print(f"Error in animation pause callback: {e}")
                return True
        return False

    def resume_animation(self, animation_id: int) -> bool:
        """Resumes a paused animation
        
        Args:
            animation_id: ID of the animation to resume
            
        Returns:
            bool: True if animation was found and resumed, False otherwise
        """
        if animation_id in self.animations:
            animation = self.animations[animation_id]
            if animation.is_paused and not animation.is_complete:
                animation.is_paused = False
                if animation.on_resume:
                    try:
                        animation.on_resume(animation_id)
                    except Exception as e:
                        print(f"Error in animation resume callback: {e}")
                return True
        return False

    def toggle_pause(self, animation_id: int) -> bool:
        """Toggles the pause state of an animation
        
        Args:
            animation_id: ID of the animation to toggle
            
        Returns:
            bool: True if animation was found and toggled, False otherwise
        """
        if animation_id in self.animations:
            animation = self.animations[animation_id]
            if animation.is_paused:
                return self.resume_animation(animation_id)
            else:
                return self.pause_animation(animation_id)
        return False

    def pause_all(self) -> None:
        """Pauses all active animations"""
        for animation_id in self.animations:
            self.pause_animation(animation_id)

    def resume_all(self) -> None:
        """Resumes all paused animations"""
        for animation_id in self.animations:
            self.resume_animation(animation_id)

    def cancel_animation(self, animation_id: int) -> bool:
        """Cancels an animation by its ID
        
        Args:
            animation_id: ID of the animation to cancel
            
        Returns:
            bool: True if animation was found and cancelled, False otherwise
        """
        if animation_id in self.animations:
            animation = self.animations[animation_id]
            # Call cancellation callback if it exists
            if animation.on_cancel:
                try:
                    animation.on_cancel(animation_id)
                except Exception as e:
                    print(f"Error in animation cancellation callback: {e}")
            del self.animations[animation_id]
            return True
        return False

    def is_animating(self, animation_id: int) -> bool:
        """Checks if an animation is still running"""
        return animation_id in self.animations

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
            c4 = (2 * math.pi) / 3
            if t == 0 or t == 1:
                return t
            return -pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4)

# Global animation manager instance
animation_manager = None

def get_animation_manager() -> AnimationManager:
    """Get the global animation manager instance"""
    global animation_manager
    if animation_manager is None:
        animation_manager = AnimationManager()
    return animation_manager