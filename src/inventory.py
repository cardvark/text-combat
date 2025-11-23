from __future__ import annotations
import src.tools as tls
import uuid

class Inventory:
    def __init__(self, inventory_cap: int) -> None:
        self.bag = []
        self.inventory_cap = inventory_cap


    def get_contents(self) -> list[tls.Holdable]:
        return self.bag


    def get_consumables(self) -> list[tls.Consumable]:
        consumables = []
        for item in self.bag:
            if item.is_consumable:
                consumables.append(item)
        
        return consumables


    def raise_inventory_cap(self, new_cap: int) -> bool:
        if new_cap < self.inventory_cap:
            raise Exception("New capacity should be greater than existing capacity.")

        self.inventory_cap = new_cap

        return True


    def add_item(self, item: tls.Holdable) -> bool:
        if len(self.bag) >= self.inventory_cap:
            return False
        
        self.bag.append(item)
        
        return True #possibly unnecessary.
    

    def remove_item(self, item: tls.Environmental) -> None:
        if item not in self.bag:
            raise Exception("Selected item not in inventory.")
        
        self.bag.remove(item)
