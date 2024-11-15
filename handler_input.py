
from enum import Enum, auto
import pygame
from pygame.locals import *
from collections import defaultdict, deque
import time
import heapq

# Import all input handlers
from handler_input_kb import KeyboardHandler
from handler_input_js import JoystickHandler
from handler_input_mouse import MouseHandler
from handler_input_buffer import FightingGameInput
from handler_input_network import NetworkInputHandler, NetworkRole

class InputSource(Enum):
    KEYBOARD = auto()
    JOYSTICK = auto()
    MOUSE = auto()
    NETWORK = auto()

class InputPriority(Enum):
    """Priority levels for input processing"""
    HIGH = 1    # Critical inputs (e.g., pause, quit)
    NORMAL = 2  # Standard gameplay inputs
    LOW = 3     # Non-essential inputs (e.g., UI hover)

class InputEvent:
    def __init__(self, source, event_type, data, timestamp=None, priority=InputPriority.NORMAL):
        self.source = source
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or time.time()
        self.priority = priority
        self.handled = False
        self.frame_number = None  # Set when added to queue
    
    def __lt__(self, other):
        """Compare events for priority queue"""
        return (self.priority.value, self.timestamp) < (other.priority.value, other.timestamp)

class EventQueue:
    """Manages event queuing and processing timing"""
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.current_queue = deque(maxlen=max_size)  # Current frame events
        self.priority_queue = []  # Priority queue for immediate processing
        self.delayed_queue = []   # Heap queue for delayed events
        self.processing_time = 0.016  # 16ms default frame time
    
    def add_event(self, event, delay=0):
        """Add event to appropriate queue based on delay and priority"""
        if delay > 0:
            heapq.heappush(self.delayed_queue, (time.time() + delay, event))
        elif event.priority == InputPriority.HIGH:
            heapq.heappush(self.priority_queue, event)
        else:
            self.current_queue.append(event)
    
    def get_ready_events(self):
        """Get all events ready for processing"""
        current_time = time.time()
        
        # Process delayed events that are ready
        while self.delayed_queue and self.delayed_queue[0][0] <= current_time:
            _, event = heapq.heappop(self.delayed_queue)
            self.add_event(event)
        
        # Get high priority events first
        priority_events = []
        while self.priority_queue:
            priority_events.append(heapq.heappop(self.priority_queue))
        
        # Combine with current queue events
        ready_events = priority_events + list(self.current_queue)
        self.current_queue.clear()
        
        return ready_events
    
    def clear(self):
        """Clear all queues"""
        self.current_queue.clear()
        self.priority_queue.clear()
        self.delayed_queue.clear()

