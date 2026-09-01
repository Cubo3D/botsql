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
        "BOT_TOKEN não encontrado no arquivo .env, você configurou o arquivo .env?"
    )

bot = telebot.TeleBot(token)


# Comando Start
@bot.message_handler(["start"])
def start(msg: types.Message):

    markup = types.InlineKeyboardMarkup()

    botton_yes = types.InlineKeyboardButton(
        "Quero me cadastrar", callback_data="botton_yes"
    )
    botton_no = types.InlineKeyboardButton("Não, obrigado", callback_data="botton_no")

    markup.add(botton_yes, botton_no)

    bot.send_message(
        msg.chat.id,
        "Olá bem-vindo ao BotSQL, esse bot serve para..., se quiser conversar com o bot você deve pedir autorização de cadastro",
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
                    "Opa! você já está na fila de espera, já notificamos o administrador, então basta apenas esperar",
                )
            else:
                bot.send_message(
                    call.from_user.id, "Pedindo permissão ao administrador..."
                )
                print(
                    f"Novo pedido de cadastro, salvando no database e notificando o administrador {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                )
                create_user(user.username, user.id)
                bot.send_message(
                    call.from_user.id,
                    "pedido concluido, espere até que o administrador permita",
                )

        case "botton_no":
            db_user = get_user(user.id)
            if db_user:
                bot.send_message(
                    call.from_user.id,
                    "Você já está na fila de cadastrado, apenas espere que o administrador permita o teu cadastro. Se quiser cancelar o cadastro digite /cancel",
                )
            else:
                bot.send_message(call.from_user.id, "Certo, tenha um bom dia!")


print("Bot em execução")
bot.infinity_polling()
