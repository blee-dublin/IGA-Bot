# IGA-Bot

Online Go League Bot for the Irish Go Association Discord

IGA-Bot is a small but it keeps an eye on online Go league games.

# History

IGA-Bot was created by Byoung-Ju Lee to reduce the amount of manual admin work involved in running the IGA online leagues — and to save a few sanity points along the way.

# IGA League

https://www.irish-go.org/iga-league/

# IGA Discord Server

https://discord.gg/4vSnhjd

# Features
## Display online game details

(Primarily OGS, with support for KGS and IGS)

```$ogs https://online-go.com/game/84446223```

This command displays the current status of the game — whether it’s still being fought out on the board or already finished with what outcome.

## Track ongoing league games

Based on the group definitions in groups.json, IGA-Bot regularly checks for ongoing league games and reports their status to the designated Discord channel.

When a game finishes, the bot will announce the result.

## EGD (European Go Database) lookup
```$egd Kachanovskyi```

Retrieves EGD details for players matching the given surname. 
