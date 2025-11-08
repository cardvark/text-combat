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
        self.__max_hp = self.calc_max_hp(level, self.__job)
        self.__max_mp = self.calc_max_mp(level, self.__job)
        self.__current_hp = self.__max_hp
        self.__current_mp = self.__max_mp

    def calc_max_hp(self, level, job):
        base_hp = 30
        hp_per_level = 5
        job_modifier = hp_modifiers[job]
        return int(base_hp * hp_per_level * job_modifier)

    def calc_max_mp(self, level, job):
        base_mp = 25
        mp_per_level = 3
        job_modifier = mp_modifiers[job]
        return int(base_mp * mp_per_level * job_modifier)

    def get_max_hp(self):
        return self.__max_hp

    def get_max_mp(self):
        return self.__max_mp

    def get_current_hp(self):
        return self.__current_hp
    
    def get_current_mp(self):
        return self.__current_mp

    def get_job(self):
        return self.__job

    def __repr__(self):
        return f"\n----------\nCombatant: {self.get_name()}\nDescription: {self.get_description()}\n\nJob: {self.get_job().capitalize()}\n\nHP: {self.get_current_hp()} / {self.get_max_hp()}\nMP: {self.get_current_mp()} / {self.get_max_mp()}\n----------\n"

    

jobs_list = [
    "fighter",
    "mage",
    "healer",
    "thief",
]

hp_modifiers = {
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

