#TODO Format All Print Statements Into Outputs/Return Statements

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("FOOD_API")

def api_request(url: str):
    # API Request
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching recipes:", response.json())
        raise requests.exceptions.HTTPError(f"API request failed to {url}, the website may currently be down or the URL may be invalid")
    
    print("\nRESPONSE TYPE:", type(response), "\n\n")

    return [response][0]

def get_recipes(ingredients: list = [], loadIngredients: bool = False):
    # Convert list to comma-separated string
    if not loadIngredients:

        # Wiping past recipe details
        with open("recipeDetails.json", "w") as f:
            f.write("")
        f.close()
        
        if not ingredients:
            return "NO INGREDIENTS GIVEN"

        ingredients_str = ",+".join(ingredients)

        print(ingredients_str)

        # Spoonacular API URL
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=2&apiKey={API_KEY}"
        
        # API Request
        response = api_request(url)
        
        # Saving data to file so it's easier to use with frontend
        recipes = response.json()
        
        # print(recipes)
        with open("recipes.json", "w") as f:
            json.dump(recipes, f, indent=4)
        f.close()

    # Loading recipes data from file to save api usage
    else:
        with open("recipes.json") as f:
            recipes = json.load(f)
        f.close()

    # print(recipes)

    for recipe in recipes:
        print(f"\nMISSING INGREDIENTS FOR {recipe['title']}:\n")

        for ingredient in recipe['missedIngredients']:
            print(ingredient['original'])
    
    return recipes


def get_recipe_details(recipe: dict):
    try:
        url = f"https://api.spoonacular.com/recipes/{recipe['id']}/analyzedInstructions?apiKey={API_KEY}"
        print(url)
    except:
        return "INVALID RECIPE DATA"
    
    # Making sure recipeDetails exists and isn't empty
    if not os.path.exists("recipeDetails.json") or os.stat("recipeDetails.json").st_size == 0:
        recipeInfo = []

    else:
        with open("recipeDetails.json", "r") as f:
            recipeInfo = json.load(f) 
            # Making sure recipeInfo is a list
            if not isinstance(recipeInfo, list):
                recipeInfo = []

    recipeInfo.append(api_request(url).json())

    # Save the updated list to the file
    with open("recipeDetails.json", "w") as f:
        json.dump(recipeInfo, f, indent=4)  # Pretty formatting
    f.close()

    return recipeInfo
    

# Get and format user input
# user_ingredients = input("Enter ingredients (comma-separated): ").lower().split(",")
# user_ingredients = [space.strip() for space in user_ingredients]

# Get recipes
# recipes = get_recipes(user_ingredients)
recipes = get_recipes(loadIngredients=True)

with open("recipeDetails.json") as f:
    recipeDetails = json.load(f)
f.close()

# recipeDetails = get_recipe_details(recipe) # Commented out so I don't waste api tokens

neededEquipment = {} # Did a dictionary so no repeats

for recipeIndex, recipe in enumerate(recipeDetails):
    print(f"\n\n{recipes[recipeIndex]['title']} Instructions:\n\n")
    for info in recipe:
        steps = info['steps']
        # print(steps, "\n\n\n")

        for step in steps:
            print(step['step'])
            for equipment in step['equipment']:
                neededEquipment[equipment['name']] = 0

    print(f"\n\nNEEDED EQUIPMENT FOR RECIPE:\n\n")
    for item in neededEquipment:
        print(item)
