import uuid

class Environmental():
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.is_equippable = False
        self.is_consumable = False
        self.uid = uuid.uuid4()
    
    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_id(self) -> uuid.UUID:
        # TODO may end up deprecating this.
        return self.uid
