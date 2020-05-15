from hail.utils.java import Env
from hail.ir import Apply, Ref
from hail.ir.renderer import CSERenderer
from hail.expr.types import hail_type
from hail.expr.expressions import construct_expr, expr_any, unify_all
from hail.typecheck import typecheck, nullable, tupleof, anytype


class Function(object):
    def __init__(self, f, param_types, ret_type, name, type_args=()):
        self._f = f
        self._name = name
        self._type_args = type_args
        self._param_types = param_types
        self._ret_type = ret_type

    def __call__(self, *args):
        return self._f(*args)


@typecheck(f=anytype, param_types=hail_type, _name=nullable(str), type_args=tupleof(hail_type))
def define_function(f, *param_types, _name=None, type_args=()):
    mname = _name if _name is not None else Env.get_uid()
    param_names = [Env.get_uid() for _ in param_types]
    body = f(*(construct_expr(Ref(pn), pt) for pn, pt in zip(param_names, param_types)))
    ret_type = body.dtype

    r = CSERenderer(stop_at_jir=True)
    code = r(body._ir)
    jbody = (Env.spark_backend('define_function')
             ._parse_value_ir(code, ref_map=dict(zip(param_names, param_types)), ir_map=r.jirs))

    Env.hail().expr.ir.functions.IRFunctionRegistry.pyRegisterIR(
        mname,
        [ta._parsable_string() for ta in type_args],
        param_names, [pt._parsable_string() for pt in param_types],
        ret_type._parsable_string(),
        jbody)

    @typecheck(args=expr_any)
    def f(*args):
        indices, aggregations = unify_all(*args)
        return construct_expr(Apply(mname, ret_type, *(a._ir for a in args), type_args=type_args), ret_type, indices, aggregations)

    return Function(f, param_types, ret_type, mname, type_args)
