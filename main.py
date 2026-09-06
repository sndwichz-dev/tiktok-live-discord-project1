import asyncio
import os
import requests

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

# Load TikTok username and Discord webhook (single channel only)
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Initialize TikTok client
client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

# Prevent duplicate notifications
notified = False

def send_discord(message):
    if DISCORD_WEBHOOK:  # only send if secret exists
        print("Sending message to Discord...")
        requests.post(
            DISCORD_WEBHOOK,
            json={"content": message},
            timeout=10
        )
    else:
        print("No Discord webhook found!")

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    global notified

    if not notified:
        message = (
            f"**{TIKTOK_USERNAME} is LIVE on TikTok!**\n\n"
            f"https://www.tiktok.com/@{TIKTOK_USERNAME}/live"
        )

        send_discord(message)
        notified = True

    print(f"Connected to @{TIKTOK_USERNAME}")

async def main():
    global notified

    while True:
        try:
            is_live = await client.is_live()
            print(f"Live status: {is_live}")

            if not is_live:
                notified = False

            if is_live and not client.connected:
                await client.connect()

            await asyncio.sleep(30)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())

