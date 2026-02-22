from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Set variables from .env
TOKEN = os.getenv("TOKEN")

IGALeagueChannelID = os.getenv("IGALeagueChannelID")
BJBotTestChannelID = os.getenv("BJBotTestChannelID")
IGAServerID = os.getenv("IGAServerID")
BJServerID = os.getenv("BJServerID")
BJChannelWebhooksURL = os.getenv("BJChannelWebhooksURL")
IGALeagueChannelWebhooksURL = os.getenv("IGALeagueChannelWebhooksURL")
IGADublinChannelWebhooksURL = os.getenv("IGADublinChannelWebhooksURL")
displayRank = os.getenv("displayRank")

# Defaults or placeholders
ServerID = ""
ChannelID = ""

