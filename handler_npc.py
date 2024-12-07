import handler_vars

class npcObject:
    def __init__(self):
        self.stat_hp = 100
        self.stat_hp_max = 100
        self.stat_mp = 0
        self.stat_mp_max = 0
        self.model_idnum = 0
        self.flag_isAwake = False
        self.flag_isPoisoned = 0 # INT > 0 IS THE NUMBER OF REMAINING SECONDS OF POISON
        self.flag_isStunned = 0 # INT > 0 IS THE NUMBER OF REMAINING SECONDS OF STUN
        self.flag_isBurning = 0 # INT > 0 IS THE NUMBER OF REMAINING SECONDS OF BURNING
        self.flag_isFrozen = 0 # INT > 0 IS THE NUMBER OF REMAINING SECONDS OF FROZEN
        self.flag_isDying = 0 # INT > 0 IS THE NUMBER OF REMAINING SECONDS IN THE DEATH ANIMATION

    ### CHECKS ###

    def return_amIDead(self):
        temp_deadStatus = False
        if self.stat_hp <= 0:
            temp_deadStatus = True
        return temp_deadStatus

    ### DEFINED FUNCTIONS SPECIFIC TO THIS NPC'S MIND (BEHAVIOR, SKILLS, DAMAGE, ETC.) ###

    def affectMe (self, input_whichStatusEffect, input_duration = 1):
        """Apply status effects like poison, stun, etc."""
        pass

    def affectTarget (self, input_target, input_whichStatusEffect, input_duration = 1):
        """Apply status effects like poison, stun, etc."""
        pass

    def ai_state_update (self, input_newState):
        """Update enemy AI state machine"""
        pass

    def ai_state_empty (self):
        """Reset enemy to doing nothing"""
        pass

    def damageMe (self, input_damageAmount, input_damageType):
        """Handle incoming damage and apply appropriate effects"""
        pass

    def damageTarget (self, target, input_damageAmount, input_damageType):
        """Execute attack behavior against target"""
        pass

    def drop_loot (self):
        """Generate and drop loot upon death"""
        pass

    def hideMe (self):
        """Hide the enemy from view when it is dead"""
        self.flag_isAwake = False

    def killMe (self):
        self.ai_state_empty()
        self.drop_loot()
        self.hideMe()

    def return_state (self):
        """Return this npc state for saving/loading"""
        pass

    def set_difficulty (self, input_level):
        """Update enemy stats based on level or difficulty"""
        pass

    def wakeMe (self, input_x, input_y):
        """Return a hidden enemy to the world and set their state to patrolling"""
        self.flag_isAwake = True

    ### DEFINED FUNCTIONS SPECIFIC TO THIS NPC'S MODEL

    def animateMe (self):
        """Play specified animation"""
        pass

    def calculate_path_to_target (self, input_targetPosition):
        """Calculate pathfinding to reach target position"""
        pass

    def changeMaterial (self, input_newMat):
        """Swap material of model when suffering from status effects"""
        pass

    def changeModel (self, input_newModel):
        """Remove the old model and swap in the new one instantly"""
        """This is useful, for instance, when an enemy is turned into a pile of ash"""
        pass

    def returnAggroDistance (self, input_playerPosition):
        """Check if player is within aggression range"""
        pass

    def teleportMe (self, input_x, input_y):
        """Move the model to a specific location without animation or pathfinding"""
        pass

    def update_position (self, delta_time):
        """Update model position based on movement patterns and time"""
        pass

    # NOTE: IDEALLY YOU DON'T WANT TO CREATE AND/OR DESTROY NPC MODELS BETWEEN LEVELS. THIS IS INEFFICIENT
    # INSTEAD, HIDE THE MODELS WHEN THEY ARE NOT IN THE IMMEDIATE AREA OF THE PLAYER