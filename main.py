import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 12345678    # replace with your API_ID
API_HASH = "your_api_hash"  # replace with your API_HASH
BOT_TOKEN = "your_bot_token"  # replace with your bot token

# Create bot instance
app = Client(
    "link_replacer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Constants
OLD_LINK = "https://www.jalwawin3.com/#/register?invitationCode=25587256605"
NEW_LINK = "https://www.jalwagame4.com/#/register?invitationCode=35818757916"

# Message format
NEW_MESSAGE = f"""Register Link 👇🥳🎰💰
{NEW_LINK}
Prediction Only For 👉 {NEW_LINK} 👈
"""

# Handler to monitor messages
@app.on_message(filters.channel)
async def replace_message(client: Client, message: Message):
    if OLD_LINK in message.text:
        try:
            await message.edit_text(NEW_MESSAGE)
        except Exception as e:
            print(f"Failed to edit message: {e}")

# Run the bot
app.run()
