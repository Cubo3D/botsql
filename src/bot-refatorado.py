import telebot, sqlite3
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()


# Necessária para quando precisar fazer algum modificação no database
def get_connection():
    """Inicia uma conexão a cada therad"""
    return sqlite3.connect("unregistered-users.db", check_same_thread=False)


# Config inicial da tabela do SQLite
conn = get_connection()
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS unregistered_users (
    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    userid INTEGER NOT NULL UNIQUE,
    admin INTEGER NOT NULL DEFAULT 0 CHECK (admin IN (0, 1)) -- Faz com que o valor seja apenas 0 ou 1, se tiver um valor diferente dá erro
    )"""
)
conn.commit()
conn.close()


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
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM unregistered_users WHERE userid = ?", (user.id,)
            )
            try:
                if cursor.fetchone():
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
                    cursor.execute(
                        """INSERT INTO unregistered_users
                            (username, userid, admin) VALUES
                            (?, ?, ?)""",
                        (user.username, user.id, 0),
                    )
                    bot.send_message(
                        call.from_user.id,
                        "pedido concluido, espere até que o administrador permita",
                    )
                conn.commit()

            except sqlite3.Error as e:
                print(f"Erro no banco: {e}")
                print("Notificando o administrador")
                bot.send_message(
                    call.from_user.id,
                    "Opa! acabamos de encontrar um erro, mensagem do erro enviado ao administrador, iremos arrumar esse erro e quando terminamos avisaremos!",
                )

            finally:
                cursor.close()
                conn.close()

        case "botton_no":
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM unregistered_users WHERE userid = ?", (user.id,)
            )
            if cursor.fetchone():
                bot.send_message(
                    call.from_user.id,
                    "Você já está na fila de cadastrado, apenas espere que o administrador permita o teu cadastro. Se quiser cancelar o cadastro digite /cancel",
                )
            else:
                bot.send_message(call.from_user.id, "Certo, tenha um bom dia")


print("Bot em execução")
bot.infinity_polling()
