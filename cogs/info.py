import discord
from discord.ext import commands
from discord.commands import slash_command
import psutil
import datetime, time
from config import config

class Info(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
        self.guildids = config.GUILDIDS
        self.psutil = psutil


    @slash_command(name="stats", description="Shows statistics of the bot", guild_ids=config.GUILDIDS)
    async def __stats(self , ctx):
            ramUsage = self.psutil.Process().memory_full_info().rss / 1024**2
            members = 0
            for guild in self.bot.guilds:
                members += guild.member_count - 1
            uptime = time.time() - self.bot.startTime.timestamp()

            day = uptime // (243600)
            uptime = uptime % (243600)
            hour = uptime // 3600
            uptime = uptime % 3600
            min = uptime // 60
            uptime %= 60
            seconds = uptime
            since = '%d d %d h %d m '  %(day , hour, min)
            if round(day) == 0:
              since = '%d h %d m '  %(hour, min)
              pass
            elif round(hour) == 0 and round(day) == 0:
              since ='%d m %s'  %(min, seconds)
            elif round(min) and round(hour) == 0 and round(day) == 0:
               since ='%s'  %(seconds)
            #print(since , hour , day)
            #print('%d d %d h %d m '  %(day , hour, min))
            memory_usage = psutil.Process().memory_info().rss / 1024 ** 2
            cpu_usage = psutil.cpu_percent() / psutil.cpu_count()
            embed = discord.Embed(title=f"",colour=discord.Color.magenta())
            embed.add_field(name=f"Latency:-", value=f" {round(self.client.latency*1000)}",inline=True)
            embed.add_field(name="Servers",value=len(ctx.bot.guilds),inline=True)
            embed.add_field(name="Users",value=len(ctx.bot.users),inline=True)
            embed.add_field(name="Libraries", value=f"Python Version:- 3.8.10 \nDiscord.py Version:- {discord.__version__}",inline=True)
            embed.add_field(name="Statistics", value=f"RAM:- {ramUsage:.2f} \nCPU:- {cpu_usage} \nMemory:- {memory_usage:.2f} \nLast boot: <t:{round(self.client.startTime.timestamp())}:R>" ,inline=True)
            embed.set_footer(text=f"Uptime:- {since}")

            await ctx.respond(embed=embed)


    @commands.command(name="stats", aliases=['statistics'], description='Statistics of the bot')
    async def _stats(self, ctx):

        ramUsage = self.psutil.Process().memory_full_info().rss / 1024**2
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count - 1
        uptime = time.time() - self.bot.startTime.timestamp()

        day = uptime // (243600)
        uptime = uptime % (243600)
        hour = uptime // 3600
        uptime = uptime % 3600
        min = uptime // 60
        uptime %= 60
        seconds = uptime
        since = '%d d %d h %d m '  %(day , hour, min)
        if round(day) == 0:
          since = '%d h %d m '  %(hour, min)
          pass
        elif round(hour) == 0 and round(day) == 0:
          since ='%d m %s'  %(min, seconds)
        elif round(min) and round(hour) == 0 and round(day) == 0:
           since ='%s'  %(seconds)
        #print(since , hour , day)
        #print('%d d %d h %d m '  %(day , hour, min))
        memory_usage = psutil.Process().memory_info().rss / 1024 ** 2
        cpu_usage = psutil.cpu_percent() / psutil.cpu_count()
        embed = discord.Embed(title=f"",colour=discord.Color.magenta())
        embed.add_field(name=f"Latency:-", value=f" {round(self.client.latency*1000)}",inline=True)
        embed.add_field(name="Servers",value=len(ctx.bot.guilds),inline=True)
        embed.add_field(name="Users",value=len(ctx.bot.users),inline=True)
        embed.add_field(name="Libraries", value=f"Python Version:- 3.8.10 \nDiscord.py Version:- {discord.__version__}",inline=True)
        embed.add_field(name="Statistics", value=f"RAM:- {ramUsage:.2f} \nCPU:- {cpu_usage} \nMemory:- {memory_usage:.2f} \nLast boot: <t:{round(self.client.startTime.timestamp())}:R>" ,inline=True)
        embed.set_footer(text=f"Uptime:- {since}")

        await ctx.send(embed=embed)





    @slash_command(name="ping", description="Shows statistics of the bot", guild_ids=config.GUILDIDS)
    async def _ee_stats(self , ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        message = await ctx.respond("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await ctx.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(name="ping",description="Shows the latency of the bot.")
    async def _ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")
def setup(bot):
  bot.add_cog(Info(bot))
