import sys
import os
import sqlite3

args = sys.argv
database_name = args[1]

# Fails to create tables if they already exist; quicker to delete db file than drop tables
if os.path.exists(database_name):
    os.remove(database_name)

conn = sqlite3.connect(database_name)


def execute_query(query):
    cur = conn.cursor()
    result = cur.execute(query)
    conn.commit()
    return result


def validate_amount(amount):
    if amount.isdigit():
        return int(amount)
    return None


def validate_measure(measure):
    if the_measure == "":
        return execute_query('SELECT measure_id from measures '
                             'WHERE measure_name = ""').fetchone()[0]
    rows = execute_query(f'SELECT measure_id from measures '
                         f'WHERE measure_name LIKE "{measure}%"').fetchall()
    if len(rows) == 1:
        return int(rows[0][0])
    return None


def validate_ingredient(ingredient):
    rows = execute_query(f'SELECT ingredient_id from ingredients '
                         f'WHERE ingredient_name LIKE "%{ingredient}%"').fetchall()
    if len(rows) == 1:
        return rows[0][0]
    return None


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

recipes_tbl = '''
CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    recipe_description TEXT
);
'''

serve_tbl = '''
CREATE TABLE serve (
    serve_id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
);
'''

quantity_tbl = '''
CREATE TABLE quantity (
    quantity_id INTEGER PRIMARY KEY,
    measure_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
);
'''

tables = [meals_tbl, ingredients_tbl, measures_tbl, recipes_tbl, serve_tbl, quantity_tbl]

execute_query("PRAGMA foreign_keys = ON;")
for insert_query in tables:
    execute_query(insert_query)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

for table in data.keys():
    for item in data[table]:
        insert_query = f'INSERT INTO {table} ({table[:-1]}_name)\nVALUES ("{item}");'
        execute_query(insert_query)
    output = execute_query(f"select * from {table};")
    print(f"{table} -> ", output.fetchall())

print("Pass the empty recipe name to exit.")
while True:
    recipe_name = input("Recipe name: ")
    if recipe_name == "":
        break
    recipe_description = input("Recipe description: ")
    insert_query = f'INSERT INTO recipes (recipe_name, recipe_description) ' \
                   f'VALUES ("{recipe_name}", "{recipe_description}")'
    recipe_id = execute_query(insert_query).lastrowid

    print(' '.join('%s) %s' % meal for meal in execute_query("select * from meals;").fetchall()))
    meal_choices = [int(x) for x in input("When the dish can be served: ").split()]
    for meal_id in meal_choices:
        insert_query = f'INSERT INTO serve (recipe_id, meal_id) ' \
                       f'VALUES ({recipe_id}, {meal_id})'
        execute_query(insert_query)
    while True:
        quantity_input = [x for x in input("Input quantity of ingredient <press enter to stop>: ").split()]
        if len(quantity_input) == 0:
            break
        the_amount, the_ingredient = [quantity_input[0], quantity_input[-1]]
        the_measure = "" if len(quantity_input) == 2 else quantity_input[1]
        quantity = validate_amount(the_amount)
        measure_id = validate_measure(the_measure)
        ingredient_id = validate_ingredient(the_ingredient)
        if None in [quantity, measure_id, ingredient_id]:
            print("The ingredient is not conclusive!")
        else:
            insert_query = f'INSERT INTO quantity (measure_id, ingredient_id, quantity, recipe_id) ' \
                           f'VALUES ({measure_id}, {ingredient_id}, {quantity}, {recipe_id})'
            execute_query(insert_query)
conn.close()
