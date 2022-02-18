import os
import random
import time

import discord
from discord.ext import commands
endStudy = False

bot = commands.Bot(command_prefix='lofi.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="lofi.help"))

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="A Lo-fi Discord Bot to relax / study to.", description= "🍵 - lofi.help - This command!\n"
                                                                                         "🐉 - lofi.image - Posts a random aesthetic lofi image.\n"
                                                                                        "☕ - lofi.play - Plays 24/7 Lofi Music\n"
                                                                                        "🥝 - lofi.pause - Pauses playing music\n"
                                                                                        "🥑 - lofi.resume - Resumes playing music\n"
                                                                                        "🧋 - lofi.stop - Stops playing music\n"
                                                                                        "🌿 - lofi.join - Joins the bot to your voice channel\n"
                                                                                        "⛰ - lofi.leave - Disconnects the bot from your voice channel\n", color=discord.Color.dark_green())
    embed.set_footer(text="by Kabuto")
    await ctx.send(embed=embed)

@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def image(ctx):
    randomImage = random.choice(os.listdir("./Images"))
    image = './Images/' + randomImage
    imageFile = discord.File(image, filename=randomImage)
    await ctx.send(file=imageFile)

@bot.command()
async def play(ctx):
    randomImage = random.choice(os.listdir("./Images"))
    image = './Images/' + randomImage

    randomfile = random.choice(os.listdir("./songs"))
    file = './songs/' + randomfile

    embed = discord.Embed(title="▶  Now Playing...",
                          description="☕ - " + randomfile,
                          color=discord.Color.dark_green())

    imageFile = discord.File(image, filename=randomImage)
    embed.set_image(url="attachment://"+randomImage)
    await ctx.send(file=imageFile, embed=embed)
    channel = ctx.message.author.voice.channel

    def playmusic():
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(file))

    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        playmusic()
        return
    if (ctx.voice_client is None):
        await channel.connect()
        playmusic()
    else:
        playmusic()

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No audio is paused.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

bot.run("BOTTOKEN")