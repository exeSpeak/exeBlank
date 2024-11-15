vars_ints = []
vars_names = []

vars_group_app = ["savegameloc"]
vars_group_01 = ["01_first", "01_last"]
vars_group_02 = ["02_first", "02_last"]
vars_group_currency = ["gold", "ore"]

def combine_groups ():
    global vars_names
    vars_names = vars_group_app + vars_group_01 + vars_group_02 + vars_group_currency

def setup_ints ():
    combine_groups()
    vars_ints = [0] * len(vars_names)

def clear ():
    setup_ints()
    vars_setMe("savegameloc", returnNextSaveFileID())
    # THIS IS WHERE YOU CAN MANUALLY SET THE DEFAULT VALUES AT THE START OF THE PROGRAM

def clear_newGame ():
    setup_ints()
    vars_setMe("savegameloc", returnNextSaveFileID())
    # THIS IS WHERE YOU CAN MANUALLY SET THE DEFAULT VALUES AT THE START OF A NEW GAME

def returnVarNameIndex (input_variableName):
    if input_variableName not in vars_names:
        return -1
    return vars_names.index(input_variableName)

def returnNextSaveFileID ():
    import os
    if not os.path.exists('saves'):
        os.makedirs('saves')
    files = os.listdir('saves')
    if len(files) == 0:
        return 0
    return max(int(x.split('.')[0]) for x in files)

def vars_addMe (input_which, input_additive):
    temp = returnVarNameIndex(input_which)
    if temp == -1:
        return
    vars_ints[temp] += input_additive

def vars_setMe (input_which, input_newValue):
    temp = returnVarNameIndex(input_which)
    if temp == -1:
        return
    vars_ints[temp] = input_newValue

def vars_getMe (input_which):
    temp = returnVarNameIndex(input_which)
    if temp == -1:
        return -1
    return vars_ints[temp]

def saveAllVars():
    import os
    if not os.path.exists('saves'):
        os.makedirs('saves')
    save_string = '|*|'.join(str(x) for x in vars_ints)
    with open('saves/save.sav', 'w') as f:
        f.write(save_string)

def loadAllVars():
    global vars_ints
    import os
    if os.path.exists('saves/save.sav'):
        with open('saves/save.sav', 'r') as f:
            save_string = f.read()
            if save_string:
                vars_ints = [int(x) for x in save_string.split('|*|')]
