# DO NOT ATTEMPT TO IMPORT main.py FROM OUTSIDE OF A FUNCTION OR YOU WILL GET A CIRCULAR IMPORT ISSUE
import handler_gui_layers
import handler_gui_panels
import handler_gui_popups

testing_coroutine_maximum = 6

def alertUser (input_message):
    popup_alert.elements[0].text = input_message
    popTo("alert")

def create_allLayers ():
    global layer_main_menu, layer_game, layer_fades, layer_loading
    layer_main_menu = handler_gui_layers.layer_main_menu_root()
    layer_game = handler_gui_layers.layer_game()
    layer_fades = handler_gui_layers.layer_fades()
    layer_loading = handler_gui_layers.layer_loading()
    # BUILD THE LAYERS GROUP
    global layers
    layers = handler_gui_layers.Layers()
    layers.element_add(layer_game)
    layers.element_add(layer_fades)
    layers.element_add(layer_main_menu)
    layers.element_add(layer_loading)
    layers.draw(thisWindow.get_window())

def create_allPanels ():
    # Create panel instances
    global panel_left, panel_right, panel_top, panel_bottom
    panel_left = handler_gui_panels.panel_sidebar_left()
    panel_right = handler_gui_panels.panel_sidebar_right()
    panel_top = handler_gui_panels.panel_toolbar_top()
    panel_bottom = handler_gui_panels.panel_status_bottom()

    # Initialize global panels group
    global panels
    panels = handler_gui_panels.Panels(200)  # Default offset
    panels.element_add(panel_left)
    panels.element_add(panel_right)
    panels.element_add(panel_top)
    panels.element_add(panel_bottom)
    
    # Initial draw
    panels.draw(thisWindow.get_window())

def create_allPopups ():
    global popup_alert, popup_gameover, popup_prompt
    # Create alert popup for general messages
    popup_alert = handler_gui_popups.popup_alert(
        "Alert",
        "This is an alert message"
    )
    
    # Create game over popup
    popup_gameover = handler_gui_popups.popup_gameover(
        "Game Over",
        "Game over reason will be set when shown"
    )
    
    # Create yes/no prompt popup
    popup_prompt = handler_gui_popups.popup_prompt(
        "Prompt",
        "Prompt question will be set when shown"
    )

    # Initialize global popups group
    global popups
    popups = handler_gui_popups.Popups()
    popups.element_add(popup_alert)
    popups.element_add(popup_gameover)
    popups.element_add(popup_prompt)
    
    # Initial draw
    popups.draw(thisWindow.get_window())

def create_allFolders ():
    import os
    temp_directoriesToCheck = ["saves", "audio", "dialog"]
    for directory in temp_directoriesToCheck:
        if not os.path.exists(directory):
            os.makedirs(directory)

def create_application():
    # ESTABLISH A REFERENCE TO THE WINDOW
    global thisWindow
    import handler_window
    thisWindow = handler_window.WindowHandler("Title of Game as Seen in Window Title")

def hideAll (input_which):
    match input_which:
        case "navTo":
            for layer in layers.elements:
                layer.hide()
        case "panelTo":
            for panel in panels.elements:
                panel.hide()
        case "popTo":
            for popup in popups.elements:
                popup.hide()

def navTo (input_which):
    hideAll("navTo")
    hideAll("panelTo")
    hideAll("popTo")
    match input_which:
        case "loading":
            layer_loading.show()
        case "fader":
            layer_fades.show()
        case "game":
            layer_game.show()
        case _:
            layer_main_menu.show()

def panelTo (input_which):
    hideAll("panelTo")
    match input_which:
        case "left":
            panel_left.show()
        case "right":
            panel_right.show()
        case "top":
            panel_top.show()
        case "bottom":
            panel_bottom.show()
        case _:
            alertUser ("Unknown panelTo request:", input_which)

def popTo (input_which):
    hideAll("popTo")
    match input_which:
        case "alert":
            popup_alert.show()
        case "gameover":
            popup_gameover.show()
        case "prompt":
            popup_prompt.show()

def processActionByID (input_actionCode):
    match input_actionCode:
        case "New Game":
            print("processActionByID: New Game")
            navTo("game")
        case "Exit":
            print("processActionByID: Exit")
            from main import exit
            exit()
        case _:
            alertUser ("Unknown action ID in proecessActionByID:", input_actionCode)
            navTo("mm") # WHEN IN DOUBT, RETURN TO MAIN MENU

def update_coroutine_1sec ():
    # THIS IS A TEST OF THE COROUTINE
    # YOU CAN DELETE THE CURRENT CONTENTS BUT LEAVE THE FUNCTION
    # YOU CAN ALSO DELETE THE VARIABLE "testing_coroutine_maximum" AT THE TOP OF THIS MODULE
    # THIS TEST CLOSES THE WINDOW AFTER SIX SECONDS
    global testing_coroutine_maximum
    testing_coroutine_maximum -= 1
    if testing_coroutine_maximum < 0:
        import main
        processActionByID("Exit")
    print("testing coroutine_maximum = " + str(testing_coroutine_maximum))

