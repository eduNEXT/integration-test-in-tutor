"""
This script runs a specified test function from a given test file to validate Open edX imports.

Usage:
    python run_openedx_imports_test.py --test-file-path <path_to_test_file> --test-function-name <function_name>

The script dynamically loads a Python module from the specified file path and executes the given test function.
"""

import argparse
import importlib.util
import os

import django


def main():
    """
    Parses command-line arguments, sets up the Django environment, dynamically loads the specified test module,
    and executes the given test function to validate Open edX imports.

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Run Open edX imports test.')
    parser.add_argument('--test-file-path', required=True, help='Path to the test file.')
    parser.add_argument('--test-function-name', required=True, help='Name of the test function to execute.')

    args = parser.parse_args()

    # Set up the Django environment to avoid AppNotReady errors
    django.setup()

    file_path = args.test_file_path
    function_name = args.test_function_name

    spec = importlib.util.spec_from_file_location('test_module', file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, function_name)
    func()


if __name__ == '__main__':
    main()
