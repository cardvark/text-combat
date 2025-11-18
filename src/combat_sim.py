from src.characters import Combatant
from src.tools import *
from src.player_functions import *
from enum import Enum
import src.print_formatting as pf
import random


class PlayerOptions(Enum):
    ATTACK = "Attack"
    ABILITIES = "Abilities"
    ITEMS = "Items"
    FLEE = "Flee"


def enemy_turn(enemy_inventory, player, enemy):
    enemy.turn_increment()
    print(f"The {enemy.name} attacks!")
    original_hp_perc = player.current_hp / player.max_hp
    damage = enemy_attack(player, enemy)
    if damage == None:
        return

    print(f"The {enemy.name} strikes you with {enemy.main_equip.name}, dealing {damage} damage.")

    new_hp_perc = player.current_hp / player.max_hp
    damage_flavor(original_hp_perc, new_hp_perc)

def generate_player_options(player, inventory):
    i = 1

    options = {
        str(i): PlayerOptions.ATTACK,
    }

    i += 1

    if player.abilities:
        options[str(i)] = PlayerOptions.ABILITIES
        i += 1

    if inventory.get_consumables():
        options[str(i)] = PlayerOptions.ITEMS
        i += 1

    options[str(i)] = PlayerOptions.FLEE

    return options


def generate_choice_prompt(printable_options):
    pass


def player_turn(inventory, player, enemy):
    pf.print_status(player, enemy)
    player.turn_increment()

    options = generate_player_options(player, inventory)

    while True:
        prompt = "Your options include: \n"

        prompt += pf.format_options_from_dict(options, True)

        prompt += "\n>> "
        
        player_choice = input(prompt)

        if player_choice in options:
            selection = options[player_choice]

            result = player_turn_selection(selection, inventory, player, enemy)
            
            if not result:
                continue #TBD?
            break
        else:
            print("Select one of the options.\n")


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
    

def player_turn_selection(selection, inventory, player, enemy):
    match selection:
        case PlayerOptions.ATTACK:
            print(f"You attack the {enemy.name}.")
            damage = player_attack(player, enemy)

            if damage != None:
                print(f"You hit your opponent squarely, dealing {damage} damage.")
            
            return True

        case PlayerOptions.ABILITIES:
            ability = ability_selection(player)

            if not ability:
                return False
            
            print(ability.name)

            ability.use_ability()
            # TODO: Implement actually using abilities.

        case PlayerOptions.ITEMS:
            item = inventory_selection(inventory)
            
            if not item:
                return False
            
            message = use_consumable(player, item)
            print(message)
            return True

        case PlayerOptions.FLEE:
            print("There is no fleeing from this fight.")
            return True
    

def ability_selection(player):
    while True:
        abilities_list = player.get_abilities() # gets list of ability objects.
        abilities_selection_dict = pf.generate_selection_dict(abilities_list) # Used to compare against player input in order to determine which ability was selected.
        num_options = len(abilities_selection_dict) + 1

        table = pf.get_abilities_table(abilities_list)

        print("Your abilities include:\n")
        print(table)
        print(pf.get_return_to_previous_option(num_options))
        player_choice = input("\n>> ")

        if player_choice == str(num_options):
            # player has chosen the "return to previous menu" option.
            return None

        if player_choice in abilities_selection_dict:
            chosen_ability = abilities_selection_dict[player_choice]

            if chosen_ability.check_ready():
                break
            else:
                print("Ability not ready to use. Choose another option.\n")
        else:
            print("Select one of the options.\n")

    return chosen_ability

        
def aggregate_inventory_items(items):
    count_dict_with_ids = {}

    for item in items:
        if item.name in count_dict_with_ids:
            count_dict_with_ids[item.name][0] += 1
            count_dict_with_ids[item.name][1].append(item.uid)
        else:
            count_dict_with_ids[item.name] = [1, [item.uid]]
        
    return count_dict_with_ids

def display_inventory_items(aggregated_items):
    # not used currently.
    print_output = "Your inventory contains:\n"
    for item_name, count in sorted(aggregated_items.items()):
        print_output += f"{item_name} x{count}\n"
    
    print(print_output)


def inventory_selection(inventory):
    while True:
        consumables = inventory.get_consumables()
        if not consumables:
            print("No usable items found!")

        aggregated_consumables = aggregate_inventory_items(consumables)
    
        i = 1
        selections = {}
        
        prompt = "Select an option: \n"
        for item_name, value in sorted(aggregated_consumables.items()):
            prompt += f"[{i}] {item_name} x{value[0]}\n"
            selections[str(i)] = value[1] # ties number selection to list of UIDs.
            i += 1

        prompt += f"[{i}] Return to previous menu.\n"
        selections[str(i)] = []

        prompt += "\n>> "
        
        player_choice = input(prompt)

        if player_choice in selections:
            break
        else:
            print("Select one of the items.\n")

    if not consumables:
        return None

        
    if player_choice == str(i):
        return None

    item_id = selections[player_choice][0]
    retrieved_item = inventory.get_item_by_id(item_id)
    return retrieved_item


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
