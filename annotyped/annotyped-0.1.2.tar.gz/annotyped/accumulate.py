from inspect import Parameter


DEFAULT_KINDS = [Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD]


def accumulate(args: tuple, kwargs: dict, params, kinds: list = None):
    '''accumulate gathers and yields all args / kwargs that have annotations matching the given kinds list.

    kinds should be a list of Parameter.kind.
    eg: [Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD]
    '''
    kinds = kinds or DEFAULT_KINDS

    kwargs.update(
        { param.name: args[index]
            for index, param in enumerate(params.values())
                if index < len(args)
                and param.kind in kinds
        }
    )

    for name, value in kwargs.items():
        param = params.get(name, None)

        if (param is None or param.default == value
        or param.annotation == param.empty):
            continue

        yield (name, value, param)
