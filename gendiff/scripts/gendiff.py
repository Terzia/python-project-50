import argparse

from ..generate_diff import generate_diff


def main():
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
                        type=str,
                        help='Set format of output')
    args = parser.parse_args()
    file_path1 = args.first_file
    file_path2 = args.second_file
    print(generate_diff(file_path1, file_path2))


if __name__ == '__main__':
    main()
