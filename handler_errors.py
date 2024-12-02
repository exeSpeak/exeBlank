import handler_game

def checkForError (inputType = ""):
	match inputType:
		case "InvalidInputType":
			print("Error 0: Invalid input type")
		case "InvalidInputValue":
			print("Error 1: Invalid input value")
		case "InvalidInputSequence":
			print("Error 2: Invalid input sequence")
		case _:
			print("Requested error type given to checkForError does not exist")
