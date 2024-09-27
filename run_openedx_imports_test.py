import os
import django
import importlib.util
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run Open edX imports test.')
    parser.add_argument('--test-file-path', required=True, help='Path to the test file.')
    parser.add_argument('--test-function-name', required=True, help='Name of the test function to execute.')

    args = parser.parse_args()

    django.setup()

    file_path = args.test_file_path
    function_name = args.test_function_name

    # Load the module from the file path
    spec = importlib.util.spec_from_file_location('test_module', file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, function_name)
    func()

if __name__ == '__main__':
    main()
