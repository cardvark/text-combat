class Environmental():
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
        self.is_equippable = False
    
    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description
