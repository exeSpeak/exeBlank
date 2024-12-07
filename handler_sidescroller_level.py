import pygame
import json
from typing import List, Dict, Tuple, Optional
from handler_animation_2d import get_animation_manager, EaseType
from handler_gui_sizing import get_sizing
from enum import Enum, auto
import math
from dataclasses import dataclass
import os
from datetime import datetime

class PlatformType(Enum):
    STATIC = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    CIRCULAR = auto()
    CUSTOM = auto()

class MovingPlatform:
    def __init__(self, platform_data: dict):
        self.platform = platform_data
        self.original_pos = (platform_data['x'], platform_data['y'])
        self.movement_type = PlatformType[platform_data.get('movement_type', 'STATIC')]
        self.movement_range = platform_data.get('movement_range', 0)
        self.movement_speed = platform_data.get('movement_speed', 1.0)
        self.current_animation_id = None
        self.waypoints = platform_data.get('waypoints', [])
        self.current_waypoint = 0
        
    def start_movement(self, animation_manager):
        if self.movement_type == PlatformType.STATIC:
            return
            
        if self.current_animation_id is not None and animation_manager.is_animating(self.current_animation_id):
            return
            
        next_pos = self._get_next_position()
        if next_pos:
            duration = self._calculate_duration(next_pos)
            self.current_animation_id = animation_manager.create_animation(
                self.platform['sprite'],
                next_pos,
                duration,
                self._get_ease_type()
            )
            
    def _get_next_position(self) -> tuple:
        if self.movement_type == PlatformType.HORIZONTAL:
            current_x = self.platform['x']
            if abs(current_x - self.original_pos[0]) >= self.movement_range:
                return (self.original_pos[0], self.original_pos[1])
            return (self.original_pos[0] + self.movement_range, self.original_pos[1])
            
        elif self.movement_type == PlatformType.VERTICAL:
            current_y = self.platform['y']
            if abs(current_y - self.original_pos[1]) >= self.movement_range:
                return (self.original_pos[0], self.original_pos[1])
            return (self.original_pos[0], self.original_pos[1] + self.movement_range)
            
        elif self.movement_type == PlatformType.CIRCULAR:
            angle = math.atan2(
                self.platform['y'] - self.original_pos[1],
                self.platform['x'] - self.original_pos[0]
            )
            angle += math.pi / 2  # Move 90 degrees along circle
            new_x = self.original_pos[0] + math.cos(angle) * self.movement_range
            new_y = self.original_pos[1] + math.sin(angle) * self.movement_range
            return (new_x, new_y)
            
        elif self.movement_type == PlatformType.CUSTOM and self.waypoints:
            next_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
            self.current_waypoint = next_waypoint
            return self.waypoints[next_waypoint]
            
        return None
        
    def _calculate_duration(self, next_pos) -> float:
        current_pos = (self.platform['x'], self.platform['y'])
        distance = math.sqrt(
            (next_pos[0] - current_pos[0])**2 +
            (next_pos[1] - current_pos[1])**2
        )
        return distance / (100 * self.movement_speed)  # Adjust speed factor as needed
        
    def _get_ease_type(self) -> EaseType:
        if self.movement_type in [PlatformType.HORIZONTAL, PlatformType.VERTICAL]:
            return EaseType.EASE_IN_OUT
        elif self.movement_type == PlatformType.CIRCULAR:
            return EaseType.LINEAR
        return EaseType.EASE_IN_OUT

@dataclass
class ParallaxLayer:
    sprite: pygame.Surface
    depth: float  # 0.0 to 1.0, where 1.0 is closest to camera
    x_offset: float = 0
    y_offset: float = 0
    scroll_speed: float = 1.0
    repeat_x: bool = True
    repeat_y: bool = False
    auto_scroll: bool = False
    auto_scroll_speed: float = 0

