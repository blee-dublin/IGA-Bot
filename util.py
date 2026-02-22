## Some other utils

import datetime
import time
import env


def printLineSeparator():
  print('=====================')
  print('(INFO) {}'.format(datetime.datetime.utcnow()))


def setServerInfo(serverId, channelId):
  env.ServerID = "{}".format(str(serverId))
  env.ChannelID = "{}".format(str(channelId))

  server_info = getServerName(str(serverId))

  return server_info


def getServerName(serverID):
  serverName = ''
  if serverID == env.BJServerID:
    serverName = 'BJ Server'
  elif serverID == env.IGAServerID:
    serverName = 'IGA Server'

  return serverName


def getChannelName(channelID):
  channelName = ''
  if channelID == env.BJBotTestChannelID:
    channelName = 'BJ Server > bot-test channel'
  elif channelID == env.IGALeagueChannelID:
    channelName = 'IGA Server > league channel'

  return channelName


def getWebhookLink(serverID):
  link = ''
  if serverID == env.BJServerID:
    link = env.BJChannelWebhooksURL
    print('(INFO) BJChannelWebhooksURL')
  elif serverID == env.IGAServerID:
    link = env.IGALeagueChannelWebhooksURL
    print('(INFO) IGALeagueChannelWebhooksURL')
  else:
    link = env.BJChannelWebhooksURL
    print('(INFO) BJChannelWebhooksURL')

  print('(info) webhook link = ' + link)

  return link


# Add only if the active game is not in the file already
def addGameToActiveListFIle(link, serverId):
#  printLineSeparator()

  filename = "{}".format(serverId)
  alreadyExitInFile = isGameInTheActiveList(link, serverId)

  if alreadyExitInFile != True:
    f = open(filename, "a+")
    f.write(link + '\n')
    f.close()
    print('(INFO) Active game: [' + link + '] has been added to ' + filename)
  else:
    print('(INFO) Active game: [' + link + '] is already in ' + filename)


# Check if the game is already in the list
def isGameInTheActiveList(link, serverId):
#  printLineSeparator()

  filename = "{}".format(serverId)
  alreadyExitInFile = False

  with open(filename) as f:
    if link in f.read():
      alreadyExitInFile = True

  print('(INFO) Game: [' + link + '] alreadyExitInFile? ' + str(alreadyExitInFile))
  return alreadyExitInFile


