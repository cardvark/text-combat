import unittest
import src.locations as loc
from src.locations import Direction
import src.characters as char
import src.tools as tls
import src.stat_calcs as sc
from src.inventory import Inventory
import src.tests.location_setup as ls
import src.tests.object_setup as obj
from unittest.mock import patch



class TestStatCalcs(unittest.TestCase):
    def test_001_calculate_hit_chance_distribution_equal(self):
        player = obj.generate_player("bob")
        enemy = obj.generate_grunt("ogre", "A grotesque, gigantic brute.")
        
        num_trials = 10000

        results_counter = {
            True: 0,
            False: 0
        }

        expected_hit_rate = sc.STANDARD_CHANCE_HIT

        for _ in range(num_trials):
            result = sc.calculate_hit(player, enemy)
            results_counter[result] += 1

        actual_hit_rate = results_counter[True] / (results_counter[True] + results_counter[False])

        print("\n\nChecking to within two places...")
        print(f"Expected: {expected_hit_rate}")
        print(f"Actual: {actual_hit_rate}")

        self.assertAlmostEqual(
            expected_hit_rate,
            actual_hit_rate,
            2
        )

    def test_002_calculate_hit_chance_distribution_min(self):
        player = obj.generate_player("bob")
        enemy = obj.generate_grunt("ogre", "A grotesque, gigantic brute.")
        enemy.level = 12
        
        num_trials = 100000

        results_counter = {
            True: 0,
            False: 0
        }

        expected_hit_rate = sc.MIN_CHANCE_HIT

        for _ in range(num_trials):
            result = sc.calculate_hit(player, enemy)
            results_counter[result] += 1

        actual_hit_rate = results_counter[True] / (results_counter[True] + results_counter[False])

        print("\n\nChecking to within two places...")
        print(f"Expected: {expected_hit_rate}")
        print(f"Actual: {actual_hit_rate}")

        self.assertAlmostEqual(
            expected_hit_rate,
            actual_hit_rate,
            2
        )
    
    def test_003_calculate_hit_chance_distribution_max(self):
        player = obj.generate_player("bob")
        enemy = obj.generate_grunt("ogre", "A grotesque, gigantic brute.")
    
        player.level = 12
        
        num_trials = 100000

        results_counter = {
            True: 0,
            False: 0
        }

        expected_hit_rate = sc.MAX_CHANCE_HIT

        for _ in range(num_trials):
            result = sc.calculate_hit(player, enemy)
            results_counter[result] += 1

        actual_hit_rate = results_counter[True] / (results_counter[True] + results_counter[False])

        print("\n\nChecking to within two places...")
        print(f"Expected: {expected_hit_rate}")
        print(f"Actual: {actual_hit_rate}")

        self.assertAlmostEqual(
            expected_hit_rate,
            actual_hit_rate,
            1
        )

    @patch('src.stat_calcs.MIN_CHANCE_HIT', 0.1)
    @patch('src.stat_calcs.STANDARD_CHANCE_HIT', 0.85)
    def test_004_calculate_hit_chance_specific(self):
        player = obj.generate_player("bob")
        enemy = obj.generate_grunt("ogre", "A grotesque, gigantic brute.")
    
        enemy.level = 7 # 2 levels higher than player.

        num_trials = 100000

        results_counter = {
            True: 0,
            False: 0
        }

        expected_hit_rate = 0.55 # using the overriden constant values, and my stat calc math. 

        for _ in range(num_trials):
            result = sc.calculate_hit(player, enemy)
            results_counter[result] += 1

        actual_hit_rate = results_counter[True] / (results_counter[True] + results_counter[False])

        print("\n\nChecking to within two places...")
        print(f"Expected: {expected_hit_rate}")
        print(f"Actual: {actual_hit_rate}")

        self.assertAlmostEqual(
            expected_hit_rate,
            actual_hit_rate,
            1
        )