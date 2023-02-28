import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime
import discord
from discord import Option
from discord.ext import commands, create_choice, create_option
from discord.ext.commands import MissingPermissions
from datetime import timedelta
intents = discord.Intents.default()
intents.message_content = True
version = "0.1.1"
bot = commands.Bot()
servers = ['1062738560588972142']

# démarrage
@bot.event  # event decorator/wrapper
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="la version " + version))

@bot.slash_command(name="reglement")
async def open_reglement(ctx):
    modal = ReglementModal(title="Crée le règlement de l'alliance")
    await ctx.response.send_modal(modal)

class ReglementModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Règlement de l'Alliance", 
            color=0x034DA2)
        embed.add_field(name="", value=self.children[0].value)
        embed.set_author(name="Flo & Thibaut les dirlos")   
        embed.set_image(url="https://cdn.discordapp.com/attachments/1070035910390992926/1070065518796624044/image.png")
        message = await bot.get_channel(int(1070036471676940339)).send(embeds=[embed])
        await message.add_reaction('✅')
        await message.add_reaction('❎')
        await interaction.response.send_message("Modal envoyé ^^", ephemeral=True, delete_after=3)

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = discord.utils.get(guild.roles, name='Règlement Approuvé')
    if member is not None and role is not None:
        if payload.emoji.name == '✅':
            await member.add_roles(role)
        elif payload.emoji.name == '❎':
            await member.remove_roles(role)
                
class id(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Information de la direction", 
            color=0x034DA2)
        embed.add_field(name="", value=self.children[0].value)
        embed.set_author(name="Flo & Thibaut les dirlos")   
        embed.set_image(url="https://cdn.discordapp.com/attachments/1070035910390992926/1070065518796624044/image.png")
        await bot.get_channel(int(1070036861403267132)).send(embeds=[embed])
        await interaction.response.send_message("Modal envoyé ^^", ephemeral=True, delete_after=3)

class ad(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Annonce de la direction", 
            color=0xFF1616)
        embed.add_field(name="", value=self.children[0].value)
        embed.set_author(name="Flo & Thibaut les dirlos")   
        embed.set_image(url="https://cdn.discordapp.com/attachments/1070035910390992926/1070065518796624044/image.png")
        await bot.get_channel(int(1070036861403267132)).send(embeds=[embed])
        await interaction.response.send_message("Modal envoyé ^^", ephemeral=True, delete_after=3)

