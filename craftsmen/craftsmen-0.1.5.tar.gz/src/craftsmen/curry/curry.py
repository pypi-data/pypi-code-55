from .placeholder import _placeholders_memo, _is_placeholder

def _concat_args(placeholders, args):
    args.reverse()
    get_arg = lambda v: args.pop() if _is_placeholder(v) else v
    return tuple([get_arg(v) for v in placeholders.args] + args[::-1])

def _check_len(args_count, placeholders, args):
    args_len = len(args) + placeholders.len
    return args_len >= args_count

def _curry_builder(function, args_count, placeholders, memo_args=()):
    def dummie(*args):
        new_args = memo_args + args
        if _check_len(args_count, placeholders, args=new_args):
            new_args = _concat_args(placeholders, args=list(new_args))
            return function(*new_args)
        else:
            return _curry_builder(
                function,
                args_count,
                placeholders,
                memo_args=new_args,
            )
    return dummie

def curry(function):
    args_count = function.__code__.co_argcount
    # args_names = function.__code__.co_varnames
    def dummie_initializer(*args):
        dummie = _curry_builder(
            function,
            args_count,
            placeholders=_placeholders_memo(args),
        )
        empty_args = ()
        return dummie(*empty_args)
    return dummie_initializer
