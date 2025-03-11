import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data/meal_planner.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
INSERT OR IGNORE INTO ingredients (name, category) VALUES
('Paprika', 'Gemüse & Obst'),
('Tomaten', 'Gemüse & Obst'),
('Pilze', 'Gemüse & Obst'),
('Lauch', 'Gemüse & Obst'),
('Kartoffeln', 'Gemüse & Obst'),
('Ei', 'Gemüse & Obst'),
('Flammkuchenteig', 'Gemüse & Obst'),
('Pizzateig', 'Gemüse & Obst'),
('Quicheteig', 'Gemüse & Obst'),
('Tofu', 'Gemüse & Obst'),
('Rucola', 'Gemüse & Obst'),
('Baguette', 'Brot'),
('Passierte Tomaten', 'Mehl'),
('Nudeln', 'Mehl'),
('Lasagne Platten', 'Mehl'),
('Kritaraki', 'Mehl'),
('Reis', 'Mehl'),
('Linsen', 'Mehl'),
('Mais', 'Mehl'),
('Wraps', 'Mehl'),
('Mais Kidneybohnen Mix', 'Mehl'),
('Dip', 'Milchprodukte'),
('Creme Fraiche', 'Milchprodukte'),
('Sahne', 'Milchprodukte'),
('Sour Creme', 'Milchprodukte'),
('Streukäse', 'Milchprodukte'),
('Ziegenkäse', 'Milchprodukte'),
('Feta', 'Milchprodukte'),
('Schmelzkäse', 'Milchprodukte'),
('Ofenkäse', 'Milchprodukte'),
('Hack', 'Fleisch'),
('Schinkenwürfel', 'Fleisch');
""")

cursor.executescript("""
INSERT OR IGNORE INTO recipes (name, portion_size, category) VALUES
('Kritaraki', 4, 'Nudel'),
('Lasagne', 4, 'Nudel'),
('Straßburger Auflauf', 4, 'Nudel'),
('Pizza', 2, 'Teig'),
('Flammkuchen', 2, 'Teig'),
('Quiche', 2, 'Teig'),
('Curry', 2, 'Reis'),
('Käse-Sahne Soße', 4, 'Nudel'),
('Omelett', 2, 'Eier'),
('Wraps', 2, 'Teig'),
('Ofenkäse', 2, 'Teig');
""")

conn.commit()
conn.close()

print("Database populated successfully!")