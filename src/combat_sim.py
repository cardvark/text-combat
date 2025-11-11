from src.characters import Combatant
from src.tools import *
from src.player_functions import *
import random

def enemy_turn(player, enemy):
    print(f"The {enemy.name} attacks!")
    original_hp_perc = player.current_hp / player.max_hp
    damage = enemy_attack(player, enemy)
    if damage == None:
        return

    print(f"The {enemy.name} strikes you with {enemy.main_equip.name}, dealing {damage} damage.")

    new_hp_perc = player.current_hp / player.max_hp
    damage_flavor(original_hp_perc, new_hp_perc)

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
    

def player_selection(player_choice, inventory, player, enemy):
    match player_choice:
        case "1":
            print(f"You attack the {enemy.name}.")
            damage = player_attack(player, enemy)

            if damage != None:
                print(f"You hit your opponent squarely, dealing {damage} damage.")
            
            return True

        case "2":
            # TODO complete item usage
            item = inventory_selection(inventory)
            
            if not item:
                return False
            
            print(f"Used {item.name}")

            return True
        case "3":
            print("There is no fleeing from this fight.")
            return True
    

def player_turn(inventory, player, enemy):
    print_status(player, enemy)

    options = {
        "1": "Attack",
        "2": "Use an item",
        "3": "Flee",
    }

    while True:
        prompt = "Your options include: \n"
        for k, v in sorted(options.items()):
            prompt += f"[{k}] {v}\n"

        prompt += "\n>> "
        
        player_choice = input(prompt)

        if player_choice in options:
            result = player_selection(player_choice, inventory, player, enemy)
            
            if not result:
                continue
            break
        else:
            print("Select one of the options.")

        
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
        
        prompt = "Your usable items include: \n"
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
            print("Select one of the items.")

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
    
    return deal_damage(player, enemy)

def enemy_attack(player, enemy):
    if not check_hit(enemy, player):
        print(f"The {enemy.name} misses their attack!")
        return None
    
    return deal_damage(enemy, player)


def print_status(player, enemy):
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

