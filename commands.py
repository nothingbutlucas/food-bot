from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import ConversationHandler

from constants import ADMIN
from renders import render_main


def handle_start(update, context):
    # print("Dentro de handle_start")

    if update.message.chat.type == 'private':

        text, keyboard = render_main(update, context)

        update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

        # Notify the admins
        if int(update.effective_message.chat_id) != int(ADMIN):
            context.bot.sendMessage(
                chat_id=ADMIN,
                text="🌟 New User! 🌟"
            )


def cancel(update, context):
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
