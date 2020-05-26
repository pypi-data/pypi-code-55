#!/usr/bin/env python3
"""
This file should be called after including this package as a git submodule
"""
import argparse
import logging
import rna.dialects


def main():
    """
    Parse arguments and invade.
    """
    parser = argparse.ArgumentParser(description='Project infrastructor.')
    parser.add_argument(
        '--dialect',
        default=None,
        help='Main programming language of your porject. default=python')
    parser.add_argument(
        'base',
        help="Path to base directory of project. This will also be used to "
             "retrieve the project name.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info("Start invasion")

    if args.dialect is None:
        logging.warning("No dialect specified. I will assume 'python'")
        args.dialect = 'python'

    module_cls = getattr(rna.dialects,
                         '{}Module'.format(args.dialect.capitalize()))
    module = module_cls.from_path(args.base)
    module.start_project()

    logging.info("Invasion completed succesfully.")


if __name__ == '__main__':
    main()
