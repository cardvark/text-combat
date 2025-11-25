from __future__ import annotations
import random
import src.characters as char
import src.abilities as abs
from src.type_enums import *

BASE_HP = 30
BASE_MP = 25
HP_PER_LEVEL = 5
MP_PER_LEVEL = 3
MISS_CHANCE = 0.125
BASE_DAMAGE_MODIFIER = 1
BASE_CHAR_DAMAGE = 5
DAMAGE_RANGE_MIN = 0.7
DAMAGE_RANGE_MAX = 1.3
MIN_CHANCE_HIT = 0.5
MAX_CHANCE_HIT = 0.975
STANDARD_CHANCE_HIT = 0.85
LEVEL_DIFF_CAP = 5

# to implement:
# HEAL_RANGE_MIN = DAMAGE_RANGE_MIN
# HEAL_RANGE_MAX = DAMAGE_RANGE_MAX

# TODO: Update jobs to enum.

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


def calc_max_hp(
		  level: int, 
		  job: str, # TODO jobs to enums
		  ) -> int:
		base_hp = BASE_HP
		hp_per_level = HP_PER_LEVEL
		job_modifier = hp_modifiers[job]
		return int((base_hp + hp_per_level * level) * job_modifier)

def calc_max_mp(
		  level: int, 
		  job: str, # TODO jobs to enums
		  ) -> int:
		base_mp = BASE_MP
		mp_per_level = MP_PER_LEVEL
		job_modifier = mp_modifiers[job]
		return int((base_mp + mp_per_level * level) * job_modifier)

def calculate_hit(
		character: char.Combatant, 
		target: char.Combatant,
		):
	# TODO: hit chance based on level diff. (can add more variation)

	clevel = character.level
	tlevel = target.level

	level_delta = clevel - tlevel

	if level_delta == 0:
		hit_chance = STANDARD_CHANCE_HIT

	if level_delta < 0:
		level_delta = max(level_delta, -LEVEL_DIFF_CAP)

		# Evenly divides the standard hit chance and the min hit chance, and based on level diff determines hit chance.
		hit_chance = STANDARD_CHANCE_HIT + (STANDARD_CHANCE_HIT - MIN_CHANCE_HIT) / LEVEL_DIFF_CAP * level_delta
	
	if level_delta > 0:
		level_delta = min(level_delta, LEVEL_DIFF_CAP)

		hit_chance = STANDARD_CHANCE_HIT + (MAX_CHANCE_HIT - STANDARD_CHANCE_HIT) / LEVEL_DIFF_CAP * level_delta

	# TODO. Can add more stats to add some variability.
	hit = random.random()
	return hit > (1 - hit_chance)

def damage_amount_randomizer(base_damage: int) -> int:
	damage = random.uniform(base_damage * DAMAGE_RANGE_MIN, base_damage * DAMAGE_RANGE_MAX)
	
	return int(damage)

def calculate_basic_attack_damage(
		  character: char.Combatant, 
		  target: char.Combatant, 
		  dmg_mult: float = 1.0
		  ) -> int:
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
	
	total_damage = damage_amount_randomizer(raw_total_damage) * dmg_modifier

	return int(total_damage)


def calculate_dmg_mult_ability_damage(
		  ability: abs.Ability, 
		  user: char.Combatant, 
		  target: char.Combatant,
		  ) -> int:
	
	if ability.effect_type != EffectType.DMG_MULT:
		raise Exception("Ability effect type is not DMG_MULT (damage multiplier).")
	
	dmg_mult = ability.effect_amount
	return calculate_basic_attack_damage(user, target, dmg_mult)


def calculate_ability_damage(
		base_damage: int, 
		damage_type: int, 
		target: char.Combatant
		) -> int:
	target_armor = target.chest_equip # does nothing yet.

	dmg_modifier = BASE_DAMAGE_MODIFIER

	if damage_type in target.weaknesses:
		dmg_modifier += 0.5
	
	if damage_type in target.resistances:
		dmg_modifier += -0.5
	
	total_damage = damage_amount_randomizer(base_damage) * dmg_modifier

	return int(total_damage)
	