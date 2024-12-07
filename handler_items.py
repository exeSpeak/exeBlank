import handler_vars
import random

list_premadeItems = list()

itemNames_all_byType = (
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

def returnItemCodeFromInt (input_itemInt):
    if not (0 <= input_itemInt <= 675):  # 26*26 - 1 = 675 (AA to ZZ)
        return None
    
    first_letter = chr(ord('A') + (input_itemInt // 26))
    second_letter = chr(ord('A') + (input_itemInt % 26))
    return first_letter + second_letter

def returnIntFromItemCode (input_itemCode):
	first_letter = ord(input_itemCode[0]) - ord('A')
	second_letter = ord(input_itemCode[1]) - ord('A')
	return (first_letter * 26) + second_letter

def returnItemStringFromIntList (input_intList):
    result = ""
    for num in input_intList:
        code = returnItemCodeFromInt(num)
        if code:  # Only add the code if it's valid
            result += code
    return result

def returnIntArrayFromItemString (input_itemString):
    result = []
    # Process string in pairs of 2 characters
    for i in range(0, len(input_itemString), 2):
        if i + 1 < len(input_itemString):  # Ensure we have 2 characters
            code = input_itemString[i:i+2]
            num = returnIntFromItemCode(code)
            result.append(num)
    return result

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
	temp_outputString = returnItemStringFromIntList(temp_buffs)
	return temp_outputString

def returnBlendedItem (input_item1, input_item2):
    # Ensure both strings have even length by padding with 'A' if needed
    if len(input_item1) % 2 != 0:
        input_item1 += 'A'
    if len(input_item2) % 2 != 0:
        input_item2 += 'A'
    max_pairs = max(len(input_item1) // 2, len(input_item2) // 2)
    input_item1 = input_item1.ljust(max_pairs * 2, 'A')
    input_item2 = input_item2.ljust(max_pairs * 2, 'A')
    
    # Split strings into pairs of characters
    pairs1 = [input_item1[i:i+2] for i in range(0, len(input_item1), 2)]
    pairs2 = [input_item2[i:i+2] for i in range(0, len(input_item2), 2)]
    
    # Create new blended item string
    blended_pairs = []
    for i in range(len(pairs1)):
        # For each position, randomly choose between item1 and item2's code
        if random.random() < 0.5:
            blended_pairs.append(pairs1[i])
        else:
            blended_pairs.append(pairs2[i])
    
    # Join all pairs back into a single string
    return ''.join(blended_pairs)

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
