import telebot
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from loguru import logger

from services import create_user, get_user

load_dotenv()

# Telegram
token = getenv("BOT_TOKEN")
if not token:
    raise ValueError(
        "BOT_TOKEN not found in .env file, did you configure the .env file?"
    )

bot = telebot.TeleBot(token)


# Comando Start
@bot.message_handler(["start"])
def start(msg: types.Message):

    markup = types.InlineKeyboardMarkup()

    botton_yes = types.InlineKeyboardButton(
        "I want to register", callback_data="botton_yes"
    )
    botton_no = types.InlineKeyboardButton("No, thank you", callback_data="botton_no")

    markup.add(botton_yes, botton_no)

    bot.send_message(
        msg.chat.id,
        "Hello, welcome to BotSQL, this bot is for..., if you want to chat with the bot you must request registration authorization",
        reply_markup=markup,
    )


# Verificação dos botões
@bot.callback_query_handler()
def resposta_botao(call: types.CallbackQuery):
    user = call.from_user

    match call.data:
        case "botton_yes":
            db_user = get_user(user.id)
            if db_user:
                bot.send_message(
                    call.from_user.id,
                    "Hey! You're already in the queue, we've already notified the administrator, just wait",
                )
            else:
                bot.send_message(
                    call.from_user.id, "Requesting permission from the administrator..."
                )
                logger.info(
                    f"New registration request, saving to database and notifying the administrator {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                )
                create_user(user.username, user.id)
                bot.send_message(
                    call.from_user.id,
                    "Request completed, wait until the administrator approves",
                )

        case "botton_no":
            db_user = get_user(user.id)
            if db_user:
                bot.send_message(
                    call.from_user.id,
                    "You're already in the registration queue, just wait for the administrator to approve your registration. If you want to cancel, type /cancel",
                )
            else:
                bot.send_message(call.from_user.id, "Sure, have a good day!")


logger.info("Bot running")
bot.infinity_polling()
