import inspect


def sig(hub):
    pass


# TODO have grains depend on each other by putting them int the args, similar to how pytest depends on fixutres
async def call(hub, ctx):
    """
    Top level contract for corn collection
    """
    argspec = inspect.getfullargspec(ctx.func)
    kwargs = argspec.kwonlyargs
    if kwargs:
        raise ValueError(
            f"Corn collection functions do not take arguments: {', '.join(kwargs)}"
        )
    args = argspec.args[1:]
    if args:
        raise ValueError(
            f"Corn collection functions do not take arguments: {', '.join(args)}"
        )

    # Ignore all errors in grain collection
    try:
        ret = await ctx.func(ctx.args[0])
        if inspect.iscoroutine(ret):
            ret = await ret
        if ret is not None:
            raise ValueError("Corn collection functions do not return values")
    except Exception as e:
        hub.log.critical(
            f"Exception raised while collecting grains in '{ctx.func.__name__}': {repr(e)}"
        )
        if isinstance(e, AssertionError):
            # Assertion errors are deliberate, let them through
            raise


# These come from corn/init.py and the top level call shouldn't affect them
def call_cli(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_standalone(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_collect(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_run_sub(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_process_subs(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_clean_value(hub, ctx) -> str or None:
    return ctx.func(*ctx.args, **ctx.kwargs)
