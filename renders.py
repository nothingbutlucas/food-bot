from telegram import InlineKeyboardButton

from API_talk import request_recipe, request_recipes, request_foods


def render_back_menu():
    keyboard = [[InlineKeyboardButton(text="🔙 Main", callback_data='main')]]
    return keyboard


def render_main(update, context):
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']

    if user_language == 'es':
        text = f'Hola, {user_first_name}!'

        keyboard = [
            [
                InlineKeyboardButton(text='📜 Ver recetas', callback_data='recipes')
            ],
            [
                InlineKeyboardButton(text='🧪 Ver Ingredientes', callback_data='ingredients')
            ],
            [
                InlineKeyboardButton(text='🥗 Ver que podes cocinar', callback_data='what_u_can_cook')
            ],
            [
                InlineKeyboardButton(text='📱 Acerca de', callback_data='about')
            ],
        ]

    else:
        text = f'Hi, {user_first_name}!'

        keyboard = [
            [
                InlineKeyboardButton(text='📜 See recipes', callback_data='recipes')
            ],
            [
                InlineKeyboardButton(text='🧪 See Ingredients', callback_data='ingredients')
            ],
            [
                InlineKeyboardButton(text='🥗 See what u can cook', callback_data='what_u_can_cook')
            ],
            [
                InlineKeyboardButton(text='📱 About', callback_data='about')
            ],
        ]

    return text, keyboard


def render_recipes(update, context):
    recipes = request_recipes()

    user_language = update.effective_user['language_code']

    keyboard = list()
    keyboard_00 = list()

    if user_language == 'en':
        text = f'Here are the recipes, touch them to see the ingredients'

        for x, recipe in enumerate(recipes):
            recipe = recipe.replace("-", " ")
            keyboard_00.append(InlineKeyboardButton(text=recipe, callback_data=f'{x}'))
            if len(keyboard_00) < 2:
                pass
            else:
                keyboard.append(keyboard_00)
                keyboard_00 = list()
        keyboard.append([InlineKeyboardButton(text="🔙 Main", callback_data=f'main')])
    else:

        text = f'Acá estan las recetas, toca una para ver los ingredientes'

        for x, recipe in enumerate(recipes):
            recipe = recipe.replace("-", " ")
            keyboard_00.append(InlineKeyboardButton(text=recipe, callback_data=f'{x}'))
            if len(keyboard_00) < 2:
                pass
            else:
                keyboard.append(keyboard_00)
                keyboard_00 = list()
        keyboard.append([InlineKeyboardButton(text="🔙 Main", callback_data=f'main')])
    return text, keyboard


def render_recipe(update, context):
    user_language = update.effective_user['language_code']

    query = update.callback_query

    query.answer()

    recipe = request_recipe(query)

    recipe_name = ''
    main_ingredients = ''
    secondary_ingredients = ''
    m_ingredients = ''
    s_ingredients = ''
    text = ''

    try:
        name = (recipe["name"]).replace("-", " ")
        recipe_name = name
        main_ingredients = recipe["main-ingredients"]
        secondary_ingredients = recipe["secondary-ingredients"]
    except KeyError:
        error = recipe["detail"][0]["msg"]
        text = ("Error: " + error)
    except Exception:
        if user_language == 'es':
            text = "Ups, no se que, pero algo salío mal :("
        else:
            text = "Ups, i don't know what, but something when wrong :("

    if recipe_name and main_ingredients:
        for ingredient in main_ingredients:
            m_ingredients += f"· {ingredient}\n"
        for ingredient in secondary_ingredients:
            s_ingredients += f"· {ingredient}\n"
        if len(s_ingredients) < 1:
            s_ingredients = "-"
        if user_language == 'es':
            text = f"<b><u>{recipe_name}</u></b>" \
                   f"\n\n<i>Ingredientes principales:</i>" \
                   f"\n {m_ingredients}" \
                   f"\n<i>Ingredientes secundarios:</i>" \
                   f"\n {s_ingredients}"
        else:
            text = f"<b><u>{recipe_name}</u></b>" \
                   f"\n\n<i>Main ingredients:</i>" \
                   f"\n {m_ingredients}" \
                   f"\n<i>Secondary ingredients:</i>" \
                   f"\n {s_ingredients}"
    keyboard = render_back_menu()
    return text, keyboard


