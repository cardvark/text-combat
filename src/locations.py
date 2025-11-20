from enum import Enum

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
        loc_id,
        name,
        short_description,
        intro_description,
        long_description,
    ):
        self.loc_id = loc_id
        self.name = name
        self.short_description = short_description
        self.intro_description = intro_description
        self.long_description = long_description
        self.environmentals = []
        self.NPCs = []
        self.players = None
        self.connections = {}
        self.has_entered = False

    def connect_locations(self, second_location, direction, one_way=False):
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

    def get_formatted_connections(self):
        formatted_directions = ""
        for direction in Direction:
            if direction in self.connections:
                loc = self.connections[direction]
                formatted_directions += f"To the <{direction.value}>, {loc.short_description}.\n"

        return formatted_directions
    
