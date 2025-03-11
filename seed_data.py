from app import app, db
from app.models import Recipe, Ingredient, RecipeIngredient
from datetime import datetime

def seed_ingredients():
    # Clear existing data
    RecipeIngredient.query.delete()
    Recipe.query.delete()
    Ingredient.query.delete()

    # Vegetables
    tomatoes = Ingredient(name='Tomatoes', season_start=6, season_end=9, category='vegetable', unit='pieces')
    spinach = Ingredient(name='Spinach', season_start=3, season_end=5, category='vegetable', unit='grams')
    carrots = Ingredient(name='Carrots', season_start=1, season_end=12, category='vegetable', unit='grams')
    zucchini = Ingredient(name='Zucchini', season_start=6, season_end=8, category='vegetable', unit='pieces')
    
    # Fruits
    strawberries = Ingredient(name='Strawberries', season_start=5, season_end=7, category='fruit', unit='grams')
    apples = Ingredient(name='Apples', season_start=9, season_end=11, category='fruit', unit='pieces')
    lemons = Ingredient(name='Lemons', season_start=1, season_end=12, category='fruit', unit='pieces')
    
    # Proteins
    chicken = Ingredient(name='Chicken Breast', season_start=1, season_end=12, category='protein', unit='grams')
    salmon = Ingredient(name='Salmon Fillet', season_start=1, season_end=12, category='protein', unit='grams')
    
    # Pantry
    olive_oil = Ingredient(name='Olive Oil', season_start=1, season_end=12, category='pantry', unit='ml')
    rice = Ingredient(name='Brown Rice', season_start=1, season_end=12, category='pantry', unit='grams')
    pasta = Ingredient(name='Whole Wheat Pasta', season_start=1, season_end=12, category='pantry', unit='grams')
    
    # Dairy
    cheese = Ingredient(name='Parmesan Cheese', season_start=1, season_end=12, category='dairy', unit='grams')
    yogurt = Ingredient(name='Greek Yogurt', season_start=1, season_end=12, category='dairy', unit='grams')

    ingredients = [tomatoes, spinach, carrots, zucchini, strawberries, apples, lemons,
                  chicken, salmon, olive_oil, rice, pasta, cheese, yogurt]
    
    for ingredient in ingredients:
        db.session.add(ingredient)
    db.session.commit()

    # Recipes
    recipes = [
        {
            'name': 'Summer Pasta Primavera',
            'description': 'A light and fresh pasta dish loaded with seasonal vegetables.',
            'instructions': '''
1. Cook pasta according to package instructions.
2. Sauté zucchini and carrots in olive oil until tender.
3. Add cherry tomatoes and cook until slightly softened.
4. Toss pasta with vegetables, olive oil, and grated parmesan cheese.
5. Season with salt and pepper to taste.
''',
            'prep_time': 15,
            'cook_time': 20,
            'servings': 4,
            'ingredients': [
                (pasta, 500),
                (zucchini, 2),
                (carrots, 200),
                (tomatoes, 4),
                (olive_oil, 45),
                (cheese, 50)
            ]
        },
        {
            'name': 'Grilled Chicken with Spring Vegetables',
            'description': 'Healthy grilled chicken served with seasonal spring vegetables.',
            'instructions': '''
1. Season chicken breasts with salt and pepper.
2. Grill chicken for 6-7 minutes per side.
3. Steam carrots and spinach until tender.
4. Drizzle with olive oil and serve.
''',
            'prep_time': 10,
            'cook_time': 25,
            'servings': 4,
            'ingredients': [
                (chicken, 600),
                (carrots, 300),
                (spinach, 200),
                (olive_oil, 30)
            ]
        },
        {
            'name': 'Salmon with Brown Rice Bowl',
            'description': 'Nutritious salmon fillet served over brown rice with seasonal vegetables.',
            'instructions': '''
1. Cook brown rice according to package instructions.
2. Season salmon with lemon juice, salt, and pepper.
3. Pan-sear salmon for 4-5 minutes per side.
4. Serve over rice with steamed vegetables and lemon wedges.
''',
            'prep_time': 10,
            'cook_time': 30,
            'servings': 2,
            'ingredients': [
                (salmon, 400),
                (rice, 200),
                (lemons, 1),
                (olive_oil, 30)
            ]
        }
    ]

    for recipe_data in recipes:
        recipe = Recipe(
            name=recipe_data['name'],
            description=recipe_data['description'],
            instructions=recipe_data['instructions'],
            prep_time=recipe_data['prep_time'],
            cook_time=recipe_data['cook_time'],
            servings=recipe_data['servings']
        )
        db.session.add(recipe)
        db.session.flush()  # Get the recipe ID

        for ingredient, quantity in recipe_data['ingredients']:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=quantity
            )
            db.session.add(recipe_ingredient)

    db.session.commit()

def seed_database():
    with app.app_context():
        seed_ingredients()
        seed_recipes()
        db.session.commit()

if __name__ == '__main__':
    seed_database() 