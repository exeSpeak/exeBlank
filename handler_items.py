import handler_vars

list_premadeItems = list()

itemNames_type = (
	"currency",
	"ore",
	"weapon",
	"armor"
)

itemNames_currency = (
	"gold",
	"scrap"
)

itemNames_ore = (
	"aluminum",
	"bronze",
	"iron",
	"steel",
	"onyx",
	"diamond"
)

itemNames_weapon = (
	"sword",
	"dagger",
	"bow"
)

itemNames_armor = (
	"helmet",
	"chest",
	"legs",
	"gloves",
	"boots"
)

def generatePremadeItemList (input_numberOfItemsToBuild):
	list_premadeItems.clear()
	temp_currentLevel = handler_vars.returnVar("player_level")
	for x in range(input_numberOfItemsToBuild):
		list_premadeItems.append(returnNewItem(temp_currentLevel))

def convertItemStringToArray (input_itemString):
	pass

def convertArrayToItemString (input_itemType, input_buffArray):
	pass

def returnNewItem (input_level):
	temp_whichItemType = returnRandomItemType()
	temp_buffs = [0,0,0,0,0,0]
	temp_pointsRemaining = input_level
	temp_indexOfBuffToIncrease = 0
	while temp_pointsRemaining > 0:
		temptemp_pointsToDistribute = returnNonZeroRandom(temp_pointsRemaining)
		temp_pointsRemaining -= temptemp_pointsToDistribute
		temp_buffs[temp_indexOfBuffToIncrease] += temptemp_pointsToDistribute
		temp_indexOfBuffToIncrease += 1
		if temp_indexOfBuffToIncrease > 5: temp_buffToIncrease = 0
	temp_outputString = convertToItemString(temp_whichItemType, temp_buffs)
	return temp_outputString

def returnRandomItemType ():
	tempRandom = 100
	match tempRandom:
		case _ if tempRandom < 14:
			return "armor"
		case _ if tempRandom < 34:
			return "ore"
		case _ if tempRandom < 54:
			return "weapon"
		case _:
			return "currency"

def returnNonZeroRandom (input_maximumInt):
	if input_maximumInt < 5: return input_maximumInt # If we allow anything less than 5, there is a huge hit to performance when mulitple items drop. For instance, imagine a series of 99 unlucky rolls of "1".
	return random.randrange(5, input_maximumInt)
