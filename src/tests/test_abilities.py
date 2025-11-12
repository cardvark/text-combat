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
            "healing",
            25,
            "self",
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
            "healing",
            25,
            "self",
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

    def test_charge_based(self):
        print("\n\nTesting charge-based abilities.")

        charge_ability = ChargeBased(
            "cleave",
            "a massive, two-handed strike",
            3,
            "damage_multiplier",
            2,
            "other",
            "battle"
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
            "healing",
            25,
            "self",
            )

        cleave = ChargeBased(
            "cleave",
            "a massive, two-handed strike",
            2,
            "damage_multiplier",
            2,
            "other",
            "battle"
        )

        rage = ChargeBased(
            "rage",
            "unrelenting, fathomless rage",
            2,
            "buff",
            1.5,
            "self",
            "daily"
        )

        lightning_ability = elementalMagic(
            "lightning bolt",
            "a lightning spell",
            20,
            "damaging",
            25,
            "other",
            0.25,
            "lightning"
        )

        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        
        player1.learn_ability(second_wind)
        player1.learn_ability(cleave)
        player1.learn_ability(rage)
        player1.learn_ability(lightning_ability)

        print(player1.list_abilities())
        # ['rage', 'cleave', 'lightning bolt', 'second wind']

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
                player1.abilities[1].check_ready(),
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