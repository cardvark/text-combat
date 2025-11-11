import uuid

class Environmental():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_equippable = False
        self.is_consumable = False
        self.uid = uuid.uuid4()
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_id(self):
        return self.uid
