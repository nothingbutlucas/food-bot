'''
Hola! Bueno, como este es el main, voy a contar muy brevemente de que va este bot.
La idea surgío de el problema de no saber que cocinar con lo que teniamos, entonces desarrollamos una API.
Este bot se conecta a la food-api, para capturar la info de las recetas.
Ahora si, empecemos a ver el codigo
-
Well, as this is the main, I'm going to tell you very briefly what this bot is about.
The idea came from the problem of not knowing what to cook with what we had, so we developed an API.
This bot connects to the food-api, to capture the recipes info.
Now, let's start looking at the code.
'''

# Obviamente importamos las librerias necesarias para que el bot funcione ok.
# En este caso estoy usando PTB
# PTB trabaja con el modulo logging para mostrar algunos outputs, sirve más que nada para debugear y
# hacer print de algunas infos
# -
# Obviously we import the necessary libraries for the bot to work ok.
# In this case I'm using PTB
# PTB works with the logging module to display some outputs, it is mostly used for debugging and
# print some infos

import logging
from telegram import InlineKeyboardMarkup, ParseMode
import telegram
from telegram.botcommand import BotCommand
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, CallbackQueryHandler

# Bueno y acá estoy importando los archivos con los que estoy trabajando, estan todos en el mismo directorio del main
# -
# Well and here I am importing the files I am working with, they are all in the same directory as the main one

from callbacks import main_recipes, see_recipe, main, lets_cook, what_cook, ingredients, about, see_step_by_step
from constants import *
from commands import handle_start, handle_help
from renders import render_back_menu

# Acá pongo este logging para cuando arranque el bot, antes de ejecutar la función main() para mostrar la hora,
# el nombre y etc.
# -
# Here I put this logging for when I start the bot, before executing the main() function to show the time,
# the name and etc.

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Esta función lo que hace es contestar a los textos (mensajes) que reciba
# A veces pongo un print justo al principio de la función para debuggear
# Luego cuando voy a devolver un mensaje al usuario, suelo capturar el nombre y el language_code
# Ambas infos las captura directamente del update.
# Luego el keyboard lo capturo de una función del archivo renders, dentro de ese keyboard, hay un botón para volver
# al menu principal. Porque la idea es que se maneje el bot con botones y que no sea necesario teclear nada :)
# Dependiendo del lenguaje que tenga el usuario en el telegram, le contesto en ingles por defecto ó en caso de que
# este en español, en español
# Luego solo por seguridad, se le envia al administrador, el texto que haya enviado el usuario
# -
# What this function does is to answer the texts (messages) that it receives.
# Sometimes I put a print right at the beginning of the function for debugging purposes.
# Then when I'm going to return a message to the user, I usually capture the name and the language_code
# Both infos are captured directly from the update.
# Then the keyboard is captured from a function of the renders file, inside that keyboard, there is a button to go back
# to the main menu. Because the idea is that the bot is managed with buttons and it is not necessary to type anything :)
# Depending on the language that the user has in the telegram, I answer in English by default or in case the user is in
# Spanish, in Spanish.
# is in Spanish, in Spanish
# Then just for security, the text sent by the user is sent to the administrator.


def handle_message(update, context):
    print("func -> handle_message")
    # print("Dentro de handle_messages")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    user_text = update.message.text

    if update.message.chat.type == 'private':

        if user_language == 'es':
            response = f"Hola {user_first_name} soy solo un bot, si quieres hablar con devycoso, envia un mail a " \
                       f"devycoso@gmail.com"
        else:
            response = f"Hi {user_first_name} im only a bot, if u want to talk with devycoso, send an email to " \
                       f"devycoso@gmail.com"

        keyboard = render_back_menu()

        update.message.reply_text(
            text=response,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.bot.sendMessage(
            chat_id=ADMIN,
            text="An user send this message to the bot:"
                 f"\n<i>{user_text}</i>",
            parse_mode=ParseMode.HTML
        )

# Acá hago esta pequeña función para capturar los errores, primero hago un print del error, luego solicito que
# se le envie el error al ADMIN
# -
# Here I make this little function to capture the errors, first I print the error, then I request that
# to send the error to ADMIN


def error_handler(update, context):
    print("func -> error_handler ❌")
    try:
        raise context.error
    except telegram.TelegramError as error:
        print(error.message)
        context.bot.sendMessage(
            chat_id=ADMIN,
            text=str(error)
        )

# Acá hago la función main_bot que no toma parametros, lo que hace esta función es ejecutar el bot


def main_bot() -> None:
    print("func -> main_bot 🤖")
    updater = Updater(token=TOKEN, use_context=True)
    bot = telegram.Bot(token=TOKEN)
    bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Cook! | Cocinar!'),
            BotCommand(command='help', description='Ayuda | Help'),

        ],
        scope=telegram.BotCommandScopeAllPrivateChats()
    )
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', handle_start))
    dp.add_handler(CommandHandler('help', handle_help))
    dp.add_handler(CallbackQueryHandler(pattern='step_by_step', callback=see_step_by_step))
    dp.add_handler(CallbackQueryHandler(pattern=f'main', callback=main))
    dp.add_handler(CallbackQueryHandler(pattern='ingredients', callback=ingredients))
    dp.add_handler(CallbackQueryHandler(pattern=f'lets_cook', callback=lets_cook))
    dp.add_handler(CallbackQueryHandler(pattern=f'about', callback=about))
    dp.add_handler(
        ConversationHandler(
            entry_points=[(CallbackQueryHandler(pattern=f'what_u_can_cook', callback=what_cook)),
                          (CallbackQueryHandler(pattern='recipes', callback=main_recipes)),
                          (CallbackQueryHandler(see_recipe)),
                          (CallbackQueryHandler(what_cook))],
            states={},
            fallbacks=[(CallbackQueryHandler(pattern=f'main', callback=main))]
        )
    )
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error_handler)
    updater.start_polling()
    print('Bot esta más vivo que vivin 🤖')
    updater.idle()


if __name__ == '__main__':
    main_bot()
