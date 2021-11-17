from constants import *
from telegram.ext import Updater, CommandHandler


def handle_start(update, context):
    print("Dentro de handle_messages")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']

    if user_language == "es":
        response = f"Hola {user_first_name}, pronto estare operativo!"
    else:
        response = f"Hi {user_first_name}, I will be operational soon!."
    update.message.reply_text(
        text=response,
    )
    context.bot.sendMessage(
        chat_id=ADMIN,
        text="Un usuario le hablo al bot! Ponete a codear así lo pueden usar!"
    )


if __name__ == '__main__':
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(
        CommandHandler('start', handle_start)
    )
    updater.start_polling()
    print('Bot esta más vivo que vivin')
    updater.idle()
