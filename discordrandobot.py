import discord
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)
        

class ButtonView(discord.ui.View):
    @discord.ui.button(label='Start group roll!', style=discord.ButtonStyle.primary)
    async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):
        final_message = await interaction.message.fetch()
        await rollEndFunc(final_message)
        button.disabled = True
        button.label = "Roll Complete!"
        button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)


def init_insults():
    insults = []
    f = open("insults.txt", "r+")
    for l in f:
        insults.append(l)
    return insults

async def randFunc(startNum, endNum):
    text = random.randint(startNum, endNum)
    print(text)
    return text

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

async def rollEndFunc(message):
    users = [ user async for user in message.reactions[0].users()]

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


async def rollFunc(message):
    parts = message.split('d')
    message = "You rolled: "
    print(parts)
    total = 0
    for i in range(int(parts[0])):
        result = random.randint(0, int(parts[1]))
        message += str(result)
        total += result
        if (i + 1 != parts[0]):
            message +=","

    if (int(parts[0]) > 1):
        message += "\n Total of {0}".format(total)
    return message

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.tree.command()
async def vm(interaction: discord.Interaction):
    """performs vicous mockery"""
    insult = insults[random.randint(0, len(insults))]
    await interaction.response.send_message(f'{insult}')


@client.tree.command(name="random")
@app_commands.describe(
    startnum='start value',
    endnum='end value',
)
async def randnum(interaction: discord.Interaction, startnum: int=0, endnum: int=100):
    """random number gen"""
    res = await randFunc(startnum, endnum)
    await interaction.response.send_message(res)
    
@client.tree.command()
@app_commands.describe(
    die="the amount of dice you want rolled. ie: 2d20, 1d6, 3d100"
)
async def roll(interaction: discord.Interaction, die: str='1d20'):
    """rolls given dice"""
    res = await rollFunc(die)
    await interaction.response.send_message(res)

@client.tree.command()
async def grouproll(interaction: discord.Interaction):
    await interaction.response.send_message("Here's your rolls", view = ButtonView())
    resp = await interaction.original_response()
    await resp.add_reaction("🎲")
            
insults = init_insults()
client.run(os.getenv('TOKEN'))

