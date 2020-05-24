from rule_engine.operator import Equals, GreaterThan, In, Contains, Invert


def test_equals():
    operator = Equals()
    assert operator.apply(10, 10)
    assert not operator.apply(10, 11)
    assert not operator.apply(10, "10")
    assert operator.apply([10, 11], [10, 11])
    assert not operator.apply([10, 11], [11, 10])
    assert operator.apply({10, 11}, {10, 11})
    assert operator.apply({10, 11}, {11, 10})


def test_greater_than():
    operator = GreaterThan()
    assert not operator.apply(10, 10)
    assert not operator.apply(10, 11)
    assert operator.apply(12, 10)


def test_in():
    array = ["10", "11", "20"]
    operator = In()
    assert operator.apply("11", array)
    assert not operator.apply("21", array)
    assert operator.apply(
        {"a": 10, "b": 20},
        [{"a": 10, "b": 20}, {"x": 10, "y": 20}, {"x": 100, "b": 20}],
    )
    assert operator.apply(
        {"a": 10, "b": 20},
        [{"b": 20, "a": 10}, {"x": 10, "y": 20}, {"x": 100, "b": 20}],
    )


def test_contains():
    array = ["10", "11", "20"]
    operator = Contains()
    assert operator.apply(array, "10")
    assert not operator.apply(array, "21")


def test_invert():
    array = ["10", "11", "20"]
    operator = Invert()
    assert operator.apply(False)
    assert not operator.apply("10")
    assert not operator.apply(array)
    assert operator.apply(None)
