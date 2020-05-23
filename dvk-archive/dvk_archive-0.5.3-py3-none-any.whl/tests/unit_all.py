#!/usr/bin/env python3

"""Combined unit tests for the dvk_archive package."""

from traceback import print_exc
from argparse import ArgumentParser
from dvk_archive.tests.error.unit_error import test_error as error
from dvk_archive.tests.file.unit_file import test_file as file
from dvk_archive.tests.processing.unit_processing import test_processing as pro
from dvk_archive.tests.reformat.unit_reformat import test_reformat as reformat
from dvk_archive.tests.web.unit_web import test_web as web


def test_all():
    """Run all test cases."""
    try:
        file()
        error()
        pro()
        reformat()
        web()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def test_error():
    """Run error tests."""
    try:
        error()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def test_file():
    """Run file tests."""
    try:
        file()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def test_processing():
    """Run processing tests."""
    try:
        pro()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def test_reformat():
    """Run reformatting tests."""
    try:
        reformat()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def test_web():
    """Run web tests."""
    try:
        web()
        print("\033[32mAll dvk_archive tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def main():
    """
    Run tests specified by command line argument.

    By default, runs all dvk_archive tests.
    """
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-e",
        "--error",
        help="Runs tests for error finding modules.",
        action="store_true")
    group.add_argument(
        "-f",
        "--file",
        help="Runs tests for file handling modules.",
        action="store_true")
    group.add_argument(
        "-p",
        "--processing",
        help="Runs tests for internal processing modules.",
        action="store_true")
    group.add_argument(
        "-r",
        "--reformatting",
        help="Runs tests for file reformatting modules.",
        action="store_true")
    group.add_argument(
        "-w",
        "--web",
        help="Runs tests for web modules.",
        action="store_true")
    args = parser.parse_args()
    if args.error:
        test_error()
    elif args.file:
        test_file()
    elif args.processing:
        test_processing()
    elif args.reformatting:
        test_reformat()
    elif args.web:
        test_web()
    else:
        test_all()


if __name__ == "__main__":
    main()
