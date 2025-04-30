import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("anon_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

users = {}
waiting_list = []

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    users.pop(message.from_user.id, None)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Boy", callback_data="gender_boy")],
        [InlineKeyboardButton("Girl", callback_data="gender_girl")]
    ])
    await message.reply(
        "✨ <b>Welcome to AnonyChat!</b>\nPlease choose your gender:",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("gender_"))
async def handle_gender(client, callback_query):
    user_id = callback_query.from_user.id
    gender = callback_query.data.split("_")[1]
    users[user_id] = {"gender": gender, "state": "idle", "partner": None}

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Chat with Stranger", callback_data="chat_stranger")],
        [InlineKeyboardButton("Chat with Boy", callback_data="chat_boy")],
        [InlineKeyboardButton("Chat with Girl", callback_data="chat_girl")]
    ])
    await callback_query.message.edit_text(
        "🔗 <b>Main Menu</b>\nWho do you want to chat with?",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("chat_"))
async def handle_chat_preference(client, callback_query):
    user_id = callback_query.from_user.id
    preference = callback_query.data.split("_")[1]
    await match_user(client, user_id, preference, callback_query.message)

async def match_user(client, user_id, preference, message):
    user = users[user_id]
    user["state"] = "waiting"
    user["preference"] = preference

    for other_id in waiting_list:
        other = users.get(other_id)
        if other and other["state"] == "waiting" and other_id != user_id:
            if preference == "stranger" and (
                other["preference"] == "stranger" or user["gender"] == other["preference"]
            ):
                await connect_users(client, user_id, other_id)
                waiting_list.remove(other_id)
                return
            if other["gender"] == preference and (
                other["preference"] == "stranger" or user["gender"] == other["preference"]
            ):
                await connect_users(client, user_id, other_id)
                waiting_list.remove(other_id)
                return

    waiting_list.append(user_id)
    await message.edit_text("🔎 Looking for a partner...")

async def connect_users(client, user1, user2):
    users[user1]["state"] = "chatting"
    users[user1]["partner"] = user2
    users[user2]["state"] = "chatting"
    users[user2]["partner"] = user1

    await client.send_message(user1, "✅ You are now connected! Say hi!")
    await client.send_message(user2, "✅ You are now connected! Say hi!")

@app.on_message(filters.text)
async def relay_message(client, message: Message):
    user_id = message.from_user.id
    user = users.get(user_id)

    if user and user["state"] == "chatting":
        partner_id = user.get("partner")
        if partner_id and partner_id in users:
            await client.send_message(partner_id, f"💬 Stranger: {message.text}")
        else:
            await message.reply("⚠️ Your partner disconnected. Type /start to begin again.")
    else:
        await message.reply("❌ You're not connected. Use /start to begin.")

@app.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    user_id = message.from_user.id
    user = users.get(user_id)

    if user:
        partner_id = user.get("partner")
        if user["state"] == "chatting" and partner_id:
            await client.send_message(partner_id, "❌ Stranger has left the chat.")
            users[partner_id]["state"] = "idle"
            users[partner_id]["partner"] = None

        if user_id in waiting_list:
            waiting_list.remove(user_id)

        users[user_id]["state"] = "idle"
        users[user_id]["partner"] = None
        await message.reply("✅ You left the chat.")
    else:
        await message.reply("⚠️ You're not in a chat.")

app.run()
