from database import fetch_all_recipes
import random


def random_meal_plan(number_meals, persons, plan=None):
    """
    Generates a random meal plan for a given number of meals and people.
    If an existing plan is provided, it adds recipes to it until the required portions are reached.

    Parameters:
    - number_meals (int): The number of meals to plan.
    - persons (int): The number of people each meal should serve.
    - plan (list, optional): A pre-existing list of selected recipes (default is an empty list).

    Returns:
    - list: The updated list of selected recipes.
    """
    if plan is None:
        plan = []

    portions_needed = number_meals * persons
    recipes = fetch_all_recipes()

    if not recipes:
        raise ValueError("No recipes available.")

    # Calculate already planned portions
    total_portions = sum(recipe[2] for recipe in plan)

    # Remove already selected recipes from the available pool
    selected_recipe_ids = {recipe[0] for recipe in plan}
    available_recipes = [r for r in recipes if r[0] not in selected_recipe_ids]

    # Fill the plan until the required portions are reached
    while total_portions < portions_needed and available_recipes:
        pick = random.choice(available_recipes)

        if total_portions + pick[2] <= portions_needed:
            plan.append(pick)
            total_portions += pick[2]
            available_recipes.remove(pick)  # Ensure no duplicate selections

    return plan
