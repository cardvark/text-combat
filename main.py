from src.characters import Combatant
from src.tools import *

def main():
    player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
    player2 = Combatant("Maria", "A comely young woman.", 4, "mage")

    print(player1)
    print(player2)

    inventory = []
    stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 5)
    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 20)
    inventory.append(stick)
    inventory.append(long_sword)
    player1.equip_item(stick)
    print(player1.main_equip.get_name())
    old_item = player1.equip_item(long_sword)
    print(f"Removed {old_item.get_name()}. Equipped {player1.main_equip.get_name()}.")




if __name__ == "__main__":
    main()
