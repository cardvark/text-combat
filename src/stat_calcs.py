import random

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
        base_hp = 30
        hp_per_level = 5
        job_modifier = hp_modifiers[job]
        return int(base_hp * hp_per_level * job_modifier)

def calc_max_mp(level, job):
        base_mp = 25
        mp_per_level = 3
        job_modifier = mp_modifiers[job]
        return int(base_mp * mp_per_level * job_modifier)

def calculate_hit(character, target):
    # TBD. Can add more stats to add some variability.
    hit = random.random()
    return hit > 0.125

def calculate_damage(character, target):
    char_weapon = character.main_equip
    weapon_damage = 0
    dmg_type = "blunt"

    if char_weapon:
        weapon_damage = char_weapon.base_damage
        dmg_type = char_weapon.damage_type

    target_armor = target.chest_equip # does nothing yet.
    char_damage = 5 # can make dependent on stats or something. TBD.
    raw_total_damage = weapon_damage + char_damage

    dmg_modifier = 1

    if dmg_type in target.weaknesses:
        dmg_modifier += 0.5
    
    if dmg_type in target.resistances:
        dmg_modifier += -0.5
    
    total_damage = random.uniform(raw_total_damage / 2, raw_total_damage * 1.5) * dmg_modifier
    return int(total_damage)