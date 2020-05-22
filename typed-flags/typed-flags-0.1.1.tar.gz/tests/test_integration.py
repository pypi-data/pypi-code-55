import sys
import unittest
from typing import List, Literal, Optional, Set, Dict
from unittest import TestCase

from typed_flags import TypedFlags


class EdgeCaseTests(TestCase):
    def test_empty(self) -> None:
        class EmptyFlags(TypedFlags):
            pass

        EmptyFlags().parse_args([])

    def test_empty_add_argument(self) -> None:
        class EmptyAddArgument(TypedFlags):
            def add_arguments(self) -> None:
                self.add_argument("--hi")

        hi = "yo"
        args = EmptyAddArgument().parse_args(["--hi", hi])
        self.assertEqual(args.hi, hi)

    def test_no_typed_args(self) -> None:
        class NoTypedFlags(TypedFlags):
            hi: str = "yay"

        args = NoTypedFlags().parse_args([])
        self.assertEqual(args.hi, "yay")

        hi = "yo"
        args = NoTypedFlags().parse_args(["--hi", hi])
        self.assertEqual(args.hi, hi)

    def test_only_typed_args(self) -> None:
        class OnlyTypedFlags(TypedFlags):
            hi: str = "sup"
            _hidden: str

        args = OnlyTypedFlags().parse_args([])
        self.assertEqual(args.hi, "sup")

        hi = "yo"
        args = OnlyTypedFlags().parse_args(["--hi", hi])
        self.assertEqual(args.hi, hi)

    def test_type_as_string(self) -> None:
        class TypeAsString(TypedFlags):
            a_number: "int" = 3
            a_list: "List[float]" = [3.7, 0.3]

        args = TypeAsString().parse_args([])
        self.assertEqual(args.a_number, 3)
        self.assertEqual(args.a_list, [3.7, 0.3])

        a_number = 42
        a_list = [3, 4, 0.7]

        args = TypeAsString().parse_args(
            ["--a-number", str(a_number), "--a-list"] + [str(i) for i in a_list]
        )
        self.assertEqual(args.a_number, a_number)
        self.assertEqual(args.a_list, a_list)


class RequiredClassVariableTests(TestCase):
    def setUp(self) -> None:
        class RequiredArgumentsParser(TypedFlags):
            arg_str_required: str
            arg_list_str_required: List[str]

        self.TypedFlags = RequiredArgumentsParser()

        # Suppress prints from SystemExit
        class DevNull:
            def write(self, msg):
                pass

        self.dev_null = DevNull()
        self.stderr = sys.stderr
        sys.stderr = self.dev_null

    def test_arg_str_required(self):
        with self.assertRaises(SystemExit):
            self.TypedFlags.parse_args(
                ["--arg-str-required", "tappy",]
            )

    def test_arg_list_str_required(self):
        with self.assertRaises(SystemExit):
            self.TypedFlags.parse_args(
                ["--arg-list-str-required", "hi", "there",]
            )

    def test_both_assigned_okay(self):
        args = self.TypedFlags.parse_args(
            ["--arg-str-required", "tappy", "--arg-list-str-required", "hi", "there",]
        )
        self.assertEqual(args.arg_str_required, "tappy")
        self.assertEqual(args.arg_list_str_required, ["hi", "there"])

    def tearDown(self) -> None:
        sys.stderr = self.stderr


class Person:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False

        return self.name == other.name


