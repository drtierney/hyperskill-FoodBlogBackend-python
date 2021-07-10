# hyperskill-FoodBlogBackend-python
You will create a simple backend that will allow you to populate an SQLite3 database. You will know how to deal with the primary key auto-increment and how to use foreign keys to create relationships between the tables. Learn how to deal with many-to-many relations. Work with SQL queries and database cursor methods.  
https://hyperskill.org/projects/167  

<img src="https://github.com/drtierney/hyperskill-FoodBlogBackend-python/blob/main/food-blog-backend.gif"/>

## Syntax
| Arg | Valuelist | Comment
| --- | --------- | ------- |
| db_name | `<String>` | Required<br>Absolute or relative path to database file|
| --ingredients | `<String>` | Optional<br>A list of ingredients each separated by comma; must be called at same time as --meals|
| --meals | `<String>` | Optional<br>A list of meal types each separated by comma; must be called at same time as --ingredients|

```
blog.py food_blog.db
```

```
blog.py food_blog.db --ingredients=strawberry --meals=lunch
```

```
blog.py food_blog.db --meals=breakfast,brunch --ingredients=blueberry,blackberry 
```

## Stages
**Stage #1: Create dictionaries**  
Create a database and prepare the dictionaries.  

**Stage #2: Time for recipes!**  
Create the main table and a simple recipe entry tool.  

**Stage #3: Many-to-many relations**  
Create an intermediary table to deal with many-to-many relations.  

**Stage #4: Too many ingredients!**  
Create a table to store quantity, measure, and ingredient names. You will also need to implement ways to speed up the database completion.  

**Stage 5: First interface**  
Create your first backend interface that will allow you to return the data you are looking for.  
