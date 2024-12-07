import handler_vars
import handler_npc

# Global lists to track different NPC groups
list_activeCompanions = []
list_activeFriendlies = []
list_activeEnemies = []
list_activeBosses = []
list_deadNPCs = []

def generatePremadeCompanionsList():
    """Generate predefined companion NPCs"""
    pass

def generatePremadeFriendlyList():
    """Generate predefined friendly NPCs"""
    pass

def generatePremadeEnemiesList():
    """Generate predefined enemy NPCs"""
    pass

def generatePremadeBossList():
    """Generate predefined boss NPCs"""
    pass

def addNPCToGroup(npc, group_type):
    """Add an NPC to the appropriate group list"""
    if group_type == "companion":
        list_activeCompanions.append(npc)
    elif group_type == "friendly":
        list_activeFriendlies.append(npc)
    elif group_type == "enemy":
        list_activeEnemies.append(npc)
    elif group_type == "boss":
        list_activeBosses.append(npc)

def removeNPCFromGroup(npc, group_type):
    """Remove an NPC from its group list"""
    if group_type == "companion":
        list_activeCompanions.remove(npc)
    elif group_type == "friendly":
        list_activeFriendlies.remove(npc)
    elif group_type == "enemy":
        list_activeEnemies.remove(npc)
    elif group_type == "boss":
        list_activeBosses.remove(npc)

def handleNPCDeath(npc, group_type):
    """Handle NPC death - remove from active group and add to dead list"""
    removeNPCFromGroup(npc, group_type)
    list_deadNPCs.append(npc)

def updateAllNPCs():
    """Update all active NPCs' states and status effects"""
    all_npcs = (list_activeCompanions + list_activeFriendlies + 
                list_activeEnemies + list_activeBosses)
    for npc in all_npcs:
        if npc.return_amIDead():
            handleNPCDeath(npc, determineNPCGroup(npc))
        # Update status effects durations
        if npc.flag_isPoisoned > 0:
            npc.flag_isPoisoned -= 1
        if npc.flag_isStunned > 0:
            npc.flag_isStunned -= 1
        if npc.flag_isBurning > 0:
            npc.flag_isBurning -= 1
        if npc.flag_isFrozen > 0:
            npc.flag_isFrozen -= 1

def determineNPCGroup(npc):
    """Determine which group an NPC belongs to"""
    if npc in list_activeCompanions:
        return "companion"
    elif npc in list_activeFriendlies:
        return "friendly"
    elif npc in list_activeEnemies:
        return "enemy"
    elif npc in list_activeBosses:
        return "boss"
    return None

def getActivePartySize():
    """Return the number of active companions"""
    return len(list_activeCompanions)

def getActiveEnemiesInRange(source_npc, range_distance):
    """Return list of enemies within specified range of source_npc"""
    nearby_enemies = []
    for enemy in list_activeEnemies + list_activeBosses:
        # Distance calculation would go here
        # For now, just return all enemies
        nearby_enemies.append(enemy)
    return nearby_enemies

def getFriendliesInRange(source_npc, range_distance):
    """Return list of friendlies within specified range of source_npc"""
    nearby_friendlies = []
    for friendly in list_activeCompanions + list_activeFriendlies:
        # Distance calculation would go here
        # For now, just return all friendlies
        nearby_friendlies.append(friendly)
    return nearby_friendlies

def resurrectNPC(npc):
    """Attempt to resurrect a dead NPC"""
    if npc in list_deadNPCs:
        list_deadNPCs.remove(npc)
        npc.stat_hp = npc.stat_hp_max // 2  # Resurrect with half HP
        addNPCToGroup(npc, determineNPCGroup(npc))
        return True
    return False

def applyGroupEffect(group_type, effect_type, duration):
    """Apply a status effect to all NPCs in a specified group"""
    target_list = []
    if group_type == "companion":
        target_list = list_activeCompanions
    elif group_type == "friendly":
        target_list = list_activeFriendlies
    elif group_type == "enemy":
        target_list = list_activeEnemies
    elif group_type == "boss":
        target_list = list_activeBosses
    
    for npc in target_list:
        npc.affectMe(effect_type, duration)

def getGroupHealth(group_type):
    """Return the average health percentage of a group"""
    target_list = []
    if group_type == "companion":
        target_list = list_activeCompanions
    elif group_type == "friendly":
        target_list = list_activeFriendlies
    elif group_type == "enemy":
        target_list = list_activeEnemies
    elif group_type == "boss":
        target_list = list_activeBosses
    
    if not target_list:
        return 0
    
    total_health_percent = sum(npc.stat_hp / npc.stat_hp_max * 100 for npc in target_list)
    return total_health_percent / len(target_list)
