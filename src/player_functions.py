from src.characters import *
from src.tools import *
import src.stat_calcs as scs
from src.type_enums import *

def check_hit(character, target):
    return scs.calculate_hit(character, target)

def deal_damage(character, target):
    damage_dealt = calculate_damage(character, target)
    target.take_damage(damage_dealt)
    return damage_dealt

def get_consumables_item_list(inventory):
    consumables_item_list = inventory.get_item_list("consumables")

    return consumables_item_list

def use_consumable(user, item):
    if not item.is_consumable:
        raise Exception("Item is not a consumable.")

    message = f"Used {item.name}, "
    amount = item.amount

    match item.consumable_type:
        case "healing":
            user.restore_hp(amount)
            message += f"restoring {amount} HPs. Current HP: {user.current_hp} out of {user.max_hp}."
        case "mana":
            user.restore_mp(amount)
            message += f"restoring {amount} MPs. Current MP: {user.current_mp} out of {user.max_mp}."
    
    return message