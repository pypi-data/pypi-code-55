def operation(el):
    """Визначає, чи текст el є операцією."""
    if el == "+" or el == "-":
        # Унарні операції
        return True
    elif el == " + " or el == " - ":
        # Бінарні операції
        return True
    elif el == " * ":
        return True
    return False


def priority(op):
    """Визначає пріоритет операції op."""
    if op == "(":
        return 0
    if op == ")":
        return 1
    if op == " + ":
        return 6
    if op == " - ":
        return 6
    if op == " * ":
        return 7
    if op == "+":
        # Унарний +
        return 8
    if op == "-":
        # Унарний -
        return 8
    return 10


def unop(op):
    """Визначає, чи є op унарною операцією."""
    if op == "-":
        return True
    if op == "+":
        return True
    return False