def render_ingredients(update, context):
    ingredientes_menu = []
    foods = request_foods()
    text = ''
    for x, food in enumerate(foods):
        ingredients = foods[str(x)]["main-ingredients"] + foods[str(x)]["secondary-ingredients"]
        for ingredient in ingredients:
            if ingredient not in ingredientes_menu:
                ingredientes_menu.append(ingredient)

    for ingredient in ingredientes_menu:
        text += f"· {ingredient}\n"

    keyboard = render_back_menu()
    return text, keyboard


def render_to_cook(update, context):
    if context.user_data.get('ingredients') is not None:
        print("Nos vamos al update del render to cook")
        return update_render_to_cook(update, context)
    else:
        user_language = update.effective_user['language_code']

        query = update.callback_query
        query.answer()

        ingredientes_menu = []
        foods = request_foods()
        keyboard = list()
        keyboard_00 = list()

        for x, food in enumerate(foods):
            ingredients = foods[str(x)]["main-ingredients"] + foods[str(x)]["secondary-ingredients"]
            for ingredient in ingredients:
                if ingredient not in ingredientes_menu:
                    ingredientes_menu.append(ingredient)

        for x, ingredient in enumerate(ingredientes_menu):
            ingredient = f"{ingredient}"
            if len(keyboard_00) < 2:
                keyboard_00.append(InlineKeyboardButton(text=ingredient, callback_data=f"{ingredient}"))
            else:
                keyboard_00.append(InlineKeyboardButton(text=ingredient, callback_data=f"{ingredient}"))
                keyboard.append(keyboard_00)
                keyboard_00 = list()

        context.user_data['ingredients'] = ingredientes_menu
        if user_language == 'en':

            text = "<b>Choose the ingredients and I'll see what you can Let's cook!</b>"

            keyboard.append([InlineKeyboardButton(text="👨‍🍳 Let's cook! 👩‍🍳", callback_data=f'lets_cook')])
            keyboard.append([InlineKeyboardButton(text="🔙 Main 🔙", callback_data=f'main')])
        else:

            text = "<b>Elegí los ingredientes y yo veo que podes A cocinar!</b>"

            keyboard.append([InlineKeyboardButton(text="👨‍🍳 A cocinar! 👩‍🍳", callback_data=f'lets_cook')])
            keyboard.append([InlineKeyboardButton(text="🔙 Menu 🔙", callback_data=f'main')])

        context.user_data['keyboard'] = keyboard

        return text, keyboard


def update_render_to_cook(update, context):
    user_language = update.effective_user['language_code']

    ingredients = context.user_data.get('ingredients')
    query = update.callback_query
    query.answer()

    keyboard = list()
    keyboard_00 = list()
    new_ingredients = list()
    for x, ingredient in enumerate(ingredients):
        ingredient = ingredient
        if query.data == ingredient:
            ingredient = ingredient
            if ingredient != f"✅ {ingredient[2:]}":
                ingredient = f"✅ {ingredient}"
            else:
                ingredient = f"{ingredient[2:]}"
        new_ingredients.append(ingredient)
        if len(keyboard_00) < 2:
            keyboard_00.append(InlineKeyboardButton(text=ingredient, callback_data=f"{ingredient}"))
        else:
            keyboard_00.append(InlineKeyboardButton(text=ingredient, callback_data=f"{ingredient}"))
            keyboard.append(keyboard_00)
            keyboard_00 = list()
    context.user_data['ingredients'] = new_ingredients
    if user_language == 'en':

        text = "<b>Keep choosing and when you are done, click on Let's cook!</b>"

        keyboard.append([InlineKeyboardButton(text="👨‍🍳 Let's cook! 👩‍🍳", callback_data=f'lets_cook')])
        keyboard.append([InlineKeyboardButton(text="🔙 Main 🔙", callback_data=f'main')])
    else:

        text = "<b>Seguí eligiendo y cuando ya estes, apreta A cocinar!</b>"

        keyboard.append([InlineKeyboardButton(text="👨‍🍳 A cocinar! 👩‍🍳", callback_data=f'lets_cook')])
        keyboard.append([InlineKeyboardButton(text="🔙 Menu 🔙", callback_data=f'main')])
    return text, keyboard