class IntegrationDefaultFlags(TypedFlags):
    """Integration default tap"""

    arg_untyped: str = "no"
    arg_str: str = "hello there"
    arg_int: int = -100
    arg_float: float = 77.3
    arg_bool_true: bool = True
    arg_bool_false: bool = False
    arg_str_literal: Literal["mercury", "venus", "mars"] = "mars"
    arg_optional_str: Optional[str] = None
    arg_optional_int: Optional[int] = None
    arg_optional_float: Optional[float] = None
    arg_optional_str_literal: Optional[Literal["english", "spanish"]] = None
    arg_list_str: List[str] = ["hello", "how are you"]
    arg_list_int: List[int] = [10, -11]
    arg_list_float: List[float] = [3.14, 6.28]
    arg_list_str_empty: List[str] = []
    arg_list_str_literal: List[Literal["H", "He", "Li", "Be", "B", "C"]] = ["H", "He"]
    arg_set_str: Set[str] = {"hello", "how are you"}
    arg_set_int: Set[int] = {10, -11}
    arg_set_float: Set[float] = {3.14, 6.28}
    arg_set_str_literal: Set[Literal["H", "He", "Li", "Be", "B", "C"]] = {"H", "He"}
    arg_dict_str_int: Dict[str, int] = {}


class SubclassTests(TestCase):
    def test_subclass(self):
        class IntegrationSubclassFlags(IntegrationDefaultFlags):
            arg_subclass_untyped: int = 33
            arg_subclass_str: str = "hello"
            arg_subclass_str_required: str
            arg_subclass_str_set_me: str = "goodbye"
            arg_float: float = -2.7

        arg_subclass_str_required = "subclassing is fun"
        arg_subclass_str_set_me = "all set!"
        arg_int = "77"
        self.args = IntegrationSubclassFlags().parse_args(
            [
                "--arg-subclass-str-required",
                arg_subclass_str_required,
                "--arg-subclass-str-set-me",
                arg_subclass_str_set_me,
                "--arg-int",
                arg_int,
            ]
        )

        arg_int = int(arg_int)

        self.assertEqual(self.args.arg_str, IntegrationDefaultFlags.arg_str)
        self.assertEqual(self.args.arg_int, arg_int)
        self.assertEqual(self.args.arg_float, -2.7)
        self.assertEqual(self.args.arg_subclass_str_required, arg_subclass_str_required)
        self.assertEqual(self.args.arg_subclass_str_set_me, arg_subclass_str_set_me)


class YamlConfigTests(TestCase):
    def test_yaml_config(self) -> None:
        args = IntegrationDefaultFlags(fromfile_prefix_chars="@").parse_args(["@tests/flags.yaml"])
        self.assertEqual(args.arg_str, "Who are you?")
        self.assertEqual(args.arg_bool_false, False)
        self.assertEqual(args.arg_str_literal, "venus")
        self.assertEqual(args.arg_list_int, [10, 11, 12])

    def test_yaml_edge_cases(self) -> None:
        class _DifficultFlags(TypedFlags):
            numbers: List[int] = [2, 3]
            my_dict: Dict[str, float] = {}

        flags = _DifficultFlags(fromfile_prefix_chars="@").parse_args(["@tests/flags2.yaml"])
        self.assertListEqual(flags.numbers, [])
        self.assertDictEqual(
            flags.my_dict, {"one": 1.0, "quarter": 0.25, "half": 0.5, "minus_two": -2.0}
        )


