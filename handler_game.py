import handler_gui_layers
import handler_gui_panels
import handler_gui_popups

def alertUser (input_message):
    popup_alert.updateMessage(input_message)

def create_allLayers ():
    layers = handler_gui_layers.Layers(window_handler.get_window())
    layer_main_menu = handler_gui_layers.layer_main_menu_root()
    layers.add_element(layer_main_menu)
    layer_game = handler_gui_layers.layer_game()
    layers.add_element(layer_game)
    layers.draw(window_handler.get_window())

def create_allPanels ():
    panels = handler_gui_panels.Panels(window_handler.get_window())
    panels.draw(window_handler.get_window())

def create_allPopups ():
    popups = handler_gui_popups.Popups(window_handler.get_window())
    popup_alert = handler_gui_popups.popup_alert("Alert", "This is an alert message")
    popups.add_element(popup_alert)
    popups.draw(window_handler.get_window())

def create_allFolders ():
    import os
    if not os.path.exists("saves"):
        os.makedirs("saves")
        
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

def hideAllLayers ():
    for layer in layers.elements:
        layer.hide()

def navTo (input_which):
    hideAll("navTo")
    hideAll("panelTo")
    match input_which:
        case "game":
            layer_game.show()
        case _:
            layer_main_menu.show()

def panelTo (input_which):
    hideAll("panelTo")

def popTo (input_which):
    hideAll("popTo")

def processButtonClick (input_buttonID):
    match input_buttonID:
        case "New Game":
            navTo("game")
        case "Exit":
            import main
            main.exit()
        case _:
            navTo("mm") # WHEN IN DOUBT, RETURN TO MAIN MENU
