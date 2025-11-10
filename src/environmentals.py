class Environmental():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_equippable = False
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
