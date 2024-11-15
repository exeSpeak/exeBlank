import socket
import json
import time
import threading
from collections import deque
from enum import Enum, auto

class NetworkRole(Enum):
    HOST = auto()
    CLIENT = auto()
    SPECTATOR = auto()

class InputState:
    def __init__(self, player_id, frame_number, inputs, timestamp):
        self.player_id = player_id
        self.frame_number = frame_number
        self.inputs = inputs
        self.timestamp = timestamp
        self.confirmed = False

class NetworkInputHandler:
    def __init__(self, host="localhost", port=5000, role=NetworkRole.HOST):
        self.role = role
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.current_frame = 0
        self.input_delay = 2  # Frames of input delay for rollback
        self.max_rollback = 7  # Maximum frames to roll back
        
        # Input buffers for each player
        self.input_buffers = {}  # player_id -> deque of InputState
        self.prediction_buffer = deque(maxlen=60)  # Store predicted inputs
        self.confirmed_inputs = deque(maxlen=120)  # Store confirmed inputs
        
        # Synchronization
        self.sync_interval = 60  # Frames between full state sync
        self.last_sync_frame = 0
        
        # Initialize networking
        self._init_network()
    
    def _init_network(self):
        """Initialize network socket based on role"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.role == NetworkRole.HOST:
            self.socket.bind((self.host, self.port))
            self._start_host_listener()
        else:
            self._start_client_listener()
    
    def _start_host_listener(self):
        """Start listening thread for host"""
        def listen():
            while self.connected:
                try:
                    data, addr = self.socket.recvfrom(1024)
                    self._handle_incoming_data(data, addr)
                except:
                    pass
        
        self.listen_thread = threading.Thread(target=listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def _start_client_listener(self):
        """Start listening thread for client"""
        def listen():
            while self.connected:
                try:
                    data = self.socket.recv(1024)
                    self._handle_incoming_data(data)
                except:
                    pass
        
        self.listen_thread = threading.Thread(target=listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def connect(self, player_id):
        """Connect to game session"""
        self.player_id = player_id
        self.connected = True
        self.input_buffers[player_id] = deque(maxlen=120)
        
        # Send initial connection message
        msg = {
            "type": "connect",
            "player_id": player_id,
            "frame": self.current_frame
        }
        self._send_message(msg)
    
    def disconnect(self):
        """Disconnect from game session"""
        self.connected = False
        msg = {
            "type": "disconnect",
            "player_id": self.player_id
        }
        self._send_message(msg)
        self.socket.close()
    
    def add_local_input(self, inputs):
        """Add local player input to buffer and send to network"""
        input_state = InputState(
            self.player_id,
            self.current_frame,
            inputs,
            time.time()
        )
        
        # Add to local buffer
        self.input_buffers[self.player_id].append(input_state)
        
        # Send to network
        msg = {
            "type": "input",
            "player_id": self.player_id,
            "frame": self.current_frame,
            "inputs": inputs,
            "timestamp": input_state.timestamp
        }
        self._send_message(msg)
    
    def predict_remote_input(self, player_id):
        """Predict input for remote player"""
        if player_id not in self.input_buffers:
            return None
            
        buffer = self.input_buffers[player_id]
        if not buffer:
            return None
            
        # Simple prediction: use last known input
        last_input = buffer[-1]
        predicted = InputState(
            player_id,
            self.current_frame,
            last_input.inputs,
            time.time()
        )
        self.prediction_buffer.append(predicted)
        return predicted
    
    def confirm_input(self, player_id, frame, inputs):
        """Confirm actual input from network"""
        if player_id not in self.input_buffers:
            return
            
        # Find and confirm the input
        for input_state in self.input_buffers[player_id]:
            if input_state.frame_number == frame:
                input_state.confirmed = True
                input_state.inputs = inputs
                self.confirmed_inputs.append(input_state)
                break
    
    def check_rollback(self):
        """Check if rollback is needed"""
        rollback_frame = None
        
        # Check confirmed inputs against predictions
        for confirmed in self.confirmed_inputs:
            for predicted in self.prediction_buffer:
                if (confirmed.player_id == predicted.player_id and
                    confirmed.frame_number == predicted.frame_number and
                    confirmed.inputs != predicted.inputs):
                    rollback_frame = confirmed.frame_number
                    break
            if rollback_frame:
                break
        
        return rollback_frame
    
    def _handle_incoming_data(self, data, addr=None):
        """Handle incoming network data"""
        try:
            msg = json.loads(data.decode())
            msg_type = msg.get("type")
            
            if msg_type == "connect":
                player_id = msg["player_id"]
                self.input_buffers[player_id] = deque(maxlen=120)
                
            elif msg_type == "disconnect":
                player_id = msg["player_id"]
                if player_id in self.input_buffers:
                    del self.input_buffers[player_id]
                    
            elif msg_type == "input":
                player_id = msg["player_id"]
                frame = msg["frame"]
                inputs = msg["inputs"]
                self.confirm_input(player_id, frame, inputs)
                
            elif msg_type == "sync":
                self._handle_sync(msg)
                
        except json.JSONDecodeError:
            pass
    
    def _handle_sync(self, msg):
        """Handle full state synchronization"""
        if msg["frame"] > self.last_sync_frame:
            self.last_sync_frame = msg["frame"]
            # Here you would typically sync the full game state
            # This is game-specific and should be implemented by the game
    
    def _send_message(self, msg):
        """Send message to network"""
        try:
            data = json.dumps(msg).encode()
            if self.role == NetworkRole.HOST:
                # Broadcast to all clients
                # In a real implementation, you'd maintain a list of client addresses
                pass
            else:
                self.socket.sendto(data, (self.host, self.port))
        except:
            pass

# EXAMPLE USAGE FOR MULTIPLAYER GAMES
"""
# Host
host = NetworkInputHandler(role=NetworkRole.HOST)
host.connect(player_id=1)

# Client
client = NetworkInputHandler(role=NetworkRole.CLIENT)
client.connect(player_id=2)

# Game loop
def game_loop():
    # Add local input
    local_input = get_local_input()  # Your input gathering code
    network.add_local_input(local_input)
    
    # Predict remote input if needed
    remote_input = network.predict_remote_input(remote_player_id)
    
    # Check for rollback
    rollback_frame = network.check_rollback()
    if rollback_frame is not None:
        rollback_to_frame(rollback_frame)  # Your rollback code
    
    # Process frame
    process_game_frame(local_input, remote_input)
"""