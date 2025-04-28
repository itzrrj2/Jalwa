import html
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
    if message.caption and (OLD_LINK in message.caption or "CLICK HERE" in message.caption):
        new_caption = message.caption

        # Replace link
        new_caption = new_caption.replace(OLD_LINK, NEW_LINK)

        # Replace "CLICK HERE" with new URL properly underlined and bold
        new_caption = new_caption.replace(
            "CLICK HERE",
            f"<u><b>{NEW_LINK}</b></u>"
        )

        # Escape full caption safely
        safe_caption = html.escape(new_caption)
        
        # After escaping, manually re-insert tags
        safe_caption = safe_caption.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
        safe_caption = safe_caption.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")

        try:
            await message.edit_caption(safe_caption, parse_mode="HTML")
            print("Caption edited successfully.")
        except Exception as e:
            print(f"Failed to edit caption: {e}")

# Run bot
app.run()
