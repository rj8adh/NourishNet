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


# Get all recipes with the given ingredients
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


# Get the details such as instructions for each recipe
def get_recipe_details(recipe: dict):
    try:
        url = f"https://api.spoonacular.com/recipes/{recipe['id']}/analyzedInstructions?apiKey={API_KEY}"
        print(url)
    except:
        return "INVALID RECIPE DATA"
    
    # Making sure recipeDetails exists and isn't empty
    if not os.path.exists("recipeDetails.json") or os.stat("recipeDetails.json").st_size == 0:
        recipeInfo = []

    # Load recipeDetails if it contains stuff
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


def get_equip_for_recip(recipe: list):
    
    # Used a set so I don't get duplicates
    neededEquipment = set()

    # Looping through each step and getting needed equipment
    for info in recipe:
        steps = info['steps']
        for step in steps:
            for equipment in step['equipment']:
                # Adding items to set
                neededEquipment.add(equipment['name'])

    # Converting a set to a list seperated by commas (you could just use the list() function but I wanted to flex my list comprehensions)
    return ", ".join([equipment for equipment in neededEquipment]).strip(", ")


def get_steps(recipe: list):

    stepsString = ""

    # Looping and adding all Steps to final output
    for detail in recipe:
        stepsData = detail['steps']
        for step_num, step in enumerate(stepsData, 1):
            stepsString += f"Step {step_num}: {step['step']}\n"

    # Removing last whitespace
    stepsString = stepsString.strip()

    return stepsString
    

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

for recipeIndex, recipe in enumerate(recipeDetails):
    print(f"\n\n{recipes[recipeIndex]['title']} Instructions:\n\n")
    
    print(get_steps(recipe))

    neededEquipment = get_equip_for_recip(recipe)

    print(f"\n\nNEEDED EQUIPMENT FOR RECIPE:\n\n")
    print(neededEquipment)