import sys

from scruf.compare import RegexError
from scruf.execute import Executor, OutOfLinesError
from scruf.parse import Parser
from scruf.run import run_test, get_failure_lines


def run(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    tests = Parser.parse(lines)
    executor = Executor()
    return tap_runner(tests, executor)


def tap_runner(tests, executor):
    success = True
    print("1..{}".format(len(tests)))
    for i, test in enumerate(tests):
        test_number = i + 1
        test_summary = get_test_summary(test, test_number)
        exec_result = executor.execute(test.command)

        try:
            compare_output = run_test(test, exec_result)
        except (RegexError, OutOfLinesError) as e:
            print(tap_failure(test_summary))
            print(tap_error_line(e), file=sys.stderr)
            success = False
            continue

        failed_tests = [r for r in compare_output if not r["comparison_result"]]
        if len(failed_tests) == 0:
            print(tap_success(test_summary))
        else:
            print(tap_failure(test_summary))
            for test in failed_tests:
                failure_lines = [
                    tap_comment_line("\t" + line) for line in get_failure_lines(test)
                ]
                print("\n".join(failure_lines), file=sys.stderr)
            success = False
    return success


def tap_success(content):
    return "ok " + content


def tap_failure(content):
    return "not ok " + content


def tap_comment_line(content):
    return "# " + content


def tap_error_line(error):
    return tap_comment_line("\t" + str(error))


def get_test_summary(test, test_number):
    test_line = str(test_number)
    if test.description:
        test_line += " - {}".format(test.description.rstrip())
    return test_line
