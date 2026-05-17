import os
import asyncio
import requests
import discord

TOKEN = os.getenv("TOKEN")

GUILD_ID = 857180887421288448
BOT_NAME = "Digger HLL"
BATTLEMETRICS_ID = "25216465"
UPDATE_INTERVAL = 60


intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_server_data():
    url = f"https://api.battlemetrics.com/servers/{BATTLEMETRICS_ID}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    attributes = response.json()["data"]["attributes"]

    players = attributes.get("players", 0)
    max_players = attributes.get("maxPlayers", 100)
    map_name = attributes.get("details", {}).get("map", "Unknown Map")

    return players, max_players, map_name


async def update_status():
    await client.wait_until_ready()

    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("ERROR: Bot cannot find the Discord server.")
        for server in client.guilds:
            print(f"- {server.name}: {server.id}")
        return

    while not client.is_closed():
        try:
            players, max_players, map_name = get_server_data()

            await guild.me.edit(nick=BOT_NAME)
            await client.change_presence(
                activity=discord.Game(f"{players}/{max_players} - {map_name}")
            )

            print(f"Updated: {players}/{max_players} - {map_name}")

        except Exception as error:
            print(f"Error updating status: {error}")

        await asyncio.sleep(UPDATE_INTERVAL)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(update_status())


client.run(TOKEN)