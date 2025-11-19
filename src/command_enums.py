from enum import Enum

class Command(Enum):
    BASIC_ATTACK = "attack"
    USE_ABILITY = "use_combatant_ability"
    USE_CONSUMABLE = "use_consumable"