import requests
from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS

app = FastAPI()

# Configure CORS (if done improper, it's a pain in the butt so be careful)
origins = [
    "http://localhost:5173",  # Configuring to our current React origin
    # Add any other origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

API_KEY = os.getenv("FOOD_API")

# Standard api request
def api_request(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"API request failed: {response.text}")
    return response.json()

# Gets 2 possible recipes with given ingredients
def get_recipes(ingredients: List[str] = [], loadIngredients: bool = False):
    if not loadIngredients:
        if not ingredients:
            raise HTTPException(status_code=400, detail="No ingredients provided.")

        # Formatting and passing ingredients to the spoonacular api
        ingredients_str = ",+".join(ingredients)
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=2&apiKey={API_KEY}"
        recipes = api_request(url)

        # Saving our data to a json file so we can use it in later defs without spam calling the API
        with open("recipes.json", "w") as f:
            json.dump(recipes, f, indent=4)
        return recipes

    # For testing purposes, in case you don't want to waste API tokens
    else:
        try:
            with open("recipes.json") as f:
                recipes = json.load(f)
            return recipes
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="recipes.json not found.")

# Returning recipe details based on ID
def get_recipe_details(recipe_id: int):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}"
    try:
        details = api_request(url)
        return details
    except HTTPException as e:
        raise e


# Getting all equipment used for the recipe
def get_equip_for_recip(recipe: List[Dict[str, Any]]):
    # Used a set so there aren't duplicates
    neededEquipment = set()
    # Don't even ask, just had to handle some weird formatting errors
    for info in recipe:
        if 'steps' in info and isinstance(info['steps'], list):
            for step in info['steps']:
                if 'equipment' in step and isinstance(step['equipment'], list):
                    for equipment in step['equipment']:
                        if 'name' in equipment:
                            neededEquipment.add(equipment['name'])
    return list(neededEquipment)


# Makes a string talking about every step of the recipe (denoted by newlines)
def get_steps(recipe: List[Dict[str, Any]]):
    stepsString = ""
    # Again, some weird formatting errors
    for detail in recipe:
        if 'steps' in detail and isinstance(detail['steps'], list):
            stepsData = detail['steps']
            for step_num, step in enumerate(stepsData, 1):
                if 'step' in step:
                    stepsString += f"Step {step_num}: {step['step']}\n"
    return stepsString.strip()

class Ingredients(BaseModel):
    ingredients: str


# Post request basically means they're giving the program some data to do stuff with in our files
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


# Getting all required equipment for each recipe
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


# Getting missing ingredients for each recipe
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


# Getting steps for each recipe in a string format
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


# Getting recipe details based on ID
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


# Google Maps Stuff

GOOGLE_API_KEY = os.getenv("VITE_GOOGLE_API_KEY")

class GeocodeResponse(BaseModel):
    results: List[dict]
    status: str


class PlacesResponse(BaseModel):
    results: List[dict]
    status: str


class PlaceDetailsResponse(BaseModel):
    result: dict
    status: str


@app.get("/foodbanks/{zip_code}")
async def get_food_banks(zip_code: str):
    """
    Retrieves food banks near a given zip code.
    """ 
    try:
        # Getting coordinates of zip code
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={GOOGLE_API_KEY}"
        geo_response = requests.get(geocode_url)
        geo_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        geo_data = GeocodeResponse(**geo_response.json())

        print(geo_data)

        if geo_data.status != "OK" or not geo_data.results:
            raise HTTPException(status_code=400, detail="Invalid zip code or no results found.")


        # Setting variables to Lat and Long
        location = geo_data.results[0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        # Searching in 50000 meter radius for charities
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=50000&type=charity&key={GOOGLE_API_KEY}"
        places_response = requests.get(places_url)
        places_response.raise_for_status()
        places_data = PlacesResponse(**places_response.json())

        print("DATA", places_data)

        if places_data.status != "OK" or not places_data.results:
            raise HTTPException(status_code=404, detail="No food banks found in your area.")

        places = places_data.results[:5]
        # places = places_data.results


        print(places)

        # Getting details of each charity place nearby
        food_banks = []
        for place in places:
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place['place_id']}&fields=name,formatted_address,formatted_phone_number,website&key={GOOGLE_API_KEY}"
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details_data = PlaceDetailsResponse(**details_response.json())

            if details_data.status != "OK" or not details_data.result:
                continue # Skipping weird places without data
            food_banks.append(details_data.result)

        return food_banks

    # Raising errors
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    

# Getting position of zipcode
@app.get("/geocode/{zip_code}")
async def geocode(zip_code: str):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={GOOGLE_API_KEY}"
    geo_response = requests.get(geocode_url)
    geo_response.raise_for_status()
    return geo_response.json()