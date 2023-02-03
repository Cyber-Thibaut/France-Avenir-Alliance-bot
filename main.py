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
bot = commands.Bot()

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

@bot.slash_command(name="help")
async def help(ctx):
    embed=discord.Embed(title="Bonjour je suis l'Assistant de direction de l'alliance France Avenir", description="Voici la liste des commandes disponibles")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1070035910390992926/1070065518796624044/image.png")
    embed.add_field(name="Pour afficher 3 trains en circulation en ce moment même", value="/spot", inline=False)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/infos", inline=True)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/annonce", inline=True)
    await ctx.respond(embed=embed)

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Ralph la casse 🧱🧱🧱🧱🧱🧱🧱",
                                            permissions = discord.Permissions(
                                                respond_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, respond_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Ralph la casse 🧱🧱🧱🧱🧱🧱🧱":
            return role
    
    return await createMutedRole(ctx)

@bot.slash_command(name="mute", description="Rendre muet un membre")
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.respond(f"{member.mention} a été mute pour {reason} !")

@bot.slash_command(name="unmute", description="Rendre muet un membre")
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.respond(f"{member.mention} a été unmute !")


@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.respond(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.respond(f"L'utilisateur {user} n'est pas dans la liste des bans")
@bot.event
async def on_message_delete(message):
    if message.channel.id == 1041660576180469852:
        await message.channel.send(f"Le message de {message.author} a été supprimé 🚨🚨🚨")

@bot.event
async def on_message_edit(before, after):
    if before.channel.id == 1041660576180469852:
        await before.channel.send(f"{before.author} a édité son message 🚨🚨🚨")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.respond(f"{user} à été kick.")

@bot.slash_command(name="clear")
async def clear(ctx, nombre : int):
    messages = [msg async for msg in ctx.channel.history(limit = nombre)] 
    for message in messages:
        await message.delete()
    await ctx.respond(f'{nombre} message clear')
load_dotenv()
bot.run(os.getenv('TOKEN'))
