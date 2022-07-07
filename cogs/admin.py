import discord
from discord.ext import commands
from discord.commands import slash_command , Option
import os
import random , asyncio

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


def paginate(lines, chars=1500):
    size = 0
    message = []
    for line in lines:
        if len(line) + size > chars:
            yield message
            message = []
            size = 0
        message.append(line)
        size += len(line)
    yield message


class Admin(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    @commands.command(name='eval', aliases=['evaluate', 'exec'], description='Executes arbitrary python code')
    # @commands.check_any(commands.is_owner())
    @commands.is_owner()
    async def _eval(self, ctx, *, code):

        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "self": self,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "os": os,
            "random": random,
            "asyncio": asyncio,
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        for message in paginate(result):
            result = ''.join(message)
            resultem = discord.Embed(title="Output", description=f"```py\n{result}```")
            await ctx.send(embed=resultem)


def setup(bot):
    bot.add_cog(Admin(bot))
