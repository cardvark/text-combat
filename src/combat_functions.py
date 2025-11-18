from src.characters import *
from src.tools import *
import src.stat_calcs as scs
from src.type_enums import *

def check_hit(character, target):
    return scs.calculate_hit(character, target)

def deal_basic_attack_damage(character, target):
    damage_dealt = calculate_basic_attack_damage(character, target)
    target.take_damage(damage_dealt)
    return damage_dealt

def get_consumables_item_list(inventory):
    consumables_item_list = inventory.get_item_list("consumables")

    return consumables_item_list

def use_consumable(user, item):
    # TODO: Split this into separate functions. Use item vs. message generated.
    # TODO: Switch to Enums for item types.
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

def use_combatant_ability(user, ability, target):
    # Decided to externalize logic for how abilities are used.
    # The "effect_type" determines the calculation, provided here.
    
    if user != ability.user:
        raise Exception("User cannot use this ability.")

    if ability.effect_target == TargetType.SELF:
        target = user

    amount = ability.effect_amount

    match ability.effect_type:
        case EffectType.DIRECT_DMG:
            outcome = calculate_ability_damage(amount, ability.damage_type, target)
            target.take_damage(outcome)
        case EffectType.DMG_MULT:
            outcome = calculate_basic_attack_damage(user, target, amount)
            target.take_damage(outcome)
        case EffectType.BUFF:
            pass
        case EffectType.DEBUFF:
            pass
        case EffectType.HEAL_DIRECT:
            outcome = amount
            target.restore_hp(amount)
        case EffectType.HEAL_PERCENT:
            outcome = int(amount * target.max_hp)
            target.restore_hp(outcome)
        case _:
            raise Exception("Ability EffectType not found.")
    
    ability.use_ability()
    return outcome

