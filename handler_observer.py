from typing import Dict, List, Callable, Any, Optional, Set
from enum import Enum, auto
from dataclasses import dataclass
from weakref import WeakKeyDictionary
import logging

from handler_input import InputEvent, InputPriority

class ObserverPriority(Enum):
    """Priority levels for observers"""
    CRITICAL = 0    # System-critical observers (error handlers, etc.)
    HIGH = 1        # High-priority game logic (collision, health, etc.)
    NORMAL = 2      # Standard game logic
    LOW = 3         # Visual effects, sound, etc.
    BACKGROUND = 4  # Logging, analytics, etc.

@dataclass
class ObserverInfo:
    """Stores information about an observer"""
    callback: Callable
    priority: ObserverPriority
    event_types: Set[str]
    enabled: bool = True

class Subject:
    """Base class for objects that can be observed"""
    def __init__(self):
        self._observers: WeakKeyDictionary = WeakKeyDictionary()
        self._event_map: Dict[str, List[object]] = {}
    
    def attach(self, observer: object, callback: Callable,
              event_types: List[str] = None,
              priority: ObserverPriority = ObserverPriority.NORMAL) -> None:
        """
        Attach an observer to this subject
        
        Args:
            observer: The observer object
            callback: The method to call when notifying
            event_types: List of event types to observe (None for all)
            priority: Priority level for this observer
        """
        if observer in self._observers:
            logging.warning(f"Observer {observer} already attached to {self}")
            return
            
        event_types_set = set(event_types) if event_types else set()
        self._observers[observer] = ObserverInfo(
            callback=callback,
            priority=priority,
            event_types=event_types_set,
            enabled=True
        )
        
        # Update event map for quick lookup
        for event_type in event_types_set:
            if event_type not in self._event_map:
                self._event_map[event_type] = []
            self._event_map[event_type].append(observer)
    
    def detach(self, observer: object) -> None:
        """Remove an observer"""
        if observer in self._observers:
            # Remove from event map
            observer_info = self._observers[observer]
            for event_type in observer_info.event_types:
                if event_type in self._event_map:
                    self._event_map[event_type].remove(observer)
                    if not self._event_map[event_type]:
                        del self._event_map[event_type]
            
            # Remove observer
            del self._observers[observer]
    
    def notify(self, event: InputEvent) -> None:
        """
        Notify all relevant observers of an event
        
        Args:
            event: The event to notify observers about
        """
        # Get observers for this event type
        observers = set()
        if event.event_type in self._event_map:
            observers.update(self._event_map[event.event_type])
        
        # Get observers listening to all events
        observers.update(o for o, info in self._observers.items()
                        if not info.event_types)
        
        # Sort observers by priority
        sorted_observers = sorted(
            [(o, self._observers[o]) for o in observers],
            key=lambda x: x[1].priority.value
        )
        
        # Notify observers
        for observer, info in sorted_observers:
            if info.enabled:
                try:
                    info.callback(event)
                except Exception as e:
                    logging.error(f"Error in observer {observer}: {e}")
    
    def enable_observer(self, observer: object) -> None:
        """Enable an observer"""
        if observer in self._observers:
            self._observers[observer].enabled = True
    
    def disable_observer(self, observer: object) -> None:
        """Disable an observer"""
        if observer in self._observers:
            self._observers[observer].enabled = False
    
    def is_observer_enabled(self, observer: object) -> bool:
        """Check if an observer is enabled"""
        return observer in self._observers and self._observers[observer].enabled

class EventSubject(Subject):
    """Subject specifically for game events"""
    def __init__(self):
        super().__init__()
        self._paused = False
        self._pause_queue: List[InputEvent] = []
    
    def notify(self, event: InputEvent) -> None:
        """Override notify to handle paused state"""
        if self._paused:
            self._pause_queue.append(event)
        else:
            super().notify(event)
    
    def pause(self) -> None:
        """Pause event processing"""
        self._paused = True
    
    def resume(self) -> None:
        """Resume event processing and process queued events"""
        self._paused = False
        queued = self._pause_queue
        self._pause_queue = []
        for event in queued:
            super().notify(event)

class GameObserver:
    """Base class for game objects that can observe events"""
    def __init__(self):
        self._subjects: WeakKeyDictionary = WeakKeyDictionary()
    
    def observe(self, subject: Subject, callback: Callable,
               event_types: List[str] = None,
               priority: ObserverPriority = ObserverPriority.NORMAL) -> None:
        """
        Start observing a subject
        
        Args:
            subject: The subject to observe
            callback: Method to call when notified
            event_types: List of event types to observe (None for all)
            priority: Priority level for this observer
        """
        subject.attach(self, callback, event_types, priority)
        self._subjects[subject] = True
    
    def stop_observing(self, subject: Optional[Subject] = None) -> None:
        """
        Stop observing a subject (or all subjects if none specified)
        
        Args:
            subject: The subject to stop observing, or None for all
        """
        if subject is None:
            for s in list(self._subjects.keys()):
                s.detach(self)
                del self._subjects[s]
        elif subject in self._subjects:
            subject.detach(self)
            del self._subjects[subject]

# Example usage
"""
# Create a game object that observes events
class Player(GameObserver):
    def __init__(self, event_subject):
        super().__init__()
        
        # Start observing specific event types
        self.observe(
            event_subject,
            self.handle_movement,
            ["keydown", "keyup", "axis"],
            ObserverPriority.HIGH
        )
        
        self.observe(
            event_subject,
            self.handle_action,
            ["button_down"],
            ObserverPriority.NORMAL
        )
    
    def handle_movement(self, event: InputEvent):
        if event.event_type == "axis":
            # Handle joystick movement
            self.move(event.data["value"])
        elif event.event_type in ("keydown", "keyup"):
            # Handle keyboard movement
            self.handle_key_movement(event)
    
    def handle_action(self, event: InputEvent):
        if event.data["button"] == 0:  # A button
            self.jump()
        elif event.data["button"] == 1:  # B button
            self.attack()

# Create the event subject
event_subject = EventSubject()

# Create game objects
player = Player(event_subject)
enemy = Enemy(event_subject)

# In game loop
def game_loop():
    # Process events
    for event in input_events:
        event_subject.notify(event)
    
    # Game can be paused/resumed
    if pause_pressed:
        event_subject.pause()
    elif resume_pressed:
        event_subject.resume()
"""