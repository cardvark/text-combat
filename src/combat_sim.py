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
            break
        else:
            print("Select one of the options.")

    match player_choice:
        case "1":
            print(f"You attack the {enemy.name}.")
            damage = player_attack(player, enemy)

            if damage != None:
                print(f"You hit your opponent squarely, dealing {damage} damage.")
            
        case "2":
            # TODO 
            print("working on this.")
            pass
        case "3":
            print("There is no fleeing from this fight.")
            pass
        
        
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

