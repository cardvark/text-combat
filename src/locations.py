from __future__ import annotations
from enum import Enum
import src.characters as char
import src.print_formatting as pf
import src.environmentals as env

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    WEST = "west"
    EAST = "east"
    UP = "up"
    DOWN = "down"

opposite_dirs = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP
}

class Location():
    def __init__(self, 
        loc_id: str,
        name: str,
        short_description: str,
        intro_description: str,
        long_description: str,
        item_location: str = "floor",
    ) -> None:
        self.loc_id = loc_id
        self.name = name
        self.short_description = short_description
        self.intro_description = intro_description
        self.long_description = long_description
        self.items = []
        self.NPCs = []
        self.player = None
        self.connections = {}
        self.has_entered = False
        self.stripped_name = pf.name_stripper(self.name)
        self.item_location = item_location

    def connect_locations(
            self, 
            second_location: Location, 
            direction: Direction, 
            one_way: bool = False
            ) -> None:
        if not isinstance(direction, Direction):
            raise Exception("Not a valid direction")
        
        if direction in self.connections:
            raise Exception(f"Location already has connection at {direction}")

        if second_location in self.connections.values():
            raise Exception(f"{second_location.name} already connected.")

        opposite = opposite_dirs[direction]
        self.connections[direction] = second_location
        
        if opposite in second_location.connections:
            # This is allowed, albeit risky behavior. Good for creating mazes and such.
            print(f"{second_location.name} already has a connection to the {opposite}")
            return
        
        if not one_way:
            second_location.connect_locations(self, opposite)

    def get_formatted_connections(self) -> str:
        formatted_directions = ""
        for direction in Direction:
            if direction in self.connections:
                loc = self.connections[direction]
                formatted_directions += f"To the <{direction.value}>, {loc.short_description}.\n"

        return formatted_directions
    
    def add_NPC(self, character: char.NPCCombatant) -> None:
        if not isinstance(character, char.NPCCombatant):
            raise Exception("Not an NPC Combatant character.")

        self.NPCs.append(character)

        self.NPCs = sorted(self.NPCs)
    
    def get_formatted_NPCs(self) -> str:
        formatted_NPCs = ""

        for npc in self.NPCs:
            formatted_NPCs += f"{npc.description} ({npc.name})\n"

        return formatted_NPCs
    
    def get_formatted_items(self) -> str:
        formatted_items = ""

        for item in self.items:
            formatted_items += f"{item.description.capitalize()} ({item.name})\n"

        return formatted_items
    
    def get_formatted_entrance(self) -> str:
        formatted_entrance_text = ""

        formatted_entrance_text += self.name + "\n"
        
        if not self.has_entered: 
            formatted_entrance_text += self.intro_description
        else:
            formatted_entrance_text += self.long_description

        formatted_entrance_text += "\n"
        
        if self.NPCs:
            formatted_entrance_text += f"Within the {self.stripped_name}, you see:\n"

            formatted_entrance_text += self.get_formatted_NPCs()
        
        return formatted_entrance_text
    
    def get_look(self) -> str:
        output = f"You take a hard look around.\n"

        if self.NPCs:
            output += "\n"
            output += f"You see:\n"

            output += self.get_formatted_NPCs()

        if self.items:
            output += "\n"
            output += f"On the {self.item_location}:\n"
            output += self.get_formatted_items()

        output += "\n"
        output += "Exits:\n"
        output += self.get_formatted_connections()
    
        return output
    
    def add_item(self, item: env.Environmental) -> None:
        if not isinstance(item, env.Environmental):
            raise Exception("Not an environmental item.")
        
        self.items.append(item)

    def player_enter(self, player: char.Combatant) -> str:
        self.player = player
        player.update_current_location(self)
        entrance_text = self.get_formatted_entrance()
        self.has_entered = True

        return entrance_text

    def player_leave(self) -> None:
        self.player = None