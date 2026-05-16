import discord
import asyncio

import os
TOKEN = os.getenv("TOKEN")
GUILD_ID = 857180887421288448
BOT_NAME = "Digger HLL"

# Replace with your server ID from BattleMetrics or API
BATTLEMETRICS_ID = "25216465"

intents = discord.Intents.default()
client = discord.Client(intents=intents)


QUERY_IP = "hll2.taskforcekoala.com.au"
QUERY_PORT = 26965

from a2s import A2S_INFO

QUERY_IP = "hll2.taskforcekoala.com.au"
QUERY_PORT = 26965

def get_server_data():
    address = (QUERY_IP, QUERY_PORT)

    info = A2S_INFO(address, timeout=5)

    players = info.player_count
    max_players = info.max_players
    map_name = info.map_name

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