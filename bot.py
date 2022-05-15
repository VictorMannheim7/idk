import os
import traceback
import discord
from discord.ext import commands
from config import config
import jishaku

class Cupid(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=['.','L '],
            intents=discord.Intents.all(),
            owner_ids=set(['526073411773005824','755851235642572971'])
        )

    async def on_ready(self):
        print(f"{self.user} is ready and goot to go")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
                print(f"cogs.{filename[:-3]} loaded")
        self.load_extension('jishaku')



    async def on_application_command_error(self, ctx, error):
        await ctx.respond(''.join(traceback.format_exception(
                type(error), error, error.__traceback__)))

bot = Cupid()


bot.run(str(config.BOT_TOKEN))
