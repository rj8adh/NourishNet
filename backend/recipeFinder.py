import requests
from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.responses import JSONResponse

app = FastAPI()

load_dotenv()

API_KEY = os.getenv("FOOD_API")

def api_request(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"API request failed: {response.text}")
    return response.json()

def get_recipes(ingredients: List[str] = [], loadIngredients: bool = False):
    if not loadIngredients:
        if not ingredients:
            raise HTTPException(status_code=400, detail="No ingredients provided.")

        ingredients_str = ",+".join(ingredients)
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=2&apiKey={API_KEY}"
        recipes = api_request(url)

        with open("recipes.json", "w") as f:
            json.dump(recipes, f, indent=4)
        return recipes

    else:
        try:
            with open("recipes.json") as f:
                recipes = json.load(f)
            return recipes
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="recipes.json not found.")

def get_recipe_details(recipe_id: int):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}"
    try:
        details = api_request(url)
        return details
    except HTTPException as e:
        raise e

def get_equip_for_recip(recipe: List[Dict[str, Any]]):
    neededEquipment = set()
    for info in recipe:
        if 'steps' in info and isinstance(info['steps'], list):
            for step in info['steps']:
                if 'equipment' in step and isinstance(step['equipment'], list):
                    for equipment in step['equipment']:
                        if 'name' in equipment:
                            neededEquipment.add(equipment['name'])
    return list(neededEquipment)

def get_steps(recipe: List[Dict[str, Any]]):
    stepsString = ""
    for detail in recipe:
        if 'steps' in detail and isinstance(detail['steps'], list):
            stepsData = detail['steps']
            for step_num, step in enumerate(stepsData, 1):
                if 'step' in step:
                    stepsString += f"Step {step_num}: {step['step']}\n"
    return stepsString.strip()

class Ingredients(BaseModel):
    ingredients: str

@app.post("/giveIngredients")
def giveIngredients(ingredients_data: Ingredients):
    foodItems = ingredients_data.ingredients.split("&")
    recipeData = get_recipes(foodItems)

    # Fetch and store recipe details
    all_details = []
    for recipe in recipeData:
        details = get_recipe_details(recipe['id'])
        all_details.append(details)

    with open("recipeDetails.json", "w") as f:
        json.dump(all_details, f, indent=4)

    return recipeData

@app.get("/getNecessaryEquipment")
def get_necessary_equipment():
    try:
        with open("recipeDetails.json") as f:
            specificRecipes = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="recipeDetails.json not found.")

    finalOutput = []
    for recip in specificRecipes:
        finalOutput.append(get_equip_for_recip(recip))
    return finalOutput

@app.get("/getMissingIngredients")
def get_missing_ingredients():
    try:
        with open("recipes.json") as f:
            recipesInfo = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="recipes.json not found.")

    finalOutput = []
    for recipe in recipesInfo:
        neededIngredients = []
        if 'missedIngredients' in recipe and isinstance(recipe['missedIngredients'], list):
            for ingredient in recipe['missedIngredients']:
                if 'original' in ingredient:
                    neededIngredients.append(ingredient['original'])
        finalOutput.append(neededIngredients)
    return finalOutput

@app.get("/getIngredientSteps")
def getIngredientSteps():
    try:
        with open("recipeDetails.json") as f:
            allRecipes = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="recipeDetails.json not found.")

    finalOutput = []
    for recip in allRecipes:
        finalOutput.append(get_steps(recip))
    return finalOutput

@app.get("/getRecipeDetails/{recipe_id}")
def get_recipe_detail_route(recipe_id: int):
    try:
        with open("recipeDetails.json") as f:
            all_details = json.load(f)
        with open("recipes.json") as f2:
            all_recipes = json.load(f2)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="recipeDetails.json or recipes.json not found.")

    for recipe in all_recipes:
        print(recipe["id"])
        print(recipe_id)
        if int(recipe["id"]) == int(recipe_id):
            print("WENT THROUGH")
            index = all_recipes.index(recipe)
            return all_details[index]

    raise HTTPException(status_code=404, detail="recipe id not found.")