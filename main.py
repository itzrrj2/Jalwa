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

# Handler for all channel messages
@app.on_message(filters.channel)
async def edit_message(client: Client, message: Message):
    text_to_edit = None

    # Case 1: If message has a caption (photo/video etc.)
    if message.caption and (OLD_LINK in message.caption or "CLICK HERE" in message.caption):
        text_to_edit = message.caption

    # Case 2: If message is a normal text message
    elif message.text and (OLD_LINK in message.text or "CLICK HERE" in message.text):
        text_to_edit = message.text

    if text_to_edit:
        # Replace old register link with new one
        updated_text = text_to_edit.replace(OLD_LINK, NEW_LINK)

        # Replace "CLICK HERE" with the new link
        updated_text = updated_text.replace(
            "CLICK HERE",
            f"{NEW_LINK}"
        )

        try:
            if message.caption:
                await message.edit_caption(updated_text)  # Edit caption if it was a photo/video
            else:
                await message.edit_text(updated_text)      # Edit text if it was a text message
            print(f"Edited message ID {message.id} successfully.")
        except Exception as e:
            print(f"Failed to edit message ID {message.id}: {e}")

# Run bot
app.run()
