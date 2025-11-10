from src.characters import *
from src.tools import *
import src.stat_calcs as scs

def use_potion(inventory, character, potion):
    if potion.potion_type == "healing":
        character.restore_hp(potion.amount)
    
    inventory.remove(potion)

def check_inventory(inventory, item):
    return item in inventory

def check_hit(character, target):
    return scs.calculate_hit(character, target)

def deal_damage(character, target):
    damage_dealt = calculate_damage(character, target)
    target.take_damage(damage_dealt)
    return damage_dealt