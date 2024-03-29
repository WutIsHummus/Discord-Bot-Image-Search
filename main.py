import discord
import requests
from discord.ext import commands
import os
import random
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SEARCH = os.getenv('SEARCH')
GOOGLE = os.getenv('GOOGLE')

def search_images(query, api_key, cse_id, start=1, num=1):
    """Search for images using Google Custom Search JSON API."""
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key,
        'searchType': 'image',
        'num': num,
        'start': start
    }
    response = requests.get(url, params=params)
    result = response.json()
    return [item['link'] for item in result.get('items', [])]

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self.ping_count = 0  # Counter for the number of times the bot has been pinged

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if self.user.mentioned_in(message) and not message.mention_everyone:
            self.ping_count += 1  # Increment the counter
            animals = ["cats", "kittens"]
            query_elements = ["silly", "baby", "cute", "funny", "adorable", "small", "fluffy", "tiny", "soft", "fat", "cuddly"] 
            selected_animal = random.choice(animals)
            selected_elements = random.sample(query_elements, 2)
            query = " ".join(selected_elements) + f" {selected_animal}"  
            start_index = self.ping_count
            images = search_images(query, GOOGLE, SEARCH, start=start_index)  
            if images:
                await message.channel.send(images[0])
            else:
                await message.channel.send("No images found.")
bot = MyBot()
bot.run(DISCORD_TOKEN) 
