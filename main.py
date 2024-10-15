import time
from discord_webhook import DiscordWebhook
import requests
import re
import argparse

# Define what arguments this file can take in
parser = argparse.ArgumentParser(description="Print input parameters")
parser.add_argument('--channel', type=str, help='The URL of the channel', required=True)
parser.add_argument('--auther', type=str, help='The name of the channel', required=True)
parser.add_argument('--timer', type=int, help='Time between checks in seconds', required=True)
parser.add_argument('--webhook_url', type=str, help='Discord webhook URL', required=True)

# The arguments
args = parser.parse_args()

#The arguments saved as our variables
channels = [args.channel]
auther = args.auther
timer = args.timer
webhook_url = args.webhook_url




def main():
    video_urls = []


    try:
        with open('video_urls.txt', 'r') as file:
            existing_urls = file.readlines()
        existing_urls = [url.strip() for url in existing_urls]  # Remove newlines
    except FileNotFoundError:
        # If file doesn't exist, assume no URLs exist
        existing_urls = []


    for channel in channels:
        try:
            # Fetches the HTML content
            html = requests.get(channel + "/videos").text

            # Finds the Name and the URL of the video
            pattern = fr'(?<={{"label":").*?{auther}(?=\s|$)'
            name = re.search(pattern, html).group()
            url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

            #If this URL is new and does not match the old one then that means that we can push a notification
            if url not in existing_urls:
                video_urls.append(url)
                discord_notification(name, url)


        except Exception as e:
            print(f"Error fetching video from {channel}: {e}")


    # Add the new URLS to the file if there is eny
    if video_urls:
        with open('video_urls.txt', 'a') as file:
            for video_url in video_urls:
                file.write(f"{video_url}\n")

    # And loop and check again
    time.sleep(timer)
    main()

def discord_notification (name, url):
    webhook = DiscordWebhook(
        url=webhook_url,
        content=f"# **{name}**\n---------------------------------------------------------------------------------------------------\n{url}")
    response = webhook.execute()



main()
