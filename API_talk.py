import requests
from constants import LINK_API


def request_recipes():
    print("func -> request_recipes")
    recipes = requests.get(f"{LINK_API}/foods/recipes")
    recipes = recipes.json()
    return recipes


def request_recipe(query):
    print("func -> request_recipe")
    recipe = requests.get(f"{LINK_API}/foods/id/{query.data}")
    code = recipe.status_code
    recipe = recipe.json()
    return recipe, code


def request_foods():
    print("func -> request_foods")
    foods = requests.get(f"{LINK_API}/foods")
    foods = foods.json()
    return foods


def request_step_by_step(recipe_name):
    print("func -> request_step_by_step")
    foods = requests.get(f"{LINK_API}/foods/step-by-step/{recipe_name}")
    code = foods.status_code
    foods = foods.json()
    return foods, code


