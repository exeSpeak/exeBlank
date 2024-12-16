import handler_game
import handler_vars
from handler_input import EventManager, InputPriority, InputEvent, InputSource
from handler_observer import EventSubject, GameObserver, ObserverPriority
import handler_gui_sizing
import time
import pygame

global flag_isRunningApplication
flag_isRunningApplication = True

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

class GameTimer:
    def __init__(self, input_interval):
        self.last_update = time.time()
        self.input_interval = input_interval
    
    def returnReadyAsBool(self):
        current_time = time.time()
        if current_time - self.last_update >= self.input_interval:
            self.last_update = current_time
            return True
        return False

class InputMapper:
    def __init__(self):
        self.mappings = {
            'new_game': [pygame.K_n, pygame.JOYBUTTONDOWN],
            'exit': [pygame.K_ESCAPE, pygame.JOYBUTTONDOWN]
        }

def start():
    # NOTE: THIS CALL TO CREATE THE APPLICATION ABSOLLUTELY MUST COME FIRST
    # Initialize core application handlers
    handler_game.create_application()
    
    # Initialize GUI sizing system and force initial cache update; this is important to make sure the game changes distances based on the current window size
    handler_gui_sizing.init_sizing(handler_game.thisWindow)
    sizing = handler_gui_sizing.get_sizing()
    sizing.update_cache()  # Force initial calculation of all relative GUI values
    
    # Initialize event system for input from keyboard, joystick, and mouse
    global event_manager, event_subject, game_controller
    event_manager = EventManager()
    event_subject = EventSubject()
    game_controller = GameController(event_subject)
    create_default_mappings()
    
    # Initialize game state
    flag_isRunningApplication = True
    handler_vars.clear_appStart() # this is different than the "clear" we do at the start of a new game

    # Initialize coroutine that runs once per second
    global timer_coroutine_1sec
    timer_coroutine_1sec = GameTimer(1.0)
    
    # Create game elements
    handler_game.create_allLayers()
    handler_game.create_allPanels()
    handler_game.create_allPopups()
    handler_game.create_allFolders()
    handler_game.navTo("mm")

def update():
    global flag_isRunningApplication
    if flag_isRunningApplication == False:
        pygame.quit()
        return

    global timer_coroutine_1sec # keep this outside of "while" loop
    clock = pygame.time.Clock()
    
    while flag_isRunningApplication:
        # Process all events
        handle_events(handler_game.thisWindow)
        
        # ONCE PER SECOND, RUN A COROUTINE
        # YOU CAN DELETE THIS (AND THE GLOBAL DECLARATION ABOVE), HOWEVER NO MATTER HOW SMALL THE GAME
        # IT IS BETTER TO PROCESS UNIMPORTANT CALCULATIONS LESS FREQUENTLY
        if timer_coroutine_1sec.returnReadyAsBool() == True:
            handler_game.update_coroutine_1sec()

        # Update display
        handler_game.thisWindow.clear_screen((0, 0, 0))  # Clear screen with black color
        handler_game.thisWindow.update_display()

        # Maintain consistent frame rate of 60 FPS
        clock.tick(60)

def create_menubar():
    handler_game.thisWindow.set_menu_bar(True)
    handler_game.thisWindow.add_menu("File", [
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

def exit ():
    print("flag_isRunningApplication set to false by exit() in main")
    global flag_isRunningApplication
    flag_isRunningApplication = False
    pygame.quit()

def handle_events(self):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            self.endProgram()
        elif event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)
            handler_gui_sizing.get_sizing().update_cache()
            handler_game.create_allLayers()  # Recreate layers with new dimensions
            handler_game.create_allPanels()  # Recreate panels with new dimensions
        elif self.menu_bar:
            self.menu_bar.handle_event(event)
    return events  # Return all events

def handle_game_input(event):
    """Central function to handle all game-related inputs"""
    if event.event_type == "keydown":
        if event.data["key"] == pygame.K_n:
            print("n key pressed prior to processActionByID")
            handler_game.processActionByID("New Game")
        if event.data["key"] == pygame.K_ESCAPE:
            print("escape key pressed prior to processActionByID")
            handler_game.processActionByID("Exit")
    
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

# THIS FUNCTION READS THE SETTINGS IN main_customize.py AND SETS THE VARIABLES
def parse_customization_file():
    for entry in main_customize.thisgame_application:
        key, value = entry.split("::")
        handler_vars.set(key, value)

if __name__ == "__main__":
    start()
    if flag_isRunningApplication == True:
        update()
