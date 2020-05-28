import argparse

from main_app import main_app


def main():
    # create argument parser object
    parser = argparse.ArgumentParser(description='RandAlgo_py')

    parser.add_argument('-q', '--query', type=str, nargs=1,
                        metavar = None, default = None, help = None)

    # parse the arguments from standard input
    args = parser.parse_args()

    RandAlgo_py = main_app()


if __name__ == '__main__':
    main()
