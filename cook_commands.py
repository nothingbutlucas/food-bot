# Code in development

from telegram import ParseMode
from telegram.ext import ConversationHandler

from contexts import *


def create_new_recipe(update, context):
    print("func -> create_new_recipe")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']

    if user_language == "es":
        response = f"Hola {user_first_name}, creemos una nueva receta." \
                   f"\nTe voy a pedir ciertos datos, si no los tienes aún o no es necesario para esa receta " \
                   f"por favor envía /nop." \
                   f"\nAhora si, para comenzar necesito el <b>nombre de la receta</b>"
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_MAIN_INGREDIENTS


def create_new_recipe_main_ingredients(update, context):
    print("func -> create_new_recipe_main_ingredients")
    user_language = update.effective_user['language_code']
    recipe_name = update.message.text

    context.user_data['recipe_name'] = recipe_name

    if user_language == "es":
        response = f"Genial! Si te confundiste, no te hagas problema, al final lo podemos corregir" \
                   f'\nAhora decime los <b>ingredientes principales</b> separados por una ","' \
                   f'\nPor ejemplo: lechuga, tomate, cebolla'
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_SECONDARY_INGREDIENTS


def create_new_recipe_secondary_ingredients(update, context):
    print("func -> create_new_recipe_secondary_ingredients")
    user_language = update.effective_user['language_code']
    recipe_main_ingredients = update.message.text

    context.user_data['recipe_main_ingredients'] = recipe_main_ingredients

    if user_language == "es":
        response = f"Genial! Si te confundiste, no te hagas problema, al final lo podemos corregir" \
                   f'\nAhora decime los <b>ingredientes secundarios</b> separados por una ","' \
                   f'\nPor ejemplo: lechuga, tomate, cebolla'
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_STEP_BY_STEP


def create_new_recipe_step_by_step(update, context):
    print("func -> create_new_recipe_step_by_step")
    user_language = update.effective_user['language_code']
    recipe_secondary_ingredients = update.message.text

    context.user_data['recipe_secondary_ingredients'] = recipe_secondary_ingredients

    if user_language == "es":
        response = f'Genial! Si te confundiste, no te hagas problema, al final lo podemos corregir' \
                   f'\nAhora decime el <b>paso a paso</b> para hacer la receta. Tene en cuenta que ' \
                   f'los "." serán tomados cómo saltos de linea.' \
                   f'\nPor ejemplo si escribis:' \
                   f'\n<code>1 - Primero vamos a cortar la cebolla en cuadraditos</code>' \
                   f'<code>..2 - Ponemos la cebolla en un bowl</code>' \
                   f'\nLo veras así:' \
                   f'\n<code>1 - Primero vamos a cortar la cebolla en cuadraditos</code>' \
                   f'\n\n<code>2 - Ponemos la cebolla en un bowl</code>' \
                   f'\n<i>Detalle: Es importante que no dejes un espacio " " luego de escribir los "."</i>'
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_IMAGE


def create_new_recipe_image(update, context):
    print("func -> create_new_recipe_image")
    user_language = update.effective_user['language_code']
    recipe_step_by_step = update.message.text

    context.user_data['recipe_step_by_step'] = recipe_step_by_step

    if user_language == "es":
        response = f'Bravo! Ahora mandame la foto de la receta'
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_LINK


def create_new_recipe_link(update, context):
    print("func -> create_new_recipe_link")
    user_language = update.effective_user['language_code']
    recipe_new_recipe_image = update.message.photo[0].file_id

    context.user_data['recipe_new_recipe_image'] = recipe_new_recipe_image

    if user_language == "es":
        response = f'Perfecto! Ahora mandame el link del video'
    else:
        response = f"pass"
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

    return CREATE_RECIPE_CHECK


def create_new_recipe_check(update, context):
    print("func -> create_new_recipe_check")
    user_language = update.effective_user['language_code']
    recipe_link = update.message.text

    context.user_data['recipe_link'] = recipe_link

    recipe_name = context.user_data.get('recipe_name')
    recipe_main_ingredients = context.user_data.get('recipe_main_ingredients')
    recipe_secondary_ingredients = context.user_data.get('recipe_secondary_ingredients')
    recipe_step_by_step = context.user_data.get('recipe_step_by_step')
    recipe_step_by_step = recipe_step_by_step.replace(".", "\n")
    recipe_new_recipe_image = context.user_data.get('recipe_new_recipe_image')

    if user_language == "es":
        response = f'Ey! Fantastico, mira cómo quedo:' \
                   f'\n<b>1</b> - <u>Nombre de la receta:</u>' \
                   f'\n<b>{recipe_name}</b>' \
                   f'\n<b>2</b> - <u>Ingredientes principales:</u>' \
                   f'\n<i>{recipe_main_ingredients}</i>' \
                   f'\n<b>3</b> - <u>Ingredientes secundarios:</u>' \
                   f'\n<i>{recipe_secondary_ingredients}</i>' \
                   f'\n<b>4</b> - <u>Paso a paso:</u>' \
                   f'\n{recipe_step_by_step}' \
                   f'\n<b>5</b> - <u>Link:</u>' \
                   f'\n{recipe_link}' \
                   f'\n<b>6</b> - <u>Imagen</u>'
        other_response = f'Enviame el número de la opción que deseas cambiar.' \
                         f'\nSi esta todo bien, mandame /ok'
    else:
        response = f"pass"
        other_response = f'pass'
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML,
        photo=recipe_new_recipe_image
    )
    update.message.reply_text(
        text=other_response,
        parse_mode=ParseMode.HTML,
    )

    return CREATE_RECIPE_CONFIRMATION


def create_new_recipe_confirmation(update, context):

    return ConversationHandler.END

# Code in development

