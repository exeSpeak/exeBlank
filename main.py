import handler_game
import handler_vars
from handler_window import WindowHandler
from handler_input import EventManager, InputPriority, InputEvent, InputSource
from handler_observer import EventSubject, GameObserver, ObserverPriority
import handler_gui_sizing
import pygame

class GameController(GameObserver):
    """Main game controller that handles core application events"""
    def __init__(self, event_subject):
        super().__init__()
        self.observe(
            event_subject,
            self.handle_system_events,
            ["keydown", "quit"],
            ObserverPriority.CRITICAL
        )
    
    def handle_system_events(self, event):
        global running
        if event.event_type == "quit":
            running = False
        elif event.event_type == "keydown" and event.data["key"] == pygame.K_ESCAPE:
            running = False

def start():
    global window_handler, event_manager, event_subject, game_controller, running, time_coroutine
    
    # Initialize core handlers
    window_handler = WindowHandler("My Game Window")
    handler_gui_sizing.init_sizing(window_handler)
    
    # Initialize event system for input from keyboard, joystick, and mouse
    event_manager = EventManager()
    event_subject = EventSubject()
    game_controller = GameController(event_subject)
    create_default_mappings()
    
    # Initialize game state
    running = True
    handler_vars.clear() # this is different than the "clear" we do at the start of a new game

    # Initialize coroutine
    timer_coroutine = coroutine_1sec()
    next(timer_coroutine) # Prime the coroutine
    
    # Create game elements
    handler_game.create_allLayers()
    handler_game.create_allPanels()
    handler_game.create_allPopups()
    handler_game.create_allFolders()
    handler_game.navTo("mm")

def update():
    global running, timer_coroutine
    clock = pygame.time.Clock()
    
    while running:
        # Process all events
        events = window_handler.handle_events()
        if events: 
            elapsed = event_manager.process_events()
            for event in event_manager.get_frame_events():
                event_subject.notify(event)
        
        # Get time from coroutine
        current_time = next(timer_coroutine)
        
        # Update display
        window_handler.clear_screen((0, 0, 0))  # Clear screen with black color
        window_handler.update_display()
        
        # Maintain consistent frame rate of 60 FPS
        clock.tick(60)

def coroutine_1sec():
    import time
    while True:
        yield time.time()
        yield from coroutine_1sec()

def create_menubar():
    window_handler.set_menu_bar(True)
    window_handler.add_menu("File", [
        ("New", lambda: event_subject.notify(InputEvent(
            InputSource.KEYBOARD, "menu", {"action": "new_game"}
        ))),
        ("Exit", lambda: exit())
    ])

def create_default_mappings():
    """Set up default input mappings for keyboard, joystick, and mouse"""
    # Register high-priority system callbacks
    event_manager.register_callback(
        "quit",
        lambda e: setattr(__builtins__, "running", False),
        InputPriority.HIGH
    )
    
    # Register standard game callbacks
    event_manager.register_callback(
        "keydown",
        lambda e: handle_game_input(e),
        InputPriority.NORMAL
    )
    
    event_manager.register_callback(
        "button_down",
        lambda e: handle_game_input(e),
        InputPriority.NORMAL
    )
    
    event_manager.register_callback(
        "mouse_down",
        lambda e: handle_game_input(e),
        InputPriority.NORMAL
    )

def handle_game_input(event):
    """Central function to handle all game-related inputs"""
    if event.event_type == "keydown":
        if event.data["key"] == pygame.K_n:
            event_subject.notify(InputEvent(
                InputSource.KEYBOARD, "action", {"command": "new_game"}
            ))
    
    elif event.event_type == "button_down":
        if event.data["button"] == 0:  # A/Cross button
            event_subject.notify(InputEvent(
                InputSource.JOYSTICK, "action", {"command": "new_game"}
            ))
        elif event.data["button"] == 1:  # B/Circle button
            event_subject.notify(InputEvent(
                InputSource.JOYSTICK, "action", {"command": "exit"}
            ))
    
    elif event.event_type == "mouse_down":
        if event.data["button"] == 1:  # Left click
            event_subject.notify(InputEvent(
                InputSource.MOUSE, "action", {"command": "select"}
            ))
        elif event.data["button"] == 3:  # Right click
            event_subject.notify(InputEvent(
                InputSource.MOUSE, "action", {"command": "menu"}
            ))

def exit():
    global running
    running = False
    pygame.quit()

if __name__ == "__main__":
    start()
    if running:
        update()
        coroutine_1sec()
    if not running:
        window_handler.exit()