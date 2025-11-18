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
    

    def test_inventory(self):
        print("\n\nChecking inventory contents.")

        inventory = self.generate_full_inventory()

        print(inventory.get_contents)

        print("\nChecking item list:")

        for item_tup in inventory.get_item_list():
            print(item_tup)


    def test_inventory_cap(self):
        print("\n\nTesting inventory cap.")

        inventory = self.generate_full_inventory()
        new_potion = Potion("small potion", "a small healing potion of dubious quality", "healing", 20)

        self.assertEqual(
            False,
            inventory.add_item(new_potion)
        )

    def test_item_retrieval_by_id(self):
        print("\n\nTesting item retrieval by id.")

        inventory = self.generate_full_inventory()
        first_item = inventory.get_item_list()[0]

        uid = first_item[0]

        retrieved_item = inventory.get_item_by_id(uid)

        with self.subTest():
            self.assertEqual(
                retrieved_item.name,
                "small potion"
            )
        with self.subTest():
            self.assertEqual(
                False,
                inventory.get_item_by_id(uid)
            )
        with self.subTest():
            self.assertEqual(
                4,
                len(inventory.get_item_list())
            )
        
    def test_potions_only(self):
        print("\n\nTesting consumables only flag")

        inventory = self.generate_full_inventory()
        consumables = inventory.get_consumables()
        consumables_item_list = inventory.get_item_list(flag="consumable")

        with self.subTest():
            self.assertEqual(
                4,
                len(consumables)
            )
        with self.subTest():
            self.assertEqual(
                4,
                len(consumables_item_list)
            )

        