import env
import discord
from webhook import *
from league import *
from ogs import *
from egd import *
from util import *


intents = discord.Intents(messages=True, guilds=False)
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  ## where am I
  if message.content.startswith('$whereami'):
    await message.channel.send('Server: {}\nChannel: {}\n{}'.format(
        message.guild.id, message.channel.id,
        setServerInfo(message.guild.id, message.channel.id)))

  if message.content.startswith('$active') or message.content.startswith(
      '!active'):
    setServerInfo(message.guild.id, message.channel.id)
    sendMessageByWebhookEachLineOfFile('{}'.format(message.guild.id))


  ## Hello
  if message.content.startswith('$hello'):
    print('(INFO) HELLO')
    await message.channel.send(
        'Hello !!\n' + setServerInfo(message.guild.id, message.channel.id))


  ## OGS, display rank (i.e 1d, 2k, etc)
  if message.content.startswith('$displayrank'):
    if env.displayRank == 'F':
      env.displayRank = 'T'
    else:
      env.displayRank = 'F'

    await message.channel.send("displayRank: " + env.displayRank)




  ## OGS (Result Only)
  if message.content.startswith('https://online-go.com/game') or message.content.startswith('<https://online-go.com/game'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getGameDetail(message.content, False))

  ## OGS
  if message.content.startswith('$ogs ') or message.content.startswith('!ogs '):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getGameDetail(message.content.split(' ')[1], False))

  ## OGS (Result Only)
  if message.content.startswith('$ogsr ') or message.content.startswith('!ogsr '):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getGameDetail(message.content.split(' ')[1], True))




  ## KGS "https://files.gokgs.com/games/2024/10/4/xxx.sgf"
  if message.content.startswith('https://files.gokgs.com/games'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getKGSResult(message.content))

  ## KGS
  if message.content.startswith('$kgs') or message.content.startswith('!kgs'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getKGSResult(message.content.split(' ')[1]))




  ## IGS "https://pandanet-igs.com/system/sgfs/15883/original/RokoCrv-janssensei-2024-10-15_B_R.sgf?1729022809"
  if message.content.startswith('https://pandanet-igs.com/system/sgfs'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getKGSResult(message.content))

  ## IGS
  if message.content.startswith('$igs') or message.content.startswith('!igs'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getKGSResult(message.content.split(' ')[1]))


  ## Other sgf links from OGS
  if message.content.startswith('https://online-go.com/api') and message.content.endswith('.sgf'):
    setServerInfo(message.guild.id, message.channel.id)
    await message.channel.send(getKGSResult(message.content))




  ## EGD
  if message.content.startswith('$egd') or message.content.startswith('!egd'):
    arg1 = message.content.split(' ')[1]
    print(type(arg1))
    if arg1.isnumeric():
      await message.channel.send(
          getEGDPlayerByPin(message.content.split(' ')[1]))
    else:
      await message.channel.send(
          getEGDPlayerByNames(message.content.split(' ')))


client.run(env.TOKEN)

