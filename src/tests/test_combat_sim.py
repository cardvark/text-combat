import unittest
from src.characters import Combatant
from src.tools import *
from src.combat_functions import *
from src.inventory import Inventory
from src.combat_sim import *
from src.type_enums import *
from src.abilities import *

class TestInventory(unittest.TestCase):

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
    
    def test_item_aggreagtion(self):
        inventory = self.generate_full_inventory()

        items = inventory.get_contents()

        for k, v in aggregate_inventory_items(items).items():
            print(k, v)

    # def test_inventory_selection(self):
    #     inventory = self.generate_full_inventory()

    #     item = inventory_selection(inventory)

    #     with self.subTest():
    #         self.assertEqual(
    #             item.name,
    #             "small potion" # user must select properly
    #         )
    #     with self.subTest():
    #         self.assertEqual(
    #             len(inventory.get_contents()),
    #             4
    #         )

class TestOptions(unittest.TestCase):
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

    def generate_player(self):
        
        second_wind = TurnBased(
            "second wind",
            "a self-heal ability",
            5,
            EffectType.HEAL_DIRECT,
            25,
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

        player = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        
        player.learn_ability(second_wind)
        player.learn_ability(cleave)
        player.learn_ability(rage)
        player.learn_ability(lightning_ability)

        return player

    def test_generate_options(self):
        inventory = self.generate_full_inventory()
        player = self.generate_player()

        options = generate_player_options(player, inventory)

        printable_options = get_printable_options_from_dict(options, True)

        with self.subTest():
            self.assertEqual(
                "[1]: Attack\n[2]: Abilities\n[3]: Items\n[4]: Flee\n",
                printable_options,
            )

    def test_abilities_lists(self):
        player = self.generate_player()
        get_player_ability_choice(player)

    