def render_lets_cook(update, context):
    user_language = update.effective_user['language_code']
    query = update.callback_query
    query.answer()
    new_ingredients = list()
    ingredients = context.user_data.get('ingredients')

    for x, ingredient in enumerate(ingredients):
        for letter in ingredient:
            if letter == "✅":
                new_ingredients.append(ingredient[2:].lower().strip())

    foods = request_foods()
    can_cook = list()
    for x, food in enumerate(foods):
        food = foods[str(x)]["name"] + " " + str(foods[str(x)]["main-ingredients"]) + " " + str(
            foods[str(x)]["secondary-ingredients"])
        main_ingredients = foods[str(x)]["main-ingredients"]
        have_ingredient = list()
        for ingredient in main_ingredients:
            if ingredient in new_ingredients:
                have_ingredient.append(ingredient)
            if len(have_ingredient) == len(main_ingredients):
                can_cook.append(food)

    if not can_cook and new_ingredients:
        new_ingredients = str(new_ingredients).replace('[', '')
        new_ingredients = str(new_ingredients).replace(']', '')
        new_ingredients = str(new_ingredients).replace("'", "")
        if user_language == 'es':
            can_cook = f'No puedes cocinar nada de lo que tengo disponible con <i>{new_ingredients}</i>'
        else:
            can_cook = f"You can't cook anything that I have available with <i>{new_ingredients}</i>"
    elif not new_ingredients:
        if user_language == 'es':
            can_cook = f'Tienes que seleccionar los ingredientes que tengas para que pueda decirte que ' \
                       f'podes A cocinar!'
        else:
            can_cook = f"You have to select the ingredients you have so that I can tell you what you can Let's cook!"
    print(can_cook)
    keyboard = render_back_menu()
    return can_cook, keyboard


def render_about(update, context):
    user_language = update.effective_user['language_code']
    query = update.callback_query
    query.answer()

    if user_language == 'es':
        text = "<b>Bot y API desarrollados por devycoso</b>" \
               "\nSomos 1 programador y 1 cocinera" \
               "\nSi este bot te fue de útilidad y te parece que esta bueno, apoyanos con un cafe ☕ (Links abajo)" \
               " o en su defecto, compartiendo el bot :)" \
               "\nTambién si tenes algún comentario o sugerencia, estaría genial que nos lo contaras a nuestro mail:" \
               "\ndevycoso@gmail.com"
        donate = "Apoyanos con un café! ☕"
        follow_us = "Mira lo que hacemos!"
        menu = "🔙 Menu"
    else:
        text = "<b>Bot and API developed by devycoso</b>" \
               "\nWe are a developer and a cook" \
               "\nIf you found this bot useful and you think it's good, buy us a coffee (Links below) " \
               "or otherwise, sharing the bot :)" \
               "\nAlso, if you have any comments or suggestions, it would be great if you could send them to our " \
               "e-mail:" \
               "\ndevycoso@gmail.com"
        donate = "Buy us a coffee!"
        follow_us = "Look what we do!"
        menu = "🔙 Main"
    keyboard = [
        [
            InlineKeyboardButton(text=f'{donate} ☕', url='https://ko-fi.com/devycoso')
        ],
        [
            InlineKeyboardButton(text=f'{follow_us} 👀', url='https://bio.link/devycoso')
        ],
        [
            InlineKeyboardButton(text=f"{menu}", callback_data=f'main')
        ]
    ]

    return text, keyboard
