from flask import Flask, render_template, request, jsonify
import json
import os
from recipe_crew import RecipeCrew
from tools.generator import RecipeGeneratorTool # Import necessary classes/tools

# Configuration and Initialization
app = Flask(__name__)
# IMPORTANT: Replace this with a strong, random key in production
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-recipe-key") 

# Instantiate the Crew
recipe_crew = RecipeCrew()

# Default values for the web form
DEFAULTS = {
    "ingredients": "chicken, bell pepper, onion",
    "dietary_needs": "low-carb, high-protein",
    "meal_type": "dinner",
    "user_email": "test-user@example.com"
}

# --- Utility Functions ---

def _build_recipe_input(payload):
    """Extracts and formats input data from the request payload."""
    return {
        "ingredients": payload.get("ingredients") or "",
        "dietary_needs": payload.get("dietary_needs") or "Standard",
        "meal_type": payload.get("meal_type") or "Dinner",
        "user_email": payload.get("user_email") or DEFAULTS["user_email"]
    }

# --- Flask Routes ---

@app.route("/", methods=["GET"])
def index():
    """Renders the main form page."""
    # Pass defaults to the template for pre-filling the form
    return render_template("index.html", form=DEFAULTS.copy())

@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint to trigger the Recipe Crew and get the result."""
    payload = request.get_json() or {}
    
    # Extract user inputs
    inputs = _build_recipe_input(payload)
    
    try:
        # Run the Crew
        mail_status, recipe_data = recipe_crew.run(
            inputs["ingredients"],
            inputs["dietary_needs"],
            inputs["meal_type"],
            inputs["user_email"]
        )

        # Return the structured result and the status of the email
        return jsonify({
            "status": "success",
            "recipe_data": recipe_data,
            "mail_status": mail_status
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({
            "status": "error",
            "message": f"An internal error occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    # Use 127.0.0.1 and a specific port for local testing
    # Use 0.0.0.0 and port 8080/5000 for deployment platforms like Render
    app.run(host="127.0.0.1", port=5000, debug=True)