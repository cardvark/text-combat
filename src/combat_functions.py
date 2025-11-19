import src.stat_calcs as scs
from src.type_enums import *

def check_hit(character, target):
    return scs.calculate_hit(character, target)

def deal_basic_attack_damage(character, target):
    damage_dealt = scs.calculate_basic_attack_damage(character, target)
    target.take_damage(damage_dealt)
    return damage_dealt


def player_attack(player, enemy):
    if not check_hit(player, enemy):
        print("You miss your attack!")
        return None
    
    return deal_basic_attack_damage(player, enemy)

def enemy_attack(player, enemy):
    if not check_hit(enemy, player):
        print(f"The {enemy.name} misses their attack!")
        return None
    
    return deal_basic_attack_damage(enemy, player)


def get_consumables_item_list(inventory):
    consumables_item_list = inventory.get_item_list("consumables")

    return consumables_item_list

def use_consumable(user, item):
    if not item.is_consumable:
        raise Exception("Item is not a consumable.")

    amount = item.amount

    match item.consumable_type:
        case EffectType.HEAL_DIRECT:
            user.restore_hp(amount)
        case EffectType.MP_DIRECT:
            user.restore_mp(amount)
        case _:
            raise Exception("Consumable type not supported.")
    
    return amount

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
            outcome = scs.calculate_ability_damage(amount, ability.damage_type, target)
            target.take_damage(outcome)
        case EffectType.DMG_MULT:
            outcome = scs.calculate_basic_attack_damage(user, target, amount)
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

