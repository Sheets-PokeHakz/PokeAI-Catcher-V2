import re
import json
import random
import string
import aiohttp
import asyncio
import discord
import numpy as np
from PIL import Image
from io import BytesIO
from discord import Webhook
from discord.ext import commands, tasks
from tensorflow.keras.models import load_model

# Config Initialisation
with open("PokeAi-2/Config.json", "r") as f:
    config = json.load(f)

token = config["BOT"]["Token"]
prefix = config["BOT"]["Prefix"]

# Webhook Initialisation
async def webhook_send(embed):
    webhook_url = config["WEBHOOK"]["Webhook"]
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed, username="PokeTwo Self Bot")


# Colour Config
class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


# Spam Config
is_spam = config["SPAM"]["Spam"]

# Bot Initialisation
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

# Model Initialisation
loaded_model = load_model("PokeAi-2/Model.h5", compile=False)
with open("PokeAi-2/Classes.json", "r") as f:
    classes = json.load(f)
with open("PokeAi-2/Pokemon", "r", encoding="utf8") as file:
    pokemon_list = file.read()

# Catch Count Updater
def update_count():
    config["CATCH"]["Count"] += 1
    with open("PokeAi-2/Config.json", "w") as f:
        json.dump(config, f, indent=4)

def count_reset():
    config["CATCH"]["Count"] = 1
    with open("PokeAi-2/Config.json", "w") as f:
        json.dump(config, f, indent=4)

# Hint Solver
def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    return re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)


async def catch(message: discord.Message):
    c = await bot.loop.run_in_executor(None, solve, message.content)
    ch = message.channel
    if not len(c):
        await ch.send("Couldn't Find The Pokemon")
    else:
        for i in c:
            await ch.send(f"<@716390085896962058> c {i}")


# Image Prediction
async def preprocess_image(image):
    image = image.resize((64, 64))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@bot.event
async def on_ready():
    print(f"{Color.YELLOW}+ ------------ PokeTwo Self Bot -----------------{Color.END}")
    print("+ -----------------------------------------------")
    print(f"{Color.GREEN}+ ---- ID : {bot.user.id}     {Color.END}")
    print("+ -----------------------------------------------")
    print(f"{Color.GREEN}+ ---- User : {bot.user.name} {Color.END}")
    print("+ -----------------------------------------------")
    print(f"+ {Color.GREEN}---- Status : Online        {Color.END}")
    print("+ -----------------------------------------------")

    count_reset()

    if is_spam == "Enabled":
        print(f"{Color.GREEN}+ ---- Spam : Enabled        {Color.END}")
        print("+ -----------------------------------------------")
        spam.start()

    


# Spam Features
spam_id = config["SPAM"]["Channel"]
intervals = config["SPAM"]["Intervals"]


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    if spam_id == "None":
        return

    spam_channel = bot.get_channel(spam_id)
    if spam_channel is None:
        print(f"{Color.RED}+ ---- Error : Channel Not Found{Color.END}")
        return

    spam_message = "".join(random.choices(string.ascii_letters + string.digits, k=50))
    if spam_message == "":
        return

    messages = open("PokeAi-2/Messages/Messages.txt", "r").readlines()
    multi_spam_message = random.choice(messages)

    spam_type = [spam_message, multi_spam_message]
    await spam_channel.send(random.choice(spam_type))


def enable_spam():
    config["SPAM"]["Spam"] = "Enabled"
    with open("PokeAi-2/Config.json", "w") as f:
        json.dump(config, f, indent=4)


def disable_spam():
    config["SPAM"]["Spam"] = "Disabled"
    with open("PokeAi-2/Config.json", "w") as f:
        json.dump(config, f, indent=4)


@bot.command()
async def start(ctx):
    enable_spam()
    spam.start()
    embed = discord.Embed(
        title="Spam Enabled",
        description=f"Spam Has Been Enabled\nSpam Channel: <#{spam_id}>",
        color=discord.Color.green(),
    )
    await webhook_send(embed)


@bot.command()
async def stop(ctx):
    disable_spam()
    spam.stop()
    embed = discord.Embed(
        title="Spam Disabled",
        description="Spam Has Been Disabled",
        color=discord.Color.red(),
    )
    await webhook_send(embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="PokeTwo Self Bot",
        description="PokeTwo Self Bot Is A Discord Self Bot That Can Be Used To Spam Messages In A Channel",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="Commands",
        value="`start` - Start The Spam \n`stop` - Stop The Spam \n`help` - Show This Message",
        inline=False,
    )
    await webhook_send(embed)

@bot.command()
async def incense(ctx):
    config["CATCH"]["Incense"] = "True"
    with open("PokeAi-2/Config.json", "w") as f:
        json.dump(config, f, indent=4)
    await ctx.send("Incense Enabled")

@bot.event
async def on_message(message):

    guilds = config["GUILDS"]["Guilds"]

    if message.author.id == bot.user.id or message.guild.id not in guilds:
        return

    if message.author.id == 716390085896962058:
        if len(message.embeds) > 0:
            embed = message.embeds[0]

            if "appeared" in embed.title:

                disable_spam()

                if embed and embed.image:

                    url = embed.image.url
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url=url) as resp:
                            if resp.status == 200:
                                content = await resp.read()
                                image_data = BytesIO(content)
                                image = Image.open(image_data)

                    preprocessed_image = await preprocess_image(image)
                    predictions = loaded_model.predict(preprocessed_image)
                    timerlist = config["CATCH"]["Intervals"]
                    classes_x = np.argmax(predictions, axis=1)
                    name = list(classes.keys())[classes_x[0]]

                    async with message.channel.typing():
                        await asyncio.sleep(random.choice(timerlist))
                        await message.channel.send(f"<@716390085896962058> c {name}")
                        print(f"{Color.GREEN}+ ---- Pokemon : {name}{Color.END}")

        elif "Congratulations" in message.content:
    
            count = config["CATCH"]["Count"]
            update_count()

            incense = config["CATCH"]["Incense"]

            if incense == "True":
                pass

            elif incense == "False":
                enable_spam()

            iv_match = re.search(r"\((.*?)\)", message.content)

            if iv_match:
                iv = iv_match.group(1)

            splitted = message.content.split("!")[1]

            pokemon_name_match = re.search(r"You caught a Level \d+ (.*?)<:", splitted)

            url = ""

            if pokemon_name_match:
                pokemon_name = pokemon_name_match.group(1)
                pokemon_level = re.search(r"Level (\d+)", splitted).group(1)

                embed = discord.Embed(
                    title="Pokemon Caught",
                    description=f"Name : {pokemon_name}\nLevel : {pokemon_level}\n\nIV : {iv}\n\nNumber : {count}",
                    color=discord.Color.green(),
                )

                with open("PokeAi-2/PokeDex.json", "r") as f:
                    pokedex = json.load(f)

                for pokemon in pokedex:
                    if pokemon_name in pokemon.get("title", ""):
                        url=pokemon["image"]["url"]

                if url:
                    embed.set_thumbnail(url=url)

                await webhook_send(embed)

        elif "wrong" in message.content:
            await asyncio.sleep(1)
            await message.channel.send("<@716390085896962058> h")

        elif "The pokémon is" in message.content:
            await asyncio.sleep(1)
            await catch(message)

    await bot.process_commands(message)

bot.run(token)