class annonce(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Quel type d'information ?", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Annonce de la direction",
                description="Pour toutes les grosses infos"
            ),
            discord.SelectOption(
                label="Information",
                description="Pour les infos plus petites"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        if select.values[0]=="Annonce de la direction":
            modal = ad(title="Crée l'annonce de la direction")
        if select.values[0]=="Information":
            modal = id(title="Crée l'information")
        await interaction.response.send_modal(modal)

@bot.slash_command(name="annonce")
async def flavor(ctx):
    await ctx.respond("Quel type d'information ?", view=annonce(), ephemeral=True, delete_after=5)

@bot.slash_command(name="aide")
async def help(ctx):
    embed=discord.Embed(title="Bonjour je suis l'Assistant de direction de l'alliance France Avenir", description="Voici la liste des commandes disponibles")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1070035910390992926/1070065518796624044/image.png")
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/infos", inline=True)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/annonce", inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(name = "ban", description = "Ban un membre")
@commands.has_permissions(ban_members = True, administrator = True)
async def ban(ctx, member: Option(discord.Member, description = "Vous voulez rouler sur qui avec le train?"), reason: Option(str, description = "Pourquoi?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! Tu ne peut t'écraser toi même !")
    elif member.guild_permissions.administrator:
        await ctx.respond("Arrête de vouloir écraser un admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"Aucune raison fournie par {ctx.author}"
        await member.ban(reason = reason)
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {member.name} (ID : {member.id}) a été ban avec succès du serveur par {ctx.author.name} (ID : {ctx.author.id})!\n\nRaison: {reason}."
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> a été ban avec succès du serveur!\n\nRaison: {reason}")
        await bot.get_channel(int(1035131793021616168)).send(log)
    
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Vous avez besoin de la permission de ban et de gérer les utilisateurs!")
    else:
        await ctx.respond("Hum c'est pas normal...") #most likely due to missing permissions
        raise error

@bot.slash_command(name = "expulser", description = "Expluser un membre")
@commands.has_permissions(kick_members = True, administrator = True)
async def kick(ctx, member: Option(discord.Member, description = "Qui voulez vous jeter du train ?"), reason: Option(str, description = "Pourquoi ?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! Tu ne peut pas te jeter du train toi même !")
    elif member.guild_permissions.administrator:
        await ctx.respond("Mais ! Arrête de vouloir jeter du train un admin ! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"Aucune raison fournie par {ctx.author}"
        await member.kick(reason = reason)
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {member.name} (ID : {member.id}) a été été poussé du train avec succès du serveur par {ctx.author.name} (ID : {ctx.author.id})!\n\nRaison: {reason}."
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> à été poussé du train avec succès!\n\nRaison: {reason}")
        await bot.get_channel(int(1035131793021616168)).send(log)

@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Tu as besoin de la permission d'expulser et gérer les membres !")
    else:
        await ctx.respond("Hum c'est pas normal...") #most likely due to missing permissions 
        raise error

@bot.slash_command(name = 'bâillonner', description = "bâillonner un membre")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("Tu ne peut pas te bâillonner toi-même!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("MAIS ! Tu ne peut pas c'est un modo !")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("Désolé je peut pas bâillonner plus de 28 jours !", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Utilisateur : {member.name} (ID : {member.id}) a été bâillonné par {ctx.author.name} (ID : {ctx.author.id})."
        await ctx.respond(f"<@{member.id}> A été bâillonné pour {days} jours, {hours} heures, {minutes} minutes, & {seconds} secondes par <@{ctx.author.id}>.")
        await bot.get_channel(int(1035131793021616168)).send(log)
    else:
        await member.timeout_for(duration, reason = reason)
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Utilisateur : {member.name} (ID : {member.id}) a été bâillonné par {ctx.author.name} (ID : {ctx.author.id}) pour '{reason}'."
        await ctx.respond(f"<@{member.id}> A été bâillonné pour {days} jours, {hours} heures, {minutes} minutes, & {seconds} secondes par <@{ctx.author.id}> pour '{reason}'.")
        await bot.get_channel(int(1035131793021616168)).send(log)

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Tu as besoin de la permission de mute et gérer les membres!")
    else:
        raise error

@bot.slash_command(name = 'débâillonner', description = "débâillonner un membre")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Utilisateur : {member.name} (ID : {member.id}) a été débâillonné par {ctx.author.name} (ID : {ctx.author.id})."
        await ctx.respond(log)
        await bot.get_channel(int(1035131793021616168)).send(log)
    else:
        await member.remove_timeout(reason = reason)
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Utilisateur : {member.name} (ID : {member.id}) a été débâillonné par {ctx.author.name} (ID : {ctx.author.id}) pour '{reason}'"
        await ctx.respond(log)
        await bot.get_channel(int(1035131793021616168)).send(log)

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Tu as besoin de la permission de mute et gérer les membres!")
    else:
        raise error

@bot.slash_command(name="menage")
@commands.has_permissions(manage_messages = True)
async def menage(ctx, nombre : int):
    messages = [msg async for msg in ctx.channel.history(limit = nombre)] 
    for message in messages:
        await message.delete()
    await ctx.respond(f'{nombre} message supprimés')

@menage.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Tu as besoin de la permission de gérer les messages!")
    else:
        raise error

async def hello(
    ctx: discord.ApplicationContext,
    name: str,
    gender: str,
    age: int,
):
    await ctx.respond(
        f"Hello {name}! Your gender is {gender} and you are {age} years old."
    )
load_dotenv()
bot.run(os.getenv('TOKEN'))
