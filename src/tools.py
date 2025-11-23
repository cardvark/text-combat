from __future__ import annotations
from src.environmentals import Environmental
from src.stat_calcs import *
import src.inventory as inv


class Holdable(Environmental):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.inventory = None
        self.is_holdable = True # items that can be placed in an inventory.
        self.is_consumable = False
        self.is_equippable = False
        self.equip_type = None
        self.amount = None
    
    def add_to_inventory(self, inventory: inv.Inventory) -> None:
        self.inventory = inventory
    
    def remove_from_inventory(self) -> None:
        self.inventory = None


class Equipment(Holdable):
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


class Consumable(Holdable):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.is_consumable = True

    def use(self) -> int:
        self.inventory.remove_item(self)
        self.remove_from_inventory()
        return self.amount


class Potion(Consumable):
    def __init__(self, name, description, potion_type, amount):
        super().__init__(name, description)
        self.is_potion = True
        self.consumable_type = potion_type
        self.amount = amount
