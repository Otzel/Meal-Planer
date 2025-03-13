import sys
import os

# Add 'src/' to sys.path
CURR_DIR = os.path.dirname(os.path.abspath(__file__))  # Get scripts/ directory
SRC_DIR = os.path.join(CURR_DIR, "../src")  # Path to src/
sys.path.append(SRC_DIR)

from database import add_recipe, add_ingredient, add_tag

# Ingredient categories and ingredients
ingredients_data = [
    ("Paprika", "Gemüse & Obst"),
    ("Tomaten", "Gemüse & Obst"),
    ("Pilze", "Gemüse & Obst"),
    ("Lauch", "Gemüse & Obst"),
    ("Kartoffeln", "Gemüse & Obst"),
    ("Ei", "Eier"),
    ("Flammkuchenteig", "Teigwaren"),
    ("Pizzateig", "Teigwaren"),
    ("Quicheteig", "Teigwaren"),
    ("Tofu", "Proteine"),
    ("Rucola", "Gemüse & Obst"),
    ("Baguette", "Brot"),
    ("Passierte Tomaten", "Dosenprodukte"),
    ("Nudeln", "Teigwaren"),
    ("Lasagne Platten", "Teigwaren"),
    ("Kritaraki", "Teigwaren"),
    ("Reis", "Teigwaren"),
    ("Linsen", "Hülsenfrüchte"),
    ("Mais", "Dosenprodukte"),
    ("Wraps", "Teigwaren"),
    ("Mais Kidneybohnen Mix", "Dosenprodukte"),
    ("Dip", "Milchprodukte"),
    ("Creme Fraiche", "Milchprodukte"),
    ("Sahne", "Milchprodukte"),
    ("Sour Creme", "Milchprodukte"),
    ("Streukäse", "Milchprodukte"),
    ("Ziegenkäse", "Milchprodukte"),
    ("Feta", "Milchprodukte"),
    ("Schmelzkäse", "Milchprodukte"),
    ("Ofenkäse", "Milchprodukte"),
    ("Hack", "Fleisch"),
    ("Schinkenwürfel", "Fleisch"),
]

# Recipes: (name, portion_size, ingredients, tags)
recipes_data = [
    ("Kritaraki", 4, [("Kritaraki", "250g"), ("Tomaten", "3 Stück"), ("Feta", "100g")], ["griechisch", "nudel"]),
    ("Lasagne", 4, [("Lasagne Platten", "12 Stück"), ("Hack", "500g"), ("Passierte Tomaten", "500ml"), ("Streukäse", "200g")], ["italienisch", "auflauf", "ofen"]),
    ("Straßburger Auflauf", 4, [("Kartoffeln", "500g"), ("Schinkenwürfel", "100g"), ("Sahne", "200ml"), ("Streukäse", "100g")], ["auflauf", "herzhaft"]),
    ("Pizza", 2, [("Pizzateig", "1 Stück"), ("Tomaten", "2 Stück"), ("Streukäse", "150g")], ["italienisch", "schnell"]),
    ("Flammkuchen", 2, [("Flammkuchenteig", "1 Stück"), ("Schinkenwürfel", "100g"), ("Creme Fraiche", "150g")], ["französisch", "teig"]),
    ("Quiche", 2, [("Quicheteig", "1 Stück"), ("Ei", "3 Stück"), ("Sahne", "200ml"), ("Feta", "100g")], ["französisch", "auflauf"]),
    ("Curry", 2, [("Reis", "200g"), ("Tofu", "200g"), ("Paprika", "2 Stück"), ("Tomaten", "3 Stück")], ["asiatisch", "würzig"]),
    ("Käse-Sahne Soße", 4, [("Sahne", "200ml"), ("Streukäse", "100g")], ["schnell", "soße"]),
    ("Omelett", 2, [("Ei", "4 Stück"), ("Sahne", "100ml"), ("Pilze", "3 Stück")], ["eiergericht", "frühstück"]),
    ("Wraps", 2, [("Wraps", "2 Stück"), ("Tofu", "150g"), ("Rucola", "50g")], ["schnell", "leicht"]),
    ("Ofenkäse", 2, [("Ofenkäse", "1 Stück"), ("Baguette", "1 Stück"), ("Dip", "100g")], ["käsegericht", "einfach"]),
]

def populate_database():
    """Populates the database with initial ingredients, categories, and recipes."""
    print("🚀 Starting database population...")

    # Insert all ingredients (ensures categories exist first)
    for name, category in ingredients_data:
        add_ingredient(name, category)

    # Insert all recipes
    for name, portion_size, ingredients, tags in recipes_data:
        add_recipe(name, portion_size, ingredients, tags)

    print("✅ Database populated successfully!")

# Run script
if __name__ == "__main__":
    populate_database()
