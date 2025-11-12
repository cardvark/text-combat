import src.stat_calcs as scs
from src.environmentals import Environmental

class Combatant(Environmental):
    def __init__(self, name, description, level, job):
        super().__init__(name, description)
        self.level = level
        self.job = job
        self.max_hp = scs.calc_max_hp(level, self.job)
        self.max_mp = scs.calc_max_mp(level, self.job)
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        self.main_equip = None
        self.off_equip = None
        self.chest_equip = None
        self.is_conscious = True
        self.weaknesses = []
        self.resistances = []
        self.abilities = []

    def get_max_hp(self):
        return self.max_hp

    def get_max_mp(self):
        return self.max_mp

    def get_current_hp(self):
        return self.current_hp
    
    def get_current_mp(self):
        return self.current_mp

    def get_job(self):
        return self.job

    def equip_item(self, equipment):
        old_equipment = None

        if not equipment.is_equippable:
            raise Exception("Not an equippable item.")

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

    def restore_hp(self, amount):
        restored_hp = min(self.current_hp + amount, self.max_hp)
        self.current_hp = restored_hp

    def restore_mp(self, amount):
        restored_mp = min(self.current_mp + amount, self.max_mp)
        self.current_mp = restored_mp

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.fall_unconscious()
        
    def use_mp(self, amount):
        if amount >= self.current_mp:
            raise Exception("Cannot spend more mp than one has.")
        
        self.current_mp -= amount

    def fall_unconscious(self):
        self.is_conscious = False

    def turn_increment(self, count=1):
        # TODO should increment all abilities and proc any turn-based status effects. E.g., taking a tick of damage from poison.
        # count is number of increments. Potentially enable a "hasted" effect that allows for more increments per turn.
        
        for ability in self.abilities:
            if ability.cost_type == "turn_based":
                ability.turn_increment()
        

    def learn_ability(self, ability):
        self.abilities.append(ability)
        self.abilities = sorted(
            self.abilities,
            key=lambda a: (a.effect_type, a.name)
        )

    def list_abilities(self):
        abilities_list = []
        for ability in self.abilities:
            abilities_list.append(ability.name)
        return abilities_list
    
    def reset_abilities(self):
        for ability in self.abilities:
            ability.reset()

    def reset_battle_abilities(self):
        # TODO  Have to test this, esp, the charge_based check.
        for ability in self.abilities:
            if ability.cost_type == "charge_based" and ability.reset_type == "daily":
                print(f"Found a daily ability: {ability.name}")
                continue
            ability.reset()

    def __repr__(self):
        return f"\n----------\nCombatant: {self.get_name()}\nDescription: {self.get_description()}\n\nJob: {self.get_job().capitalize()}\n\nHP: {self.get_current_hp()} / {self.get_max_hp()}\nMP: {self.get_current_mp()} / {self.get_max_mp()}\n----------\n"
        

