from src.environmentals import Environmental
from src.stat_calcs import *

class Equipment(Environmental):
    def __init__(self, name, description, equip_type):
        super().__init__(name, description)
        self.equip_type = equip_type
        self.is_equippable = True


class Weapon(Equipment):
    def __init__(self, name, description, weapon_type, damage_type, base_damage):
        super().__init__(name, description, "weapon")
        self.weapon_type = weapon_type
        self.damage_type = damage_type
        self.base_damage = base_damage


class Consumable(Environmental):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.is_consumable = True


class Potion(Consumable):
    def __init__(self, name, description, potion_type, amount):
        super().__init__(name, description)
        self.is_potion = True
        self.consumable_type = potion_type
        self.amount = amount
