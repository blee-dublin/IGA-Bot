## Check and report ongoing league games every a few mins

import env
import threading
import datetime
import time
from ogs import *
from webhook import *

checkFrequencyInMin = 3
checkedCnt = 0


# OGS IDs by league groups
with open("groups.json") as f:
    groups = json.load(f)

a_group_players = groups["a_group_players"]
b_group_players = groups["b_group_players"]
c_group_players = groups["c_group_players"]
d_group_players = groups["d_group_players"]
e_group_players = groups["e_group_players"]
f_group_players = groups["f_group_players"]
g_group_players = groups["g_group_players"]
h_group_players = groups["h_group_players"]
i_group_players = groups["i_group_players"]
j_group_players = groups["j_group_players"]
k_group_players = groups["k_group_players"]
l_group_players = groups["l_group_players"]



def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def check_league_games():
    global checkedCnt

    # Assuming that nobody plays league games between midnight and 6am
    if checkedCnt != 0 and is_time_between(datetime.time(6,00), datetime.time(23,59)): # UTC
        print("=====================")
        print("Checking every 2 mins") 
        checkActiveGames(env.IGAServerID)
        
        time.sleep(1)
        checkActiveGames(env.BJServerID)

        if checkedCnt % checkFrequencyInMin == 1:
            checkActiveGamesInGroup("A", a_group_players)
            checkActiveGamesInGroup("B", b_group_players)
            checkActiveGamesInGroup("C", c_group_players)
            checkActiveGamesInGroup("D", d_group_players)
        elif checkedCnt % checkFrequencyInMin == 2:
            checkActiveGamesInGroup("E", e_group_players)
            checkActiveGamesInGroup("F", f_group_players)
            checkActiveGamesInGroup("G", g_group_players)
            checkActiveGamesInGroup("H", h_group_players)
        elif checkedCnt % checkFrequencyInMin == 0:
            checkActiveGamesInGroup("I", i_group_players)
            checkActiveGamesInGroup("J", j_group_players)
            checkActiveGamesInGroup("K", k_group_players)
            checkActiveGamesInGroup("L", l_group_players)

        print("=====================")
        print("checkedCnt = {}\n".format(checkedCnt)) 


    checkedCnt += 1
    timer = threading.Timer(checkFrequencyInMin * 60, check_league_games)
    timer.start()

check_league_games()

