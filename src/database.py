import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data/meal_planner.db")


### 🔍 FETCHING DATA ###

def fetch_all_recipes():
    """Fetch all recipes with their ingredients and tags."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT r.id, r.name, r.portion_size, GROUP_CONCAT(t.name, ', ') AS tags
            FROM recipes r
            LEFT JOIN recipe_tags rt ON r.id = rt.recipe_id
            LEFT JOIN tags t ON rt.tag_id = t.id
            GROUP BY r.id
        """)
        recipes = cursor.fetchall()
        return recipes

    finally:
        conn.close()


def fetch_all_ingredients():
    """Fetch all ingredients with their categories."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT i.id, i.name, c.name AS category
            FROM ingredients i
            JOIN ingredient_categories c ON i.category_id = c.id
        """)
        ingredients = cursor.fetchall()
        return ingredients

    finally:
        conn.close()


def fetch_all_tags():
    """Fetch all tags."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tags")
        tags = cursor.fetchall()
        return tags

    finally:
        conn.close()


def fetch_ingredients_by_recipe(recipe_id):
    """
    Fetches all ingredients for a given recipe ID.

    Parameters:
    - recipe_id (int): The ID of the recipe.

    Returns:
    - List of tuples (ingredient_id, ingredient_name, amount, category_name)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT i.id, i.name, ri.amount, c.name AS category
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            JOIN ingredient_categories c ON i.category_id = c.id
            WHERE ri.recipe_id = ?
        """, (recipe_id,))

        ingredients = cursor.fetchall()
        return ingredients

    finally:
        conn.close()


### ❌ DELETING DATA ###

def delete_recipe(recipe_id):
    """Delete a recipe and its related entries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
        cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        print(f"✅ Recipe with ID {recipe_id} deleted successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


def delete_ingredient(ingredient_id):
    """Delete an ingredient and remove it from recipes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM recipe_ingredients WHERE ingredient_id = ?", (ingredient_id,))
        cursor.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
        conn.commit()
        print(f"✅ Ingredient with ID {ingredient_id} deleted successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


def delete_tag(tag_id):
    """Delete a tag and remove it from recipes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM recipe_tags WHERE tag_id = ?", (tag_id,))
        cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        conn.commit()
        print(f"✅ Tag with ID {tag_id} deleted successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


### ✏️ UPDATING DATA ###

def update_recipe(recipe_id, **kwargs):
    """
    Updates a recipe dynamically.

    Parameters:
    - recipe_id (int): The ID of the recipe to update.
    - kwargs: Column-value pairs to update.

    Example:
        update_recipe(1, name="New Name", portion_size=6)
    """
    if not kwargs:
        print("⚠️ No updates provided.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [recipe_id]
        query = f"UPDATE recipes SET {columns} WHERE id = ?"

        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Recipe ID {recipe_id} updated successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


def update_ingredient(ingredient_id, **kwargs):
    """
    Updates an ingredient dynamically.

    Parameters:
    - ingredient_id (int): The ID of the ingredient to update.
    - kwargs: Column-value pairs to update.

    Example:
        update_ingredient(1, name="New Ingredient", category_id=2)
    """
    if not kwargs:
        print("⚠️ No updates provided.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [ingredient_id]
        query = f"UPDATE ingredients SET {columns} WHERE id = ?"

        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Ingredient ID {ingredient_id} updated successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


def update_tag(tag_id, **kwargs):
    """
    Updates a tag dynamically.

    Parameters:
    - tag_id (int): The ID of the tag to update.
    - kwargs: Column-value pairs to update.

    Example:
        update_tag(1, name="New Tag Name")
    """
    if not kwargs:
        print("⚠️ No updates provided.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [tag_id]
        query = f"UPDATE tags SET {columns} WHERE id = ?"

        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Tag ID {tag_id} updated successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()
