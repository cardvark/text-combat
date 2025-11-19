from src.type_enums import *

class Ability:
    def __init__(self, 
        name, 
        description, 
        cost_type, 
        effect_type, 
        effect_amount, 
        effect_target,
        damage_type=None,
        ):
        self.name = name
        self.description = description
        self.cost_type = cost_type
        self.effect_type = effect_type
        self.effect_amount = effect_amount # int
        self.effect_target = effect_target # self, other
        self.reset_type = ResetType.BATTLE
        self.user = None
        self.damage_type = damage_type

    def use_ability(self):
        pass
    
    def reset(self):
        pass

    def turn_increment(self, count=1):
        pass

    def check_ready(self):
        return True


class MPBased(Ability):
    def __init__(self, 
        name, 
        description, 
        mp_cost, 
        effect_type, 
        effect_amount, 
        effect_target,
        cost_modifier,
        damage_type=None,
        ):
        super().__init__(name, description, CostType.MP, effect_type, effect_amount, effect_target, damage_type)
        self.base_mp_cost = int(mp_cost)
        self.current_mp_cost = self.base_mp_cost
        self.cost_modifier = cost_modifier
    
    def use_ability(self):
        self.current_mp_cost = int(self.current_mp_cost * (1 + self.cost_modifier))

    def reset(self):
        self.current_mp_cost = self.base_mp_cost
    
    def check_ready(self):
        return self.current_mp_cost <= self.user.current_mp

class elementalMagic(MPBased):
    def __init__(self,
        name, 
        description, 
        mp_cost, 
        effect_type, 
        effect_amount, 
        effect_target,
        cost_modifier,
        element,
        ):
        super().__init__(
            name, 
            description, 
            mp_cost, 
            effect_type, 
            effect_amount, 
            effect_target,
            cost_modifier,
            damage_type=element
        )


class TurnBased(Ability):
    def __init__(self, 
        name, 
        description,
        max_turns,
        effect_type, 
        effect_amount, 
        effect_target,
        damage_type=None,
        ):
        super().__init__(name, description, CostType.TURN, effect_type, effect_amount, effect_target,damage_type)
        self.max_turns = max_turns
        self.turns_to_ready = 0

    def use_ability(self):
        if not self.check_ready():
            raise Exception("Ability not ready to use.")
        self.turns_to_ready = self.max_turns

    def turn_increment(self, count=1):
        if self.turns_to_ready == 0:
            return
        
        new_total = self.turns_to_ready - count
        self.turns_to_ready = max(new_total, 0)

    def reset(self):
        self.turns_to_ready = 0

    def check_ready(self):
        return self.turns_to_ready == 0


class DelayBased(TurnBased):
    def __init__(self,
        name, 
        description,
        max_turns,
        effect_type, 
        effect_amount, 
        effect_target,
        damage_type=None,
        starting_delay=None,
        ):
        super().__init__(name, description, max_turns, effect_type, effect_amount, effect_target, damage_type)
        self.starting_delay = starting_delay if starting_delay else self.max_turns
        self.turns_to_ready = self.starting_delay

    def reset(self):
        self.turns_to_ready = self.starting_delay


class ChargeBased(Ability):
    def __init__(self, 
        name, 
        description,
        charges,
        effect_type,
        effect_amount,
        effect_target,
        reset_type,
        damage_type=None,
        ):
        super().__init__(name, description, CostType.CHARGE, effect_type, effect_amount, effect_target, damage_type)

        self.total_charges = charges
        self.current_charges = charges
        self.reset_type = reset_type

    def check_ready(self):
        return self.current_charges > 0

    def reset(self):
        self.current_charges = self.total_charges

    def use_ability(self):
        if not self.check_ready():
            raise Exception("No charges remaining; cannot use ability.")
        
        self.current_charges -= 1

    