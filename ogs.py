# Handles OGS and SGF-based game logic (also used for KGS/IGS result parsing)

import env
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import time
from math import ceil, log
from webhook import *
from util import *
from sgfmill import sgf



# check active games within the group
def checkActiveGamesInGroup(group, players):
  printLineSeparator()
  print('Group {}'.format(group))

  for p in players:
    getOGSUsersLatestActiveGameID(group, p, players)


# Check active games
def checkActiveGames(filename):
  printLineSeparator()
  print('Games from {}, {}'.format(filename, getServerName(filename)))

  previous_game_link = ''
  new_file_data = ''

  with open(filename, 'r') as f:
    lines = f.readlines()
    for line in lines:
      data = line.replace(" ", "").replace("\n", "")

      if data.startswith('https://online-go.com/game'):
        if data != previous_game_link:
          time.sleep(3)
          print('(INFO) Checking [' + data + ']' + ' from ' + filename)
          if (isGameFinished(data)):
            ## The following game has just been finished
            ## Instead of calling $ogsr, just message the result (2025-04-18)
            ##sendMessageToWebhook(filename, '$ogsr <' + data + '>')
            sendMessageToWebhook(filename, getGameDetail(data, True))            

            previous_game_link = data
            ## Remove finished game from the file
            data = data.replace(data, '')
          else:
            new_file_data = new_file_data + data + '\n'

  with open(filename, 'w') as f:
    f.write(new_file_data)


# Check if the game is finished
def isGameFinished(ogs_link):
  ogs_link = ogs_link.replace(" ", "")
  gameFinished = False

  gameID = ogs_link.split('/')[4]
  response = requests.get("https://online-go.com/api/v1/games/" + gameID)
  parseData = response.json()

  if parseData["gamedata"]["phase"] == "finished":
    gameFinished = True

  print("(INFO) [{}] gameFinished? {}".format(ogs_link, gameFinished))
  return gameFinished


# Get OGS Game Details (either 'in progress' or 'finished')
# If showResultOnly is True, show result only
def getGameDetail(ogs_link, showResultOnly):
  ogs_link = ogs_link.replace('<', '').replace('>', '')

  printLineSeparator()
  print('(INFO) Reporting the game status for [' + ogs_link + ']')

  gameID = ogs_link.replace(" ", "").split('/')[4]
  response = requests.get("https://online-go.com/api/v1/games/" + gameID)
  parseData = response.json()

#  print("============")
#  print(parseData)
#  print("============")


  outcome = parseData["outcome"]

  white_user = parseData["players"]["white"]["username"]
  white_id = parseData["players"]["white"]["id"]
  whilte_flag = getOGSUserCountryFlag(white_id)
  white_rating = parseData["players"]["white"]["ratings"]["overall"]["rating"]
  white_rank = rating2rank(white_rating)

  black_user = parseData["players"]["black"]["username"]
  black_id = parseData["players"]["black"]["id"]
  black_flag = getOGSUserCountryFlag(black_id)
  black_rating = parseData["players"]["black"]["ratings"]["overall"]["rating"]
  black_rank = rating2rank(black_rating)

  # Rank doesn't look very accurate
  print("(INFO) W {},{}, B {}, {}".format(white_rating, white_rank,
                                          black_rating, black_rank))

  printLineSeparator()
  name = parseData["gamedata"]["game_name"]

  if env.displayRank != "F":
    white = '{}  {}  [{:.0f}, {}]'.format(white_user, whilte_flag,
                                          white_rating, white_rank)
    black = '{}  {}  [{:.0f}, {}]'.format(black_user, black_flag, black_rating,
                                          black_rank)
  else:
    white = '{}  {}  [{:.0f}]'.format(white_user, whilte_flag, white_rating)
    black = '{}  {}  [{:.0f}]'.format(black_user, black_flag, black_rating)

  players = 'B: ' + black + '\nW: ' + white

  game_info = ""
  time_control = parseData["gamedata"]["time_control"]["time_control"]

  ## byoyomi or fischer
  if time_control == "byoyomi":
    main_time = parseData["gamedata"]["time_control"]["main_time"]
    if main_time > 0:
      main_time = round(main_time / 60, 0)

    period_time = parseData["gamedata"]["time_control"]["period_time"]
    periods = parseData["gamedata"]["time_control"]["periods"]

    game_info = '\n\n{}, {:.0f} min, {}x{} sec '.format(
#    game_info = '\n\n{}, Main Time: {:.0f} min, Byo-Yomi {} times {} sec'.format(
        name, main_time, periods, period_time)
  elif time_control == "fischer":
    initial_time = parseData["gamedata"]["time_control"]["initial_time"]
    if initial_time > 0:
      initial_time = round(initial_time / 60, 0)

    time_increment = parseData["gamedata"]["time_control"]["time_increment"]
    max_time = parseData["gamedata"]["time_control"]["max_time"]
    if max_time > 0:
      max_time = round(max_time / 60, 0)

    game_info = '\n\n{}, Fischer Initial Time: {:.0f} min, increments by {} sec, up to max {:.0f} min'.format(
        name, initial_time, time_increment, max_time)

  ## start and end time
  start_time = parseData["gamedata"]["start_time"]

  end_time = 0
  try:
    end_time = parseData["gamedata"]["end_time"]
  except KeyError:
    print()

  ## start_time
  game_info = game_info + '\nStarted: <t:{}:f>'.format(start_time)

  ## end_time
  if end_time > 0:
    game_info = game_info + '\nEnded: <t:{}:f>'.format(end_time)

  ## outcome
  if outcome != "":
    winner = ""
    if parseData["black_lost"] == True:
      winner = white_user
    elif parseData["white_lost"] == True:
      winner = black_user

    winner = ':partying_face:  __' + winner + " won by " + outcome + "__  :partying_face:\n"
  else:
    winner = ':alarm_clock::fire:  ' + '__Game in progress...__  :muscle::popcorn:\n'

    ## Only Add if the channel is League
    if env.ChannelID == env.IGALeagueChannelID or env.ChannelID == env.BJBotTestChannelID:
      printLineSeparator()
      print("(INFO) {}. Adding to active list !!\n{}".format(
          getChannelName(env.ChannelID), ogs_link))
      addGameToActiveListFIle(ogs_link, env.ServerID)
    else:
      printLineSeparator()
      print("(INFO) Not adding to active list. Not League or Bot-Test Channel")

  ## Result
  result = winner + players + game_info

  printLineSeparator()
  print(result)
  printLineSeparator()

  if showResultOnly is True:
    return winner
  else:
    return result


