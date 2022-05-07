import os
import discord
from discord import option
from discord.ext import commands
from discord.commands import  Option


bot = commands.Bot(
    comamnd_prefix=['e'],
    intents=discord.Intents.all(),
    debug_guilds=[914830703974305842]
)

cogs = []
for filename in os.listdir('./cogs'):

    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        cogs.append(filename[:-3])
        print(f'cog.{filename[:-3]} loaded')

@bot.event
async def on_ready():
    print(bot.user , discord.__version__)
    print(cogs)


@bot.slash_command(guild_ids=[914830703974305842])
@option("cog", description="Choose the cog", choices=cogs)
async def load(
        ctx: discord.ApplicationContext,
        cog: str
):
    bot.load_extension(f"cogs.{cog}")
    await ctx.respond(cog + " loaded" + cogs)
    pass

@bot.slash_command(guild_ids=[914830703974305842])
@option("cog", description="Choose the cog", choices=cogs)
async def unload(
        ctx: discord.ApplicationContext,
        cog: str
):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.respond(cog + " unloaded")
    pass

@bot.slash_command(guild_ids=[914830703974305842])
@option("cog", description="Choose the cog", choices=cogs)
async def reload(
        ctx: discord.ApplicationContext,
        cog: str
):
    bot.unload_extension(f"cogs.{cog}")
    bot.load_extension(f"cogs.{cog}")
    await ctx.respond(cog + " reloaded")
    pass




bot.run("OTE2NjU2NDU5ODM0NTk3NDE2.YatU2g.X3KDFzW_z_2ryLR3jTcpQ7v0mvA")
