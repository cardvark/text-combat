from __future__ import annotations
from prettytable import PrettyTable, TableStyle
from src.type_enums import *
import src.tools as tls
import random
import src.characters as char
import src.abilities as abs

def print_status(
        player: char.Combatant, 
        enemy: char.NPCCombatant
        ) -> None:
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

def format_options_from_dict(
        options_dict: dict[str, str | Enum], 
        enums: bool = False,
        ) -> str:
    output = ""

    for k, v in sorted(options_dict.items()):
        if enums:
            v = v.value.capitalize()

        output += f"[{k}]: {v.capitalize()}\n"
    
    return output


def generate_selection_dict(
        object_list: list[abs.Ability], 
        go_back: bool = False
        ) -> dict[str, abs.Ability]: 
    #currently only used to generate abilities selection dict.
    selection_dict = {}
    i = 1
    
    for object in object_list:
        selection_dict[str(i)] = object
        i += 1

    if go_back:
        selection_dict[str(i)] = "Return to previous menu."

    return selection_dict


def generate_aggregated_selection_dict(
        object_list: list[tls.Holdable],
        ) -> dict[str, list[str, int, list[tls.Holdable]]]:
    
    count_dict = generate_aggregated_items(object_list)
    selection_dict = {}
    i = 1

    for name, values in sorted(count_dict.items()):
        idx = str(i)
        count = values[0]
        items = values[1]
        selection_dict[idx] = [name, count, items]

        i += 1

    return selection_dict


def generate_aggregated_items(
        items: list[tls.Environmental]
        ) -> dict[str, list[int, list[tls.Environmental]]]:
    count_dict_with_ids = {}

    for item in items:
        if item.name in count_dict_with_ids:
            count_dict_with_ids[item.name][0] += 1
            count_dict_with_ids[item.name][1].append(item)
        else:
            count_dict_with_ids[item.name] = [1, [item]]
        
    return count_dict_with_ids


def get_inventory_table(
        selection_dict: dict[str, list[str, int]],
        ) -> PrettyTable:
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


def get_abilities_table(
        abilities_list: list[abs.Ability],
        ) -> PrettyTable:
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


def get_return_to_previous_table(table: PrettyTable) -> PrettyTable:
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


def get_table_bottom_border(table: PrettyTable) -> str:
    table_string = table.get_string()
    table_lines = table_string.split("\n")
    table_width = len(table_lines[0])

    return "-" * table_width
    

def get_ability_status(ability: abs.Ability) -> str:
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

def format_ability_outcome_text(
        ability: abs.Ability, 
        outcome: int, 
        target: char.Combatant,
        ) -> str:
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

def format_enemy_ability_outcome_text(
        ability: abs.Ability, 
        outcome: int, 
        enemy: char.NPCCombatant
        ) -> str:
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


def format_target_name(
        target_name: str, 
        capitalize: bool = False,
        ) -> str:
    output = target_name

    if not target_name[0].isupper():
        output = f"the {target_name}"

        if capitalize:
            output = output.capitalize()

    return output

def get_consumable_message(
        user: char.Combatant, 
        item: tls.Consumable, 
        amount: int
        ) -> str:
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


def damage_flavor(
        original_hp_perc: float, 
        new_hp_perc: float,
        ) -> str:
    # TODO consider returning string to print. 
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

    return flavor

def name_stripper(text: str) -> str:
    output = text[0].lower() + text[1:]

    output = output.removeprefix("a ")
    output = output.removeprefix("an ")
    output = output.removeprefix("the ")
    
    return output