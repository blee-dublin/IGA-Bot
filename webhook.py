# Very small wrapper around discord_webhook

import time
from discord_webhook import DiscordWebhook
from util import *


# IGA or BL
def sendMessageToWebhook(serverID, webhook_message):
  url = getWebhookLink(serverID)

  webhook = DiscordWebhook(url, content=webhook_message)
  response = webhook.execute()


# Specify a link
def sendMessageToWebhookLink(whlink, webhook_message):
  webhook = DiscordWebhook(whlink, content=webhook_message)

  #print(webhook_message)

  response = webhook.execute()

