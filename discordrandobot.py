import discord
import random
import os

client = discord.Client()
rand_prefix = "!rand"
roll_prefix = "!roll"
rollEnd_prefix = "!rollend"

random.seed()
USAGE_RAND_MSG = "Usage: !rand [startNum] [endNum]"
USAGE_ROLL_MSG = "Usage: !roll [description] ------> !rollend [rollID] to finalize"

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def safe_args(args):
    for arg in args:
        if (safe_cast(arg, int) == None):
            return False
    return True

def clean_input(inp):
    tempinp = [];
    if (len(inp) > 0):
        for x in inp:
            if x.strip():
                print(x)
                tempinp.append(x)

    return tempinp

async def randFunc(message):
    args = message.content[len(rand_prefix):].strip().split(' ')
    args = clean_input(args)
    text = ""
    if len(args) == 2:
        for arg in args:
            if (safe_args(args)):
                text = random.randint(safe_cast(args[0], int), safe_cast(args[1], int))
            else:
                text = USAGE_RAND_MSG 
    elif len(args) == 1:
        if (safe_args(args)):
            text = random.randint(0, safe_cast(args[0], int))
        else:                
            text = USAGE_RAND_MSG
    elif len(args) == 0:
        text = random.randint(0,100)
    else:
        text = USAGE_RAND_MSG
    await message.channel.send(text)

async def rollFunc(message):
    args = message.content[len(roll_prefix):].strip()
    parts = args.split(' ')
    print(args, parts)
    text = "Rolling: \n"
    if args:
        text += "> " + args
    roll_message = await message.channel.send(text)
    await roll_message.add_reaction("🎲")
    await message.channel.send("**Use This Roll ID**:\n > " + str(roll_message.id))

async def rollEndFunc(message, client):
    args = message.content[len(rollEnd_prefix):].strip()
    parts = args.split(' ')
    print(args, parts)
    msg_id = -1
    if (len(clean_input(parts)) == 1):
        try:
            msg_id = int(args)
        except (ValueError, TypeError):
            mes_id = -1
    if (msg_id == -1):
        await message.channel.send("Missing/Invalid ID")
    else:    
        updated_msg = await message.channel.fetch_message(msg_id)
        users = await updated_msg.reactions[0].users().flatten()

        results = []
        for u in range(0, len(users)):
            if (users[u] != client.user):
                val = random.randint(0,99)
                results.append((users[u].mention, val))
                await message.channel.send(users[u].mention + " Rolled a " + str(val))

        winner = ("",0)
        for fin in range(0, len(results)):
            if (results[fin][1] > winner[1]):
                winner = results[fin]
        print("winner", winner)
        await message.channel.send(winner[0] + " Wins with a " + str(winner[1]))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    inp = message.content.strip().split(' ')
    print("input: ", inp)
    if (len(inp) >= 1 and inp[0].find("!") != -1):
        command = inp[0]
        print("command: ", command)
        if (command == rand_prefix):
            await randFunc(message)
        elif (command == roll_prefix):
            await rollFunc(message)
        elif (command == rollEnd_prefix):
            await rollEndFunc(message, client)
        elif (command == "!shrek_help"):
            await message.channel.send("Ey Donkeh! This is easy to use! \n> " + USAGE_RAND_MSG + "\n> " + USAGE_ROLL_MSG)
            
    
client.run(os.getenv('TOKEN'))

