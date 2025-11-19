from prettytable import PrettyTable, TableStyle
from src.type_enums import *
import random

def print_status(player, enemy):
    # TODO: make enemy status part of the enemy's object that can be called as needed.
    enemy_status_dict = {
        0.9: "pristine and malevolent",
        0.8: "barely scratched",
        0.6: "bleeding, but hardly winded",
        0.3: "tired, but determined",
        0.15: "haggard, and panting heavily",
        0.0: "on death's door",
    }

    enemy_hp_perc = enemy.current_hp / enemy.max_hp

    enemy_status = "bland."

    for k, v in sorted(enemy_status_dict.items(), reverse=True):
        if k <= enemy_hp_perc:
            enemy_status = v
            break
        

    print(f"You have {player.current_hp} out of {player.max_hp} HPs.")
    print(f"Your opponent appears {enemy_status}.")
    print()

def format_options_from_dict(options_dict, enums=False):
    output = ""

    for k, v in sorted(options_dict.items()):
        if enums:
            v = v.value.capitalize()

        output += f"[{k}]: {v.capitalize()}\n"
    
    return output


def generate_selection_dict(object_list, go_back=False):
    selection_dict = {}
    i = 1
    
    for object in object_list:
        selection_dict[str(i)] = object
        i += 1

    if go_back:
        selection_dict[str(i)] = "Return to previous menu."

    return selection_dict

def generate_options_from_list(item_list, go_back=False):
    i = 1

    options = {}

    for item in item_list:
        if isinstance(item, str):
            item_name = item
        else:
            item_name = item.name
        options[str(i)] = item_name
        i += 1

    if go_back:
        options[str(i)] = "Return to previous menu."
    
    return options


def get_inventory_table(selection_dict):
    table = PrettyTable()
    table.field_names = ["#", "Name", "Count"]

    for index, value_list in sorted(selection_dict.items()):
        name = value_list[0]
        count = value_list[1]
        table.add_row([
            f"[{index}]",
            name,
            count
        ])
    
    return table


def get_abilities_table(abilities_list):
    i = 1

    table = PrettyTable()
    table.field_names = ["#", "Name", "Ready", "Status"]

    for ability in abilities_list:
        ready = "X" if ability.check_ready() else "-"
        ability_status = get_ability_status(ability)
        
        table.add_row([
            f"[{i}]",
            ability.name,
            ready,
            ability_status
        ])

        i += 1
    
    table.align["Name"] = "l"
    table.align["Status"] = "l"

    return table


def get_return_to_previous_table(table):
    table_string = table.get_string()
    table_lines = table_string.split("\n")
    table_width = len(table_lines[0])

    index = len(table.rows) + 1

    return_1 = f"[{index}]"
    return_2 = "Return to the previous."

    add_length = table_width - len(return_1) - len(return_2) - 7

    return_2 += " " * add_length

    return_table = PrettyTable()
    return_table.add_row([
       return_1,
       return_2
        ])
    
    return_table.set_style(TableStyle.MSWORD_FRIENDLY)
    return_table.header = False
    
    return return_table


def get_return_to_previous_option(index):
    return f"[{index}] Return to previous menu.\n"


def get_table_bottom_border(table):
    table_string = table.get_string()
    table_lines = table_string.split("\n")
    table_width = len(table_lines[0])

    return "-" * table_width
    


def get_ability_status(ability):
    ability_status = ""

    match ability.cost_type:
        case CostType.TURN:
            current = ability.turns_to_ready
            max_turns = ability.max_turns
            ability_status = f"{current} / {max_turns} turns to ready"
        case CostType.MP:
            mp_cost = ability.current_mp_cost
            mp_base = ability.base_mp_cost
            ability_status = f"{mp_cost} MP from {mp_base} base"
        case CostType.CHARGE:
            current_charges = ability.current_charges
            total_charges = ability.total_charges
            ability_status = f"{current_charges} / {total_charges} charges"
        case _:
            raise Exception("Ability cost type not recognized.")

    return ability_status

def format_ability_outcome_text(ability, outcome, target):
    output = ""
    output += f"You used {ability.name}!\n"
    target_name = "yourself" if ability.effect_target == TargetType.SELF else target.name

    match ability.effect_type:
        case EffectType.DIRECT_DMG | EffectType.DMG_MULT:
            target_name = format_target_name(target_name, True)
            output += f"{target_name} took {outcome} damage!"
        case EffectType.BUFF:
            pass
        case EffectType.DEBUFF:
            pass
        case EffectType.HEAL_DIRECT | EffectType.HEAL_PERCENT:
            output += f"You healed {target_name} for {outcome} HPs."
        case _:
            raise Exception("Ability EffectType not found.")

    return output

def format_enemy_ability_outcome_text(ability, outcome, enemy):
    output = ""
    enemy_name = format_target_name(enemy.name, True)
    output += f"{enemy_name} used {ability.name}!\n"
    target_name = "themselves" if ability.effect_target == TargetType.SELF else "you"

    match ability.effect_type:
        case EffectType.DIRECT_DMG | EffectType.DMG_MULT:
            target_name = format_target_name(target_name, True)
            output += f"{target_name} took {outcome} damage!"
        case EffectType.BUFF:
            pass
        case EffectType.DEBUFF:
            pass
        case EffectType.HEAL_DIRECT | EffectType.HEAL_PERCENT:
            output += f"{enemy_name} healed {target_name}!"
            # TODO when I fix enemy status flavor text, call it here, probably.

            # output += f"You healed {target_name} for {outcome} HPs."
        case _:
            raise Exception("Ability EffectType not found.")

    return output


def format_target_name(target_name, capitalize=False):
    output = target_name

    if not target_name[0].isupper():
        output = f"the {target_name}"

        if capitalize:
            output = output.capitalize()

    return output

def get_consumable_message(user, item, amount):
    if not item.is_consumable:
        raise Exception("Item is not a consumable.")

    message = f"Used {item.name}, "

    match item.consumable_type:
        case EffectType.HEAL_DIRECT:
            message += f"restoring {amount} HPs. Current HP: {user.current_hp} out of {user.max_hp}."
        case EffectType.MP_DIRECT:
            message += f"restoring {amount} MPs. Current MP: {user.current_mp} out of {user.max_mp}."
        case _:
            raise Exception("Consumable type not supported.")
    
    return message


def damage_flavor(original_hp_perc, new_hp_perc):
    damage_delta = original_hp_perc - new_hp_perc

    flavor = ""

    if damage_delta > 0.25:
        options = [
            "You gasp with the shock of pain, clutching at the fresh wound in your side with a feeling of disbelief. ",
            "Your head rings from the blow, and your enemy appears doubled in your vision for a long, lingering moment. ",
        ]
        flavor += random.choice(options)

    if original_hp_perc > 0.2 and new_hp_perc <= 0.2:
        flavor += "The world dims at the edges, and takes on a grainy aspect. The sharp pains have dulled, and some dim part of you recognizes that you are in deep trouble."
    elif original_hp_perc > 0.5 and new_hp_perc <= 0.5:
        flavor += "Your body flags under the onslaught, but you grip your weapon tighter, and face your opponent squarely, ready for more."

    if flavor:
        print(flavor)