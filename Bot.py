import discord
from discord.ext import commands
import os
import asyncio
from utils.config import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

async def main():
    async with bot:
        # ⬇️ CHARGEMENT DES COGS ICI
        await bot.load_extension("cogs.games")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())



