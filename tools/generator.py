import json
import logging
from typing import List, Optional

# Using Pydantic to define the strict JSON schema for the recipe
# This ensures Gemini always returns a perfectly structured output.
class Ingredient:
    """Schema for a single ingredient item."""
    name: str
    quantity: str # e.g., "2", "1/2 cup"
    unit: str    # e.g., "cups", "tsp", "g"

class Recipe:
    """The main schema for the generated recipe."""
    title: str
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]

# --- Mock Generative AI Setup ---
# In a real-world scenario, you would use:
# from google import genai
# from pydantic import BaseModel, Field
# from google.genai import types
# from google.genai.errors import APIError
#
# Replace this with a working client that can call the Gemini API
# For demonstration, we'll use a mocked function that returns a structure similar to the expected JSON.

log = logging.getLogger(__name__)

class RecipeGeneratorTool:
    def __init__(self):
        # In a real app, initialize the Gemini Client here.
        # self.client = genai.Client()
        pass

    def _call_gemini_recipe_generator(self, prompt: str) -> dict:
        """
        Mocks a call to the Gemini API with structured output configuration.
        In a real application, this function would use the 'response_json_schema'
        to enforce the Recipe schema defined above.
        """
        # We will hardcode a mock JSON output for now, but this is where the 
        # API call would return the parsed JSON.
        
        # NOTE: In the actual implementation, you would use the Gemini API
        # to enforce the JSON structure defined by the Recipe class.
        
        log.info(f"Simulating Gemini call with prompt: {prompt[:50]}...")
        
        # Simple rule to mock a different recipe based on ingredients for realism
        if "chicken" in prompt.lower():
            return {
                "title": "One-Pan Honey-Garlic Chicken & Veggies",
                "prep_time_minutes": 15,
                "cook_time_minutes": 35,
                "servings": 4,
                "ingredients": [
                    {"name": "Chicken Thighs", "quantity": "4", "unit": "pieces"},
                    {"name": "Honey", "quantity": "1/4", "unit": "cup"},
                    {"name": "Soy Sauce", "quantity": "2", "unit": "tbsp"},
                    {"name": "Minced Garlic", "quantity": "1", "unit": "tbsp"},
                    {"name": "Broccoli florets", "quantity": "3", "unit": "cups"}
                ],
                "instructions": [
                    "Preheat oven to 400°F (200°C).",
                    "Mix honey, soy sauce, and garlic in a small bowl.",
                    "Toss chicken and broccoli with half the sauce on a baking sheet.",
                    "Bake for 30 minutes, then brush with remaining sauce and bake for 5 more minutes until chicken is cooked through."
                ]
            }
        else:
            return {
                "title": "Simple Tomato and Basil Pasta",
                "prep_time_minutes": 10,
                "cook_time_minutes": 20,
                "servings": 2,
                "ingredients": [
                    {"name": "Pasta (Spaghetti or Linguine)", "quantity": "200", "unit": "g"},
                    {"name": "Canned Crushed Tomatoes", "quantity": "1", "unit": "can (400g)"},
                    {"name": "Fresh Basil", "quantity": "1/2", "unit": "cup"},
                    {"name": "Olive Oil", "quantity": "3", "unit": "tbsp"},
                    {"name": "Salt and Pepper", "quantity": "to taste", "unit": ""}
                ],
                "instructions": [
                    "Cook pasta according to package directions.",
                    "In a pan, heat olive oil and add crushed tomatoes. Simmer for 15 minutes.",
                    "Stir in fresh basil, salt, and pepper.",
                    "Drain pasta and toss with the sauce. Serve immediately."
                ]
            }

    def generate_recipe(self, ingredients: str, dietary_needs: str, meal_type: str) -> str:
        """
        Generates a recipe using the provided input and returns it as a JSON string.
        """
        
        # Build the prompt for Gemini
        prompt = f"""
        Generate a unique, personalized recipe based on the following constraints:
        - Main Ingredients: {ingredients}
        - Dietary/Style Preference: {dietary_needs}
        - Meal Type: {meal_type}
        
        The output MUST be a JSON object that strictly adheres to the Recipe schema.
        Ensure the cooking times are realistic.
        """
        
        try:
            # Call the mock function to get the structured dictionary
            recipe_dict = self._call_gemini_recipe_generator(prompt)
            return json.dumps(recipe_dict, indent=2)
        except Exception as e:
            log.error(f"Failed to generate recipe: {e}")
            # Fallback for critical errors (e.g., API key issue)
            return json.dumps({"error": "Failed to generate recipe using AI.", "reason": str(e)})
