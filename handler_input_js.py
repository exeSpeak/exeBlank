import pygame
from pygame.locals import *
from enum import Enum, auto

class ControllerType(Enum):
    UNKNOWN = auto()
    XBOX = auto()
    PS4 = auto()
    PS5 = auto()

class ControllerScheme(Enum):
    DEFAULT = auto()
    INVERTED = auto()
    CUSTOM = auto()

class StandardButtons:
    # Common button mappings across controllers
    A_CROSS = 0
    B_CIRCLE = 1
    X_SQUARE = 2
    Y_TRIANGLE = 3
    LB_L1 = 4
    RB_R1 = 5
    BACK_SHARE = 6
    START_OPTIONS = 7
    L_STICK = 8
    R_STICK = 9

class StandardAxes:
    # Common axis mappings
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5

class ControllerProfile:
    def __init__(self, name, button_mappings=None, axis_mappings=None):
        self.name = name
        self.button_mappings = button_mappings or {}
        self.axis_mappings = axis_mappings or {}
        self.deadzone = 0.15  # Default deadzone

class JoystickHandler:
    def __init__(self):
        """Initialize the joystick handler"""
        pygame.joystick.init()
        self.joysticks = {}
        self.controller_types = {}  # Maps joystick ID to ControllerType
        self.profiles = {}  # Stores different control schemes
        self.active_profiles = {}  # Maps joystick ID to active profile
        self.button_states = {}
        self.axis_states = {}
        self._init_default_profiles()
        self._init_joysticks()
    
    def _init_default_profiles(self):
        """Initialize default controller profiles"""
        # Xbox controller default profile
        xbox_profile = ControllerProfile("Xbox Default")
        xbox_profile.button_mappings = {
            StandardButtons.A_CROSS: "confirm",
            StandardButtons.B_CIRCLE: "cancel",
            StandardButtons.X_SQUARE: "action1",
            StandardButtons.Y_TRIANGLE: "action2",
            StandardButtons.LB_L1: "shoulder_left",
            StandardButtons.RB_R1: "shoulder_right",
            StandardButtons.BACK_SHARE: "back",
            StandardButtons.START_OPTIONS: "start",
            StandardButtons.L_STICK: "l3",
            StandardButtons.R_STICK: "r3"
        }
        
        # PlayStation controller default profile
        ps_profile = ControllerProfile("PlayStation Default")
        ps_profile.button_mappings = {
            StandardButtons.A_CROSS: "confirm",
            StandardButtons.B_CIRCLE: "cancel",
            StandardButtons.X_SQUARE: "action1",
            StandardButtons.Y_TRIANGLE: "action2",
            StandardButtons.LB_L1: "shoulder_left",
            StandardButtons.RB_R1: "shoulder_right",
            StandardButtons.BACK_SHARE: "share",
            StandardButtons.START_OPTIONS: "options",
            StandardButtons.L_STICK: "l3",
            StandardButtons.R_STICK: "r3"
        }
        
        self.profiles["xbox_default"] = xbox_profile
        self.profiles["ps_default"] = ps_profile
    
    def _init_joysticks(self):
        """Initialize all connected joysticks"""
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            self.joysticks[i] = joy
            self.axis_states[i] = {}
            self.button_states[i] = {}
            
            # Detect controller type
            controller_name = joy.get_name().lower()
            if "xbox" in controller_name:
                self.controller_types[i] = ControllerType.XBOX
                self.active_profiles[i] = self.profiles["xbox_default"]
            elif "ps4" in controller_name:
                self.controller_types[i] = ControllerType.PS4
                self.active_profiles[i] = self.profiles["ps_default"]
            elif "ps5" in controller_name:
                self.controller_types[i] = ControllerType.PS5
                self.active_profiles[i] = self.profiles["ps_default"]
            else:
                self.controller_types[i] = ControllerType.UNKNOWN
                self.active_profiles[i] = self.profiles["xbox_default"]  # Default to Xbox mapping
            
            # Initialize axis states
            for axis in range(joy.get_numaxes()):
                self.axis_states[i][axis] = 0.0
            
            # Initialize button states
            for button in range(joy.get_numbuttons()):
                self.button_states[i][button] = False
    
    def create_custom_profile(self, name, base_profile="xbox_default"):
        """Create a new custom profile based on an existing one"""
        base = self.profiles[base_profile]
        new_profile = ControllerProfile(
            name,
            button_mappings=dict(base.button_mappings),
            axis_mappings=dict(base.axis_mappings)
        )
        self.profiles[name] = new_profile
        return new_profile
    
    def set_profile(self, joy_id, profile_name):
        """Set the active profile for a controller"""
        if profile_name in self.profiles:
            self.active_profiles[joy_id] = self.profiles[profile_name]
    
    def remap_button(self, profile_name, button, action):
        """Remap a button in a specific profile"""
        if profile_name in self.profiles:
            self.profiles[profile_name].button_mappings[button] = action
    
    def set_deadzone(self, profile_name, deadzone):
        """Set the deadzone for analog sticks"""
        if profile_name in self.profiles:
            self.profiles[profile_name].deadzone = max(0.0, min(1.0, deadzone))
    
    def get_controller_type(self, joy_id):
        """Get the type of a connected controller"""
        return self.controller_types.get(joy_id, ControllerType.UNKNOWN)
    
    def handle_event(self, event):
        """Process a joystick event"""
        if event.type == JOYAXISMOTION:
            self.axis_states[event.joy][event.axis] = event.value
            self._handle_axis_event(event)
        
        elif event.type == JOYBUTTONDOWN:
            self.button_states[event.joy][event.button] = True
            self._handle_button_event(event, True)
        
        elif event.type == JOYBUTTONUP:
            self.button_states[event.joy][event.button] = False
            self._handle_button_event(event, False)
    
    def _handle_axis_event(self, event):
        """Handle joystick axis movement"""
        profile = self.active_profiles.get(event.joy)
        if not profile:
            return
            
        value = event.value
        deadzone = profile.deadzone
        
        # Apply deadzone
        if abs(value) < deadzone:
            value = 0.0
        else:
            # Normalize value after deadzone
            value = (value - (deadzone * (value/abs(value)))) / (1 - deadzone)
        
        # Handle different axes
        if event.axis == StandardAxes.LEFT_X:
            if abs(value) > 0:
                action = "move_horizontal"
                magnitude = value
                return (action, magnitude)
                
        elif event.axis == StandardAxes.LEFT_Y:
            if abs(value) > 0:
                action = "move_vertical"
                magnitude = value
                return (action, magnitude)
                
        elif event.axis == StandardAxes.RIGHT_X:
            if abs(value) > 0:
                action = "look_horizontal"
                magnitude = value
                return (action, magnitude)
                
        elif event.axis == StandardAxes.RIGHT_Y:
            if abs(value) > 0:
                action = "look_vertical"
                magnitude = value
                return (action, magnitude)
                
        elif event.axis in (StandardAxes.LEFT_TRIGGER, StandardAxes.RIGHT_TRIGGER):
            if value > -0.9:  # Triggers usually start at -1 and go to 1
                action = "left_trigger" if event.axis == StandardAxes.LEFT_TRIGGER else "right_trigger"
                magnitude = (value + 1) / 2  # Convert to 0-1 range
                return (action, magnitude)
    
    def _handle_button_event(self, event, pressed):
        """Handle joystick button press/release"""
        profile = self.active_profiles.get(event.joy)
        if not profile:
            return
            
        action = profile.button_mappings.get(event.button)
        if action:
            return (action, pressed)
    
    def get_axis_value(self, joy_id, axis):
        """Get the current value of a specific axis"""
        return self.axis_states.get(joy_id, {}).get(axis, 0.0)
    
    def is_button_pressed(self, joy_id, button):
        """Check if a specific button is currently pressed"""
        return self.button_states.get(joy_id, {}).get(button, False)
    
    def get_connected_joysticks(self):
        """Get number of connected joysticks"""
        return len(self.joysticks)
    
    def get_active_profile(self, joy_id):
        """Get the active profile for a controller"""
        return self.active_profiles.get(joy_id)
