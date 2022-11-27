import discord
from discord.ext import commands
import subprocess
import sys
import os # default module
from dotenv import load_dotenv
import linecache
from random import choice
intents = discord.Intents.default()
intents.message_content = True
version = "0.1.1"
from selenium import webdriver
import geckodriver_autoinstaller

driver = webdriver.Firefox()
bot = commands.Bot()

print ("Firefox ✔")
# démarrage
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="la version " + version))

@bot.slash_command(name="travaux")
async def travaux(ctx, message: discord.Option(str)):
    embed = discord.Embed(
        title="Attention Travaux",
        description=message,
        color=0xE55D27, # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name="Autorité de régulation", icon_url="https://media.discordapp.net/attachments/1044705168534556755/1046468665832378478/travaux.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1044705168534556755/1046461698896318524/image.png")
    await ctx.respond("", embed=embed)

@bot.slash_command(name="annonce")
async def annonce(ctx, message: discord.Option(str)):
    embed = discord.Embed(
        title="Annonce",
        description=message,
        color=0xFF1616, # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name="Autorité de régulation", icon_url="https://media.discordapp.net/attachments/1044705168534556755/1046468665530392636/annonce.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1044705168534556755/1046449552036729012/image.png")
    await ctx.respond("", embed=embed)

@bot.slash_command(name="info")
async def info(ctx, message: discord.Option(str)):
    embed = discord.Embed(
        title="Information",
        description=message,
        color=0x034DA2, # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name="Concessions", icon_url="https://media.discordapp.net/attachments/1044705168534556755/1046468665182257172/concess.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1044705168534556755/1046461639572082738/image.png")
    await ctx.respond("", embed=embed)

@bot.slash_command(name="spot")
async def spotgm(ctx):

    try:
        message = await ctx.respond("Spot en préparation")
        
        driver.set_window_size(1200, 810)
        driver.get('https://gare-manager.fr/bot_trafic.php')
        driver.save_screenshot('spot.png')

        with open('spot.png', "rb") as fh:
            f = discord.File(fh, filename='spot.png')
        await ctx.send(file=f)
        await message.delete()
    except Exception as e:
        await printerror(e, ctx)

async def printerror(e, ctx):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    embed = discord.Embed(
        description = ':red_circle: Quelque chose s\'est mal passé',
        color = discord.Color.from_rgb(215, 2, 2)
    )    

@bot.slash_command(name="help")
async def help(ctx):
    embed=discord.Embed(title="Bonjour je suis l'Assistant de l'Autorité de régulation de Gare Manager", description="Voici la liste des commandes disponibles")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036736309248659526/1046465938427494400/Design_sans_titre.png")
    embed.add_field(name="Pour afficher 4 trains en circulation en ce moment même", value="/spot", inline=False)
    embed.add_field(name="Oups celle-ci est réservée aux concessionnaires ^^", value="/infos", inline=True)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/travaux", inline=True)
    await ctx.respond(embed=embed)
load_dotenv()
bot.run(os.getenv('TOKEN'))
