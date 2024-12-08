import handler_gui_layers
import handler_gui_panels
import handler_gui_popups

def alertUser (input_message):
    popup_alert.elements[0].text = input_message
    popTo("alert")

def create_allLayers ():
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
    layers.draw(window_handler.get_window())

def create_allPanels ():
    # Create panel instances
    panel_left = handler_gui_panels.panel_sidebar_left()
    panel_right = handler_gui_panels.panel_sidebar_right()
    panel_top = handler_gui_panels.panel_toolbar_top()
    panel_bottom = handler_gui_panels.panel_status_bottom()

    # Initialize global panels group
    global panels, panel_left, panel_right, panel_top, panel_bottom
    panels = handler_gui_panels.Panels(200)  # Default offset
    panels.element_add(panel_left)
    panels.element_add(panel_right)
    panels.element_add(panel_top)
    panels.element_add(panel_bottom)
    
    # Initial draw
    panels.draw(window_handler.get_window())

def create_allPopups ():
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
    global popups, popup_alert, popup_gameover, popup_prompt
    popups = handler_gui_popups.Popups(window_handler.get_window())
    popups.add_element(popup_alert)
    popups.add_element(popup_gameover)
    popups.add_element(popup_prompt)
    
    # Initial draw
    popups.draw(window_handler.get_window())

def create_allFolders ():
    import os
    temp_directoriesToCheck = ["saves", "audio", "dialog"]
    for directory in temp_directoriesToCheck:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
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

def processButtonClick (input_buttonID):
    match input_buttonID:
        case "New Game":
            navTo("game")
        case "Exit":
            import main
            main.exit()
        case _:
            alertUser ("Unknown button ID in proecessButtonClick:", input_buttonID)
            navTo("mm") # WHEN IN DOUBT, RETURN TO MAIN MENU
