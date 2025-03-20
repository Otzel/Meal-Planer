from database import fetch_ingredients_by_recipe

def create_shopping_list(meal_plan):
    meal_ids = [meal_plan[i][0] for i in range(len(meal_plan))]
    print(meal_ids)
    ingredients = []
    for meal_id in meal_ids:
        ingredients.extend(fetch_ingredients_by_recipe(meal_id))
    print(ingredients)