import handler_game

def checkForError (inputType = "", inputSpecific = ""):
	temp_errorExplanation = "Requested error type", inputType, " given to checkForError does not exist"
	match inputType:
		case "InvalidInputType":
			temp_errorExplanation = "Invalid input type"
		case "InvalidInputValue":
			temp_errorExplanation = "Invalid input value"
		case "InvalidInputSequence":
			temp_errorExplanation = "Invalid input sequence"
	
	# TWO TYPES OF FEEDBACK IN CASE DEVELOPER IS USING A TERMINAL
	handler_game.alertUser (temp_errorExplanation)
	print(temp_errorExplanation)
