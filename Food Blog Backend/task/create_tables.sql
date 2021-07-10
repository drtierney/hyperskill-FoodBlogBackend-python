CREATE TABLE IF NOT EXISTS meals (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS measures (
    measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    measure_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    recipe_description TEXT
);

CREATE TABLE IF NOT EXISTS serve (
    serve_id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
);

CREATE TABLE IF NOT EXISTS quantity (
    quantity_id INTEGER PRIMARY KEY,
    measure_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
);
