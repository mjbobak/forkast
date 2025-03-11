from app import db
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    season_start = db.Column(db.Integer)  # Month number (1-12)
    season_end = db.Column(db.Integer)    # Month number (1-12)
    category = db.Column(db.String(50))   # e.g., vegetable, fruit, meat, dairy
    unit = db.Column(db.String(20))       # e.g., grams, pieces, cups

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients')

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    meal_type = db.Column(db.String(20))  # breakfast, lunch, dinner
    recipe = db.relationship('Recipe', backref='meal_plans')

class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_start = db.Column(db.Date, nullable=False)
    week_end = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('GroceryItem', backref='grocery_list', lazy=True)

class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grocery_list_id = db.Column(db.Integer, db.ForeignKey('grocery_list.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    purchased = db.Column(db.Boolean, default=False)
    ingredient = db.relationship('Ingredient') 