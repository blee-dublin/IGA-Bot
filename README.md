# IGA-Bot

Online Go League Bot for the Irish Go Association Discord.

IGA-Bot is a small but it keeps an eye on online Go league games.

# History

IGA-Bot was created to reduce the amount of manual admin work involved in running the IGA online leagues — and to save a few sanity points along the way.

# IGA League

https://www.irish-go.org/iga-league/

# IGA Discord Server

https://discord.gg/4vSnhjd

# Features
## Display online game details

(Primarily OGS, also support for KGS and IGS)

```$ogs https://online-go.com/game/84446223```

This command displays the current status of the game — whether it’s still being fought out on the board or already finished with what outcome.

## Track ongoing league games

Based on the group definitions in groups.json, IGA-Bot regularly checks for ongoing league games and reports their status to the designated Discord channel.

When a game finishes, the bot will announce the result.

## EGD (European Go Database) lookup
```$egd Kachanovskyi```

Retrieves EGD details for players matching the given surname. 


# How to use
".env" file is required in the home directory of the Bot that contains the following details.

```
TOKEN=<Discord-Bot-Token>
IGALeagueChannelID=<League-Channel-ID>
BJBotTestChannelID=<Test-Chennel-ID>
IGAServerID=<League-Server-ID>
BJServerID=<Test-Server-ID>
displayRank=T
BJChannelWebhooksURL=<Test-Channel-Webhook-URL>
IGALeagueChannelWebhooksURL=<League-Channel-Webhook-URL>
```

# Disclaimer
The creator of IGA-Bot, "Byoung-Ju Lee", is not a professional Python developer, so some parts of the code may be a little untidy — and there may well be a few bugs lurking about.
If you spot anything odd or have suggestions, feel free to reach out via the IGA Discord.
