from src.characters import Combatant
from src.tools import *
from src.combat_functions import *
from src.combat_sim import *
from src.inventory import Inventory
from src.abilities import *
from src.type_enums import *
import time

def main():
    player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
    enemy_combatant = Combatant("ogre", "A foul, be-stenched beast looms three spans high.", 6, "fighter")

    stick = Weapon("stick", "A sad, sickly little twig of a weapon.", "mace", "blunt", 3)
    long_sword = Weapon("long sword", "A steel sword of some quality.", "sword", "slashing", 10)
    small_heal = Potion("small healing potion", "A small vial of a wan red liquid.", "healing", 25)
    med_heal = Potion("large healing potion", "A vial of a bright red liquid.", "healing", 50)

    player_inventory = Inventory(10)
    enemy_inventory = Inventory(10)
    items_list = [
       small_heal,
       small_heal,
       med_heal
    ]

    for item in items_list:
        player_inventory.add_item(item)
        enemy_inventory.add_item(item)

    player1.equip_item(stick)
    enemy_combatant.equip_item(long_sword)

    second_wind = TurnBased(
        "second wind",
        "a self-heal ability",
        5,
        EffectType.HEAL_PERCENT,
        0.25,
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

    player1.learn_ability(second_wind)
    player1.learn_ability(cleave)
    player1.learn_ability(lightning_ability)

    player_move = True
    while (player1.is_conscious and enemy_combatant.is_conscious):
        print("\n------------\n")
        if player_move:
            player_turn(player_inventory, player1, enemy_combatant)
            player_move = False
        else:
            time.sleep(1)
            enemy_turn(enemy_inventory, player1, enemy_combatant)
            player_move = True
            time.sleep(1)
    



if __name__ == "__main__":
    main()
