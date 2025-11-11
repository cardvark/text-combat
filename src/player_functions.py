from src.characters import *
from src.tools import *
import src.stat_calcs as scs

def check_hit(character, target):
    return scs.calculate_hit(character, target)

def deal_damage(character, target):
    damage_dealt = calculate_damage(character, target)
    target.take_damage(damage_dealt)
    return damage_dealt

def get_consumables_item_list(inventory):
    consumables_item_list = inventory.get_item_list("consumables")

    return consumables_item_list
