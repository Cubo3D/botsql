# O que falta:
# O bot já consegue cadastrar usuários
# O bot não tem comandos pro admin
# o bot não consegue atualizar informações
# O bot está com alguns problemas em partes específicas de cadastro no bot, exemplo se você clicar no comando "sim" duas vezes ele vai dar erro na segunda ou vai falar que você já está cadastrado mesmo não estando
# Quando você está na fila de espera e aperta no não ele fala que o cadastro foi cancelado mesmo não sendo cancelado
# Talvez eu esteja errado em algumas coisas, porque a ultima vez que testei já faz mais de uma semana

# O que é bom adicionar:
# umas segunda tabela dos usuários que querem fazer o cadastro, mas ainda não foi validado pelo admin

# Se quiser testar o bot: https://t.me/lansqlbot_bot

import telebot, sqlite3
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()


# SQLite
def get_connection():
    """Inicia uma conexão a cada therad"""  # Sempre que for criar um novo comando defina as váriaveis de função
    return sqlite3.connect("unregistered-users.db", check_same_thread=False)


def init_db():
    """Inicia recria a tabela se ele não existir"""
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS unregistered_users (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    userid INTEGER NOT NULL UNIQUE,
                    admin INTEGER NOT NULL DEFAULT 0 CHECK (admin IN (0, 1)) -- Faz com que o valor seja apenas 0 ou 1, se tiver um valor diferente dá erro
                    )""")
    conexao.commit()
    conexao.close()


# Telegram
token = getenv("BOT_TOKEN")
if not token:
    raise ValueError(
        "BOT_TOKEN não encontrado no arquivo .env, você seguiu o exemplo que eu deixei?"
    )

bot = telebot.TeleBot(token)


# Nos meus ultimos testes aqui não teve nenhuma problema
@bot.message_handler(["start"])
def start(msg: types.Message):
    conexao = get_connection()
    cursor = conexao.cursor()

    markup = types.InlineKeyboardMarkup()

    botao_sim = types.InlineKeyboardButton("Sim", callback_data="botao_sim")
    botao_nao = types.InlineKeyboardButton("Não", callback_data="botao_nao")
    botao_sobre = types.InlineKeyboardButton("Sobre", callback_data="botao_sobre")

    markup.add(botao_sim, botao_nao, botao_sobre)

    bot.send_message(
        msg.chat.id, "Olá! Você gostaria de se cadastrar?", reply_markup=markup
    )


@bot.callback_query_handler()
def resposta_botao(call: types.CallbackQuery):
    conexao = get_connection()
    cursor = conexao.cursor()

    user = call.from_user

    match call.data:

        case "botao_sim":
            cursor.execute(
                "SELECT userid FROM unregistered_users WHERE id = ?", (user.id,)
            )
            result_id = cursor.fetchone()
            # Nesse if que vive o problema
            if result_id:
                bot.send_message(
                    call.message.chat.id, "Você já está na fila de cadastro"
                )
            else:
                bot.send_message(call.message.chat.id, "Cadastrando")
                print(
                    f"Cadastrando novo usuário {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"
                )
                cursor.execute(
                    """INSERT INTO unregistered_users
                            (username, userid, admin) VALUES (?, ?, ?)""",
                    (user.username, user.id, "0"),
                )
                conexao.commit()
                conexao.close()

                bot.send_message(
                    call.message.chat.id,
                    "Agora espere que o admin permita o seu cadastro",
                )
                print(
                    "Necessita de permissão do admin para concluir o cadastro. Avisando"
                )

        case "botao_nao":
            cursor.execute(
                "SELECT userid FROM unregistered_users WHERE id = ?", (user.id,)
            )
            result_id = cursor.fetchone()
            # E nesse também
            if result_id:
                bot.send_message(
                    call.message.chat.id,
                    "Você já está na fila de espera, mas caso queira sair:",  # Irei colocar depois os botões: "Quero sair" e "Não, obrigado"
                )

            else:
                bot.send_message(call.message.chat.id, "Certo, tenha um ótimo dia")
            conexao.close()
        case "botao_sobre":
            bot.send_message(
                call.message.chat.id,
                "Esse bot é só um bot de testes para uma banco de dados",
            )


print("Bot executando👍")
bot.infinity_polling()
