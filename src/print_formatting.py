from prettytable import PrettyTable
from src.type_enums import *

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

def get_return_to_previous_option(index):
    return f"[{index}] Return to previous menu.\n"


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