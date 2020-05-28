import discord

def standart(title, desc, img = None):
    embed = discord.Embed(title = title, description = desc, color = 0xffaaff, timestamp = ntx.message.created_at)
    embed.set_footer(text = ntx.author.name, icon_url = ntx.author.avatar_url)
    if img != None:
        embed.set_image(url=img)
    return embed

def init(ctx):
    global ntx
    ntx = ctx
