def string_contains(string: str, substr: str) -> bool:
    """Determines whether substring is part of string or not
    >>> string_contains("hello", "he")
    True
    >>> string_contains("hello", "wo")
    False
    """
    return substr in string


def string_begins_with(string: str, substr: str) -> bool:
    """Determines whether string starts with substring or not
    >>> string_begins_with("hello", "he")
    True
    >>> string_begins_with("hello", "wo")
    False
    """
    return string.startswith(substr)
