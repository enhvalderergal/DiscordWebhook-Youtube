import sys
import time
from discord_webhook import DiscordWebhook
import requests
import re
import argparse

# Definerer parseren til kommando-linje-argumenter
parser = argparse.ArgumentParser(description="Print input parameters")
parser.add_argument('--channel', type=str, help='URL på Youtube kanalen', required=True)
parser.add_argument('--auther', type=str, help='Navn på kanalen', required=True)
parser.add_argument('--timer', type=int, help='Tid mellem tjek i sekunder', required=True)
parser.add_argument('--webhookurl', type=int, help='Tid mellem tjek i sekunder', required=True)

# Parser argumenterne
args = parser.parse_args()

channel = args.channel
auther = args.auther
timer = args.timer
webhookurl = args.webhookurl

def main():
    # Henter HTML-indholdet
    html = requests.get(channel + "/videos").text

    # Finder navn og URL på den nyeste video
    pattern = fr'(?<={{"label":").*?{auther}(?=\s|$)'
    name = re.search(pattern, html).group()
    url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

    # Sender beskeden til Discord
    webhook = DiscordWebhook(
        url=webhookurl,
        content=f"# **{name}**\n---------------------------------------------------------------------------------------------------\n{url}")
    response = webhook.execute()
    time.sleep(timer)
    main()


main()