def getOGSUserCountryFlag(userid):
  response = requests.get(
      "https://online-go.com/api/v1/players/{}".format(userid))
  parseData = response.json()

#  print("============")
#  print(parseData)
#  print("============")


  country_code = parseData["country"]

  if country_code == 'un':
    flag = ':united_nations:'
  elif country_code == '001':
    flag = ':united_nations:'
  elif country_code == '_Starfleet':
    flag = ':stars:'
  elif country_code == '_Pirate':
    flag = ':pirate_flag:'
  elif country_code == '_LGBT':
    flag = ':rainbow_flag:'
  elif country_code == '_England':
    flag = ':england:'
  elif country_code == '_Northern_Ireland':
    flag = '' ## Not available in Discord
  elif len(country_code) == 2:
    flag = ':flag_' + country_code + ':'
  else:
    flag = ''

  return flag


def rating2rank(ogs_rating):
  """Return a human readable go rank from a OGS rating number"""
  total = ceil(30 - (log(ogs_rating / 525) * 23.15))
  # https://forums.online-go.com/t/2021-rating-and-rank-adjustments/33389
  if total <= 0:
    return str(abs(total - 1)) + 'd'
  else:
    return str(total) + 'k'



def getOGSUsersLatestActiveGameID(group, userid, groupPlayers):
  session = requests.Session()
  retries = Retry(
      total=3,
      backoff_factor=1,
      status_forcelist=[500, 502, 503, 504],
      raise_on_status=False
  )
  adapter = HTTPAdapter(max_retries=retries)
  session.mount('https://', adapter)
  session.mount('http://', adapter)

  try:
    url = "https://online-go.com/api/v1/players/{}/games?ended__isnull=1&ordering=-id&width=19&rengo=false&time_control=byoyomi&handicap=0&page_size=1&format=json".format(userid)
    response = session.get(url, timeout=10)
    response.raise_for_status()
    parseData = response.json()

    print("User {}: {}".format(userid, str(parseData["count"])))

    if parseData["count"] > 0:
      game_id = parseData["results"][0]["id"]
      black_player_id = parseData["results"][0]["black"]
      white_player_id = parseData["results"][0]["white"]

      time_params = json.loads(parseData["results"][0]["time_control_parameters"])
      time_control = time_params['time_control']
      speed = time_params['speed']
      main_time = time_params['main_time']
      if main_time > 0:
        main_time = round(main_time / 60, 0)

      # The IGA league time control is 45 minutes of main time with 3 × 30-second byoyomi.
      # This is currently hard-coded, as the bot was developed specifically for the IGA league.
      # TODO: Make this configurable.
      if black_player_id in groupPlayers and white_player_id in groupPlayers and game_id != "" and time_control == "byoyomi" and main_time == 45:
        print("(INFO) Game ID: {}, black: {}, white: {}, main_time: {:.0f}, time_control: {}, speed: {}"
              .format(game_id, black_player_id, white_player_id, main_time, time_control, speed))

        ogs_link = "https://online-go.com/game/" + str(game_id)

        setServerInfo(env.IGAServerID, env.IGALeagueChannelID)

        if isGameInTheActiveList(ogs_link, env.IGAServerID) == False:
          sendMessageToWebhook(env.IGAServerID,
                               ':regional_indicator_{}: Group League game is underway — let the fun begin! :tada::fire:'.format(group.lower()))
          time.sleep(1)
          sendMessageToWebhook(env.IGAServerID, '$ogs <' + ogs_link + '>')
          addGameToActiveListFIle(ogs_link, env.IGAServerID)
          time.sleep(1)

  except requests.exceptions.RequestException as e:
    print(f"(ERROR) Failed to get data for user {userid}: {e}")

  return "test"



def getKGSResult(kgs_link):
  printLineSeparator()
  print('(INFO) Reporting the game status for [' + kgs_link + ']')

  response = requests.get(kgs_link)
  game = sgf.Sgf_game.from_bytes(response.content)

  root_node = game.get_root()
  print("(INFO) root_note: " + str(root_node))

  gamedate = root_node.get("DT")
  maintime = getSgfRootNode(root_node, "TM")
  overtime = getSgfRootNode(root_node, "OT")
  komi = getSgfRootNode(root_node, "KM")
  rule = getSgfRootNode(root_node, "RU")
  b_player = root_node.get("PB")
  w_player = root_node.get("PW")
  result = getSgfRootNode(root_node, "RE")

  kgs_result = '{}, {:.0f}min, {} \n{}, komi:{:.1f}\nB: {}\nW: {}\nResult: {}  :partying_face:'.format(gamedate, maintime / 60, overtime, rule, komi, b_player, w_player, result)

  print("(INFO) " + kgs_result)

  return kgs_result


def getSgfRootNode(root_node, attr):
  s = 0

  try:
    s = root_node.get(attr)
  except KeyError as e:
    s = 0

  return s

