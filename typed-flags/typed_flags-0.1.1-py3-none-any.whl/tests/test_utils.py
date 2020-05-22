import unittest
from typing import Any, Callable, Dict, List, Literal, Set, Tuple, Union
from unittest import TestCase

# get_class_variables
from typed_flags.utils import get_string_literals, type_to_str


class TypeToStrTests(TestCase):
    def test_type_to_str(self) -> None:
        self.assertEqual(type_to_str(str), "str")
        self.assertEqual(type_to_str(int), "int")
        self.assertEqual(type_to_str(float), "float")
        self.assertEqual(type_to_str(bool), "bool")
        self.assertEqual(type_to_str(Any), "Any")
        self.assertEqual(type_to_str(Callable[[str], str]), "Callable[[str], str]")
        self.assertEqual(
            type_to_str(Callable[[str, int], Tuple[float, bool]]),
            "Callable[[str, int], Tuple[float, bool]]",
        )
        self.assertEqual(type_to_str(List[int]), "List[int]")
        self.assertEqual(type_to_str(List[str]), "List[str]")
        self.assertEqual(type_to_str(List[float]), "List[float]")
        self.assertEqual(type_to_str(List[bool]), "List[bool]")
        self.assertEqual(type_to_str(Set[int]), "Set[int]")
        self.assertEqual(type_to_str(Dict[str, int]), "Dict[str, int]")
        self.assertEqual(
            type_to_str(Union[List[int], Dict[float, bool]]), "Union[List[int], Dict[float, bool]]"
        )
        self.assertEqual(type_to_str(Literal["mars", "venus"]), "Literal['mars', 'venus']")
        self.assertEqual(
            type_to_str(List[Literal["mars", "venus"]]), "List[Literal['mars', 'venus']]"
        )


class GetStringLiteralsTests(TestCase):
    def test_get_string_literals(self) -> None:
        shapes = get_string_literals(Literal["square", "triangle", "circle"], "shape")
        self.assertEqual(shapes, ["square", "triangle", "circle"])
        with self.assertRaises(ValueError):
            get_string_literals(Literal["one", 2], "number")


if __name__ == "__main__":
    unittest.main()