class EventManager:
    def __init__(self):
        # Initialize all input handlers
        self.keyboard = KeyboardHandler()
        self.joystick = JoystickHandler()
        self.mouse = MouseHandler()
        self.input_buffer = FightingGameInput()
        self.network = None  # Initialize later when network role is known
        
        # Event queuing system
        self.event_queue = EventQueue()
        self.event_history = deque(maxlen=300)  # Last 5 seconds at 60fps
        
        # Callback registrations
        self.callbacks = defaultdict(list)
        
        # Input state tracking
        self.pressed_keys = set()
        self.pressed_buttons = defaultdict(set)  # per joystick
        self.mouse_position = (0, 0)
        self.mouse_buttons = set()
        
        # Frame counting and timing
        self.current_frame = 0
        self.last_process_time = time.time()
        self.frame_time = 1/60  # Target 60 FPS
    
    def init_network(self, host="localhost", port=5000, role=NetworkRole.HOST):
        """Initialize network handler with specific role"""
        self.network = NetworkInputHandler(host=host, port=port, role=role)
    
    def register_callback(self, event_type, callback, priority=InputPriority.NORMAL):
        """Register a callback for a specific event type with priority"""
        self.callbacks[event_type].append((priority, callback))
        # Sort callbacks by priority
        self.callbacks[event_type].sort(key=lambda x: x[0].value)
    
    def unregister_callback(self, event_type, callback):
        """Remove a callback for a specific event type"""
        self.callbacks[event_type] = [(p, cb) for p, cb in self.callbacks[event_type] 
                                    if cb != callback]
    
    def process_events(self):
        """Process all pending events for the current frame"""
        current_time = time.time()
        elapsed = current_time - self.last_process_time
        
        # Collect events from all sources
        self._collect_pygame_events()
        self._collect_network_events()
        self._collect_buffer_events()
        
        # Process ready events
        ready_events = self.event_queue.get_ready_events()
        
        # Update event history
        self.event_history.extend(ready_events)
        
        # Dispatch events
        self._dispatch_events(ready_events)
        
        # Update timing
        self.last_process_time = current_time
        self.current_frame += 1
        
        # Return elapsed time for frame timing purposes
        return elapsed
    
    def _collect_pygame_events(self):
        """Collect and queue pygame events"""
        for event in pygame.event.get():
            input_event = None
            
            # Determine priority (example: QUIT is high priority)
            priority = InputPriority.HIGH if event.type == QUIT else InputPriority.NORMAL
            
            # Keyboard events
            if event.type in (KEYDOWN, KEYUP):
                input_event = self._handle_keyboard_event(event, priority)
            
            # Joystick events
            elif event.type in (JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP):
                input_event = self._handle_joystick_event(event, priority)
            
            # Mouse events
            elif event.type in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                input_event = self._handle_mouse_event(event, priority)
            
            if input_event:
                self.event_queue.add_event(input_event)
    
    def _handle_keyboard_event(self, event, priority=InputPriority.NORMAL):
        """Process keyboard events"""
        if event.type == KEYDOWN:
            self.pressed_keys.add(event.key)
            return InputEvent(
                InputSource.KEYBOARD,
                "keydown",
                {"key": event.key, "mod": event.mod},
                priority=priority
            )
        elif event.type == KEYUP:
            self.pressed_keys.discard(event.key)
            return InputEvent(
                InputSource.KEYBOARD,
                "keyup",
                {"key": event.key, "mod": event.mod},
                priority=priority
            )
    
    def _handle_joystick_event(self, event, priority=InputPriority.NORMAL):
        """Process joystick events"""
        if event.type == JOYAXISMOTION:
            return InputEvent(
                InputSource.JOYSTICK,
                "axis",
                {
                    "joy": event.joy,
                    "axis": event.axis,
                    "value": event.value
                },
                priority=priority
            )
        elif event.type == JOYBUTTONDOWN:
            self.pressed_buttons[event.joy].add(event.button)
            return InputEvent(
                InputSource.JOYSTICK,
                "button_down",
                {"joy": event.joy, "button": event.button},
                priority=priority
            )
        elif event.type == JOYBUTTONUP:
            self.pressed_buttons[event.joy].discard(event.button)
            return InputEvent(
                InputSource.JOYSTICK,
                "button_up",
                {"joy": event.joy, "button": event.button},
                priority=priority
            )
    
    def _handle_mouse_event(self, event, priority=InputPriority.NORMAL):
        """Process mouse events"""
        if event.type == MOUSEMOTION:
            self.mouse_position = event.pos
            return InputEvent(
                InputSource.MOUSE,
                "motion",
                {"pos": event.pos, "rel": event.rel},
                priority=InputPriority.LOW  # Mouse motion is usually low priority
            )
        elif event.type == MOUSEBUTTONDOWN:
            self.mouse_buttons.add(event.button)
            return InputEvent(
                InputSource.MOUSE,
                "button_down",
                {"button": event.button, "pos": event.pos},
                priority=priority
            )
        elif event.type == MOUSEBUTTONUP:
            self.mouse_buttons.discard(event.button)
            return InputEvent(
                InputSource.MOUSE,
                "button_up",
                {"button": event.button, "pos": event.pos},
                priority=priority
            )
    
    def _collect_network_events(self):
        """Collect and queue network events"""
        if not self.network or not self.network.connected:
            return
            
        # Check for rollback
        rollback_frame = self.network.check_rollback()
        if rollback_frame is not None:
            self.event_queue.add_event(InputEvent(
                InputSource.NETWORK,
                "rollback",
                {"frame": rollback_frame},
                priority=InputPriority.HIGH  # Rollback needs immediate processing
            ))
    
    def _collect_buffer_events(self):
        """Collect and queue input buffer events"""
        if not self.input_buffer:
            return
            
        # Check for completed moves in the buffer
        move = self.input_buffer.process_input(None, None)  # Modified to not require current event
        if move:
            self.event_queue.add_event(InputEvent(
                InputSource.NETWORK,
                "special_move",
                {"move": move},
                priority=InputPriority.NORMAL
            ))
    
    def _dispatch_events(self, events):
        """Dispatch events to registered callbacks"""
        for event in events:
            if event.event_type in self.callbacks:
                for priority, callback in self.callbacks[event.event_type]:
                    callback(event)
                    event.handled = True
    
    def add_delayed_event(self, event_type, data, delay, priority=InputPriority.NORMAL):
        """Add an event to be processed after a delay (in seconds)"""
        event = InputEvent(InputSource.NETWORK, event_type, data, priority=priority)
        self.event_queue.add_event(event, delay)
    
    def is_key_pressed(self, key):
        """Check if a keyboard key is currently pressed"""
        return key in self.pressed_keys
    
    def is_button_pressed(self, joy, button):
        """Check if a joystick button is currently pressed"""
        return button in self.pressed_buttons.get(joy, set())
    
    def is_mouse_button_pressed(self, button):
        """Check if a mouse button is currently pressed"""
        return button in self.mouse_buttons
    
    def get_mouse_pos(self):
        """Get current mouse position"""
        return self.mouse_position
    
    def get_frame_events(self, frame=None):
        """Get events for a specific frame"""
        if frame is None:
            return list(self.event_queue.current_queue)
        
        return [e for e in self.event_history if e.frame_number == frame]

# Example usage with queue system
"""
event_manager = EventManager()

# Register high-priority pause callback
def on_pause(event):
    game.pause()

event_manager.register_callback("keydown", on_pause, InputPriority.HIGH)

# Register normal priority move callback
def on_move(event):
    player.move(event.data['axis'])

event_manager.register_callback("axis", on_move, InputPriority.NORMAL)

# Add delayed event (e.g., power-up expiration)
event_manager.add_delayed_event("power_up_end", {"type": "speed"}, delay=10.0)

# In game loop
def game_loop():
    elapsed = event_manager.process_events()
    
    # Use elapsed time for frame timing
    if elapsed < event_manager.frame_time:
        time.sleep(event_manager.frame_time - elapsed)
"""