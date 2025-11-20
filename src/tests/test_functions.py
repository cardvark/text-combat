import unittest
from src.characters import Combatant
from src.tools import Weapon
from src.combat_functions import *
from src.inventory import Inventory
from src.combat_sim import *
from src.type_enums import *
from src.abilities import *

class TestCharacters(unittest.TestCase):
    def generate_full_inventory(self):
        inventory = Inventory(5)

        for i in range(2):
            inventory.add_item(
                Potion("small potion", "a small healing potion of dubious quality", EffectType.HEAL_DIRECT, 20)
            )

        for i in range(2):
            inventory.add_item(
                Potion("medium potion", "a medium healing potion of reasonable quality", EffectType.HEAL_DIRECT, 50)
            )

        for i in range(1):
            inventory.add_item(
                Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)
            )
    
        return inventory

    def generate_player(self, name):
        second_wind = TurnBased(
            "second wind",
            "a self-heal ability",
            5,
            EffectType.HEAL_PERCENT,
            0.25,
            TargetType.SELF,
            )

        cleave = ChargeBased(
            "cleave",
            "a massive, two-handed strike",
            2,
            EffectType.DMG_MULT,
            2,
            TargetType.OTHER,
            ResetType.BATTLE
        )

        rage = ChargeBased(
            "rage",
            "unrelenting, fathomless rage",
            2,
            EffectType.BUFF,
            1.5,
            TargetType.SELF,
            ResetType.DAILY
        )

        lightning_ability = elementalMagic(
            "lightning bolt",
            "a lightning spell",
            20,
            EffectType.DIRECT_DMG,
            25,
            TargetType.OTHER,
            0.25,
            ElementType.LIGHTNING,
        )

        player = Combatant(name, "A vaguely nebbish creature.", 5, "fighter")
        
        player.learn_ability(second_wind)
        player.learn_ability(cleave)
        player.learn_ability(rage)
        player.learn_ability(lightning_ability)

        return player

    def test_01_attack(self):
        print("\n\nPrinting basic attack.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        player2 = Combatant("Maria", "A comely young woman.", 4, "mage")
        long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 20)
        player1.equip_item(long_sword)

        print(f"{player1.get_name()} attacks {player2.get_name()} with a {player1.main_equip.name}")

        if not check_hit(player1, player2):
            print(f"{player1.name} misses!")
            pass

        damage = deal_basic_attack_damage(player1, player2)

        print(f"{player1.name} deals {damage} damage, leaving {player2.name} with {player2.current_hp} HPs out of {player2.max_hp}")

    def test_02_continuous(self):
        print("\n\nPrinting basic attack.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        player2 = Combatant("Maria", "A comely young woman.", 4, "mage")
        long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)
        stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 2)
        player1.equip_item(stick)
        player2.equip_item(long_sword)

        i = 0

        players = [player1, player2]

        while (player2.is_conscious and player1.is_conscious):
            i += 1
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
                continue

            damage = deal_basic_attack_damage(player, target)

            print(f"{player.name} deals {damage} damage, leaving {target.name} with {target.current_hp} HPs out of {target.max_hp}")

            if not target.is_conscious:
                print(f"{target.name} has been rendered unconscious!")


    def test_03_resistances(self):
        pass
    
    def test_04_abilities(self):
        player1 = self.generate_player("Bob")
        player2 = self.generate_player("Mark")

        print(player1.list_ability_names())
        # ['rage', 'lightning bolt', 'cleave', 'second wind']

        p1_second_wind = player1.abilities[3]

        outcome = use_combatant_ability(player1, p1_second_wind, player1)
        print(outcome)