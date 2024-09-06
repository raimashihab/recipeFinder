import tkinter as tk
from tkinter import scrolledtext
import requests

def search_recipes(ingredients, dietary_restrictions=None, max_cooking_time=None):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    api_key = "c6208a30599d4cafbe88753e18c34efb"

    params = {
        "apiKey": api_key,
        "includeIngredients": ','.join(ingredients),
        "number": 2,  # Number of recipes to fetch
        "addRecipeInformation": True,
        "instructionsRequired": True
    }

    if dietary_restrictions:
        params["diet"] = ','.join(dietary_restrictions)

    if max_cooking_time:
        params["maxReadyTime"] = max_cooking_time

    response = requests.get(url, params=params)
    data = response.json()

    return data["results"]

def display_recipe(recipe):
    # Construct the recipe information string with emojis
    recipe_info = f"🍽 {recipe['title']}\n\n"
    recipe_info += f"🕒 Cooking time: {recipe['readyInMinutes']} minutes\n"
    recipe_info += f"🥘 Servings: {recipe['servings']}\n"

    if 'spoonacularScore' in recipe:
        recipe_info += f"⭐ Rating: {recipe['spoonacularScore']}\n"
    else:
        recipe_info += "⭐ Rating: N/A\n"

    recipe_info += f"👉 Instructions: {recipe['sourceUrl']}\n"
    recipe_info += "📝 Recipe:\n"

    instructions = recipe.get('analyzedInstructions', [])
    if instructions:
        for i, step in enumerate(instructions[0]['steps'], 1):
            recipe_info += f"Step {i}: {step['step']}\n"
    else:
        recipe_info += "No instructions available.\n"

    recipe_info += "🥦 Ingredients:\n"

    ingredients = recipe.get('extendedIngredients', recipe.get('ingredients', []))
    if ingredients:
        for ingredient in ingredients:
            recipe_info += f"- {ingredient}\n"
    else:
        recipe_info += "Open link to see in detail\n"

    return recipe_info

def main():
    def search_button_click():
        # Retrieve user inputs from the input fields
        ingredients = input_ingredients.get().split(",")
        dietary_restrictions = input_dietary_restrictions.get().split(",")
        max_cooking_time = input_max_cooking_time.get()

        try:
            max_cooking_time = int(max_cooking_time)
        except ValueError:
            max_cooking_time = None

        # Search for recipes based on user inputs
        recipes = search_recipes(ingredients, dietary_restrictions, max_cooking_time)
        if recipes:
            # Display recipe information in the output text area
            recipe_info = display_recipe(recipes[0])  # Only display the first recipe
            output_text.configure(state='normal')
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, recipe_info)
            output_text.configure(state='disabled')
        else:
            # Display a message if no recipes are found
            output_text.configure(state='normal')
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "No recipes found.")
            output_text.configure(state='disabled')

    # Create the main GUI window
    window = tk.Tk()
    window.title("Recipe Search")

    # Create input fields and labels
    tk.Label(window, text="Enter the ingredients you have (comma-separated):").pack()
    input_ingredients = tk.Entry(window)
    input_ingredients.pack()

    tk.Label(window, text="Enter any dietary restrictions (comma-separated, leave blank if none):").pack()
    input_dietary_restrictions = tk.Entry(window)
    input_dietary_restrictions.pack()

    tk.Label(window, text="Enter the maximum cooking time (in minutes, leave blank if none):").pack()
    input_max_cooking_time = tk.Entry(window)
    input_max_cooking_time.pack()

    # Create the search button
    search_button = tk.Button(window, text="Search", command=search_button_click)
    search_button.pack()

    # Create the output text area
    output_text = scrolledtext.ScrolledText(window, width=80, height=20, state='disabled')
    output_text.pack()

    # Start the main event loop for the GUI
    window.mainloop()

if __name__ == "__main__":
    main()