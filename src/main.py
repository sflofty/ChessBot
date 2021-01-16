import os
import json

from keep_alive import keep_alive
from replit import db
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Successfully logged in as {}".format(bot.user))

@bot.event
async def on_message(message):
    
    await bot.process_commands(message)
    await message.channel.purge(limit=None, check=lambda msg: not msg.pinned)


@bot.command()
async def request(ctx, *args):

    request = ""
    for arg in args:
        request = request + " " + arg

    requests = db["requests"]
    requests[ctx.author.id] = request
    db["requests"] = requests

    await ctx.author.send("Your request has been added!")


@bot.command()
async def requests(ctx):
    requests = db["requests"]

    message = "Here are all the open requests:\n```"
    for key in requests:
        message = "{}\n{}: {}".format(message, bot.get_user(key),
                                      requests[key])
    message = message + "```"
    
    await ctx.channel.send(message)


keep_alive()
bot.run(os.getenv("TOKEN"))
