from dotenv import load_dotenv
import os
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import discord

load_dotenv()
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')

def send_message_to_discord(message):

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
        channel_id = CHANNEL_ID  # Replace with your channel's ID
        channel = client.get_channel(CHANNEL_ID)

        if channel:
            # Send the "Hello World!" message
            await channel.send("Hello again!")

        await client.close()


# Run the bot with your token
# client.run(BOT_TOKEN)  # Replace with your bot's token
