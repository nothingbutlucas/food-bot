from telegram import InlineKeyboardMarkup, ParseMode
from renders import render_main, render_recipes, render_recipe, render_ingredients, render_to_cook, render_lets_cook, \
    render_about


def main(update, context):
    query = update.callback_query
    query.answer()

    text, keyboard = render_main(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main_recipes(update, context):
    query = update.callback_query
    query.answer()

    text, keyboard = render_recipes(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def see_recipe(update, context):
    query = update.callback_query
    query.answer()

    text, keyboard = render_recipe(update, context)

    if text == "Error: value is not a valid integer":
        return what_cook(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)

    )


def ingredients(update, context):
    query = update.callback_query
    query.answer()

    text, keyboard = render_ingredients(update, context)
    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def what_cook(update, context):
    print("Estamos en what_cook")
    query = update.callback_query
    query.answer()

    text, keyboard = render_to_cook(update, context)
    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def lets_cook(update, context):
    user_language = update.effective_user['language_code']

    query = update.callback_query
    query.answer()

    text, keyboard = render_lets_cook(update, context)

    if user_language == 'en':
        main_ingredients = "Main ingredients: "
        secondary_ingredients = "Secondary ingredients: "
        can_cook = "What can you cook with what you have?"
    else:
        main_ingredients = "Ingredientes principales: "
        secondary_ingredients = "Ingredientes secundarios: "
        can_cook = "¿Que puedes cocinar con lo que tienes?"

    if type(text) is type(list()):
        text_ = f'<b>{can_cook}</b>\n\n'
        for x in text:
            texto = x.split('[')
            title = texto[0]
            main_ings = texto[1]
            main_ings = main_ings.replace("'", "")
            main_ings = main_ings.replace("]", "")
            secon_ings = texto[2]
            secon_ings = secon_ings.replace("'", "")
            secon_ings = secon_ings.replace("]", "")
            if len(secon_ings) < 1:
                secon_ings = "-"
            text_ += f"<b><u>{title.replace('-', ' ')}</u></b>" \
                     f"\n\n<b>{main_ingredients}</b>\n<i>{main_ings}</i>" \
                     f"\n<b>{secondary_ingredients}</b>\n<i>{secon_ings}</i>" \
                     f"\n\n"
        text = text_
        print("The user has not input output")
    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def about(update, context):
    query = update.callback_query
    query.answer()

    text, keyboard = render_about(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


'''
def handle_ver_codigo(update, context):
    print("Dentro de handle_ver_codigo")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    if user_language == 'es':
        response = (f"Hola {user_first_name}! Puedes ver el codigo en GitHub usando el botón de abajo!"
                    f"<i>De paso seguime ;)</i>")
        button = f"Ver el codigo en GitHub"
    else:
        response = (f"Hi {user_first_name}! You can see the code on GitHub using the button below!"
                    f"\n<i>By the way, follow me! ;)</i>")
        button = f"See the code on GitHub"

    update.message.reply_text(
        text=response,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=button, url='https://github.com/lucaslucasprogram/plant_base_food_bot')],
        ])
    )
'''
