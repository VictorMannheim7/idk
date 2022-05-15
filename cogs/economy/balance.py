import discord
from discord.ext import commands
from discord.commands import slash_command , Option


class EconomyBalance(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    @slash_command(
        name="balance",
        description="Show the current wallet and bank balance of the user",
        guild_ids=[self.guild_ids]
    )
    async def _balance(
        self,
        ctx,
        user: Option(discord.User, "The user who's balance has to be checked")
    ):
        if user is None:
            user = ctx.author
        balance_embed = discord.Embed(
            title=user
        )
        await ctx.respond(embed=balance_embed)

    @_balance.error
    async def _balanceerror(
        self,
        ctx: discord.ApplicationContext,
        error: discord.error
    ):
        await ctx.respond(error)

def setup(bot):
    bot.add_cog(EconomyBalance(bot))
