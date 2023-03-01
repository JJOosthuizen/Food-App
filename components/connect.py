import requests
import json
import configparser
import os

config = configparser.ConfigParser()
config.read("components/config.ini")

api_key = config["spoonacular"]["api_key"]


def fetch_data(recipe_name):
    """Function that connect to the spoonacular API and store the data in a json file"""

    # API endpoint and parameters
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"query": recipe_name, "number": 6, "apiKey": api_key}

    file_path = "recipes.json"

    if os.path.exists(file_path):
        print("The JSON file exists")
    else:
        response = requests.get(url, params=params)
        save_to_file(response)
        print("made file")


def save_to_file(response):
    """Function that writes API data to json file"""
    if response.status_code == 200:
        # Parse the response content as JSON
        data = response.json()["results"]
        # Write the JSON data to a file
        with open("recipes.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        print("Failed to fetch data from Spoonacular API")


def view_requested_recipe(button_id):
    """Function that gets recipe id and looksup the instructions and ingredients of the recipe
    *   :button_id (__int__): id of determine which button was pressed
    *   :returns title (__str__), instructions (__str__), ingredients (__dict__):"""
    # try read from file and get the recipe id
    try:
        with open("recipes.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return

    recipe_id = data[button_id]["id"]
    # Send GET request to Spoonacular API
    url = (
        f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
    )
    response = requests.get(url)

    # Parse response JSON data
    recipe_data = json.loads(response.text)

    title = recipe_data["title"]
    instructions = recipe_data["instructions"]
    ingredients = recipe_data["extendedIngredients"]

    return title, instructions, ingredients
