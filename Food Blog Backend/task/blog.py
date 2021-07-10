import sqlite3
from sqlite3 import OperationalError
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("db_name")
parser.add_argument("--ingredients", default=argparse.SUPPRESS)
parser.add_argument("--meals", default=argparse.SUPPRESS)

args = parser.parse_args()

conn = sqlite3.connect(args.db_name)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


def execute_query(command):
    cur = conn.cursor()
    result = cur.execute(command)
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


def execute_queries_from_file(filename):
    with open(filename, "r") as f:
        content = f.read()
        queries = content.split(";")
    for command in queries:
        try:
            execute_query(command)
        except OperationalError as opErr:
            print(f"{opErr}")


execute_query("PRAGMA foreign_keys = ON;")
execute_queries_from_file("create_tables.sql")

for table in data.keys():
    for item in data[table]:
        item_exists = execute_query(f"SELECT * FROM {table} WHERE {table[:-1]}_name = '{item}'").fetchone()
        if not item_exists:
            execute_query(f'INSERT INTO {table} ({table[:-1]}_name)\nVALUES ("{item}");')
    output = execute_query(f"select * from {table};")

if all({"ingredients", "meals" in args}):
    ingredients = str(args.ingredients).split(",")
    meals = str(args.meals).split(",")

    quantity, serve, output = [], [], []
    for ingredient_name in ingredients:
        query = f"SELECT recipe_id FROM quantity WHERE ingredient_id IN " \
                f"(SELECT ingredient_id FROM ingredients WHERE ingredient_name = '{ingredient_name}')"
        quantity.append(set(recipe_id[0] for recipe_id in execute_query(query)))
    quantity = set.intersection(*quantity)

    for meal_name in meals:
        query = f"SELECT recipe_id FROM serve WHERE meal_id IN " \
                f"(SELECT meal_id FROM meals WHERE meal_name = '{meal_name}')"
        serve.append(set(recipe_id[0] for recipe_id in execute_query(query)))
    for item in [*serve]:
        for item_ in item:
            if item_ in quantity:
                output.append(item_)
    recipes = ", ".join([execute_query(f"SELECT recipe_name FROM recipes WHERE recipe_id = '{recipe_id}'").fetchone()[0]
                         for recipe_id in output])
    print(f"Recipes selected for you: {recipes}" if recipes else "There are no such recipes in the database.")

else:
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
            the_quantity = validate_amount(the_amount)
            measure_id = validate_measure(the_measure)
            ingredient_id = validate_ingredient(the_ingredient)
            if None in [the_quantity, measure_id, ingredient_id]:
                print("The ingredient is not conclusive!")
            else:
                insert_query = f'INSERT INTO quantity (measure_id, ingredient_id, quantity, recipe_id) ' \
                               f'VALUES ({measure_id}, {ingredient_id}, {the_quantity}, {recipe_id})'
                execute_query(insert_query)

conn.close()
