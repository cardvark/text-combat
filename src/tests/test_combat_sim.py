import unittest
from src.characters import Combatant
from src.tools import *
from src.player_functions import *
from src.inventory import Inventory
from src.combat_sim import *

class TestInventory(unittest.TestCase):

    def generate_full_inventory(self):
        inventory = Inventory(5)

        for i in range(2):
            inventory.add_item(
                Potion("small potion", "a small healing potion of dubious quality", "healing", 20)
            )

        for i in range(2):
            inventory.add_item(
                Potion("medium potion", "a medium healing potion of reasonable quality", "healing", 50)
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

    def test_inventory_selection(self):
        inventory = self.generate_full_inventory()

        item = inventory_selection(inventory)

        with self.subTest():
            self.assertEqual(
                item.name,
                "small potion" # user must select properly
            )
        with self.subTest():
            self.assertEqual(
                len(inventory.get_contents()),
                4
            )