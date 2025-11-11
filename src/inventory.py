

class Inventory:
    def __init__(self, inventory_cap):
        self.bag = []
        self.inventory_cap = inventory_cap

    def get_contents(self):
        return self.bag

    def get_item_list(self, flag=None):
        tups_list = []
        
        match flag:
            case "consumable":
                bag = self.get_consumables()
            case _:
                bag = self.bag

        for item in bag:
            uid = item.uid
            name = item.name
            description = item.description

            item_tup = (uid, name, description)

            tups_list.append(item_tup)
        
        return tups_list
    
    def get_consumables(self):
        consumables = []
        for item in self.bag:
            if item.is_consumable:
                consumables.append(item)
        
        return consumables

    def raise_inventory_cap(self, new_cap):
        self.inventory_cap = new_cap
        return True

    def add_item(self, item):
        if len(self.bag) >= self.inventory_cap:
            return False
        
        self.bag.append(item)
        return True

    def get_item_by_id(self, item_id):
        for item in self.bag:
            if item.uid == item_id:
                found_item = item
                self.bag.remove(item)
                return found_item
        
        return False
        
