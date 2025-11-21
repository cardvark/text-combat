import unittest
import src.locations as loc
from src.locations import Direction
import src.characters as char
import src.tools as tls
from src.inventory import Inventory
import src.tests.location_setup as ls
import src.tests.object_setup as obj


class TestLocations(unittest.TestCase):
    def test_001_location_creation(self):
        new_location = ls.generate_locations()[0]

        print(new_location.long_description)

    
    def test_002_location_connections(self):
        cave_entrance, cave_hallway, *others = ls.generate_locations()

        with self.subTest():
            with self.assertRaises(Exception) as e:
                cave_entrance.connect_locations(cave_hallway, "up")

            self.assertEqual(
                str(e.exception),
                "Not a valid direction"
            )

        cave_entrance.connect_locations(cave_hallway, Direction.SOUTH)
        print(cave_entrance.connections)

        with self.subTest():
            self.assertEqual(
                cave_entrance.connections[Direction.SOUTH].name,
                "A long passageway",
            )

        with self.subTest():
            with self.assertRaises(Exception) as e:
                cave_entrance.connect_locations(cave_hallway, Direction.SOUTH)
            
            self.assertEqual(
                str(e.exception),
                "Location already has connection at Direction.SOUTH"
            )

        with self.subTest():
            with self.assertRaises(Exception) as e:
                cave_entrance.connect_locations(cave_hallway, Direction.WEST)
            
            self.assertIn(
                "already connected.",
                str(e.exception),
            )

    def test_003_formatted_connections(self):
        cave_entrance, cave_hallway, cave_chamber, *others = ls.generate_locations()
        cave_entrance.connect_locations(cave_hallway, Direction.SOUTH)
        cave_hallway.connect_locations(cave_chamber, Direction.SOUTH)

        formatted_directions = cave_hallway.get_formatted_connections()
        print(formatted_directions)

        self.assertEqual(
            "To the <north>, the entrance to the cave.\nTo the <south>, a large, well-lit chamber.\n",
            formatted_directions,
        )
        
    def test_004_enemies_in_location(self):
        cave_entrance, cave_hallway, cave_chamber, *others = ls.generate_connected_locations()
        player = obj.generate_player("bob")
        enemy = obj.generate_grunt("ogre", "A grotesque, gigantic brute.")
        inventory = obj.generate_full_inventory()
        long_sword = tls.Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)

        with self.subTest():
            with self.assertRaises(Exception) as e:
                cave_chamber.add_NPC(long_sword)

            self.assertEqual(
                str(e.exception),
                "Not an NPC Combatant character."
            )

        cave_chamber.add_NPC(enemy)

        # print(cave_chamber.get_formatted_NPCs())

        # print(cave_chamber.get_formatted_entrance())

        entrance_text = cave_chamber.player_enter(player)
        print(entrance_text)
        print("\n\n")

        for item in inventory.bag:
            cave_chamber.add_item(item)

        print(cave_chamber.get_look())

        print("\n\n")
        entrance_text = cave_chamber.player_enter(player)
        print(entrance_text)
        print("\n\n")