from enum import Enum, auto
from handler_gui_layers import layer_fades

# NOTE: THIS FILE CONTROLS THE FUNCTIONALITY OF layer_fades INSIDE OF hanlder_gui_layers

class FadeState(Enum):
    INACTIVE = auto()
    FADING_IN = auto()
    FADING_OUT = auto()

class FadeHandler:
    def __init__(self):
        self.fade_layer = layer_fades()
        self.state = FadeState.INACTIVE
        self.frame_counter = 0
        self.TOTAL_FRAMES = 100  # Exactly 100 frames for fade
        
    def begin_fade_in(self):
        """Start fading in from transparent to opaque"""
        self.state = FadeState.FADING_IN
        self.frame_counter = 0
        self.fade_layer.show()
        self.fade_layer.set_fade_alpha(0)  # Start fully transparent
        
    def begin_fade_out(self):
        """Start fading out from opaque to transparent"""
        self.state = FadeState.FADING_OUT
        self.frame_counter = 0
        self.fade_layer.show()
        self.fade_layer.set_fade_alpha(100)  # Start fully opaque
    
    def update(self) -> bool:
        """
        Update fade transition. Returns True if fade is complete.
        Should be called once per frame.
        """
        if self.state == FadeState.INACTIVE:
            return True
            
        self.frame_counter += 1
        
        if self.state == FadeState.FADING_IN:
            # Calculate alpha (0 to 100 over 100 frames)
            alpha = int((self.frame_counter / self.TOTAL_FRAMES) * 100)
            self.fade_layer.set_fade_alpha(alpha)
            
            if self.frame_counter >= self.TOTAL_FRAMES:
                self.fade_layer.set_fade_alpha(100)  # Ensure we end at fully opaque
                self.state = FadeState.INACTIVE
                return True
                
        elif self.state == FadeState.FADING_OUT:
            # Calculate alpha (100 to 0 over 100 frames)
            alpha = int(100 - (self.frame_counter / self.TOTAL_FRAMES) * 100)
            self.fade_layer.set_fade_alpha(alpha)
            
            if self.frame_counter >= self.TOTAL_FRAMES:
                self.fade_layer.set_fade_alpha(0)  # Ensure we end at fully transparent
                self.fade_layer.hide()  # Hide the layer when fully transparent
                self.state = FadeState.INACTIVE
                return True
                
        return False
    
    def is_fading(self) -> bool:
        """Return True if currently in a fade transition"""
        return self.state != FadeState.INACTIVE

# Global fade handler instance
fade_handler = None

def get_fade_handler() -> FadeHandler:
    """Get the global fade handler instance"""
    global fade_handler
    if fade_handler is None:
        fade_handler = FadeHandler()
    return fade_handler