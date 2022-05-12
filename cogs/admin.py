import discord
from discord.ext import commands
from discord.commands import slash_command , Option


class Admin(commands.Cog):
    def __init__(self , bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Admin(bot))
