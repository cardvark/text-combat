import src.stat_calcs as scs
from src.environmentals import Environmental

class Combatant(Environmental):
    def __init__(self, name, description, level, job):
        super().__init__(name, description)
        self.__level = level
        self.__job = job
        self.__max_hp = scs.calc_max_hp(level, self.__job)
        self.__max_mp = scs.calc_max_mp(level, self.__job)
        self.__current_hp = self.__max_hp
        self.__current_mp = self.__max_mp
        self.main_equip = None
        self.off_equip = None
        self.chest_equip = None

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

    def equip_item(self, equipment):
        old_equipment = None

        match equipment.equip_type:
            case "weapon":
                old_equipment = self.remove_main()
                self.main_equip = equipment
            case "armor":
                old_equipment = self.remove_chest()
                self.chest_equip = equipment
            case _: 
                old_equipment = self.remove_off()
                self.off_equip = equipment
    
        return old_equipment
    
    def remove_main(self):
        equipment = self.main_equip
        self.main_equip = None        
        return equipment

    def remove_off(self):
        equipment = self.off_equip
        self.off_equip = None        
        return equipment

    def remove_chest(self):
        equipment = self.chest_equip
        self.chest_equip = None        
        return equipment

    def __repr__(self):
        return f"\n----------\nCombatant: {self.get_name()}\nDescription: {self.get_description()}\n\nJob: {self.get_job().capitalize()}\n\nHP: {self.get_current_hp()} / {self.get_max_hp()}\nMP: {self.get_current_mp()} / {self.get_max_mp()}\n----------\n"

