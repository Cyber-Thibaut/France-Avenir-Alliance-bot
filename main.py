import discord
from discord.ext import commands
import os # default module
from dotenv import load_dotenv
from random import choice
from discord import Option
from discord.ext import commands
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

@bot.slash_command(name="rolereact")
async def rolereact(ctx, *, message: str):
    message = await ctx.send(message)
    await message.add_reaction('✅')
    await message.add_reaction('❎')

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = discord.utils.get(guild.roles, name='prout')
    if role is not None:
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
        await bot.get_channel(int(1062738561939550250)).send(embeds=[embed])
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
        await bot.get_channel(int(1062738561939550250)).send(embeds=[embed])
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
    embed.add_field(name="Pour afficher 3 trains en circulation en ce moment même", value="/spot", inline=False)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/infos", inline=True)
    embed.add_field(name="Oups celle-ci est réservée à l'administration", value="/annonce", inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = servers, name = "ban", description = "Ban un membre")
@commands.has_permissions(ban_members = True, administrator = True)
async def ban(ctx, member: Option(discord.Member, description = "Who do you want to ban?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! Tu ne peut te ban toi même !")
    elif member.guild_permissions.administrator:
        await ctx.respond("Arrête de vouloir ban un admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"Aucune raison fournie par {ctx.author}"
        await member.ban(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> a été ban avec succès du serveur!\n\nRaison: {reason}")
    
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Vous avez besoin de la permission s de ban et de gérer les utilisateurs!")
    else:
        await ctx.respond("Hum c'est pas normal...") #most likely due to missing permissions
        raise error

@bot.slash_command(guild_ids = servers, name = "expulser", description = "Expluser un membre")
@commands.has_permissions(kick_members = True, administrator = True)
async def kick(ctx, member: Option(discord.Member, description = "Who do you want to kick?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! Tu ne peut pas t'expulser toi même !")
    elif member.guild_permissions.administrator:
        await ctx.respond("Mais ! Arrête de vouloir expulser un admin ! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"Aucune raison fournie par {ctx.author}"
        await member.kick(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> à été expulsé du serveur avec succès!\n\nRaison: {reason}")

@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Tu as besoin de la permission d'expulser et gérer les membres !")
    else:
        await ctx.respond("Hum c'est pas normal...") #most likely due to missing permissions 
        raise error

@bot.slash_command(guild_ids = servers, name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@bot.slash_command(guild_ids = servers, name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@bot.slash_command(name="clear")
async def clear(ctx, nombre : int):
    messages = [msg async for msg in ctx.channel.history(limit = nombre)] 
    for message in messages:
        await message.delete()
    await ctx.respond(f'{nombre} message clear')
load_dotenv()
bot.run(os.getenv('TOKEN'))
