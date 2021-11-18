import logging

from telegram import InlineKeyboardMarkup

from callbacks import main_recipes, see_recipe, main, lets_cook, what_cook, ingredients, about
from constants import *
import telegram
from telegram.botcommand import BotCommand
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, CallbackQueryHandler
from commands import handle_start
from renders import render_back_menu

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def handle_message(update, context):
    # print("Dentro de handle_messages")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    user_text = update.message.text
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
             f"\n<i>{user_text}</i>"
    )


def error_handler(update, context):
    try:
        raise context.error
    except telegram.TelegramError as error:
        print(error.message)
        context.bot.sendMessage(
            chat_id=ADMIN,
            text=error
        )


def main_bot() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    bot = telegram.Bot(token=TOKEN)
    bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Cook! | Cocinar!'),
        ],
        scope=telegram.BotCommandScopeAllPrivateChats()
    )
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', handle_start))
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
    print('Bot esta más vivo que vivin')
    updater.idle()


if __name__ == '__main__':
    main_bot()
