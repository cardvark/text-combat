import unittest
import src.tests.test_characters
import sys
import importlib


def main():

    try: 
        test_mod = importlib.import_module(sys.argv[1])
    except ImportError as e:
        print(f"Error importing module{e}.")

    suite = unittest.TestLoader().loadTestsFromModule(test_mod)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
