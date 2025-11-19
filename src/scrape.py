import os
import discord
import logging
import pickle
import json
import asyncio
import sys

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class KirbyClient(discord.Client):

    # Attach to on_ready event
    async def on_ready(self):

        # Print some verbose messages to console
        print('Logged on as ' + str(self.user))

        # Initiate scraping all channels
        await self.scrape_channels()

        print('Complete')
        await self.close()

    # Scrapes the wordle channel and inline calculates statistics
    async def scrape_channels(self):

        messages = {}

        for server in self.guilds:
            for channel in server.channels:

                if str(channel.type) == 'text':

                    print('Scraping channel: ' + channel.name)

                    # Make sure channel name exists in messages array
                    if channel.name not in messages:
                        messages[channel.name] = []

                    # Iterate over channel history
                    async for message in channel.history(limit = int(os.getenv('LIMIT')), oldest_first = True):

                        author = message.author.name
                        message_content = message.content
                        messages[channel.name].append({
                            'author': author,
                            'content': message_content,
                            'created_at': str(message.created_at),
                            'updated_at': str(message.edited_at) if message.edited_at else ""
                        })

        # Save raw messages to disk
        with open('/data/raw-messages.json', 'w') as f:
            json.dump(messages, f, indent = 4)

intents = discord.Intents.default()
intents.message_content = True

client = KirbyClient(intents = intents)
client.run(os.getenv('TOKEN'), log_handler = handler)
