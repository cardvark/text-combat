from src.characters import Combatant
import src.combat_functions as cf
from enum import Enum
import src.print_formatting as pf
import random
from src.command_enums import *
import src.enemy_manager as em


class PlayerOptions(Enum):
    ATTACK = "Attack"
    ABILITIES = "Abilities"
    ITEMS = "Items"
    FLEE = "Flee"


def enemy_turn(enemy_inventory, player, enemy):
    enemy.turn_increment()
    decision, chosen_object = enemy.get_combat_action(enemy_inventory, player)

    if decision == Command.BASIC_ATTACK:
        em.handle_basic_attack(enemy, player)
    if decision == Command.USE_ABILITY:
        em.handle_enemy_ability(enemy, chosen_object, player)
    if decision == Command.USE_CONSUMABLE:
        em.handle_enemy_item(enemy, enemy_inventory, chosen_object, player)


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
            damage = cf.player_attack(player, enemy)

            if damage != None:
                print(f"You hit your opponent squarely, dealing {damage} damage.")
            
            return True

        case PlayerOptions.ABILITIES:
            chosen_ability = ability_selection(player)

            if not chosen_ability:
                return False

            outcome = cf.use_combatant_ability(player, chosen_ability, enemy)

            outcome_text = pf.format_ability_outcome_text(chosen_ability, outcome, enemy)
            print(outcome_text)

            return True

        case PlayerOptions.ITEMS:
            item = inventory_selection(inventory)
            
            if not item:
                return False
            
            amount = cf.use_consumable(player, item)
            message = pf.get_consumable_message(player, item, amount)
            print(message)
            return True

        case PlayerOptions.FLEE:
            #TODO Implement fleeing logic.
            # Need to first implement a concept of location.
            print("There is no fleeing from this fight.")
            return False
    

def ability_selection(player):
    while True:
        abilities_list = player.get_abilities() # gets list of ability objects.
        abilities_selection_dict = pf.generate_selection_dict(abilities_list) # Used to compare against player input in order to determine which ability was selected.
        num_options = len(abilities_selection_dict) + 1

        table = pf.get_abilities_table(abilities_list)

        print("Your abilities include:\n")
        print(table)
        # print(pf.get_return_to_previous_option(num_options))
        print(pf.get_return_to_previous_table(table))
        print(pf.get_table_bottom_border(table))
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
            return None

        aggregated_consumables = aggregate_inventory_items(consumables)
        selection_dict = aggregated_inventory_selection_dict(aggregated_consumables)
        num_options = len(selection_dict) + 1
        
        print("Select an option: \n")
        table = pf.get_inventory_table(selection_dict)
        print(table)
        print(pf.get_return_to_previous_table(table))
        print(pf.get_table_bottom_border(table))

        prompt = "\n>> "
        
        player_choice = input(prompt)

        if int(player_choice) == num_options:
            # Player chose "return to previous" option.
            return None

        if player_choice in selection_dict:
            break
        else:
            print("Select one of the items.\n")
        
        
    item_id = selection_dict[player_choice][2]
    retrieved_item = inventory.get_item_by_id(item_id)
    return retrieved_item


def aggregated_inventory_selection_dict(aggregated_items):
    selection_dict = {}
    i = 1
    for item_name, value_list in sorted(aggregated_items.items()):
        count = value_list[0]
        first_uid = value_list[1][0]
        selection_dict[str(i)] = [item_name, count, first_uid]
        i += 1

    return selection_dict


def aggregate_inventory_items(items):
    count_dict_with_ids = {}

    for item in items:
        if item.name in count_dict_with_ids:
            count_dict_with_ids[item.name][0] += 1
            count_dict_with_ids[item.name][1].append(item.uid)
        else:
            count_dict_with_ids[item.name] = [1, [item.uid]]
        
    return count_dict_with_ids
