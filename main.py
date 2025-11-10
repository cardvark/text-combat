from src.characters import Combatant
from src.tools import *
from src.player_functions import *

def main():
    player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
    player2 = Combatant("Maria", "A comely young woman.", 4, "mage")

    print(player1)
    print(player2)

    stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 5)
    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 20)
    small_heal = Potion("small healing potion", "A small vial of a wan red liquid.", "healing", 25)
    med_heal = Potion("large healing potion", "A vial of a bright red liquid.", "healing", 50)

    inventory = [
       stick,
       long_sword,
       small_heal,
       med_heal
    ]

    player1.equip_item(stick)
    print(player1.main_equip.get_name())
    old_item = player1.equip_item(long_sword)
    print(f"Removed {old_item.get_name()}. Equipped {player1.main_equip.get_name()}.")

    player1.take_damage(50)
    print(player1.current_hp)
    use_potion(inventory, player1, small_heal)
    
    print(player1.current_hp)
    print(inventory)

    use_potion(inventory, player1, med_heal)
        
    print(player1.current_hp)
    print(inventory)



if __name__ == "__main__":
    main()
