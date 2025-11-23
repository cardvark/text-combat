import unittest
from src.characters import Combatant
from src.tools import *
from src.combat_functions import *
from src.inventory import Inventory

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
    

    def test_inventory_cap(self):
        print("\n\nTesting inventory cap.")

        inventory = self.generate_full_inventory()
        new_potion = Potion("small potion", "a small healing potion of dubious quality", EffectType.HEAL_DIRECT, 20)

        self.assertEqual(
            False,
            inventory.add_item(new_potion)
        )

        
    def test_potions_only(self):
        print("\n\nTesting consumables only flag")

        inventory = self.generate_full_inventory()
        consumables = inventory.get_consumables()

        with self.subTest():
            self.assertEqual(
                4,
                len(consumables)
            )