import discord
from discord.ext import commands


class error(commands.Cog):
	def __init__(self , bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_application_command_error(self , ctx , error):
		raise error
		return
		await ctx.respond(error ,ephemeral = True)

def setup(bot):
	bot.add_cog(error(bot))
