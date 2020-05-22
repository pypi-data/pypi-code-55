# -*- coding: utf-8 -*-
'''
    saltpylint.process
    ~~~~~~~~~~~~~~~~~~

    Lint checks to make sure subclasses of Salt's multiprocessing process implementations
    get it's parent run method called.
'''

# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function

import astroid
from saltpylint.checkers import BaseChecker, utils
from pylint.interfaces import IAstroidChecker

MESSAGES = {
    'E3000': (
        'run method from base class %r is not called',
        'super-run-not-called',
        'Failed to call super(MySubClass, self).run()'
    )
}


def _ancestors_to_call(klass_node, method='run'):
    """return a dictionary where keys are the list of base classes providing
    the queried method, and so that should/may be called from the method node
    """
    to_call = {}
    for base_node in klass_node.ancestors(recurs=False):
        try:
            to_call[base_node] = next(base_node.igetattr(method))
        except astroid.InferenceError:
            continue
    return to_call


class ProcessSuperChecker(BaseChecker):

    __implements__ = IAstroidChecker
    name = 'process-super-checks'
    msgs = MESSAGES
    priority = -2

    def visit_functiondef(self, node):
        '''
        :param node: info about a function or method
        :return: None
        '''
        # ignore actual functions
        if not node.is_method():
            return

        if node.name != "run":
            return
        klass_node = node.parent.frame()
        import pprint
        #print('RUN', klass)
        #pprint.pprint(node.__dict__)
        to_call = _ancestors_to_call(klass_node)
        not_called_yet = dict(to_call)
        print('TO CALL')
        pprint.pprint(to_call)
        for stmt in node.nodes_of_class(astroid.Call):
            expr = stmt.func
            if not isinstance(expr, astroid.Attribute) or expr.attrname != 'run':
                continue
            # skip the test if using super
            print('EXPR', expr, expr.__dict__)
            if (
                isinstance(expr.expr, astroid.Call)
                and isinstance(expr.expr.func, astroid.Name)
                and expr.expr.func.name == "super"
            ):
                return
            try:
                for klass in expr.expr.infer():
                    if klass is astroid.Uninferable:
                        continue
                    # The inferred klass can be super(), which was
                    # assigned to a variable and the `run`
                    # was called later.
                    #
                    # base = super()
                    # base.run(...)

                    if (
                        isinstance(klass, astroid.Instance)
                        and isinstance(klass._proxied, astroid.ClassDef)
                        and is_builtin_object(klass._proxied)
                        and klass._proxied.name == "super"
                    ):
                        return
                    if isinstance(klass, objects.Super):
                        return
                    try:
                        del not_called_yet[klass]
                    except KeyError:
                        continue
                        #if klass not in to_call:
                        #    self.add_message(
                        #        "non-parent-init-called", node=expr, args=klass.name
                        #    )
            except astroid.InferenceError:
                continue
        for klass, method in not_called_yet.items():
            if utils.decorated_with(node, ["typing.overload"]):
                continue
            cls = utils.node_frame_class(method)
            if klass.name == "object" or (cls and cls.name == "object"):
                continue
            self.add_message('super-run-not-called', args=klass.name, node=node)

    def _visit_classdef(self, node):
        for base in node.bases:
            if not hasattr(base, 'attrname'):
                continue
            print('BASE', base.attrname)


def register(linter):
    '''
    Required method to auto register this checker
    '''
    linter.register_checker(ProcessSuperChecker(linter))
