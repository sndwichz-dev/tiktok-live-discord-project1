import asyncio
import os
import requests

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

# Load TikTok usernames and Discord webhook
TIKTOK_USERNAME_1 = os.getenv("TIKTOK_USERNAME")
TIKTOK_USERNAME_2 = os.getenv("TIKTOK_USERNAME_2")
TIKTOK_USERNAME_3 = os.getenv("TIKTOK_USERNAME_3")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Put usernames in a list (skip None values)
USERNAMES = [u for u in [TIKTOK_USERNAME_1, TIKTOK_USERNAME_2, TIKTOK_USERNAME_3] if u]

# Prevent duplicate notifications per user
notified = {username: False for username in USERNAMES}

def send_discord(message):
    if DISCORD_WEBHOOK:
        print("Sending message to Discord...")
        requests.post(
            DISCORD_WEBHOOK,
            json={"content": message},
            timeout=10
        )
    else:
        print("No Discord webhook found!")

# Create a client for each TikTok username
clients = [TikTokLiveClient(unique_id=username) for username in USERNAMES]

for client in clients:
    @client.on(ConnectEvent)
    async def on_connect(event: ConnectEvent, client=client):
        username = client.unique_id
        global notified

        if not notified[username]:
            message = (
                f"**{username} is LIVE on TikTok!**\n\n"
                f"https://www.tiktok.com/@{username}/live"
            )
            send_discord(message)
            notified[username] = True

        print(f"Connected to @{username}")

async def main():
    global notified

    while True:
        try:
            for client in clients:
                username = client.unique_id
                is_live = await client.is_live()
                print(f"Live status for @{username}: {is_live}")

                if not is_live:
                    notified[username] = False

                if is_live and not client.connected:
                    await client.connect()

            await asyncio.sleep(30)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    print("Loaded usernames:", USERNAMES)
    asyncio.run(main())
