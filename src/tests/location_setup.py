import unittest
import src.locations as loc
from src.locations import Direction
import src.characters as char
import src.tools as tls
from src.inventory import Inventory

def generate_locations():
    locations_list = []

    cave_entrance = loc.Location(
        "001CAVE_ENTRANCE",
        "A dark cave",
        "the entrance to the cave",
        "You find yourself standing in the entrance of a deep, dark cave. Pale moonlight filters through the dense forest canopy outside, providing just enough light to note the craggy features of the walls, and what appears to be a torch, abandoned on the hard-packed dirt floor.\n\nPick up the torch. << get torch >>",
        "You stand at the entrance of a deep, dark cave. The forest outside promises terrors in the night. The depths of the cave, dark and ominous as they are in the flickering light of your torch, offer a glimpse of salvation."
    )
    
    cave_hallway = loc.Location(
        "002CAVE_HALLWAY",
        "A long passageway",
        "a long, narrow cavern passageway",
        "You progress deeper into the cave, accompanied by the distant howling of the wind behind you and the cramped echoes of your footfalls. The passage twists and turns, contracts and expands, like a great mountainous serpent. You walk until your feet ache, and your hands are rubbed raw from navigating the narrow corridor. But ahead, warm yellow light spills past the twists and turns.",
        "The twisted cavern passageway extends before you, promising a long, tiresome trek.",
    )

    cave_chamber = loc.Location(
        "003CAVE_CHAMBER",
        "A large chamber",
        "a large, well-lit chamber",
        "You arrive in a large, well-lit chamber. Flickering torches line the walls in rusted sconces. The chamber is warm, but you find yourself cold and uneasy. There is a taste of deceit in the air. Lies that have yet to be discovered. As you approach the center of the chamber, a smoldering firepit flares back to life. It is warm, and you have been very cold. You appropach the fire, and stare into the flames. You have no food. You have no water. But you have warmth and shelter, however strange its happenstance may have been.",
        "The large, well-lit chamber spreads before you. The fire beckons.",
    )

    locations_list = [
        cave_entrance,
        cave_hallway,
        cave_chamber,
    ]
    
    return locations_list

def generate_connected_locations():
    locations_list = generate_locations()
    
    locations_list[0].connect_locations(locations_list[1], Direction.SOUTH)
    locations_list[1].connect_locations(locations_list[2], Direction.SOUTH)

    return locations_list
