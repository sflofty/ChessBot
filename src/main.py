import json

from keep_alive import keep_alive
from discord.ext import commands

db = {}


#  ____________________________
# |
# | FUNCTIONS
# |____________________________

def init():
    # check if bot has entry in database

    with open("database.json", "r") as file_name:
        database = json.load(file_name)

    print("database initialized: {}".format(database))


def save_db():
    # check if bot has entry in database
    with open("database.json", "w") as file_name:
        json.dump(db, file_name)

    print(db)


#  ____________________________
# |
# | COMMANDS: General
# |____________________________

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Successfully logged in as {}".format(bot.user))


# new messages and commands will always land here
@bot.event
async def on_message(message):
    # do nothing on messages from this bot
    if message.author == bot.user:
        return

    # if its a command, it will land here
    await bot.process_commands(message)


#  ____________________________
# |
# | COMMANDS: adding nicknames for Lichess or chess.com
# |____________________________

@bot.command()
async def addLichess(ctx, args):
    # get variables
    server_id = ctx.message.guild.id
    user_id = ctx.message.author.id
    nickname = args

    # check if user exits on Lichess

    # add user to database
    if server_id not in db:
        db[server_id] = {}

    if "users" not in db[server_id]:
        db[server_id]["users"] = {}

    if user_id not in db[server_id]["users"]:
        db[server_id]["users"][user_id] = {}

    db[server_id]["users"][user_id]["Lichess"] = nickname
    save_db()
    await ctx.author.send("Your account {} on Lichess has been added".format(nickname))


#  ____________________________
# |
# |  COMMANDS: requests and offers
# |____________________________

@bot.command()
async def request(ctx, *args):
    # get variables
    server_id = ctx.message.guild.id
    user_id = ctx.message.author.id

    # add user to database
    if server_id not in db:
        db[server_id] = {}

    if "requests" not in db[server_id]:
        db[server_id]["requests"] = {}

    try:
        user_request = {
            "rating-me": args[0],
            "time-control": args[1],
            "website": args[2],
            "rating-you": args[3],
            "voice": args[4]
        }

        if len(args) > 5:
            user_request["notes"] = args[5]

        db[server_id]["requests"][user_id] = user_request

        save_db()
        await ctx.author.send("Your request has been added!:\n{}"
                              .format(json.dumps(request)))

    except Exception as e:
        print(e)
        await ctx.author.send("There was an error accepting your requesting. "
                              "Make sure your input matches the requirements.")


@bot.command()
async def requests(ctx):
    message = "Here are all the open requests:\n```"
    for key in requests:
        message = "{}\n{}: {}".format(message, bot.get_user(key),
                                      requests[key])
    message = message + "```"

    await ctx.channel.send(message)


#  ____________________________
# |
# |  COMMANDS: requests and offers
# |____________________________

init()
keep_alive()

with open("bot_token.json", "r") as file:
    data = json.load(file)
    bot.run(data["token"])
