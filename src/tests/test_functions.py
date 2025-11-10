import unittest
from src.characters import Combatant
from src.tools import Weapon
from src.player_functions import *

class TestCharacters(unittest.TestCase):

    def test_attack(self):
        print("\n\nPrinting basic attack.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        player2 = Combatant("Maria", "A comely young woman.", 4, "mage")
        long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 20)
        player1.equip_item(long_sword)

        print(f"{player1.get_name()} attacks {player2.get_name()} with a {player1.main_equip.name}")

        if not check_hit(player1, player2):
            print(f"{player1.name} misses!")
            pass

        damage = deal_damage(player1, player2)

        print(f"{player1.name} deals {damage} damage, leaving {player2.name} with {player2.current_hp} HPs out of {player2.max_hp}")

    def test_continuous(self):
        print("\n\nPrinting basic attack.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        player2 = Combatant("Maria", "A comely young woman.", 4, "mage")
        long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 20)
        stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 10)
        player1.equip_item(stick)
        player2.equip_item(long_sword)

        i = 1

        players = [player1, player2]

        while (player2.is_conscious and player1.is_conscious):
            print(f"\n\nTurn {i}.")

            if i % 2 == 1:
                player = player1
                target = player2
            else:
                player = player2
                target = player1

            print(f"{player.get_name()} attacks {target.get_name()} with a {player.main_equip.name}.")

            if not check_hit(player, target):
                print(f"{player.name} misses!")
                pass

            damage = deal_damage(player, target)

            print(f"{player.name} deals {damage} damage, leaving {target.name} with {target.current_hp} HPs out of {target.max_hp}")

            if not target.is_conscious:
                print(f"{target.name} has been rendered unconscious!")

            i += 1

    def test_resistances(self):
        pass