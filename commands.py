# Importamos las librerias de PTB
# -
# We import PTB libraries

from telegram import InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

# Importamos los archivos de constantes y renders para poder usarlos
# -
# We import the constants and renders files to be able to use them.

from constants import ADMIN
from renders import render_main

# Hacemos el handle del start, basicamente, si el chat es privado, le contestamos al usuario con un texto y un
# keyboard con el menu. La idea es que ese sea el menu principal del bot. El bot se puede usar en su totalidad
# Usando unicamente este mensaje
# Notificar al admin de que alguien le mando un mensaje al bot
# -
# We make the handle of the start, basically, if the chat is private, we answer the user with a text and a
# keyboard with the menu. The idea is that this is the main menu of the bot. The bot can be used in its entirety
# Using only this message
# Notify the admin that someone sent a message to the bot


def handle_start(update, context):
    print("func -> handle_start")

    if update.message.chat.type == 'private':

        users_ids = context.bot_data.get('message_chats')

        if not users_ids:
            users_ids = [ADMIN]

        text, keyboard = render_main(update, context)

        update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

        chat_id = update.effective_message.chat_id

        if int(chat_id) != int(ADMIN) and chat_id not in users_ids:
            users_ids.append(ADMIN)
            context.bot.sendMessage(
                chat_id=ADMIN,
                text="🌟 New User! 🌟"
            )


# Esta función la suelo usar cuando genero contextos, basicamente le manda un mensaje al usuario diciendo que
# se cancelo la operación y muy importante: sale del contexto con un ConversationHandler.END
# -
# I use this function when I generate contexts, basically it sends a message to the user saying that
# the operation was cancelled and very important: it exits the context with a ConversationHandler.END

def cancel(update, context):
    print("func -> cancel")

    user_language = update.effective_user['language_code']

    if user_language == 'es':
        mensaje = 'Acción cancelada, como Foucault'
    else:
        mensaje = 'The action is cancelled, like Foucault'

    update.message.reply_text(
        text=mensaje,
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END


def handle_help(update, context):
    print("func -> handle_help")

    user_language = update.effective_user['language_code']

    if user_language == 'es':
        mensaje = 'Usa /start para ver el menú principal. ' \
                  '\nTodas mis funcionalidades se encuentran ahí.' \
                  '\nEl idioma lo capturo directamente de tu usuario de telegram :) ' \
                  '(Depende del idioma en el que tengas instalada la app). Por ahora soporto inglés por defecto ' \
                  'y español.' \
                  '\nMira el video de ejemplo de uso aquí' \
                  '\n👉 https://youtu.be/ffgrUZghz6I'
    else:
        mensaje = 'Use /start to see the main menu. ' \
                  '\nAll my features are there. ' \
                  '\nThe language is captured directly from your telegram user :) ' \
                  '(It depends on the language in which you have installed the app). ' \
                  'For now I support english by default and spanish.'\
                  '\nTake a look to this video' \
                  '\n👉 https://youtu.be/ffgrUZghz6I'

    update.message.reply_text(
        text=mensaje,
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END
