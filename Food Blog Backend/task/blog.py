import sys
import sqlite3
import os

args = sys.argv
database_name = args[1]

# fails to create tables if they already exist; quicker to delete db file than drop tables
if os.path.exists(database_name):
    os.remove(database_name)

conn = sqlite3.connect(database_name)
cur = conn.cursor()

meals_tbl = '''
CREATE TABLE meals (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_name TEXT UNIQUE NOT NULL
);
'''

ingredients_tbl = '''
CREATE TABLE ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT UNIQUE NOT NULL
);
'''

measures_tbl = '''
CREATE TABLE measures (
    measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    measure_name TEXT UNIQUE
);
'''

print("CREATING TABLES....")
for query in [meals_tbl, ingredients_tbl, measures_tbl]:
    print(f"TABLE CREATED: {query.split()[2]}.")
    cur.execute(query)
    conn.commit()

print()
print("POPULATING TABLES....")
data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

for table in data.keys():
    for item in data[table]:
        query = f'INSERT INTO {table} ({table[:-1]}_name)\nVALUES ("{item}");'
        cur.execute(query)
        conn.commit()
    print(f"{table} -> ", cur.execute(f"select * from {table};").fetchall())

conn.close()
