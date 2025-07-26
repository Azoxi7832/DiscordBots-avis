import requests
import json
import time
import datetime

from discord import SyncWebhook, Embed

with open("config.json") as f:
    config = json.load(f)

lapis_api_key = config["lapis_api_key"]
place_id = config["place_id"]
webhook_url = config["webhook_url"]

webhook = SyncWebhook.from_url(webhook_url)
avis_envoyes = set()

def get_reviews():
    url = f"https://api.lapis.to/v1/places/{place_id}/reviews"
    headers = {
        "Authorization": f"Bearer {lapis_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get("reviews", [])

def envoyer_avis(avis):
    for review in avis:
        id_unique = review.get("review_id") or f"{review.get('author_name')}-{review.get('time')}"
        if id_unique in avis_envoyes:
            continue

        avis_envoyes.add(id_unique)

        embed = Embed(
            title="📢 Nouvel avis Google",
            color=0x00AE86,
            timestamp=datetime.datetime.utcfromtimestamp(review.get("time", time.time()))
        )
        embed.add_field(name="👤 Nom", value=review.get("author_name", "Inconnu"), inline=True)
        embed.add_field(name="⭐ Note", value=f"{review.get('rating', '?')}/5", inline=True)
        embed.add_field(name="💬 Avis", value=review.get("text", "Aucun commentaire"), inline=False)
        embed.set_footer(text="Google Reviews via Lapis", icon_url="https://www.gstatic.com/images/branding/product/1x/google_reviews_512dp.png")

        webhook.send(embed=embed)

print("🟢 Bot lancé. Surveillance des avis toutes les secondes...")

while True:
    try:
        reviews = get_reviews()
        envoyer_avis(reviews)
    except Exception as e:
        print(f"❌ Erreur : {e}")
    time.sleep(1)