class ParallaxBackground:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layers: List[ParallaxLayer] = []
        self.sprite_handler = SpriteHandler()
        
    def add_layer(self, 
                  sprite_path: str, 
                  depth: float, 
                  scroll_speed: float = 1.0,
                  repeat_x: bool = True,
                  repeat_y: bool = False,
                  auto_scroll: bool = False,
                  auto_scroll_speed: float = 0) -> None:
        """Add a new parallax layer"""
        sprite = self.sprite_handler.get_sprite(sprite_path)
        if sprite:
            layer = ParallaxLayer(
                sprite=sprite,
                depth=max(0.0, min(1.0, depth)),  # Clamp between 0 and 1
                scroll_speed=scroll_speed,
                repeat_x=repeat_x,
                repeat_y=repeat_y,
                auto_scroll=auto_scroll,
                auto_scroll_speed=auto_scroll_speed
            )
            # Insert layer in sorted order by depth (furthest first)
            insert_idx = 0
            for i, existing_layer in enumerate(self.layers):
                if existing_layer.depth > depth:
                    insert_idx = i
                    break
            self.layers.insert(insert_idx, layer)
            
    def update(self, camera_x: float, camera_y: float, delta_time: float) -> None:
        """Update all parallax layers based on camera position"""
        for layer in self.layers:
            # Calculate parallax offset based on depth and camera position
            parallax_factor = 1.0 - layer.depth
            target_x = -camera_x * parallax_factor * layer.scroll_speed
            
            # Apply auto-scrolling if enabled
            if layer.auto_scroll:
                layer.x_offset += layer.auto_scroll_speed * delta_time
                
            # Smooth movement towards target position
            layer.x_offset += (target_x - layer.x_offset) * 0.1
            
            # Handle wrapping for repeating backgrounds
            if layer.repeat_x:
                layer.x_offset = layer.x_offset % layer.sprite.get_width()
                
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all parallax layers to the screen"""
        for layer in self.layers:
            # Calculate how many times we need to repeat the sprite to fill the screen
            if layer.repeat_x:
                num_repeats_x = (self.screen_width // layer.sprite.get_width()) + 2
            else:
                num_repeats_x = 1
                
            if layer.repeat_y:
                num_repeats_y = (self.screen_height // layer.sprite.get_height()) + 2
            else:
                num_repeats_y = 1
                
            # Draw the layer with proper repetition
            for x in range(num_repeats_x):
                for y in range(num_repeats_y):
                    pos_x = (x * layer.sprite.get_width() + int(layer.x_offset)) % self.screen_width
                    pos_y = y * layer.sprite.get_height()
                    
                    # Only draw if the sprite would be visible
                    if (pos_x > -layer.sprite.get_width() and 
                        pos_x < self.screen_width and
                        pos_y > -layer.sprite.get_height() and 
                        pos_y < self.screen_height):
                        surface.blit(layer.sprite, (pos_x, pos_y))

@dataclass
class CheckpointFlag:
    x: float
    y: float
    width: int
    height: int
    sprite: pygame.Surface
    is_activated: bool = False
    save_id: str = ""
    animation_frame: int = 0
    animation_timer: float = 0
    ANIMATION_FRAME_TIME: float = 0.1
    
    def update(self, delta_time: float) -> None:
        """Update flag animation"""
        if self.is_activated:
            self.animation_timer += delta_time
            if self.animation_timer >= self.ANIMATION_FRAME_TIME:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4  # Assuming 4 animation frames

class SaveState:
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
    def save_checkpoint(self, level_id: str, checkpoint_id: str, player_data: dict) -> bool:
        """Save player progress at checkpoint"""
        try:
            save_data = {
                'level_id': level_id,
                'checkpoint_id': checkpoint_id,
                'player_data': player_data,
                'timestamp': datetime.now().isoformat()
            }
            
            save_path = os.path.join(self.save_dir, f"checkpoint_{level_id}.json")
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving checkpoint: {e}")
            return False
            
    def load_checkpoint(self, level_id: str) -> dict:
        """Load the latest checkpoint data"""
        try:
            save_path = os.path.join(self.save_dir, f"checkpoint_{level_id}.json")
            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return None

class SideScrollerLevel:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        self.camera_y = 0
        self.platforms = []
        self.obstacles = []
        self.collectibles = []
        self.spawn_point = (0, 0)
        self.level_width = 0
        self.level_height = 0
        self.parallax_background = ParallaxBackground(screen_width, screen_height)
        self.moving_platforms = []
        self.animation_manager = get_animation_manager()
        self.checkpoint_flags: List[CheckpointFlag] = []
        self.current_checkpoint: Optional[CheckpointFlag] = None
        self.level_id: str = ""
        self.save_state = SaveState()
        
    def load_level(self, level_data: str) -> bool:
        try:
            data = json.loads(level_data)
            self.level_width = data.get('level_width', 0)
            self.level_height = data.get('level_height', 0)
            self.platforms = data.get('platforms', [])
            self.obstacles = data.get('obstacles', [])
            self.collectibles = data.get('collectibles', [])
            self.spawn_point = tuple(data.get('spawn_point', (0, 0)))
            
            # Load level ID
            self.level_id = data.get('level_id', '')
            
            # Load parallax backgrounds
            background_data = data.get('backgrounds', [])
            for bg in background_data:
                self.parallax_background.add_layer(
                    sprite_path=bg['sprite_path'],
                    depth=bg.get('depth', 0.0),
                    scroll_speed=bg.get('scroll_speed', 1.0),
                    repeat_x=bg.get('repeat_x', True),
                    repeat_y=bg.get('repeat_y', False),
                    auto_scroll=bg.get('auto_scroll', False),
                    auto_scroll_speed=bg.get('auto_scroll_speed', 0)
                )
            
            # Load checkpoint flags
            checkpoint_data = data.get('checkpoints', [])
            for checkpoint in checkpoint_data:
                sprite = self.sprite_handler.get_sprite(checkpoint['sprite_path'])
                if sprite:
                    flag = CheckpointFlag(
                        x=checkpoint['x'],
                        y=checkpoint['y'],
                        width=checkpoint.get('width', 32),
                        height=checkpoint.get('height', 64),
                        sprite=sprite,
                        save_id=checkpoint.get('id', '')
                    )
                    self.checkpoint_flags.append(flag)
            
            # Initialize moving platforms
            for platform in self.platforms:
                if 'movement_type' in platform:
                    self.moving_platforms.append(MovingPlatform(platform))
                    
            # Load last checkpoint if exists
            saved_data = self.save_state.load_checkpoint(self.level_id)
            if saved_data:
                last_checkpoint_id = saved_data['checkpoint_id']
                for flag in self.checkpoint_flags:
                    if flag.save_id == last_checkpoint_id:
                        flag.is_activated = True
                        self.current_checkpoint = flag
                        # Restore player position to last checkpoint if needed
                        self.spawn_point = (flag.x + flag.width/2, flag.y + flag.height)
            
            return True
        except Exception as e:
            print(f"Error loading level: {e}")
            return False
            
    def update(self, delta_time: float) -> None:
        """Update level state including moving platforms"""
        # Update platform movements
        for platform in self.moving_platforms:
            platform.start_movement(self.animation_manager)
            
        # Update camera position if needed
        if hasattr(self, 'target_camera_x'):
            self.update_camera(self.target_camera_x, 0)
            
        # Update parallax backgrounds
        self.parallax_background.update(self.camera_x, self.camera_y, delta_time)
        
        # Update checkpoint flags
        for flag in self.checkpoint_flags:
            flag.update(delta_time)
            
    def update_camera(self, player_x: float, player_y: float) -> None:
        target_x = player_x - self.screen_width // 2
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.camera_x, self.level_width - self.screen_width))
        
    def get_visible_objects(self) -> Tuple[List, List, List]:
        visible_range = (self.camera_x - 100, self.camera_x + self.screen_width + 100)
        visible_platforms = [p for p in self.platforms 
                           if visible_range[0] <= p['x'] <= visible_range[1]]
        visible_obstacles = [o for o in self.obstacles 
                           if visible_range[0] <= o['x'] <= visible_range[1]]
        visible_collectibles = [c for c in self.collectibles 
                              if visible_range[0] <= c['x'] <= visible_range[1]]
        return visible_platforms, visible_obstacles, visible_collectibles
        
    def check_collision(self, entity_rect: pygame.Rect) -> Dict:
        collision_info = {
            'ground': False,
            'ceiling': False,
            'left': False,
            'right': False,
            'platform': None,
            'obstacle': None,
            'collectible': None
        }
        
        # Get only visible objects for optimization
        visible_platforms, visible_obstacles, visible_collectibles = self.get_visible_objects()
        
        # Check platform collisions
        for platform in visible_platforms:
            platform_rect = pygame.Rect(
                platform['x'] - self.camera_x,
                platform['y'],
                platform['width'],
                platform['height']
            )
            
            if entity_rect.colliderect(platform_rect):
                collision_info['platform'] = platform
                # Determine collision side
                if entity_rect.bottom >= platform_rect.top and entity_rect.top < platform_rect.top:
                    collision_info['ground'] = True
                elif entity_rect.top <= platform_rect.bottom and entity_rect.bottom > platform_rect.bottom:
                    collision_info['ceiling'] = True
                elif entity_rect.right >= platform_rect.left and entity_rect.left < platform_rect.left:
                    collision_info['right'] = True
                elif entity_rect.left <= platform_rect.right and entity_rect.right > platform_rect.right:
                    collision_info['left'] = True
                    
        return collision_info
        
    def check_checkpoint_collision(self, player_rect: pygame.Rect, player_data: dict) -> bool:
        """Check if player has reached a new checkpoint"""
        for flag in self.checkpoint_flags:
            if not flag.is_activated:
                flag_rect = pygame.Rect(
                    flag.x - self.camera_x,
                    flag.y,
                    flag.width,
                    flag.height
                )
                
                if player_rect.colliderect(flag_rect):
                    # Activate flag and save progress
                    flag.is_activated = True
                    self.current_checkpoint = flag
                    self.save_state.save_checkpoint(
                        self.level_id,
                        flag.save_id,
                        player_data
                    )
                    return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the entire level including backgrounds, platforms, and objects"""
        # Draw parallax backgrounds first
        self.parallax_background.draw(surface)
        
        # Draw other level elements
        visible_platforms, visible_obstacles, visible_collectibles = self.get_visible_objects()
        
        # Draw platforms
        for platform in visible_platforms:
            if 'sprite' in platform:
                surface.blit(
                    platform['sprite'],
                    (platform['x'] - self.camera_x, platform['y'])
                )
                
        # Draw obstacles and collectibles similarly...
        
        # Draw checkpoint flags
        for flag in self.checkpoint_flags:
            # Calculate the source rectangle for the animation frame
            frame_width = flag.sprite.get_width() // 4  # Assuming 4 frames in sprite sheet
            source_rect = pygame.Rect(
                frame_width * flag.animation_frame,
                0,
                frame_width,
                flag.sprite.get_height()
            )
            
            # Draw the flag with the current animation frame
            dest_rect = pygame.Rect(
                flag.x - self.camera_x,
                flag.y,
                flag.width,
                flag.height
            )
            surface.blit(flag.sprite, dest_rect, source_rect)
            
    def get_spawn_position(self) -> Tuple[float, float]:
        return self.spawn_point
        
    def is_level_complete(self, player_x: float) -> bool:
        # Consider level complete if player has reached 90% of level width
        return player_x >= self.level_width * 0.9