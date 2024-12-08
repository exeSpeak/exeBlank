import pygame
import handler_gui_layers
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum, auto
from handler_gui_sizing import get_sizing
from handler_animation_2d import get_animation_manager

class LoadingState(Enum):
    INACTIVE = auto()
    FADE_IN = auto()
    LOADING = auto()
    FADE_OUT = auto()

@dataclass
class LoadingTask:
    name: str
    weight: float  # How much this task contributes to total progress (0.0 to 1.0)
    callback: Callable[[], None]
    completed: bool = False

class LoadingHandler:
    def __init__(self):
        self.current_state = LoadingState.INACTIVE
        self.tasks: List[LoadingTask] = []
        self.tasks_count_starting: int = 0
        self.tasks_count_current: int = 0
        self.background_surface: Optional[pygame.Surface] = None
        self.loading_text: str = "Loading..."
        self.fade_alpha: int = 0
        self.on_complete: Optional[Callable[[], None]] = None
    
    def initialize(self) -> None:
        """Initialize the loading screen with default settings"""
        self.loading_layer = handler_gui_layers.layer_loading()
        self.loading_layer.hide()  # Start hidden
        self.current_state = LoadingState.INACTIVE
    
    def begin(self, on_complete: Optional[Callable[[], None]] = None) -> None:
        """Begin the loading sequence"""
        self.current_state = LoadingState.LOADING
        self.on_complete = on_complete
        self.tasks_count_starting = len(self.tasks)
        self.tasks_count_current = 0
        self.loading_layer.show()
        self.callfade_blackToVisible()
    
    def callfade_blackToVisible(self) -> None:
        """Tells handler_loading_fade.py to start a fade in transition"""
        import handler_loading_fade
        handler_loading_fade.get_fade_handler().begin_fade_in()
    
    def callfade_VisibleToBlack(self) -> None:
        """Tells handler_loading_fade.py to start a fade out transition"""
        import handler_loading_fade
        handler_loading_fade.get_fade_handler().begin_fade_out()
    
    def return_isLoading(self) -> bool:
        """Check if loading screen is currently active"""
        return self.current_state != LoadingState.INACTIVE
    
    def set_background(self, surface: pygame.Surface) -> None:
        """Set a custom background for the loading screen"""
        if hasattr(self, 'loading_layer'):
            self.loading_layer.background = surface
    
    def set_text(self, text: str) -> None:
        """Set custom loading text"""
        if hasattr(self, 'loading_layer'):
            self.loading_layer.loading_text.text = text
    
    def set_progressBar(self) -> None:
        temp_howFarAlongAreWe = self.tasks_count_current / self.tasks_count_starting
        temp_howFarAlongAreWe = max(min(temp_howFarAlongAreWe, 1.0), 0.0)
        temp_howFarAlongAreWe *= 100.0
        handler_gui_layers.layer_loading.update_progress(temp_howFarAlongAreWe)
    
    def tasks_add(self, name: str, callback: Callable[[], None], weight: float = 1.0) -> None:
        """Add a task to be executed during loading"""
        task = LoadingTask(name=name, callback=callback, weight=weight, completed=False)
        self.tasks.append(task)
    
    def tasks_clear(self) -> None:
        """Clear all registered loading tasks"""
        self.tasks.clear()
        self.tasks_count_starting = 0
        self.tasks_count_current = 0
    
    def tasks_executeNext(self) -> bool:
        """Execute the next pending task in the queue"""
        for task in self.tasks:
            if not task.completed:
                try:
                    task.callback()
                    task.completed = True
                    self.tasks_count_current += 1
                    return True
                except Exception as e:
                    print(f"Error executing task {task.name}: {str(e)}")
                    return False
        return False
    
    def tasks_remove(self, name: str) -> None:
        """Remove a specific loading task by name"""
        self.tasks = [task for task in self.tasks if task.name != name]
        # Update counts
        self.tasks_count_starting = len(self.tasks)
        self.tasks_count_current = len([task for task in self.tasks if task.completed])
    
    def update(self, delta_time: float) -> None:
        """Update loading screen state and progress"""
        if self.current_state != LoadingState.LOADING:
            return

        # Execute next task if available
        if not self.tasks_executeNext():
            # All tasks completed
            if self.tasks_count_current >= self.tasks_count_starting:
                self.callfade_VisibleToBlack()
                if self.on_complete:
                    self.on_complete()
                self.current_state = LoadingState.INACTIVE
                self.loading_layer.hide()
        
        # Update progress bar
        self.set_progressBar()
    
# Global loading handler instance
loading_handler = None

def get_loading_handler() -> LoadingHandler:
    """Get the global loading handler instance"""
    global loading_handler
    if loading_handler is None:
        loading_handler = LoadingHandler()
        loading_handler.initialize()
    return loading_handler
