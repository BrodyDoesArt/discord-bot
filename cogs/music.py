import discord
from discord.ext import commands
from discord.utils import get

from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe

class Music(commands.Cog, name='Musique'):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

            embed = (discord.Embed(title='🎵 Musique en cours :', description=f"[{info['title']}]({info['webpage_url']})", color=discord.Color.blue())
                    .add_field(name='Duration', value=Music.parse_duration(info['duration']))
                    .add_field(name='Requested by', value=author)
                    .add_field(name='Uploader', value=f"[{info['uploader']}]({info['channel_url']})")
                    .add_field(name="Queue", value=f"Empty queue")
                    .set_thumbnail(url=info['thumbnail']))
            
            return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title']}

    async def edit_message(self, ctx):
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) if len(self.song_queue[ctx.guild]) > 1 else "Empty queue"
        embed.set_field_at(index=3, name="File d'attente :", value=content, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue[ctx.guild]) > 1:
            del self.song_queue[ctx.guild][0]
            run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
            voice.play(discord.FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
        else:
            run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
            run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)

    @commands.command(aliases=['p'], brief='!play [url/words]', description='Plays the requested video')
    async def play(self, ctx, *, arg):
        await ctx.channel.purge(limit=1)
        try: channel = ctx.author.voice.channel
        except: await ctx.send("❌ You're not connected to any channel!", delete_after = 5.0)
        else: 
            channel = ctx.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            song = Music.search(ctx.author.mention, arg)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()     

            if not voice.is_playing():
                self.song_queue[ctx.guild] = [song]
                self.message[ctx.guild] = await ctx.send(embed=song['embed'])
                voice.play(discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
                voice.is_playing()
            else:
                self.song_queue[ctx.guild].append(song)
                await self.edit_message(ctx)

    @commands.command(brief='!pause', description='Pauses or resumes the video')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        await ctx.channel.purge(limit=1)
        if voice and voice.is_connected():
            if voice.is_playing():
                await ctx.send('⏸️ Music paused', delete_after = 5.0)
                voice.pause()
            else:
                await ctx.send('⏯️ Music resumed', delete_after = 5.0)
                voice.resume()
        else:
            await ctx.send("❌ I'm not connected to any channel!", delete_after = 5.0)

    @commands.command(aliases=['pass'], brief='!skip', description='Skips the current video')
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)
        if voice and voice.is_playing():
            await ctx.send('⏭️ Music skipped', delete_after = 5.0)
            voice.stop()
        else:
            await ctx.send("❌ I'm not playing any songs!", delete_after = 5.0)

    @commands.command(brief='!remove [video]', description="Removes the video from queue")
    async def remove(self, ctx, *, arg):
        await ctx.channel.purge(limit=1)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            for video in self.song_queue[ctx.guild][1:]:
                if arg.lower() in video['title'].lower():
                    self.song_queue[ctx.guild].remove(video)
            await self.display_message(ctx)
        else:
            await ctx.send("❌ I'm not playing any songs!")

def setup(bot):
    bot.add_cog(Music(bot))
