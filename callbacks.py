# Importamos las librerias de PTB
# -
# We import PTB libraries
import query as query
from telegram import InlineKeyboardMarkup, ParseMode, InlineKeyboardButton, ReplyKeyboardRemove

# Importamos los archivos de constantes y renders para poder usarlos
# -
# We import the constants and renders files to be able to use them.
from telegram.ext import ConversationHandler

from renders import render_main, render_recipes, render_recipe, render_ingredients, render_to_cook, render_lets_cook, \
    render_about, render_step_by_step


# Generamos la función main que captura el query, para luego poder editar el mensaje y llamamos con un render
# al main
# -
# We generate the main function that captures the query, so we can then edit the message and call with a render
# to the main


def main(update, context):
    print("func -> main")
    query = update.callback_query
    query.answer()

    text, keyboard = render_main(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Y se repite lo mismo para los distintos menus, se captura el query, se llama a la función de los renders y se
# manda el mensaje al usuario


def main_recipes(update, context):
    print("func -> main_recipes")
    query = update.callback_query
    query.answer()

    text, keyboard = render_recipes(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def see_recipe(update, context):
    print("func -> see_recipe")
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
    print("func -> ingredients")
    query = update.callback_query
    query.answer()

    text, keyboard = render_ingredients(update, context)
    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def what_cook(update, context):
    print("func -> what_cook")
    query = update.callback_query
    query.answer()

    text, keyboard = render_to_cook(update, context)
    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def lets_cook(update, context):
    print("func -> lets_cook")
    user_language = update.effective_user['language_code']

    query = update.callback_query
    query.answer()

    foods, keyboard = render_lets_cook(update, context)

    if user_language == 'en':
        prev_main_ingredients = "Main ingredients: "
        prev_secondary_ingredients = "Secondary ingredients: "
        can_cook = "What can you cook with what you have?"
    else:
        prev_main_ingredients = "Ingredientes principales: "
        prev_secondary_ingredients = "Ingredientes secundarios: "
        can_cook = "¿Que puedes cocinar con lo que tienes?"

    if isinstance(foods, list):
        update.effective_message.reply_text(
            text=can_cook,
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
        for food in foods:
            str_main_ingredients = ''
            str_secondary_ingredients = ''
            food_name = food["name"]
            main_ingredients = food["main_ingredients"]
            secondary_ingredients = food["secondary_ingredients"]

            for ingredient in main_ingredients:
                str_main_ingredients += f'· {ingredient}\n'

            for ingredient in secondary_ingredients:
                str_secondary_ingredients += f'· {ingredient}\n'

            response = f'<b><u>{food_name}</u></b>' \
                       f'\n\n<b>{prev_main_ingredients}</b>\n<i>{str_main_ingredients}</i>' \
                       f'\n<b>{prev_secondary_ingredients}</b>\n<i>{str_secondary_ingredients}</i>'

            update.effective_message.reply_text(
                text=response,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="Ver paso a paso 🦶", callback_data=f'{food_name}')]
                ])
            )
    else:
        query.edit_message_text(
            text=foods,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    return ConversationHandler.END


def about(update, context):
    print("func -> about")
    query = update.callback_query
    query.answer()

    text, keyboard = render_about(update, context)

    query.edit_message_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def see_step_by_step(update, context):
    print("func -> see_step_by_step")

    query = update.callback_query
    query.answer()

    text, keyboard = render_step_by_step(update, context)

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
