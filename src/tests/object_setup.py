from src.inventory import Inventory
from src.characters import Combatant, GruntEnemy
from src.tools import Potion, Weapon
from src.type_enums import *
from src.command_enums import *
from src.abilities import *


def generate_full_inventory():
    inventory = Inventory(5)

    for i in range(2):
        inventory.add_item(
            Potion("small potion", "a small healing potion of dubious quality", EffectType.HEAL_DIRECT, 20)
        )

    for i in range(2):
        inventory.add_item(
            Potion("medium potion", "a medium healing potion of reasonable quality", EffectType.HEAL_DIRECT, 50)
        )

    for i in range(1):
        inventory.add_item(
            Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)
        )

    return inventory

def generate_player(name):
    
    second_wind = TurnBased(
        "second wind",
        "a self-heal ability",
        5,
        EffectType.HEAL_DIRECT,
        25,
        TargetType.SELF,
        )

    cleave = ChargeBased(
        "cleave",
        "a massive, two-handed strike",
        2,
        EffectType.DMG_MULT,
        2,
        TargetType.OTHER,
        ResetType.BATTLE
    )

    rage = ChargeBased(
        "rage",
        "unrelenting, fathomless rage",
        2,
        EffectType.BUFF,
        1.5,
        TargetType.SELF,
        ResetType.DAILY
    )

    lightning_ability = elementalMagic(
        "lightning bolt",
        "a lightning spell",
        20,
        EffectType.DIRECT_DMG,
        25,
        TargetType.OTHER,
        0.25,
        ElementType.LIGHTNING,
    )

    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)

    player = Combatant(name, "A vaguely nebbish creature.", 5, "fighter")
    
    player.learn_ability(second_wind)
    player.learn_ability(cleave)
    player.learn_ability(rage)
    player.learn_ability(lightning_ability)
    player.equip_item(long_sword)

    return player

def generate_grunt(name, description):
    
    second_wind = TurnBased(
        "second wind",
        "a self-heal ability",
        5,
        EffectType.HEAL_DIRECT,
        25,
        TargetType.SELF,
        )

    cleave = ChargeBased(
        "cleave",
        "a massive, two-handed strike",
        2,
        EffectType.DMG_MULT,
        2,
        TargetType.OTHER,
        ResetType.BATTLE
    )

    claw = DelayBased(
        "claw",
        "a rending strike with vicious claws",
        3,
        EffectType.DIRECT_DMG,
        15,
        TargetType.OTHER,
        starting_delay=5,
        damage_type=DamageType.SLASHING,
    )

    grunt = GruntEnemy(name, description, 5, "fighter")

    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)

    grunt.equip_item(long_sword)
    grunt.learn_ability(cleave)

    grunt.assign_primary(claw)
    grunt.assign_self_heal(second_wind)

    return grunt