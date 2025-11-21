from __future__ import annotations
import src.stat_calcs as scs
from src.abilities import EffectType, CostType, ResetType
from src.command_enums import *
import src.tools as tls
import src.locations as loc
import src.abilities as abs
import src.inventory as inv
import src.environmentals as env

class Combatant(env.Environmental):
    def __init__(self, 
                 name: str, 
                 description: str, 
                 level: int, 
                 job: str, # TODO job enum
                 ) -> None:
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
        self.buffs = []
        self.debuffs = []
        self.current_location = None

    def get_max_hp(self) -> int:
        return self.max_hp

    def get_max_mp(self) -> int:
        return self.max_mp

    def get_current_hp(self) -> int:
        return self.current_hp
    
    def get_current_mp(self) -> int:
        return self.current_mp

    def get_current_hp_perc(self) -> float:
        return self.current_hp / self.max_hp

    def get_current_mp_perc(self) -> float:
        return self.current_mp / self.max_mp

    def get_job(self) -> str:
        # TODO job enum
        return self.job

    def equip_item(self, equipment: tls.Equipment) -> tls.Equipment:
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
    
    def remove_main(self) -> tls.Equipment:
        equipment = self.main_equip
        self.main_equip = None        
        return equipment

    def remove_off(self) -> tls.Equipment:
        equipment = self.off_equip
        self.off_equip = None        
        return equipment

    def remove_chest(self) -> tls.Equipment:
        equipment = self.chest_equip
        self.chest_equip = None        
        return equipment

    def restore_hp(self, amount: int) -> None:
        restored_hp = min(self.current_hp + amount, self.max_hp)
        self.current_hp = restored_hp

    def restore_mp(self, amount: int) -> None:
        restored_mp = min(self.current_mp + amount, self.max_mp)
        self.current_mp = restored_mp

    def take_damage(self, amount: int) -> None:
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.fall_unconscious()
        
    def use_mp(self, amount: int) -> None:
        if amount >= self.current_mp:
            raise Exception("Cannot spend more mp than one has.")
        
        self.current_mp -= amount

    def fall_unconscious(self) -> None:
        self.is_conscious = False

    def turn_increment(self, count: int = 1) -> None:
        for ability in self.abilities:
            ability.turn_increment(count)
        

    def learn_ability(self, ability: abs.Ability) -> None:
        if ability in self.abilities:
            return

        ability.user = self
        self.abilities.append(ability)
        self.abilities = sorted(
            self.abilities,
            key=lambda a: (a.effect_type.name, a.name)
        )

    def list_ability_names(self) -> list[str]:
        abilities_list = []
        for ability in self.abilities:
            abilities_list.append(ability.name)
        return abilities_list

    def get_abilities(self) -> list[abs.Ability]:
        return self.abilities
    
    def reset_abilities(self) -> None:
        for ability in self.abilities:
            ability.reset()

    def reset_battle_abilities(self) -> None:
        for ability in self.abilities:
            if ability.reset_type == ResetType.BATTLE:
                ability.reset()

    def update_current_location(self, location: loc.Location) -> None:
        self.current_location = location

    def __repr__(self) -> str:
        return f"\n----------\nCombatant: {self.get_name()}\nDescription: {self.get_description()}\n\nJob: {self.get_job().capitalize()}\n\nHP: {self.get_current_hp()} / {self.get_max_hp()}\nMP: {self.get_current_mp()} / {self.get_max_mp()}\n----------\n"
        

class NPCCombatant(Combatant):
    def __init__(self, 
        name: str, 
        description: str, 
        level: int, 
        job: str, # TODO job enum
        ) -> None:
        super().__init__(name, description, level, job)
        self.primary_special_ability = None
        self.secondary_special_ability = None
        self.self_heal = None

    def assign_primary(self, ability) -> None:
        self.learn_ability(ability)
        self.primary_special_ability = ability

    def assign_secondary(self, ability) -> None:
        self.learn_ability(ability)
        self.secondary_special_ability = ability
    
    def assign_self_heal(self, ability) -> None:
        self.learn_ability(ability)
        self.self_heal = ability
    
    def get_combat_action(self, inventory: inv.Inventory, enemy: Combatant) -> None:
        pass


class GruntEnemy(NPCCombatant):
    def __init__(self, 
                 name: str, 
                 description: str, 
                 level: int, 
                 job: str, # TODO job enum
                 ) -> None:
        super().__init__(name, description, level, job)
    
    def get_combat_action(self, 
                          inventory: inv.Inventory, 
                          enemy: Combatant,
                          ) -> tuple[Command, abs.Ability | tls.Consumable]:
        if self.get_current_hp_perc() <= 0.5 and self.self_heal.check_ready():
            return Command.USE_ABILITY, self.self_heal
        if self.primary_special_ability.check_ready():
            return Command.USE_ABILITY, self.primary_special_ability
        # if self.secondary_special_ability.check_ready():
        #     return Command.USE_ABILITY, self.secondary_special_ability
        
        return Command.BASIC_ATTACK, None
