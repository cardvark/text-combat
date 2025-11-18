import random

BASE_HP = 30
BASE_MP = 25
HP_PER_LEVEL = 5
MP_PER_LEVEL = 3
MISS_CHANCE = 0.125
BASE_DAMAGE_MODIFIER = 1
BASE_CHAR_DAMAGE = 5

jobs_list = [
    "fighter",
    "mage",
    "healer",
    "thief",
]

hp_modifiers = {
    "fighter": 1.2,
    "mage": 0.8,
    "healer": 0.8,
    "theif": 1.0,
}

mp_modifiers = {
    "fighter": 0,
    "mage": 1.2,
    "healer": 1,
    "theif": 0,
}


def calc_max_hp(level, job):
        base_hp = BASE_HP
        hp_per_level = HP_PER_LEVEL
        job_modifier = hp_modifiers[job]
        return int((base_hp + hp_per_level * level) * job_modifier)

def calc_max_mp(level, job):
        base_mp = BASE_MP
        mp_per_level = MP_PER_LEVEL
        job_modifier = mp_modifiers[job]
        return int((base_mp + mp_per_level * level) * job_modifier)

def calculate_hit(character, target):
    # TBD. Can add more stats to add some variability.
    hit = random.random()
    return hit > MISS_CHANCE

def calculate_basic_attack_damage(character, target, dmg_mult=1):
    char_weapon = character.main_equip
    weapon_damage = 0
    dmg_type = "blunt"

    if char_weapon:
        weapon_damage = char_weapon.base_damage
        dmg_type = char_weapon.damage_type

    target_armor = target.chest_equip # does nothing yet.
    char_damage = BASE_CHAR_DAMAGE # can make dependent on stats or something. TBD.
    raw_total_damage = weapon_damage + char_damage

    dmg_modifier = BASE_DAMAGE_MODIFIER * dmg_mult

    if dmg_type in target.weaknesses:
        dmg_modifier += 0.5
    
    if dmg_type in target.resistances:
        dmg_modifier += -0.5
    
    total_damage = random.uniform(raw_total_damage / 2, raw_total_damage * 1.5) * dmg_modifier
    return int(total_damage)

def calculate_dmg_mult_ability_damage(ability, user, target):
    dmg_mult = ability.effect_amount
    return calculate_basic_attack_damage(user, target, dmg_mult)


def calculate_ability_damage(base_damage, damage_type, target):
    target_armor = target.chest_equip # does nothing yet.

    dmg_modifier = BASE_DAMAGE_MODIFIER

    if damage_type in target.weaknesses:
        dmg_modifier += 0.5
    
    if dmg_type in target.resistances:
        dmg_modifier += -0.5
    
    total_damage = random.uniform(raw_total_damage / 2, raw_total_damage * 1.5) * dmg_modifier
    return int(total_damage)
    