class DefaultClassVariableTests(TestCase):
    def test_get_default_args(self) -> None:
        args = IntegrationDefaultFlags().parse_args([])

        self.assertEqual(args.arg_untyped, "no")
        self.assertEqual(args.arg_str, "hello there")
        self.assertEqual(args.arg_int, -100)
        self.assertEqual(args.arg_float, 77.3)
        self.assertEqual(args.arg_bool_true, True)
        self.assertEqual(args.arg_bool_false, False)
        self.assertEqual(args.arg_str_literal, "mars")
        self.assertTrue(args.arg_optional_str is None)
        self.assertTrue(args.arg_optional_int is None)
        self.assertTrue(args.arg_optional_float is None)
        self.assertTrue(args.arg_optional_str_literal is None)
        self.assertEqual(args.arg_list_str, ["hello", "how are you"])
        self.assertEqual(args.arg_list_int, [10, -11])
        self.assertEqual(args.arg_list_float, [3.14, 6.28])
        self.assertEqual(args.arg_list_str_empty, [])
        self.assertEqual(args.arg_list_str_literal, ["H", "He"])
        self.assertEqual(args.arg_set_str, {"hello", "how are you"})
        self.assertEqual(args.arg_set_int, {10, -11})
        self.assertEqual(args.arg_set_float, {3.14, 6.28})
        self.assertEqual(args.arg_set_str_literal, {"H", "He"})
        self.assertEqual(args.arg_dict_str_int, {})

    def test_set_default_args(self) -> None:
        arg_untyped = "yes"
        arg_str = "goodbye"
        arg_int = "2"
        arg_float = "1e-2"
        arg_bool_true = False
        arg_bool_false = True
        arg_str_literal = "venus"
        arg_optional_str = "hello"
        arg_optional_int = "77"
        arg_optional_float = "7.7"
        arg_optional_str_literal = "spanish"
        arg_list_str = ["hi", "there", "how", "are", "you"]
        arg_list_int = ["1", "2", "3", "10", "-11"]
        arg_list_float = ["2.2", "-3.3", "2e20"]
        arg_list_str_empty = []
        arg_list_str_literal = ["Li", "Be"]
        arg_set_str = ["hi", "hi", "hi", "how"]
        arg_set_int = ["1", "2", "2", "2", "3"]
        arg_set_float = ["1.23", "4.4", "1.23"]
        arg_set_str_literal = ["C", "He", "C"]
        arg_dict_str_int = ["me=2", "you=3", "they=-7"]

        args = IntegrationDefaultFlags().parse_args(
            [
                "--arg-untyped",
                arg_untyped,
                "--arg-str",
                arg_str,
                "--arg-int",
                arg_int,
                "--arg-float",
                arg_float,
                "--arg-bool-true",
                str(arg_bool_true),
                "--arg-bool-false",
                str(arg_bool_false),
                "--arg-str-literal",
                arg_str_literal,
                "--arg-optional-str",
                arg_optional_str,
                "--arg-optional-int",
                arg_optional_int,
                "--arg-optional-float",
                arg_optional_float,
                "--arg-optional-str-literal",
                arg_optional_str_literal,
                "--arg-list-str",
                *arg_list_str,
                "--arg-list-int",
                *arg_list_int,
                "--arg-list-float",
                *arg_list_float,
                "--arg-list-str-empty",
                *arg_list_str_empty,
                "--arg-list-str-literal",
                *arg_list_str_literal,
                "--arg-set-str",
                *arg_set_str,
                "--arg-set-int",
                *arg_set_int,
                "--arg-set-float",
                *arg_set_float,
                "--arg-set-str-literal",
                *arg_set_str_literal,
                "--arg-dict-str-int",
                *arg_dict_str_int,
            ]
        )

        arg_int = int(arg_int)
        arg_float = float(arg_float)
        arg_optional_int = float(arg_optional_int)
        arg_optional_float = float(arg_optional_float)
        arg_list_int = [int(arg) for arg in arg_list_int]
        arg_list_float = [float(arg) for arg in arg_list_float]
        arg_set_str = set(arg_set_str)
        arg_set_int = {int(arg) for arg in arg_set_int}
        arg_set_float = {float(arg) for arg in arg_set_float}
        arg_set_str_literal = set(arg_set_str_literal)
        arg_dict_str_int = {"me": 2, "you": 3, "they": -7}

        self.assertEqual(args.arg_untyped, arg_untyped)
        self.assertEqual(args.arg_str, arg_str)
        self.assertEqual(args.arg_int, arg_int)
        self.assertEqual(args.arg_float, arg_float)
        # Note: setting the bools as flags results in the opposite of their default
        self.assertEqual(args.arg_bool_true, arg_bool_true)
        self.assertEqual(args.arg_bool_false, arg_bool_false)
        self.assertEqual(args.arg_str_literal, arg_str_literal)
        self.assertEqual(args.arg_optional_str, arg_optional_str)
        self.assertEqual(args.arg_optional_int, arg_optional_int)
        self.assertEqual(args.arg_optional_float, arg_optional_float)
        self.assertEqual(args.arg_optional_str_literal, arg_optional_str_literal)
        self.assertEqual(args.arg_list_str, arg_list_str)
        self.assertEqual(args.arg_list_int, arg_list_int)
        self.assertEqual(args.arg_list_float, arg_list_float)
        self.assertEqual(args.arg_list_str_empty, arg_list_str_empty)
        self.assertEqual(args.arg_list_str_literal, arg_list_str_literal)
        self.assertEqual(args.arg_set_str, arg_set_str)
        self.assertEqual(args.arg_set_int, arg_set_int)
        self.assertEqual(args.arg_set_float, arg_set_float)
        self.assertEqual(args.arg_set_str_literal, arg_set_str_literal)
        self.assertEqual(args.arg_dict_str_int, arg_dict_str_int)


