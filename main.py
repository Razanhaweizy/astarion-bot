import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import re
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
#define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

bot = commands.Bot(command_prefix='&', intents=intents)

#globals
mha = ["mha", "hero academia", "academia", "my hero academia", "ultra", "dementia", "bakugo", "deku", "ochaco", "todoroki", "all-might", "bkdk", "AFO", "OFA", "kamino"]
hello_responses = ["My daily penance", "You again", "What do you need now?", "You're staring at me again. What do you want?", "Yes?", "Sorry, darling, I haven't got time for underlings. If your boss wants to speak with me, I'm all pointy ears.", "Why in the hells are you bothering me now?"]
random_react = ["acceptance", "investigation", "charm", "virtue", "guess", "letter", "body"]
#event handlers

@bot.event
async def on_ready():
    '''Prints a message to terminal when the bot is successfully running'''
    print(f"{bot.user.name} is ready to commit sins")

@bot.event
async def on_member_join(member):
    '''Sends a message on the server when a new member joins'''
    await member.send(f"Ah, {member.name}, a new traveling companion")

@bot.event
async def on_message(message):
    #bot shouldn't reply to itself, or endless loop
    if message.author == bot.user:
        return
    
    content = message.content.lower()

    if any(re.search(rf"\b{re.escape(keyword)}\b", content) for keyword in mha):
        await message.channel.send("Shut up, shut up, SHUT UP.")

    if any(re.search(rf"\b{re.escape(keyword)}\b", content) for keyword in random_react):
        await message.channel.send("Astarion reacted to your message")
        await message.add_reaction("😈")


    await bot.process_commands(message)

#commands
#TODO add docstring
@bot.command()
async def hello(ctx):
    await ctx.send(f"{random.choice(hello_responses)}")

#TODO add docstring
@bot.command()
async def bomb(ctx, *, message="everyone"):
    gif_url = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZm5hYzBocmZ3czJ3b3hmN2NlZXlrb2pkOHpuNTN6aTFxZWtuNGRwYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT8qBt2943MLRO8zuM/giphy.gif"
    embed = discord.Embed(title=f"{ctx.author} has bombed {message}")
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

@bot.command()
async def menu(ctx):
    '''Help menu showing available commands'''
    embed = discord.Embed(
        title="Astarion Help Menu",
        description="A list of all available commands:",
        color=discord.Color.pink()
    )
    embed.add_field(name="`&hello`", value="Say hello to Astarion :3", inline=False)
    embed.add_field(name="`&bomb <name>`", value="Bomb a friend :P", inline=False)

    await ctx.send(embed=embed)


#actually run the bot
bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)