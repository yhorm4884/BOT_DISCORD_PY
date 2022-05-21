import discord
from discord.ext import commands
import datetime
import typing
import os
import random
import converciones
import fichero
from webserver import keep_alive
import json

#Configuración más importante del command
command =commands.Bot(command_prefix='y!',description='Bot Oficial de Yhorm',allowed_mentions = discord.AllowedMentions(everyone = True),kick_members=True)
links = json.load(open("gifs.json"))
#autoroles
for filename in os.listdir('./niveles'):
  if filename.endswith('.py'):
    command.load_extension(f'niveles.{filename[:-3]}')
client=discord.Client()
#ver avatar del usuario
@command.command()
async def avatar(ctx, member : discord.Member = None):
  member = ctx.author if not member else member
  embed =discord.Embed(title=member.name + "#"+member.discriminator)
  embed.set_image(url=member.avatar_url)
  await ctx.send(embed=embed)
  

#Libro de Chistes
ficheros = fichero.fichero("./chistes.txt",";")
ficheros.generarListaChistes()

####################################################################################
@command.command(name="gif", aliases=["feed", "play", "sleep"])
async def Gif(ctx):
	await ctx.send(random.choice(links[ctx.invoked_with]))
###################################################################################
  #Comando de Ayudas
@command.command()
async def ayuda(ctx):
    embed=discord.Embed(title='AYUDA', description='Muestra una pequeña ayuda de todos los commandos', color=0xcd1aff)
    embed.set_author(name='Yhorm #4884', url='https://www.instagram.com/yhorm/', icon_url='https://cdn.discordapp.com/avatars/610099597213433858/062a5425519065b3b946469dae18dcbe.png?size=2048')
    embed.set_thumbnail(url='https://discord.com/channels/@me/765276775205961739/770647516513304646')
    embed.add_field(name='info', value='Muestra información básica del servidor (en desarollo)', inline=True)
    embed.add_field(name='kick', value='Expulsión de Personas', inline=True)
    embed.add_field(name='ban', value='Baneo de Personas', inline=True)
    embed.add_field(name='clear', value='Limpiar chat', inline=True)
    embed.add_field(name='gif', value='Envía de manera aleatoria gif de las acciones programadas', inline=True)
    embed.add_field(name='Decimal_a_Binario', value='Utiliza Decimal_a_Binario para pasar de decimal a binario', inline=True)
    embed.add_field(name='chiste', value='Cuenta un chiste random', inline=True)
    embed.add_field(name='DM', value='Manda un dm a la persona etiquetada', inline=True)
    embed.add_field(name='avatar', value='Te muestra tu avatar', inline=True)
    embed.add_field(name='rank', value='Muestra tu rango', inline=True)
    embed.add_field(name='ranklist', value='Consulta lista de rangos del bot', inline=True)
    embed.set_footer(text='Este command aún está en mantenimiento, disculpen las molestias.')
    await ctx.send(embed=embed)


# funcion BaD: convierte de decimal a binario.
@command.command()
async def Decimal_a_Binario(ctx,num : int):
    embed = discord.Embed(title="Conversor Decimal a Binario")
    embed.add_field(name="Decimal",value=str(num))
    num = converciones.B10aB2(num)
    embed.add_field(name="Binario", value=str(num))
    await ctx.send(embed=embed)
    
# Informacion del server
@command.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description='Datos Básicos', timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(name='Creación del server ', value=f'{ctx.guild.created_at}')
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
    embed.add_field(name='Propietario del command', value='Yhorm #4884')
    embed.set_thumbnail(url='https://pluralsight.imgix.net/paths/python-7be70baaac.png')
    await ctx.send(embed=embed)
    
# limpiar chat
@command.command()
async def clear(ctx, num : int =10):
    async for message in ctx.channel.history(limit=num + 1):
        await message.delete()

# funcion DM:  permite mandar un mensaje por privado por medio del command.
@command.command()
async def dm(ctx, user : discord.Member,*mensaje):
  if ctx.author.guild_permissions.administrator: 
    texto = ""
    for i in mensaje:
      if str(i) != "&":
        texto += str(i) + " "
      else:
        texto += "\n"
    await user.send(texto)
    await ctx.message.delete()
  
# funcion  chiste: muestra un chiste de forma aleatoria desde la lista.
@command.command()
async def chiste(ctx):
    embed = discord.Embed(title="Chistes Malos.",description= random.choice(ficheros.obtenerListaChistes()))
    await ctx.send(embed=embed)
    
# kickear usuarios
@command.command()
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f"{user} ha sido asesinado")

# Banear usuarios
@command.command()
async def ban(ctx, members: commands.Greedy[discord.Member],
    delete_days: typing.Optional[int] = 0, *,
    reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)
    await member.ctx.send(f'{member.name} ha sido expulsado')
    await ctx.message.delete()
    
# Evento de inicio
@command.event
async def on_ready():
    await command.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='lloros de yhorm'))
    print('Yhorm está despierto')
    discord.Intents.members = True

keep_alive()
command.run('TOKEN')