class AddArgumentTests(TestCase):
    def test_positional(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("arg_str")

        arg_str = "positional"
        args = IntegrationAddArgumentFlags().parse_args([arg_str])

        self.assertEqual(args.arg_str, arg_str)

    def test_positional_ordering(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("arg_str")
                self.add_argument("arg_int")
                self.add_argument("arg_float")

        arg_str = "positional"
        arg_int = "5"
        arg_float = "1.1"
        args = IntegrationAddArgumentFlags().parse_args([arg_str, arg_int, arg_float])

        arg_int = int(arg_int)
        arg_float = float(arg_float)

        self.assertEqual(args.arg_str, arg_str)
        self.assertEqual(args.arg_int, arg_int)
        self.assertEqual(args.arg_float, arg_float)

    def test_one_dash(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("-arg-str")

        arg_str = "one_dash"
        args = IntegrationAddArgumentFlags().parse_args(["-arg-str", arg_str])

        self.assertEqual(args.arg_str, arg_str)

    def test_two_dashes(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-str")

        arg_str = "two_dashes"
        args = IntegrationAddArgumentFlags().parse_args(["--arg-str", arg_str])

        self.assertEqual(args.arg_str, arg_str)

    def test_one_and_two_dashes(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("-a", "--arg-str")

        arg_str = "one_or_two_dashes"
        args = IntegrationAddArgumentFlags().parse_args(["-a", arg_str])

        self.assertEqual(args.arg_str, arg_str)

        args = IntegrationAddArgumentFlags().parse_args(["--arg-str", arg_str])

        self.assertEqual(args.arg_str, arg_str)

    def test_not_class_variable(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--non-class-arg")

        arg_str = "non_class_arg"
        self.TypedFlags = IntegrationAddArgumentFlags()
        self.assertFalse(
            "non_class_arg" in self.TypedFlags._get_argument_names()
        )  # ensure it's actually not a class variable
        args = self.TypedFlags.parse_args(["--non-class-arg", arg_str])

        self.assertEqual(args.non_class_arg, arg_str)

    def test_complex_type(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            arg_person: Person = Person("TypedFlags")
            # arg_person_required: Person  # TODO
            arg_person_untyped = Person("TypedFlags untyped")

            # TODO: assert a crash if any complex types are not explicitly added in add_argument
            def add_arguments(self) -> None:
                self.add_argument("--arg-person", type=Person)
                # self.add_argument('--arg_person_required', type=Person)  # TODO
                self.add_argument("--arg-person-untyped", type=Person)

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(args.arg_person, Person("TypedFlags"))
        self.assertEqual(args.arg_person_untyped, Person("TypedFlags untyped"))

        arg_person = Person("hi there")
        arg_person_untyped = Person("heyyyy")
        args = IntegrationAddArgumentFlags().parse_args(
            ["--arg-person", arg_person.name, "--arg-person-untyped", arg_person_untyped.name]
        )
        self.assertEqual(args.arg_person, arg_person)
        self.assertEqual(args.arg_person_untyped, arg_person_untyped)

    def test_repeat_default(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-str", default=IntegrationDefaultFlags.arg_str)

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(args.arg_str, IntegrationDefaultFlags.arg_str)

    def test_conflicting_default(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-str", default="yo dude")

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(args.arg_str, "yo dude")

    # TODO: this
    def test_repeat_required(self) -> None:
        pass

    # TODO: this
    def test_conflicting_required(self) -> None:
        pass

    def test_repeat_type(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-int", type=int)

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(type(args.arg_int), int)
        self.assertEqual(args.arg_int, IntegrationDefaultFlags.arg_int)

        arg_int = "99"
        args = IntegrationAddArgumentFlags().parse_args(["--arg-int", arg_int])
        arg_int = int(arg_int)
        self.assertEqual(type(args.arg_int), int)
        self.assertEqual(args.arg_int, arg_int)

    def test_conflicting_type(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-int", type=str)

        arg_int = "yo dude"
        args = IntegrationAddArgumentFlags().parse_args(["--arg-int", arg_int])
        self.assertEqual(type(args.arg_int), str)
        self.assertEqual(args.arg_int, arg_int)

    # TODO
    def test_repeat_help(self) -> None:
        pass

    # TODO
    def test_conflicting_help(self) -> None:
        pass

    def test_repeat_nargs(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument("--arg-list-str", nargs="*")

        arg_list_str = ["hi", "there", "person", "123"]
        args = IntegrationAddArgumentFlags().parse_args(["--arg-list-str", *arg_list_str])
        self.assertEqual(args.arg_list_str, arg_list_str)

    # TODO: figure out how to check for system exit
    # def test_conflicting_nargs(self) -> None:
    #     class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
    #         def add_arguments(self) -> None:
    #             self.add_argument('--arg_list_str', nargs=3)
    #
    #     arg_list_str = ['hi', 'there', 'person', '123']
    #     self.assertRaises(SystemExit, IntegrationAddArgumentFlags().parse_args(['--arg_list_str', *arg_list_str]))

    def test_repeat_action(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument(
                    "--arg-bool-false", type=eval, default=False, choices=[True, False]
                )

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(args.arg_bool_false, False)

        args = IntegrationAddArgumentFlags().parse_args(["--arg-bool-false", "True"])
        self.assertEqual(args.arg_bool_false, True)

    def test_conflicting_action(self) -> None:
        class IntegrationAddArgumentFlags(IntegrationDefaultFlags):
            def add_arguments(self) -> None:
                self.add_argument(
                    "--arg-bool-false", type=eval, default=True, choices=[True, False]
                )

        args = IntegrationAddArgumentFlags().parse_args([])
        self.assertEqual(args.arg_bool_false, True)

        args = IntegrationAddArgumentFlags().parse_args(["--arg-bool-false", "False"])
        self.assertEqual(args.arg_bool_false, False)


class KnownFlags(TypedFlags):
    arg_int: int = 2


class ParseKnownArgsTests(TestCase):
    arg_int = 3
    arg_float = 3.3

    def test_all_known(self) -> None:
        args = KnownFlags().parse_args(["--arg-int", str(self.arg_int)], known_only=True)
        self.assertEqual(args.arg_int, self.arg_int)
        self.assertEqual(args.extra_args, [])

    def test_some_known(self) -> None:
        args = KnownFlags().parse_args(
            ["--arg-int", str(self.arg_int), "--arg-float", str(self.arg_float)], known_only=True
        )
        self.assertEqual(args.arg_int, self.arg_int)
        self.assertEqual(args.extra_args, ["--arg-float", "3.3"])

    def test_none_known(self) -> None:
        args = KnownFlags().parse_args(["--arg-float", str(self.arg_float)], known_only=True)
        self.assertEqual(args.extra_args, ["--arg-float", "3.3"])


if __name__ == "__main__":
    unittest.main()
