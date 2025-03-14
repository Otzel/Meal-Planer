import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data/meal_planner.db")

### 🔍 ADDING DATA ###
def add_recipe(name, portion_size, ingredients, tags=None):
    """
    Adds a recipe to the database along with its ingredients and optional tags.

    Parameters:
    - name (str): The name of the recipe
    - portion_size (int): Number of portions
    - ingredients (list of tuples): A list containing (ingredient_name, amount)
    - tags (list of str): A list of tags associated with the recipe (default: None)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Insert recipe into recipes table
        cursor.execute("""
            INSERT INTO recipes (name, portion_size)
            VALUES (?, ?)
        """, (name, portion_size))

        # Get the recipe ID
        recipe_id = cursor.lastrowid

        # Process ingredients
        for ingredient_name, amount in ingredients:
            # Get the ingredient ID
            cursor.execute("""
                SELECT id FROM ingredients WHERE name = ?
            """, (ingredient_name,))
            result = cursor.fetchone()

            if not result:
                print(f"⚠️ Warning: Ingredient '{ingredient_name}' not found. Skipping.")
                continue

            ingredient_id = result[0]

            # Insert into recipe_ingredients
            cursor.execute("""
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount)
                VALUES (?, ?, ?)
            """, (recipe_id, ingredient_id, amount))

        # Process tags (if provided)
        if tags:
            for tag in tags:
                cursor.execute("""
                    INSERT OR IGNORE INTO tags (name) VALUES (?)
                """, (tag,))

                cursor.execute("""
                    SELECT id FROM tags WHERE name = ?
                """, (tag,))
                tag_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO recipe_tags (recipe_id, tag_id)
                    VALUES (?, ?)
                """, (recipe_id, tag_id))

        # Commit changes
        conn.commit()
        print(f"✅ Recipe '{name}' added successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()

    finally:
        conn.close()


def add_ingredient(name, category_name):
    """
    Adds an ingredient to the database if it does not already exist.
    Ensures the category exists in the ingredient_categories table.

    Parameters:
    - name (str): The name of the ingredient.
    - category_name (str): The category of the ingredient.

    Returns:
    - ingredient_id (int): The ID of the ingredient in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Ensure the category exists
        cursor.execute("""
            INSERT OR IGNORE INTO ingredient_categories (name)
            VALUES (?)
        """, (category_name,))

        # Get the category ID
        cursor.execute("""
            SELECT id FROM ingredient_categories WHERE name = ?
        """, (category_name,))
        category_id = cursor.fetchone()[0]

        # Insert the ingredient
        cursor.execute("""
            INSERT OR IGNORE INTO ingredients (name, category_id)
            VALUES (?, ?)
        """, (name, category_id))

        # Retrieve the ingredient ID
        cursor.execute("""
            SELECT id FROM ingredients WHERE name = ?
        """, (name,))
        ingredient_id = cursor.fetchone()[0]

        conn.commit()
        print(f"✅ Ingredient '{name}' added successfully!")
        return ingredient_id

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return None

    finally:
        conn.close()


def add_tag(tag_name):
    """
    Adds a tag to the database if it does not already exist.

    Parameters:
    - tag_name (str): The tag to add.

    Returns:
    - tag_id (int): The ID of the tag in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Insert tag
        cursor.execute("""
            INSERT OR IGNORE INTO tags (name)
            VALUES (?)
        """, (tag_name,))

        # Retrieve tag ID
        cursor.execute("""
            SELECT id FROM tags WHERE name = ?
        """, (tag_name,))
        tag_id = cursor.fetchone()[0]

        conn.commit()
        print(f"✅ Tag '{tag_name}' added successfully!")
        return tag_id

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return None

    finally:
        conn.close()

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
