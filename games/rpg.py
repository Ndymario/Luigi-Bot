#####################
# This is the RPG system for Luigi Bot! Made by Ndymario
#####################

from math import ceil
import random

class Player:
    # The default player stats
    def __init__(self):
        self._name = ""
        self._avatar = ""
        self._id = 0
        self._level = 1
        self._exp = 0
        self._hp = 0
        self._max_hp = 0
        self._sp = 0
        self._max_sp = 0
        self._power = 0
        self._shield = 0
        self._spd = 0
        self._lk = 0
        self._inventory = []
        self._defeated = False

    # Accessors
    def get_name(self):
        return self._name

    def get_avatar(self):
        return self._avatar

    def get_id(self):
        return self._id

    def get_level(self):
        return self._level
    
    def get_exp(self):
        return self._exp

    def get_hp(self):
        return self._hp

    def get_max_hp(self):
        return self._max_hp
    
    def get_sp(self):
        return self._sp

    def get_max_sp(self):
        return self._max_sp

    def get_power(self):
        return self._power

    def get_shield(self):
        return self._shield

    def get_spd(self):
        return self._spd

    def get_lk(self):
        return self._lk

    def get_inventory(self):
        return self._inventory

    def get_defeated(self):
        return self._defeated

    # Mutators
    def set_name(self, name):
        self._name = name

    def set_avatar(self, avatar):
        self._avatar = avatar

    def set_id(self, id):
        self._id = id

    def set_level(self, level):
        self._level = level
    
    def set_exp(self, exp):
        self._exp = exp

    def set_hp(self, hp):
        self._hp = hp
    
    def set_sp(self, sp):
        self._sp = sp

    def set_power(self, power):
        self._power = power

    def set_shield(self, shield):
        self._shield = shield

    def set_spd(self, spd):
        self._spd = spd

    def set_lk(self, lk):
        self._lk = lk

    def set_inventory(self, inventory):
        self._inventory = inventory

    def set_defeated(self, defeated):
        self._defeated = defeated
    
class Enemy:
    # TODO Make enemy class
    def __init__(self):
        return

class Battle():
    def __init__(self):
        # Make a list of every entity in the battle
        self._participants = []

        # Dictionary to store entity stats (accessed using the ID)
        self._participant_stats = {}

        # List that stores the turn order
        self._turn_order_list = []
        self._key_list = []

        # Keep track of who's turn it is
        self._turn_number = 0

    # Accessors
    def get_turn_order_list(self):
        return self._turn_order_list

    def get_key_list(self):
        return self._key_list

    def get_turn_number(self):
        return self._turn_number

    def assign_entities(self, *args):
        # Store what entities are in the current battle
        for arg in args:
            self._participants.append(arg)

        for participants in self._participants:
            self._participant_stats[participants.get_id()] = {
                # Create a nested dictionary for the entity stats in any given battle
                "hp" : participants.get_hp(),
                "sp" : participants.get_sp(),
                "power" : participants.get_power(),
                "shield" : participants.get_shield(),
                "spd" : participants.get_spd(),
                "lk" : participants.get_lk(),
                "inventory" : participants.get_inventory()
            }

    def turn_order(self):
        # Temp list to keep track of the entities to determine the turn order
        temp_list = []

        def turn_order_speed(participant):
            self._key_list = list(participant)
            key = self._key_list[0]
            return participant[key]

        # Loop through all of the entities and get their speed stat
        for participants in self._participants:
            temp_list.append({participants.get_id():participants.get_spd()})

        # Sort the turn order based on speed stat
        temp_list.sort(reverse=True, key=turn_order_speed)
        self._turn_order_list = temp_list
    
    def turn_number(self):
        if (len(self._turn_order_list) < self._turn_number):
            self._turn_number = 0
        else:
            self._turn_number += 1

    def attack(self, attacker, target):
        # Get the ID & relevant stats of the attacker and target for finding their stats in the dictionary
        atk_stats = [attacker.get_id(), attacker.get_power(), attacker.get_lk()]
        tar_stats = [target.get_id(), target.get_hp(), target.get_shield()]

        # Define a helper function to calculate attack power based on the opponent's shield and the attacker's luck
        def attack_power(atk_stats, tar_stats):
            crit = False
            lk_multiplier = 0.1
            atk_multiplier = 0.2
            shield_multiplier = 0.1
            # First, lets determine if the attack is a crit or not
            if (1 <= atk_stats[2]*(lk_multiplier)+(random.randint(0, 100))**2/10000):
                crit = True

            # Now, lets determine how much damage is being delt
            damage_total = (atk_stats[1] * atk_multiplier) - (tar_stats[2] * shield_multiplier)
            # Add a crit bonus if the entity recieved a crit
            if (crit):
                return ceil(damage_total + (damage_total * 0.4))
            else:
                return ceil(damage_total)
        
        damage = attack_power(atk_stats, tar_stats)

        new_health = tar_stats[1] - damage

        # Just in case some weird rounding things occur, don't let the attack heal the target
        if(new_health > target.get_hp()):
            new_health = target.get_hp()

        target.set_hp(new_health)

        if(new_health <= 0):
            target.set_defeated(True)

        self.turn_number()

def battle_generator(*player_info, enemy_info, is_quest):
    battle = Battle()

    # If this battle is part of a quest, load the enemies into the battle
    if(is_quest):
        for enemy in enemy_info:
            battle.assign_entities(enemy)

    # Convert the player information to be useable in the battle system,
    #  then assign the player into the battle
    for player in player_info:
        new_player = Player()
        new_player.set_name(player.name)
        new_player.set_avatar(player.avatar_url)
        new_player.set_id(player.id)
        new_player.set_level(player.level)
        new_player.set_exp(player.exp)
        new_player.set_hp(player.hp)
        new_player.set_sp(player.sp)
        new_player.set_power(player.power)
        new_player.set_shield(player.shield)
        new_player.set_spd(player.spd)
        new_player.set_lk(player.lk)
        new_player.set_inventory(player.inventory)
        battle.assign_entities(new_player)

    return battle

    