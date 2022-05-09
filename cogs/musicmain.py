import asyncio

import discord
from config import config
from discord.ext import commands
from musicbot import linkutils, utils
from discord.commands import slash_command , Option


class MusicMain(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
        self.guildids = config.GUILDIDS
    @slash_command(
        name="play",
        description="obv play a song lmao",
        guild_ids=config.GUILDIDS
    )
    async def _play(
        self,
        ctx,
        track: Option(str, "Enter the url or track or sm shit idk", required = True)
    ):
        await ctx.respond(f"{ctx.bot} is processing....")
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) == False:
            return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            await ctx.respond("Loop is enabled! Use {}loop to disable".format(config.BOT_PREFIX))
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.edit(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.edit(content= None ,embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.edit(content= None ,embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.edit(content=config.SONGINFO_PLAYLIST_QUEUED)


    @slash_command(
        name="loop",
        description="loop? udk wt tht means lmao",
        guild_ids=config.GUILDIDS
    )
    async def _loop(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            await ctx.respond("No songs in queue!")
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            await ctx.respond("Loop enabled :arrows_counterclockwise:")
        else:
            audiocontroller.playlist.loop = False
            await ctx.respond("Loop disabled :x:")

    @slash_command(
        name="shuffle",
        description="google the meaning if udk lmao",
        guild_ids=config.GUILDIDS
    )
    async def shuffle(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.respond("Queue is empty :x:")
            return

        audiocontroller.playlist.shuffle()
        await ctx.respond("Shuffled queue :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @slash_command(
        name="pause",
        description="pause the song?",
        guild_ids=config.GUILDIDS
    )
    async def pause(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.respond("Playback Paused :pause_button:")

    @slash_command(
        name="queue",
        description="show the queue ig",
        guild_ids=config.GUILDIDS
    )
    async def queue(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.respond("Queue is empty :x:")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        # Embeds are limited to 25 fields
        if config.MAX_SONG_PRELOAD > 25:
            config.MAX_SONG_PRELOAD = 25

        embed = discord.Embed(title=":scroll: Queue [{}]".format(
            len(playlist.playque)), color=config.EMBED_COLOR)

        for counter, song in enumerate(list(playlist.playque)[:config.MAX_SONG_PRELOAD], start=1):
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)

        await ctx.respond(embed=embed)

    @slash_command(
        name="stop",
        description="stops the music",
        guild_ids=config.GUILDIDS
    )
    async def _stop(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.respond("Stopped all sessions :octagonal_sign:")

    @slash_command(
        name="skip",
        description="skips the song lmao",
        guild_ids=config.GUILDIDS
    )
    async def skip(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.respond("Queue is empty :x:")
            return
        current_guild.voice_client.stop()
        await ctx.respond("Skipped current song :fast_forward:")

    @slash_command(
        name="clear",
        description="clears the queue",
        guild_ids=config.GUILDIDS
    )
    async def clear(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.respond("Cleared queue :no_entry_sign:")

    @slash_command(
        name="resume",
        guild_ids=config.GUILDIDS
    )
    async def res(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()
        await ctx.respond("Resumed playback :arrow_forward:")

    @slash_command(
        name="volume",
        guild_id=config.GUILDIDS
    )
    async def _volume(
        self,
        ctx,
        args: Option(int , "the volume", required=True, min_value=0,max_value=100)
    ):
        if ctx.guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return

        if await utils.play_check(ctx) == False:
            return

        if args == 0:
            await ctx.respond("Current volume: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume))
            return
        a = 1
        # try:
        if a == 1:
            volume = args
            volume = int(volume)
            if volume > 100 or volume < 0:
                raise Exception('')
            current_guild = utils.get_guild(self.bot, ctx)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                await ctx.respond('Volume set to {}% :sound:'.format(str(volume)))
            else:
                await ctx.respond('Volume set to {}% :loud_sound:'.format(str(volume)))
            utils.guild_to_audiocontroller[current_guild].volume = volume
        # except:
        #     await ctx.respond("Error: Volume must be a number 1-100")

    @slash_command(
            name="np",
            description="now playing lmao",
            guild_ids=config.GUILDIDS
    )
    async def np(
        self,
        ctx
    ):
        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.respond(config.NO_GUILD_MESSAGE)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.respond(embed=song.info.format_output(config.SONGINFO_SONGINFO))
def setup(bot):
    bot.add_cog(MusicMain(bot))
