import discord
import requests
import asyncio
import os

TOKEN = os.getenv("TOKEN")

GUILD_ID = 857180887421288448
BOT_NAME = "Digger HLL"

# Your BattleMetrics server ID
BATTLEMETRICS_ID = "39070835"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_server_data():
    url = f"https://api.battlemetrics.com/servers/{BATTLEMETRICS_ID}"

    res = requests.get(url).json()

    data = res["data"]["attributes"]

    players = data.get("players", 0)
    max_players = data.get("maxPlayers", 100)

    map_name = data.get("details", {}).get("map", "Unknown Map")

    return players, max_players, map_name

async def update_status():
    await client.wait_until_ready()

    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("ERROR: Could not find the Discord server.")
        print("Check that GUILD_ID is correct and the bot is invited to that server.")
        print("Servers this bot is in:")
        for g in client.guilds:
            print(f"- {g.name}: {g.id}")
        return

    bot_member = guild.me

    while not client.is_closed():
        try:
            players, max_players, map_name = get_server_data()

            await bot_member.edit(nick=BOT_NAME)

            activity = discord.Game(f"{players}/{max_players} - {map_name}")
            await client.change_presence(activity=activity)

            print(f"Updated: {players}/{max_players} - {map_name}")

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    client.loop.create_task(update_status())

client.run(TOKEN)