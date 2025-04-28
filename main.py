from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 19593445
API_HASH = "f78a8ae025c9131d3cc57d9ca0fbbc30"
BOT_TOKEN = "7834936430:AAFL6GZDWXeSbZaJ870dSN6wdZObWrrvTrc"

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
    if message.caption and (OLD_LINK in message.caption or "CLICK HERE" in message.caption):
        new_caption = message.caption

        # Replace link
        new_caption = new_caption.replace(OLD_LINK, NEW_LINK)

        # Replace "CLICK HERE" with the new URL
        new_caption = new_caption.replace(
            "CLICK HERE",
            f"{NEW_LINK}"
        )

        try:
            await message.edit_caption(new_caption)  # ❗ No parse_mode
            print("Caption edited successfully.")
        except Exception as e:
            print(f"Failed to edit caption: {e}")

# Run bot
app.run()
