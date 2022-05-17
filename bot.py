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
            intents=discord.Intents.all()
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

    async def is_owner(self, user: discord.User):
        if user == 526073411773005824:  # Implement your own conditions here
            return True

        # Else fall back to the original
        return await super().is_owner(user)

bot = Cupid()


bot.run(str(config.BOT_TOKEN))
