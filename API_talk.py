import requests
from constants import LINK_API


def request_recipes():
    recipes = requests.get(f"{LINK_API}/foods/recipes")
    recipes = recipes.json()
    return recipes


def request_recipe(query):
    recipe = requests.get(f"{LINK_API}/foods/id/{query.data}")
    recipe = recipe.json()
    return recipe


def request_foods():
    foods = requests.get(f"{LINK_API}/foods")
    foods = foods.json()
    return foods
