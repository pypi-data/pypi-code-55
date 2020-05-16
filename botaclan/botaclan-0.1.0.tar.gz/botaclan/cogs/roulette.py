from discord.ext.commands import Cog, Bot, Context, group
import botaclan.helpers.text
import random
import logging

log = logging.getLogger(__name__)


class Roulette(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name="roulette")
    async def roulette_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Roulette help here")

    @roulette_group.command(name="options")
    async def options(self, ctx: Context, *, content: str):
        items = botaclan.helpers.text.parse_comma_list_message(content)
        chosen = random.choice(items)
        log.debug(f"Message({ctx.message.id} - options - {content}) {chosen}")
        await ctx.send(content=f"I choose {chosen}")


def setup(bot: Bot) -> None:
    """Load the Roulette cog."""
    bot.add_cog(Roulette(bot))
