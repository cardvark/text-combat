from __future__ import annotations
import src.characters as char
import src.combat_functions as cf
from enum import Enum
import src.print_formatting as pf
import random
from src.command_enums import *
import src.enemy_manager as em
import src.inventory as inv
import src.abilities as abs
import src.tools as tls
import uuid


class PlayerOption(Enum):
    ATTACK = "Attack"
    ABILITIES = "Abilities"
    ITEMS = "Items"
    FLEE = "Flee"


def enemy_turn(
        enemy_inventory: inv.Inventory, 
        player: char.Combatant, 
        enemy: char.NPCCombatant,
        ) -> None:
    enemy.turn_increment()
    decision, chosen_object = enemy.get_combat_action(enemy_inventory, player)

    if decision == Command.BASIC_ATTACK:
        em.handle_basic_attack(enemy, player)
    if decision == Command.USE_ABILITY:
        em.handle_enemy_ability(enemy, chosen_object, player)
    if decision == Command.USE_CONSUMABLE:
        em.handle_enemy_item(enemy, enemy_inventory, chosen_object, player)


def generate_player_options(
        player: char.Combatant, 
        inventory: inv.Inventory,
        ) -> dict[str, PlayerOption]:
    
    i = 1

    options = {
        str(i): PlayerOption.ATTACK,
    }

    i += 1

    if player.abilities:
        options[str(i)] = PlayerOption.ABILITIES
        i += 1

    if inventory.get_consumables():
        options[str(i)] = PlayerOption.ITEMS
        i += 1

    options[str(i)] = PlayerOption.FLEE

    return options


def player_turn(
    inventory: inv.Inventory, 
    player: char.Combatant, 
    enemy: char.NPCCombatant,
    ) -> None:
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
                continue
                #TODO unclear how / if I want to use the result bool.
            break
        else:
            print("Select one of the options.\n")
    

def player_turn_selection(
        selection: PlayerOption, 
        inventory: inv.Inventory, 
        player: char.Combatant, 
        enemy: char.NPCCombatant,
        ) ->bool:
    #TODO evaluate whether returning bool is necessary.

    match selection:
        case PlayerOption.ATTACK:
            print(f"You attack the {enemy.name}.")
            damage = cf.player_attack(player, enemy)

            if damage != None:
                print(f"You hit your opponent squarely, dealing {damage} damage.")
            
            return True

        case PlayerOption.ABILITIES:
            chosen_ability = ability_selection(player)

            if not chosen_ability:
                return False

            outcome = cf.use_combatant_ability(player, chosen_ability, enemy)

            outcome_text = pf.format_ability_outcome_text(chosen_ability, outcome, enemy)
            print(outcome_text)

            return True

        case PlayerOption.ITEMS:
            item = inventory_selection(inventory)
            
            if not item:
                return False
            
            amount = cf.use_consumable(player, item)
            message = pf.get_consumable_message(player, item, amount)
            print(message)
            return True

        case PlayerOption.FLEE:
            #TODO Implement fleeing logic.
            # Need to first implement a concept of location.
            print("There is no fleeing from this fight.")
            return False
    

def ability_selection(player: char.Combatant) -> abs.Ability:
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


def inventory_selection(inventory: inv.Inventory) -> tls.Consumable:
    while True:
        consumables = inventory.get_consumables()
        if not consumables:
            print("No usable items found!")
            return None

        selection_dict = pf.generate_aggregated_selection_dict(consumables)
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
        
        
    item = selection_dict[player_choice][2][0]

    return item