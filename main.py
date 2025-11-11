from src.characters import Combatant
from src.tools import *
from src.player_functions import *
from src.combat_sim import *
import time

def main():
    player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
    player2 = Combatant("ogre", "A foul, be-stenched beast looms three spans high.", 6, "fighter")

    stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 3)
    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)
    small_heal = Potion("small healing potion", "A small vial of a wan red liquid.", "healing", 25)
    med_heal = Potion("large healing potion", "A vial of a bright red liquid.", "healing", 50)

    inventory = [
       stick,
       long_sword,
       small_heal,
       med_heal
    ]

    player1.equip_item(stick)
    player2.equip_item(long_sword)

    player_move = True
    while (player1.is_conscious and player2.is_conscious):
        print("\n------------\n")
        if player_move:
            player_turn(inventory, player1, player2)
            player_move = False
        else:
            time.sleep(1)
            enemy_turn(player1, player2)
            player_move = True
            time.sleep(1)
    



if __name__ == "__main__":
    main()
