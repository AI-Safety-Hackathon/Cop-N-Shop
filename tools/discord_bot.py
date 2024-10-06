
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

import discord

# Set up intents (for reading message content, if required)
intents = discord.Intents.default()
intents.message_content = True  # Ensure this is enabled

# Initialize the bot client
client = discord.Client(intents=intents)


# Event to trigger when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Specify the channel ID you want to send the message to
    channel_id = 'CHANNEL_ID'  # Replace with your channel's ID
    channel = client.get_channel(channel_id)

    if channel:
        # Send the "Hello World!" message
        await channel.send("Hello, world!")


# Run the bot with your token
client.run('BOT_TOKEN')  # Replace with your bot's token
