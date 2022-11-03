import argparse

from gendiff.generate_diff import generate_diff


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file',
                        type=str,
                        help='Inputs path to the first compared file')
    parser.add_argument('second_file',
                        type=str,
                        help='Inputs path to the second compared file')
    parser.add_argument('-f', '--format',
                        choices=['stylish', 'plain', 'json'],
                        default='stylish',
                        help='Set format of output')
    return parser.parse_args()


def main():
    args = parse_arguments()
    file_path1 = args.first_file
    file_path2 = args.second_file
    formatter = args.format
    print(generate_diff(file_path1, file_path2, formatter))


if __name__ == '__main__':
    main()
