from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Client("your_bot_token")

@app.on_message(filters.command("start"))
def random_answer(client, message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("View Movies", callback_data="view")]]
    )
    message.reply_text(
        "Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\nShare and Support💝",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

@app.on_message(filters.command("view"))
def start(client, message):
    message.reply_text("Please wait for 10 seconds", parse_mode="Markdown")
    tamilmv()
    keyboard = make_keyboard()
    message.reply_text(
        "Select a Movie from the list 🙂 : ", reply_markup=keyboard, parse_mode="HTML"
    )
