from discord.ext import commands


# Handles commands.CommandNotFound
async def handle_command_not_found(_ctx, _error, _next):
    if _ctx.guild:
        _next(_error)
    await _ctx.send_exception(
        f"We don't know where to find the command {_ctx.command.name}. Did you spell it wrong?",
        title="Where? What?",
    )


def setup(handler):
    handler.handles(
        commands.CommandNotFound
    )(handle_command_not_found)
