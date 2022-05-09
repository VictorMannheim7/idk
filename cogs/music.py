import discord
from discord.ext import commands
from discord.commands import slash_command , Option
import youtube_dl
from discord import option
from musicbot import utils
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings
from config import config

class Music(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
        self.yt = youtube_dl
        self.guildids = config.GUILDIDS


    @commands.Cog.listener()
    async def on_ready(self):

        for guild in self.bot.guilds:
            print(guild.name)
            await self.register(guild)


    async def register(self , guild):

            guild_to_settings[guild] = Settings(guild)
            guild_to_audiocontroller[guild] = AudioController(self.bot, guild)

            sett = guild_to_settings[guild]

            try:
                await guild.me.edit(nick=sett.get('default_nickname'))
            except:
                pass

                if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
                    return

                vc_channels = guild.voice_channels

                if sett.get('vc_timeout') == False:
                    if sett.get('start_voice_channel') == None:
                        try:
                            await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
                        except Exception as e:
                            print(e)

                    else:
                        for vc in vc_channels:
                            if vc.id == sett.get('start_voice_channel'):
                                try:
                                    await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                                except Exception as e:
                                    print(e)


    @slash_command(
        name="connect",
        description="Connect to a voice channel",
        guild_ids=config.GUILDIDS
        )
    async def _connect(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.uconnect(ctx)

    @slash_command(
        name="disconnect",
        description="Disconnect to a voice channel",
        guild_ids=config.GUILDIDS
        )
    async def _disconnect(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)
        if current_guild is None:
            return await ctx.respond("You aren't in the voice channel")
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.udisconnect(ctx)

    @slash_command(
        name="reset",
        description="idk actually",
        guild_ids=config.GUILDIDS
     )
    async def _restart(
        self,
        ctx
     ):
        current_guild = utils.get_guild(self.bot, ctx)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.respond("{} Connected to {}".format(":white_check_mark:", ctx.author.voice.channel.name))



def setup(bot):
    bot.add_cog(Music(bot))
