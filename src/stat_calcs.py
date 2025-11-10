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
