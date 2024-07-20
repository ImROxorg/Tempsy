import discord
import asyncio
import json
from discord.ext import commands

# Load token from config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

token = config["TOKEN"]
message_content = "<@800383254389194754> dig"

intents = discord.Intents.all()
bot_prefix = "."
bot = commands.Bot(command_prefix=bot_prefix, case_insensitive=True, self_bot=True, intents=intents)
bot.remove_command("help")

send_message = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def start(ctx):
    global send_message
    send_message = True
    await ctx.send('Starting message spam every 10 seconds.')
    bot.loop.create_task(send_repeated_message(ctx.channel))

@bot.command()
async def stop(ctx):
    global send_message
    send_message = False
    await ctx.send('Stopping message spam.')

async def send_repeated_message(channel):
    global send_message
    while send_message:
        await channel.send(message_content)
        await asyncio.sleep(10)

bot.run(token, bot=False)

