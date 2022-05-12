import os
import discord
from discord.ext import commands

class Cupid(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=['.'],
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print(f"{self.user} is ready and goot to go")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
                print(f"cogs.{filename[:-3]} loaded")


bot = Cupid()
bot.run("OTczMjY1NTU5NDE4NDQ1OTQ1.GUuSMy.7krscdAXYwIzFbzKZnQGOWxbrgxVK1VCdednRw")
