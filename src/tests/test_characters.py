import unittest

from src.characters import Combatant

class TestCharacters(unittest.TestCase):

    def test_char_creation(self):
        print("\n\nTesting basic character creation.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")
        player2 = Combatant("Maria", "A comely young woman.", 4, "mage")

        print(player1)
        print(player2)
    
    def test_hp_modification(self):
        print("\n\nTesting HP modification.")
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")

        max_hp = player1.get_current_hp()
        expected_current_hp = max_hp

        self.assertEqual(expected_current_hp, 66)

        damage1 = 50
        expected_current_hp -= damage1
        player1.take_damage(damage1)
        self.assertEqual(expected_current_hp, player1.get_current_hp())

        restore1 = 25
        expected_current_hp += restore1
        player1.restore_hp(restore1)
        self.assertEqual(expected_current_hp, player1.get_current_hp())

        restore2 = 500
        player1.restore_hp(restore2)
        self.assertEqual(max_hp, player1.get_current_hp())

    def test_consciousness(self):
        player1 = Combatant("Bob", "A vaguely nebbish creature.", 5, "fighter")

        while player1.is_conscious:
            dmg = 25
            print(f"Player taking {dmg} damage.")
            player1.take_damage(dmg)
            print(f"Health remaining: {player1.get_current_hp()}")
        
        print(f"{player1.get_name()} took too much damage and fell unconscious. Current hp: {player1.get_current_hp()}")

if __name__ == "__main__":
    unittest.main()
