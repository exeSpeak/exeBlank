from collections import deque
from enum import Enum, auto
import time

class InputType(Enum):
    BUTTON = auto()
    DIRECTION = auto()
    COMBINATION = auto()

class Direction(Enum):
    NEUTRAL = "5"
    UP = "8"
    DOWN = "2"
    LEFT = "4"
    RIGHT = "6"
    UP_LEFT = "7"
    UP_RIGHT = "9"
    DOWN_LEFT = "1"
    DOWN_RIGHT = "3"

class InputState:
    def __init__(self, input_type, value, timestamp):
        self.input_type = input_type
        self.value = value
        self.timestamp = timestamp
        self.consumed = False  # Track if this input has been used in a move

class SpecialMove:
    def __init__(self, name, input_sequence, timing_window=0.5):
        self.name = name
        self.input_sequence = input_sequence  # List of required inputs
        self.timing_window = timing_window    # Time allowed between inputs (seconds)

class InputBuffer:
    def __init__(self, buffer_size=60):  # 60 frame buffer by default
        self.buffer = deque(maxlen=buffer_size)
        self.special_moves = {}  # Dictionary of registered special moves
        self.input_window = 0.5  # Default 500ms window for input sequences
        self.shortcuts = {
            "236": ["2", "3", "6"],  # Quarter circle forward
            "214": ["2", "1", "4"],  # Quarter circle back
            "623": ["6", "2", "3"],  # Dragon punch
            "421": ["4", "2", "1"],  # Dragon punch (reverse)
            "63214": ["6", "3", "2", "1", "4"],  # Half circle back
            "41236": ["4", "1", "2", "3", "6"],  # Half circle forward
            "360": ["6", "3", "2", "1", "4", "7", "8", "9"]  # 360 motion
        }
    
    def add_input(self, input_type, value):
        """Add a new input to the buffer"""
        input_state = InputState(input_type, value, time.time())
        self.buffer.append(input_state)
    
    def register_special_move(self, name, input_sequence, timing_window=None):
        """Register a new special move"""
        if timing_window is None:
            timing_window = self.input_window
            
        # Handle shortcut notation
        expanded_sequence = []
        for input_item in input_sequence:
            if input_item in self.shortcuts:
                expanded_sequence.extend(self.shortcuts[input_item])
            else:
                expanded_sequence.append(input_item)
                
        self.special_moves[name] = SpecialMove(name, expanded_sequence, timing_window)
    
    def check_move(self, move_name):
        """Check if a specific move has been input"""
        if move_name not in self.special_moves:
            return False
            
        move = self.special_moves[move_name]
        sequence = move.input_sequence
        current_time = time.time()
        
        # Convert buffer to list for easier manipulation
        recent_inputs = list(self.buffer)
        sequence_index = len(sequence) - 1
        last_matched_time = current_time
        
        # Work backwards through the buffer
        for input_state in reversed(recent_inputs):
            # Skip if input is too old
            if last_matched_time - input_state.timestamp > move.timing_window:
                return False
                
            # Skip if input was already used
            if input_state.consumed:
                continue
                
            if sequence_index >= 0:
                expected_input = sequence[sequence_index]
                
                # Check if current input matches expected input
                if self._match_input(input_state, expected_input):
                    sequence_index -= 1
                    last_matched_time = input_state.timestamp
                    
                    # Mark input as consumed
                    input_state.consumed = True
                    
                    # If we've matched all inputs, move is complete
                    if sequence_index < 0:
                        return True
                        
        return False
    
    def _match_input(self, input_state, expected):
        """Check if an input matches the expected input"""
        if input_state.input_type == InputType.DIRECTION:
            return input_state.value == Direction[expected].value
        elif input_state.input_type == InputType.BUTTON:
            return input_state.value == expected
        return False
    
    def clear_buffer(self):
        """Clear the input buffer"""
        self.buffer.clear()
    
    def get_last_inputs(self, count=10):
        """Get the last N inputs for display/debug purposes"""
        return list(self.buffer)[-count:]

class FightingGameInput:
    def __init__(self):
        self.buffer = InputBuffer()
        self._setup_default_moves()
    
    def _setup_default_moves(self):
        """Register some common fighting game moves"""
        # Fireball motions
        self.buffer.register_special_move("fireball", ["236", "P"])
        self.buffer.register_special_move("reverse_fireball", ["214", "P"])
        
        # Dragon punch motions
        self.buffer.register_special_move("dragon_punch", ["623", "P"])
        self.buffer.register_special_move("reverse_dragon_punch", ["421", "P"])
        
        # Charge moves (back-forward)
        self.buffer.register_special_move("charge_forward", ["4", "6", "P"], 1.0)
        
        # 360 motion
        self.buffer.register_special_move("spinning_piledriver", ["360", "P"], 0.8)
    
    def process_input(self, input_type, value):
        """Process new input and check for special moves"""
        self.buffer.add_input(input_type, value)
        
        # Check for all registered special moves
        for move_name in self.buffer.special_moves:
            if self.buffer.check_move(move_name):
                return move_name
        
        return None

# EXAMPLE USAGE FOR FIGHTING VIDEO GAMES
"""
game_input = FightingGameInput()

# Add custom move
game_input.buffer.register_special_move("custom_move", ["236", "236", "P"], 0.7)

# Process inputs
game_input.process_input(InputType.DIRECTION, Direction.DOWN.value)
game_input.process_input(InputType.DIRECTION, Direction.DOWN_RIGHT.value)
game_input.process_input(InputType.DIRECTION, Direction.RIGHT.value)
game_input.process_input(InputType.BUTTON, "P")

# Will return "fireball" if inputs were within timing window
"""