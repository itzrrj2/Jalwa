import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 19593445
API_HASH = "f78a8ae025c9131d3cc57d9ca0fbbc30"
BOT_TOKEN = "7558999351:AAG0N7kKfEv-ZwQMqMqo6TM84zmHSvuMNoE"

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

# Handler
@app.on_message(filters.channel)
async def replace_caption(client: Client, message: Message):
    if message.caption and OLD_LINK in message.caption:
        new_caption = message.caption.replace(OLD_LINK, NEW_LINK)

        # Also update "CLICK HERE" text part
        new_caption = new_caption.replace(
            "Prediction Only For 👉 CLICK HERE 👈",
            f"Prediction Only For 👉 {NEW_LINK} 👈"
        )

        try:
            await message.edit_caption(new_caption, parse_mode="HTML")
            print("Caption edited successfully.")
        except Exception as e:
            print(f"Failed to edit caption: {e}")

# Run bot
app.run()
