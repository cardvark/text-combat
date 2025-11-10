from src.characters import *
from src.tools import *

def use_potion(inventory, character, potion):
    if potion.potion_type == "healing":
        character.restore_hp(potion.amount)
    
    inventory.remove(potion)

def check_inventory(inventory, item):
    return item in inventory