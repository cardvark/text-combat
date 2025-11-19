import src.stat_calcs as scs
import src.combat_functions as cf
import src.print_formatting as pf


def handle_enemy_ability(enemy, chosen_ability, target):
    outcome = cf.use_combatant_ability(enemy, chosen_ability, target)
    outcome_text = pf.format_enemy_ability_outcome_text(chosen_ability, outcome, enemy)
    print(outcome_text)


def handle_enemy_item(enemy, inventory, chosen_item, target):
    #TODO implement item usage for enemies.
    pass


def handle_basic_attack(enemy, target):
    print(f"The {enemy.name} attacks!")
    original_hp_perc = target.current_hp / target.max_hp
    damage = cf.enemy_attack(target, enemy)
    if damage == None:
        return

    print(f"The {enemy.name} strikes you with {enemy.main_equip.name}, dealing {damage} damage.")

    new_hp_perc = target.current_hp / target.max_hp
    pf.damage_flavor(original_hp_perc, new_hp_perc)