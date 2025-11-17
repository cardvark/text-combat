from enum import Enum

class EffectType(Enum):
    HEALING = "healing"
    DIRECT_DMG = "damage"
    DMG_MULT = "damage multiplier"
    BUFF = "buff"
    DEBUFF = "debuff"

class CostType(Enum):
    TURN = "turn based"
    MP = "mp based"
    CHARGE = "charge based"

class ResetType(Enum): 
    BATTLE = "battle"
    DAILY = "daily"

class TargetType(Enum):
    SELF = "self"
    OTHER = "other"

class ElementType(Enum):
    FIRE = "fire"
    ICE = "ice"
    WIND = "wind"
    WATER = "water"
    EARTH = "earth"
    LIGHTNING = "lightning"
