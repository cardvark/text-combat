import unittest
import src.tests.test_characters
import sys
import importlib
import os

TEST_PREFIX = "test_"
TEST_PATH = "./src/tests"
MOD_PATH = "src.tests."

def get_test_files(path):
    entries = os.listdir(path)
    test_files = []

    for entry in entries:
        file_path = os.path.join(path, entry)
        if not os.path.isfile(file_path):
            continue
        if entry.startswith(TEST_PREFIX):
            test_files.append(entry)

    return test_files


def main():

    # if len(sys.argv) == 1:
    #     print(f"Running all tests in {TEST_PATH}.")
    #     test_files = get_test_files(TEST_PATH)

    #     for test_file in test_files:
    #         test_mod_name = MOD_PATH + test_file[:-3]
    #         print(test_mod_name)
        
    #         test_mod = importlib.import_module(test_mod_name)
    #         suite = unittest.TestLoader().loadTestsFromModule(test_mod)
    #         unittest.TextTestRunner(verbosity=2).run(suite)
    
    #     return


    try: 
        test_mod = importlib.import_module(sys.argv[1])
    except ImportError as e:
        print(f"Error importing module{e}.")

    suite = unittest.TestLoader().loadTestsFromModule(test_mod)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
