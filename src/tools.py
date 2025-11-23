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
        self.inventory.remove_item(self)
        self.inventory = None


class Equipment(Holdable):
    def __init__(
            self, 
            name: str, 
            description: str, 
            equip_type: str, # TODO equip type to enum
            ) -> None:
        super().__init__(name, description)
        self.equip_type = equip_type
        self.is_equippable = True


class Weapon(Equipment):
    def __init__(
            self, 
            name: str, 
            description: str, 
            weapon_type: str, # TODO weapon type enum 
            damage_type: DamageType | ElementType, 
            base_damage: int
            ) -> None:
        super().__init__(name, description, "weapon")
        self.weapon_type = weapon_type
        self.damage_type = damage_type
        self.base_damage = base_damage


class Consumable(Holdable):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.is_consumable = True

    def use(self) -> int:
        self.remove_from_inventory()
        return self.amount


class Potion(Consumable):
    def __init__(
            self, 
            name: str, 
            description: str, 
            potion_type: EffectType, 
            amount: int
            ) -> None:
        super().__init__(name, description)
        self.is_potion = True
        self.consumable_type = potion_type
        self.amount = amount
