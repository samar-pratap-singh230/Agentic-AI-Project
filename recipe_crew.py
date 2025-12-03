import json
from crewai import Agent 
from tools.generator import RecipeGeneratorTool
from tools.mailer import MailerTool

class RecipeCrew:
    def __init__(self):
        self.generator = RecipeGeneratorTool()
        self.mailer = MailerTool()
        
        # --- Agents (Defined for startup check only) ---
        # llm=False fixes the environment crash.
        self.generator_agent = Agent(
            role="AI Sous Chef and Recipe Generator",
            goal="Generate a unique, high-quality, fully structured JSON recipe.",
            backstory="Specialist in generating complex, structured recipe data for digital assistants.",
            llm=False
        )

        self.notification_agent = Agent(
            role="Recipe Notification Specialist",
            goal="Review the generated recipe and ensure the email notification is sent.",
            backstory="Manages the final communication channel with the end-user.",
            llm=False
        )

    def run(self, ingredients: str, dietary_needs: str, meal_type: str, user_email: str):
        
        # === Task 1: Generate Recipe (Procedural step) ===
        print("\n=== Task 1: Generating Structured Recipe... ===")
        
        recipe_json_str = self.generator.generate_recipe(ingredients, dietary_needs, meal_type)
        
        try:
            recipe_data = json.loads(recipe_json_str)
            if "error" in recipe_data:
                return f"Recipe Generation Failed: {recipe_data['reason']}", recipe_data
        except json.JSONDecodeError:
            return "Recipe Generation Failed: Invalid JSON output from generator.", {"raw_output": recipe_json_str}

        # === Task 2: Email Notification (Procedural Action) ===
        # CRITICAL: The entire Crew/Task instantiation block is REMOVED from here.
        print("\n=== Task 2: Sending Notification... ===")

        # Create a clean, human-readable summary for the email body
        email_summary = f"""
        Your personalized recipe, "{recipe_data.get('title', 'Untitled Recipe')}", is ready!

        **Prep Time:** {recipe_data.get('prep_time_minutes', '?')} minutes
        **Cook Time:** {recipe_data.get('cook_time_minutes', '?')} minutes
        **Servings:** {recipe_data.get('servings', '?')}

        Full recipe details are included below.
        """
        
        # Format the full JSON for the email
        full_recipe_body = f"""
        {email_summary.strip()}

        ----------------------------------------------------
        FULL RECIPE DETAILS (JSON Format):

        {recipe_json_str}
        """

        subject = f"Your Personalized Recipe: {recipe_data.get('title', 'Recipe Ready')}"
        
        # This is the single, direct call to the mailer tool that we want.
        mail_status = self.mailer.send_mail(subject, full_recipe_body, user_email)

        return mail_status, recipe_data