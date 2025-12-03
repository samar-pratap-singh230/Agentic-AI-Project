import json
from recipe_crew import RecipeCrew

# --- Example Input Data ---
ingredients = "salmon, avocado, rice"
dietary_needs = "Gluten-Free, Quick Prep"
meal_type = "Lunch"
user_email = "test.user@example.com"

crew = RecipeCrew()

print(f"Starting Recipe Generation for: {ingredients} ({dietary_needs} {meal_type})...")

# The run function returns the mail status and the structured recipe data
mail_status, recipe_data = crew.run(ingredients, dietary_needs, meal_type, user_email)

print("\n--- FINAL OUTPUT ---")
print(f"Mail Status: {mail_status}")
print("Generated Recipe:")
print(json.dumps(recipe_data, indent=2))