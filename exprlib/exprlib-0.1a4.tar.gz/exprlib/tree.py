"""Побудова дерев виразів"""

from exprlib.polish import polish
from exprlib.common import operation, priority, unop


class Tree():
    """Клас дерев виразів."""
    def __init__(self):
        self.op = None
        self.lt = None
        self.rt = None

    def getop(self):
        return self.op

    def getleft(self):
        return self.lt

    def getright(self):
        return self.rt

    def setop(self, op):
        self.op = op

    def setleft(self, left):
        self.lt = left

    def setright(self, right):
        self.rt = right

    def unary(self):
        # Чи операція, розташована в корені дерева, є унарною?
        return self.lt is None

    def binary(self):
        # Чи операція, розташована в корені дерева, є бінарною?
        return self.lt is not None

    def tostring(self):
        res = treeexpr(self)
        return res


def createtree(op, lt, rt):
    """Утворює дерево з бінарною операцією op і піддеревами lt та rt."""
    etree = Tree()
    etree.setop(op)
    etree.setleft(lt)
    etree.setright(rt)
    return etree


def poltree(polexpr):
    """Перетворює вираз expr, заданий оберненим польським записом, в дерево виразу.
    Служить ще одним конструктором класу Tree."""
    if len(polexpr) == 1:
        return polexpr[0]
    etree = Tree()
    stack = []
    for el in polexpr:
        if operation(el):
            etree = Tree()
            etree.setop(el)
            right = stack.pop()
            #if len(stack) > 0:
            if not unop(el):
                left = stack.pop()
                etree.setleft(left)
            etree.setright(right)
            stack.append(etree)
        else:
            stack.append(el)
    return etree


def exprtree(expr):
    """Перетворює вираз expr, заданий у інфіксній формі, в дерево виразу
     через обернений польський запис. Служить ще одним конструктором класу Tree."""
    polexpr = polish(expr)
    etree = poltree(polexpr)
    return etree


def treeexpr(etree, fop="(", lr="lt"):
    """Перетворює дерево виразу etree у вираз інфіксної форми.
    fop - це операція батьківського виразу.
    lr - її лівий операнд ("lt") або правий ("rt").
    Рекурсивна функція."""
    if (etree is True) or (etree is False):
        return str(etree)
    if type(etree) is str:
        return etree
    elif type(etree) is int:
        return str(etree)
    else:
        op = etree.getop()
        rt = etree.getright()
        if (op == "True") or (op == "False"):
            return op
        if etree.unary():
            # Унарна операція
            subtree = op + treeexpr(rt, op, "rt")
            if priority(fop) > priority(op):
                return "(" + subtree + ")"
            else:
                return subtree
        else:
            # Бінарна операція
            lt = etree.getleft()
            subtree = treeexpr(lt, op, "lt") + op + treeexpr(rt, op, "rt")
            if fop == "-":
                return subtree
            elif priority(fop) > priority(op):
                return "(" + subtree + ")"
            elif fop == " - ":
                if op == " * ":
                    subtree = treeexpr(lt, op, "lt") + op + treeexpr(rt, op, "rt")
                else:
                    if lr == "lt":
                        subtree = treeexpr(lt, op, "lt") + op + treeexpr(rt, op, "rt")
                    else:
                        subtree = "(" + treeexpr(lt, op, "lt") + op + treeexpr(rt, op, "rt") + ")"
                return subtree
            else:
                return subtree


def expr_expr(expr):
    """Перетворює заданий вираз expr в дерево і назад."""
    tree = exprtree(expr)
    rexpr = treeexpr(tree)
    return rexpr

