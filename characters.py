from enum import Enum
class Environmental():
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
    
    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

class Combatant(Environmental):
    def __init__(self, name, description, level, job):
        super().__init__(name, description)
        self.__level = level
        self.__job = job
        self.__max_hp = self.get_max_hp(level, self.__job)
        self.__max_mp = self.get_max_mp(level, self.__job)
        self.__current_hp = self.__max_hp
        self.__current_mp = self.__max_mp

    def get_max_hp(self, level, job):
        base_hp = 30
        hp_per_level = 5
        job_modifier = hp_modifiers[job]
        return base_hp * hp_per_level * job_modifier

    def get_max_mp(self, level, job):
        base_mp = 25
        mp_per_level = 3
        job_modifier = mp_modifiers[job]
        return base_mp * mp_per_level * job_modifier

    def __repr__(self):
        return f"Combatant: {self.__name}\nDescription: {self.__description}\n\nJob: {self.__job.capitalize()}.\n\nHP: {self.__current_hp} / {self.__max_hp}\nMP: {self.__current_mp} / {self.__max_mp}"

    

jobs_list = [
    "fighter",
    "mage",
    "healer",
    "thief",
]

mp_modifiers = {
    "fighter": 1.2,
    "mage": 0.8,
    "healer": 0.8,
    "theif": 1.0,
}

mp_modifiers = {
    "fighter": 0,
    "mage": 1.2,
    "healer": 1,
    "theif": 0,
}

