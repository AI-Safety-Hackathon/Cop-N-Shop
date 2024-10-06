from dotenv import load_dotenv
import os
import discord

def price_comparison(product_data, market_data, product_name_or_id):
    market_lookup = {product['id']: product 
                     for product in market_data['products']}
    
    for data in product_data:
          if (data['id'] == product_name_or_id or 
              data['name'] == product_name_or_id):
              market_product = market_lookup.get(data['id'])
              if market_product:
                  vendor_price = data['original_price']
                  market_price = market_product['average_market_price']
                  
                  return {
                      "product_name": data['name'],
                      "vendor_price": vendor_price,
                      "market_price": market_price,
                      "comparison": (
                        "lower" if vendor_price < market_price else
                        "higher" if vendor_price > market_price else
                        "equal")
                  }
              else:
                  return {
                      "product_name": data['name'],
                      "error": "No market data available for this product."
                  }
    
    return {"error": "Product not found in the vendor list."}
  



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
            await channel.send(message)

        await client.close()

    client.run(BOT_TOKEN)
