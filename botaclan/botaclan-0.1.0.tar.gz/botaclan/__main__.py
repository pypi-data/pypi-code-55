from discord.ext import commands
import botaclan.constants
import discord
import logging

log = logging.getLogger(__name__)

bot = commands.Bot(
    command_prefix=botaclan.constants.COMMAND_PREFIX, case_insensitive=True
)
if botaclan.constants.FEATURE_ROULETTE:
    bot.load_extension("botaclan.cogs.roulette")

if botaclan.constants.FEATURE_CALENDAR:
    bot.load_extension("botaclan.cogs.calendar")


@bot.event
async def on_ready():
    guild = discord.utils.find(
        lambda g: g.id == botaclan.constants.DISCORD_GUILD_ID, bot.guilds
    )
    log.info(f"{bot.user} connected to the following guild {guild.name}({guild.id}):")


bot.run(botaclan.constants.DISCORD_TOKEN)
