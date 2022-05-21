import discord
import json

from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

#si desea otorgar un rol al usuario en cualquier actualización de nivel específico, puede hacer esto
#ingrese el nombre del rol en una lista
level = ["Nivel 1", "Nivel 2", "Nivel 3"]

#add the level number at which you want to give the role
level_num = [1, 2, 3]

class Levelsys(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Yhorm el dictador está listo")

  
#esto aumentará la xp del usuario cada vez que envíe un mensaje
  @commands.Cog.listener()
  async def on_message(self, message):

    #el prefijo del bot es y! es por eso que estamos agregando esta declaración para que el xp del usuario no aumente cuando usa cualquier comando
    if not message.content.startswith("y!"):

      
#comprobando si el bot no ha enviado el mensaje
      if not message.author.bot:
        with open("levels.json", "r") as f:
          data = json.load(f)
        
        #comprobando si los datos del usuario ya están en el archivo o no
        if str(message.author.id) in data:
          xp = data[str(message.author.id)]['xp']
          lvl = data[str(message.author.id)]['level']
          #aumentar el xp por el número que tiene 100 como su múltiplo
          increased_xp = xp+25
          new_level = int(increased_xp/100)

          data[str(message.author.id)]['xp']=increased_xp

          with open("levels.json", "w") as f:
            json.dump(data, f)

          if new_level > lvl:
            await message.channel.send(f"{message.author.mention} ha subido a nivel  {new_level}!!!")

            data[str(message.author.id)]['level']=new_level
            data[str(message.author.id)]['xp']=0

            with open("levels.json", "w") as f:
              json.dump(data, f)
            
            for i in range(len(level)):
              if new_level == level_num[i]:
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))

                mbed = discord.Embed(title=f"{message.author} tu has obtenido el rol de **{level[i]}**!", color = message.author.colour)
                mbed.set_thumbnail(url=message.author.avatar_url)
                await message.channel.send(embed=mbed)
        else:
          data[str(message.author.id)] = {}
          data[str(message.author.id)]['xp'] = 0
          data[str(message.author.id)]['level'] = 1

          with open("levels.json", "w") as f:
            json.dump(data, f)

  @commands.command(name="rank")
  async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
    userr = user or ctx.author

    with open("levels.json", "r") as f:
      data = json.load(f)

    xp = data[str(userr.id)]["xp"]
    lvl = data[str(userr.id)]["level"]

    next_level_xp = (lvl+1) * 100
    xp_need = next_level_xp
    xp_have = data[str(userr.id)]["xp"]

    percentage = int(((xp_have * 100)/ xp_need))

    if percentage < 1:
      percentage = 0
    
    ## Rank card
    background = Editor(f"zIMAGE.jpg")
    profile = await load_image_async(str(userr.avatar_url))

    profile = Editor(profile).resize((150, 150)).circle_image()
    
    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    
#puedes omitir esta parte, estoy agregando esto porque el texto es difícil de leer en mi imagen seleccionada
    ima = Editor("zBLACK.png")
    background.blend(image=ima, alpha=.5, on_top=False)

    background.paste(profile.image, (30, 30))

    background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
    background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=percentage,
        fill="#FF0000",
        radius=20,
    )
    background.text((200, 40), str(userr.name), font=poppins, color="#ff9933")

    background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
    background.text(
        (200, 130),
        f"Nivel : {lvl}   "
        + f" XP : {xp} / {(lvl+1) * 100}",
        font=poppins_small,
        color="#FFFFFF",
    )

    card = File(fp=background.image_bytes, filename="zCARD.png")
    await ctx.send(file=card)

  @commands.command(name="ranklist")
  async def ranklist(self, ctx, range_num=5):
    with open("levels.json", "r") as f:
      data = json.load(f)

    l = {}
    total_xp = []

    for userid in data:
      xp = int(data[str(userid)]['xp']+(int(data[str(userid)]['level'])*100))

      l[xp] = f"{userid};{data[str(userid)]['level']};{data[str(userid)]['xp']}"
      total_xp.append(xp)

    total_xp = sorted(total_xp, reverse=True)
    index=1

    mbed = discord.Embed(
      title="Tabla de Puntos"
    )

    for amt in total_xp:
      id_ = int(str(l[amt]).split(";")[0])
      level = int(str(l[amt]).split(";")[1])
      xp = int(str(l[amt]).split(";")[2])

      member = await self.bot.fetch_user(id_)

      if member is not None:
        name = member.name
        mbed.add_field(name=f"{index}. {name}",
        value=f"**Level: {level} | XP: {xp}**", 
        inline=False)

        if index == range_num:
          break
        else:
          index += 1

    await ctx.send(embed = mbed)

  @commands.command("rank_reset")
  async def rank_reset(self, ctx, user: Optional[discord.Member]):
    member = user or ctx.author

#esta declaración if verificará que el usuario que está usando este comando está tratando de eliminar sus datos o cualquier otro dato de usuario
#si ella está tratando de eliminar los datos de cualquier otro usuario, vamos a verificar si tiene un rol específico o no (en mi caso, es 'Mortal') para que solo los Mortalistradores puedan eliminar los datos de los usuarios y no otras personas. quitar otro
    if not member == ctx.author:
      role = discord.utils.get(ctx.author.guild.roles, name="Mortal")

      if not role in member.roles:
        await ctx.send(f"Solo puedes resetear tus datos, para resetear otros datos debes tener el rol de {role.mention}")
        return 
    
    with open("levels.json", "r") as f:
      data = json.load(f)

    del data[str(member.id)]

    with open("levels.json", "w") as f:
      json.dump(data, f)

    await ctx.send(f"{member.mention} has renacido")
  
  @commands.command(name="increase_level")
  @commands.has_role("Mortal")
  async def increase_level(self, ctx, increase_by: int, user: Optional[discord.Member]):
    member = user or ctx.author

    with open("levels.json", "r") as f:
      data = json.load(f)
    
    data[str(member.id)]['level'] += increase_by

    with open("levels.json", "w") as f:
      json.dump(data, f)
    
    await ctx.send(f"{member.mention}, tu nivel se incrementó por {increase_by}")

  @commands.command(name="increase_xp")
  @commands.has_role("Mortal")
  async def increase_xp(self, ctx, increase_by: int, user: Optional[discord.Member]):
    member = user or ctx.author

    with open("levels.json", "r") as f:
      data = json.load(f)

    data[str(member.id)]['xp'] += increase_by

    with open("levels.json", "w") as f:
      json.dump(data, f)

    await ctx.send(f"{member.mention}, tu xp se incrementó por {increase_by}")

def setup(client):
  client.add_cog(Levelsys(client))