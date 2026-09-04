import telebot
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

from services import create_user, get_user

load_dotenv()

# Telegram
token = getenv("BOT_TOKEN")
if not token:
    raise ValueError(
        "TOKEN not found. Please set the BOT_TOKEN environment variable in the .env file."
    )

try:
    bot = telebot.TeleBot(token)

    # Start Command

    @bot.message_handler(["start"])
    def start(msg: types.Message):

        markup = types.InlineKeyboardMarkup()

        button_yes = types.InlineKeyboardButton(
            "I want to register", callback_data="button_yes"
        )
        button_no = types.InlineKeyboardButton(
            "No, thank you", callback_data="button_no")

        markup.add(button_yes, button_no)

        bot.send_message(
            msg.chat.id,
            "Hello, welcome to BotSQL! This bot is used for... If you want to chat with the bot, you must request registration authorization.",
            reply_markup=markup,
        )

    # Button Verification

    @bot.callback_query_handler()
    def button_response(call: types.CallbackQuery):
        user = call.from_user

        match call.data:
            case "button_yes":
                db_user = get_user(user.id)
                if db_user:
                    bot.send_message(
                        call.from_user.id,
                        "Oops! You are already on the waiting list. We have already notified the administrator, so just wait.",
                    )
                else:
                    bot.send_message(
                        call.from_user.id, "Requesting permission from the administrator..."
                    )
                    print(
                        f"New registration request, saving to database and notifying the administrator: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                    )
                    create_user(user.username, user.id)
                    bot.send_message(
                        call.from_user.id,
                        "Request completed. Wait until the administrator approves.",
                    )

            case "button_no":
                db_user = get_user(user.id)
                if db_user:
                    bot.send_message(
                        call.from_user.id,
                        "You are already on the registration waiting list. Just wait for the administrator to approve your registration. If you want to cancel the registration, type /cancel",
                    )
                else:
                    bot.send_message(call.from_user.id,
                                     "Alright, have a great day!")

    print("Bot is running...")
    bot.infinity_polling()

except Exception as e:
    print(f"Error on startup: {e}")
