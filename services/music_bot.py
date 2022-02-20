import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
        self.volume = 1

    # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            if type(self.vc.source) is discord.player.FFmpegPCMAudio:
                self.vc.source = discord.PCMVolumeTransformer(self.vc.source)
                self.vc.source.volume = self.volume
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            if type(self.vc.source) is discord.player.FFmpegPCMAudio:
                self.vc.source = discord.PCMVolumeTransformer(self.vc.source)
                self.vc.source.volume = self.volume
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Jestem dziwką i nie mogę tego pobrać")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await ctx.send("Skipped 8==>")
            # try to play next in the queue if it exists
            await self.play_music()

    @commands.command()
    async def volume(self, ctx: commands.Context, *, volume: int):
        self.vc.source.volume = volume / 100
        self.volume = self.vc.source.volume
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(pass_context=True)
    async def łajcior(self, ctx):
        f = open('./resources/songs.txt', 'r')
        song_list = f.read().splitlines()
        for link in song_list:
            await self.p(ctx, link)
        await ctx.send("ŁAJCIOR :call_me:")
        await ctx.send("https://tenor.com/view/pogu-oooo-pogchamp-twitch-gif-24053886")


        #TODO obsluga bledow z odtwarzaniem - forbidden access do linku z muzyczka, zmienic to ze bota wypierdala po chwilii nieaktywenosci, dodac bass boostera i ustawic go na permissionie :)
        #TODO zmienic rolnika zeby byl malym tekstem a nie plikiem tekstowym



