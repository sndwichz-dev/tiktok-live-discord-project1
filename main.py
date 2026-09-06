import asyncio
import os
import requests

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK"),
os.getenv("DISCORD_WEBHOOK_2")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

notified = False


def send_discord(message):
    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=10
    )


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    global notified

    if not notified:
        message = (
            f"🔴 **{TIKTOK_USERNAME} is LIVE on TikTok!**\n\n"
            f"👉 https://www.tiktok.com/@{TIKTOK_USERNAME}/live"
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


asyncio.run(main())
