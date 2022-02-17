import discord
from discord.ext import commands,tasks
import os
import youtube_dl
import ffmpeg

bot = commands.Bot(command_prefix='lofi.')
bot.remove_command('help')

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="lofi.help"))

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="A Lo-fi Discord Bot to relax / study to.", description="☕ - lofi.play - Plays 24/7 Lofi Music\n"
                                                                                        "🧋 - lofi.stop - Stops playing music\n"
                                                                                        "🍵 - lofi.help - This command!\n"
                                                                                        "☕ - lofi.startstudy - Begins the study timer\n"
                                                                                        "🍡 - lofi.stopstudy - Ends the study timer\n"
                                                                                        "🌿 - lofi.pomodoro - Links to a web based pomodoro study timer", color=discord.Color.dark_green())
    embed.set_footer(text="by Kabuto")
    await ctx.send(embed=embed)

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def play(ctx):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        url = "https://www.youtube.com/watch?v=-5KAN9_CzSA"
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        embed = discord.Embed(title="▶  Now Playing...",
                              description="☕ - coffee shop radio // 24/7 lofi hip-hop beats",
                              color=discord.Color.dark_green())
        await ctx.send(embed=embed)
    except:
        await ctx.send("The bot is not connected to a voice channel.")


bot.run("OTQzOTY1OTQ5MTQzNDI5MTMw.Yg6uzA.JhZoI-nPhteF0fa6Fs4MLiGN6ak")