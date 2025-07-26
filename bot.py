import discord
import asyncio
import json
import datetime
from avis_scraper import setup_driver, get_reviews

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["token"]
CHANNEL_ID = config["channel_id"]
MAPS_URL = config["google_maps_url"]
INTERVAL = config.get("check_interval", 30)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
driver = setup_driver()

@client.event
async def on_ready():
    print(f"✅ Connecté en tant que {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Channel introuvable !")
        return
    await avis_scraping_loop(channel)

async def avis_scraping_loop(channel):
    await asyncio.sleep(5)
    print(f"📡 Scraping lancé toutes les {INTERVAL} secondes...")

    while True:
        try:
            reviews = get_reviews(driver, MAPS_URL)
            for review in reviews:
                embed = discord.Embed(
                    title="📢 Nouvel avis Google (scrapé)",
                    color=0x00AE86,
                    timestamp=datetime.datetime.fromtimestamp(review["timestamp"])
                )
                embed.add_field(name="👤 Nom", value=review["nom"], inline=True)
                embed.add_field(name="⭐ Note", value=f"{review['note']}/5", inline=True)
                embed.add_field(name="💬 Avis", value=review["commentaire"], inline=False)
                embed.set_footer(text="Scrapé depuis Google Maps")

                await channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erreur scraping ou Discord : {e}")
        await asyncio.sleep(INTERVAL)

client.run(TOKEN)
