import unittest

from src.characters import *
from src.abilities import *


class TestAbilities(unittest.TestCase):
    def test_turn_based(self):
        print("\n\nTesting turn-based abilities.")

        turns_to_ready = 5

        turn_ability = TurnBased(
            "second wind",
            "a self-heal ability",
            turns_to_ready,
            EffectType.HEAL_DIRECT,
            25,
            TargetType.SELF,
            )
        with self.subTest():
            self.assertEqual(
                turn_ability.check_ready()
                , True
            )

        turn_ability.use_ability()

        with self.subTest():
            self.assertEqual(
                turn_ability.turns_to_ready,
                turns_to_ready
            )
        with self.subTest():
            with self.assertRaises(Exception) as cm:
                turn_ability.use_ability()
                self.assertEqual(
                    str(cm.exception), 
                    "Ability not ready to use."
                )
        
        turn_ability.turn_increment()
        with self.subTest():
            self.assertEqual(
                turn_ability.turns_to_ready,
                4
            )
        
        turn_ability.turn_increment()
        turn_ability.turn_increment()
        turn_ability.turn_increment()
        turn_ability.turn_increment()

        with self.subTest():
            self.assertEqual(
                turn_ability.turns_to_ready,
                0
            )
        
        with self.subTest():
            self.assertEqual(
                turn_ability.check_ready(),
                True
            )

    def test_delay_based(self):
        print("\n\nTesting delay-based abilities.")

        turns_to_ready = 5

        delay_ability = DelayBased(
            "second wind",
            "a self-heal ability",
            turns_to_ready,
            EffectType.HEAL_DIRECT,
            25,
            TargetType.SELF,
            )
        
        with self.subTest():
            self.assertEqual(
                delay_ability.check_ready(),
                False
            )
        
        delay_ability.turn_increment()
        delay_ability.turn_increment()
        delay_ability.turn_increment()
        delay_ability.turn_increment()
        delay_ability.turn_increment()

        with self.subTest():
            self.assertEqual(
                delay_ability.check_ready(),
                True
            )
        
        delay_ability.reset()
        with self.subTest():
            self.assertEqual(
                delay_ability.check_ready(),
                False
            )
        
        delay_ability2 = DelayBased(
            "another second wind",
            "a self-heal ability",
            turns_to_ready,
            EffectType.HEAL_DIRECT,
            25,
            TargetType.SELF,
            8
            )
        
        with self.subTest():
            self.assertEqual(
                delay_ability2.turns_to_ready,
                8
            )
        
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()
        delay_ability2.turn_increment()

        with self.subTest():
            self.assertEqual(
                delay_ability2.check_ready(),
                True
            )

        delay_ability2.use_ability()

        with self.subTest():
            self.assertEqual(
                delay_ability2.turns_to_ready,
                5
            )

        delay_ability2.reset()

        with self.subTest():
            self.assertEqual(
                delay_ability2.check_ready(),
                False
            )

    def test_charge_based(self):
        print("\n\nTesting charge-based abilities.")

        charge_ability = ChargeBased(
            "cleave",
            "a massive, two-handed strike",
            3,
            EffectType.DMG_MULT,
            2,
            TargetType.OTHER,
            ResetType.BATTLE
        )
        
        charge_ability.use_ability()

        with self.subTest():
            self.assertEqual(
                charge_ability.current_charges,
                2
            )

        charge_ability.use_ability()
        charge_ability.use_ability()
        
        with self.subTest():
            self.assertEqual(
                charge_ability.check_ready(),
                False
            )
        
        charge_ability.reset()

        with self.subTest():
            self.assertEqual(
                charge_ability.check_ready(),
                True
            )

        with self.subTest():
            self.assertEqual(
                charge_ability.current_charges,
                3
            )

    def test_inherited_mp_based(self):
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
    
        lightning_ability.use_ability()

        self.assertEqual(
            lightning_ability.current_mp_cost,
            int(1.25 * 20)
        )




class TestCharacterAbilities(unittest.TestCase):

    def use_ability_by_name(self, player, ability_name):
        for ability in player.abilities:
            if ability.name == ability_name:
                ability.use_ability()
                return True
        return False

    def test_ability_list(self):
        print("\n\nTesting abilities list")

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

        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        
        player1.learn_ability(second_wind)
        player1.learn_ability(cleave)
        player1.learn_ability(rage)
        player1.learn_ability(lightning_ability)

        print(player1.list_ability_names())
        # ['rage', 'lightning bolt', 'cleave', 'second wind']

        player1.abilities

        self.use_ability_by_name(player1, "second wind")

        with self.subTest():
            self.assertEqual(
                False,
                player1.abilities[3].check_ready()
            )

        self.use_ability_by_name(player1, "rage")
        self.use_ability_by_name(player1, "rage")
        self.use_ability_by_name(player1, "lightning bolt")
        self.use_ability_by_name(player1, "cleave")

        player1.reset_battle_abilities()

        with self.subTest():
            self.assertEqual(
                player1.abilities[2].check_ready(),
                True
            )
        
        with self.subTest():
            self.assertEqual(
                player1.abilities[0].check_ready(),
                False
            )
        
        player1.reset_abilities()
    
        with self.subTest():
            self.assertEqual(
                player1.abilities[0].check_ready(),
                True
            )

        self.use_ability_by_name(player1, "second wind")
        player1.turn_increment()
        player1.turn_increment()

        with self.subTest():
            self.assertEqual(
                player1.abilities[3].turns_to_ready,
                3
            )

        # print(player1.abilities[0].user)

        with self.subTest():
            self.assertEqual(
                player1.abilities[0].user.name,
                "Bob"
            )
        

