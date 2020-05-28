import discord

def standart(title, desc):
    embed = discord.Embed(title = title, description = desc, color = 0xffaaff, timestamp = ntx.message.created_at)
    embed.set_footer(text = ntx.author.name, icon_url = ntx.author.avatar_url)
    return embed

def init(ctx):
    global ntx
    ntx = ctx
