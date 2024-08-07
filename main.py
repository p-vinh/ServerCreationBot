import discord
import asyncio
from dotenv import load_dotenv
import os
import MenuButtons as mb

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, *args, **kwargs)
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        self.run(token)
        
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!menu'):
            # Create an Action Row that will be added to the message
            view = mb.MenuButtons(self)
            await message.channel.send("Choose an option:", view=view)

  

client = MyClient()
