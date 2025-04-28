import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 19593445
API_HASH = "f78a8ae025c9131d3cc57d9ca0fbbc30"
BOT_TOKEN = "7834936430:AAFL6GZDWXeSbZaJ870dSN6wdZObWrrvTrc"

# Channels list
CHANNEL_IDS = ["-1002639969488", "-1002372000442"]
# Example: ["jalwawin", "jalwagame4"] or ["-1001234567890", "-1009876543210"]

# Create bot instance
app = Client(
    "link_replacer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Constants
OLD_LINK_PATTERN = r"https://www\.jalwawin3\.com/#/register\?invitationCode=\d+"
NEW_LINK = "https://www.jalwagame4.com/#/register?invitationCode=35818757916"

async def process_message(message: Message):
    text_to_edit = None

    if message.caption and (re.search(OLD_LINK_PATTERN, message.caption) or "CLICK HERE" in message.caption):
        text_to_edit = message.caption
    elif message.text and (re.search(OLD_LINK_PATTERN, message.text) or "CLICK HERE" in message.text):
        text_to_edit = message.text

    if text_to_edit:
        updated_text = re.sub(OLD_LINK_PATTERN, NEW_LINK, text_to_edit)
        updated_text = updated_text.replace("CLICK HERE", f"{NEW_LINK}")

        try:
            if message.caption:
                await message.edit_caption(updated_text)
            else:
                await message.edit_text(updated_text)
            print(f"Edited message ID {message.id} successfully in chat {message.chat.id}.")
        except Exception as e:
            print(f"Failed to edit message ID {message.id}: {e}")

@app.on_message(filters.channel)
async def on_new_message(client: Client, message: Message):
    if str(message.chat.id) in CHANNEL_IDS or message.chat.username in CHANNEL_IDS:
        await process_message(message)

@app.on_edited_message(filters.channel)
async def on_edited_message(client: Client, message: Message):
    if str(message.chat.id) in CHANNEL_IDS or message.chat.username in CHANNEL_IDS:
        await process_message(message)

async def main():
    await app.start()
    print("Bot Started.")

    print("Scanning old messages for all channels...")
    for chat_id in CHANNEL_IDS:
        try:
            async for message in app.get_chat_history(chat_id, limit=500):
                await process_message(message)
            print(f"Finished scanning chat: {chat_id}")
        except Exception as e:
            print(f"Failed to scan chat {chat_id}: {e}")
    print("Old messages scan complete.")

    await idle()  # To keep the bot alive

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
