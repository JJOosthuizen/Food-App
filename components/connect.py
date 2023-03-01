import requests
import json
import configparser
import os
import pprint


def fetch_data(recipe_name):
    """Function that connect to the spoonacular API and store the data in a json file"""

    config = configparser.ConfigParser()
    config.read("components/config.ini")

    api_key = config["spoonacular"]["api_key"]

    # API endpoint and parameters
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"query": recipe_name, "number": 6, "apiKey": api_key}

    # Make request to the API

    # url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={recipe_name}&number=6"

    file_path = "recipes.json"

    if os.path.exists(file_path):
        print("The JSON file exists")
    else:
        response = requests.get(url, params=params)
        save_to_file(response, api_key)
        print("made file")


def save_to_file(response, api_key):
    """Function that writes API data to json file"""
    if response.status_code == 200:
        # Parse the response content as JSON
        data = response.json()["results"]
        recipes = []
        for result in data:
            recipe_dict = {}
            recipe_id = result["id"]
            # Make another request to get recipe details
            recipe_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
            recipe_params = {"apiKey": api_key}
            recipe_response = requests.get(recipe_url, params=recipe_params)

            recipe_instructions = recipe_response.json()["instructions"]
            recipe_ingredients = recipe_response.json()["extendedIngredients"]

            recipe_dict = {
                "id": recipe_id,
                "title": result["title"],
                "image": result["image"],
                "instructions": recipe_instructions,
                "ingredients": recipe_ingredients,
            }

            recipes.append(recipe_dict)

        # Write the JSON data to a file
        with open("recipes.json", "w") as f:
            json.dump(recipes, f, indent=4)
    else:
        print("Failed to fetch data from Spoonacular API")
