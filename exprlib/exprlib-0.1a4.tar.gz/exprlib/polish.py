"""Цей модуль перетворює вираз з операціями,
заданими в інфіксній формі,
в обернений польский запис.
Обернений польський запис виразу -
це список елементів виразу,
у якому операнди передують операції."""

from exprlib.common import priority


def is_letter(sym):
    """Визначає, чи символ sym є малою латинською літерою."""
    return "a" <= sym <= "z"


def is_digit(sym):
    """Визначає, чи символ sym є цифрою."""
    return "0" <= sym <= "9"


def peek(stack):
    """Видає останній елемент непустого списку stack."""
    ns = len(stack) - 1
    fs = stack[ns]
    return fs


def dijkstra(mode, op, stackop, res):
    """Реалізує алгоритм Дейкстри.
    mode - це тип лексеми:
    u - унарна операція,
    b - бінарна операція,
    ( - дужка,
    v - змінна
    n - число
    e - заключна обробка стеку операцій.
    stackop - це стек операцій,
    res - це результуючий стек елементів виразу."""
    if mode == "v":
        res.append(op)
    elif mode == "n":
        num = int(op)
        res.append(num)
    elif mode == "e":
        ops = stackop.pop()
        res.append(ops)
    else:
        # унарні, бінарні операції або дужки
        if len(stackop) == 0:
            stackop.append(op)
        elif op == "(":
            stackop.append(op)
        elif op == "-" or op == "+":
            # Унарна операція
            stackop.append(op)
        else:
            last = peek(stackop)
            prlast = priority(last)
            priop = priority(op)
            if priop == 0:
                stackop.append(op)
            elif op == ")" and last == "(":
                stackop.pop()
            elif priop > prlast:
                stackop.append(op)
            else:
                while len(stackop) > 0 and priop <= prlast:
                    ops = stackop.pop()
                    res.append(ops)
                    if len(stackop) > 0:
                        last = peek(stackop)
                        prlast = priority(last)
                if last == "(" and op == ")":
                    stackop.pop()
                else:
                    stackop.append(op)


def polish(expr):
    """Здійснюючи лексичний аналіз виразу expr,
    записаного в інфіксній формі,
    готуючи для застосування алгоритму Дейкстри
    для перетворення в обернений польський запис."""
    stackop = []
    res = []
    ident = ""
    num = ""
    op = ""
    for sym in expr:
        if sym == "(":
            dijkstra("(", sym, stackop, res)
        elif sym == ")" or sym == " ":
            if len(ident) > 0:
                # Ідентифікатор
                if ident == "not":
                    # Унарна літерна операція
                    dijkstra("u", ident + " ", stackop, res)
                    ident = ""
                elif ident == "and" or ident == "or":
                    # Бінарна літерна операція
                    dijkstra("b", " " + ident + " ", stackop, res)
                    ident = ""
                else:
                    # Змінна
                    if len(op) > 0 and op != " ":
                        # Унарна операція
                        dijkstra("u", op, stackop, res)
                        # op = ""
                    # elif sym == " ":
                    if sym == " ":
                        op = " "
                    dijkstra("v", ident, stackop, res)
                    ident = ""
            elif len(num) > 0 and op != " ":
                # Число
                if len(op) > 0:
                    # Унарна операція
                    dijkstra("u", op, stackop, res)
                    op = ""
                if sym == " ":
                    op = " "
                dijkstra("n", num, stackop, res)
                num = ""
            elif len(op) > 0:
                # Завершується бінарна операція
                dijkstra("b", op + " ", stackop, res)
                op = ""
            elif sym == " ":
                # Починається бінарна операція
                op = " "
            if sym == ")":
                dijkstra("(", sym, stackop, res)
                op = ""
        elif is_letter(sym):
            ident += sym
        elif is_digit(sym):
            if ident == "":
                num += sym
            else:
                ident += sym
        elif sym == "+" or sym == "-" or sym == "*":
            if op == " ":
                # Бінарна операція
                op = " " + sym
            elif sym == "+" or sym == "-":
                if len(op) > 0:
                    # Декілька унарних операцій підряд
                    dijkstra("u", op, stackop, res)
                op = sym
        elif sym == "=":
            op += sym
        elif sym == "!":
            op += sym
        elif sym == "<":
            op += sym
        elif sym == ">":
            op += sym
    if len(ident) > 0:
        dijkstra("v", ident, stackop, res)
        if len(op) > 0:
            # Унарна операція
            dijkstra("u", op, stackop, res)
    if len(num) > 0:
        dijkstra("n", num, stackop, res)
        if len(op) > 0:
            # Унарна операція
            dijkstra("u", op, stackop, res)
    while len(stackop) > 0:
        dijkstra("e", op, stackop, res)
    return res
