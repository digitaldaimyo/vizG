# run_tests.py

import pytest

def run_tests():
    # You can specify individual test files or directories here
    pytest_args = ["tests"]  # This will run all tests in the 'tests' directory
    exit_code = pytest.main(pytest_args)
    return exit_code

if __name__ == "__main__":
    exit(run_tests())