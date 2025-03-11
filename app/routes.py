from flask import render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from app import app, db
from app.models import Recipe, Ingredient, RecipeIngredient, MealPlan, GroceryList, GroceryItem
from datetime import datetime, timedelta
import calendar

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes/')
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/new/')
def new_recipe():
    ingredients = Ingredient.query.order_by(Ingredient.category, Ingredient.name).all()
    return render_template('new_recipe.html', ingredients=ingredients)

@app.route('/recipe/<int:recipe_id>/')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/meal-plan/')
def meal_plan():
    # Get current week's dates
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Get all recipes for the form
    recipes = Recipe.query.order_by(Recipe.name).all()
    
    return render_template('meal_plan.html', 
                         meal_plan={},  # Empty for static version
                         recipes=recipes,
                         week_start=week_start,
                         week_end=week_end)

@app.route('/grocery-list/')
def grocery_list():
    # Get current week's dates
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    return render_template('grocery_list.html', 
                         grocery_list=None,  # Empty for static version
                         week_start=week_start,
                         week_end=week_end)

@app.route('/seasonal-ingredients/')
def seasonal_ingredients():
    # Get all ingredients grouped by season
    ingredients = Ingredient.query.order_by(Ingredient.category, Ingredient.name).all()
    return render_template('seasonal_ingredients.html', ingredients=ingredients)

# The following routes are API endpoints and won't be frozen
@app.route('/api/toggle-grocery-item/<int:item_id>', methods=['POST'])
def toggle_grocery_item(item_id):
    return jsonify({'status': 'error', 'message': 'Not available in static version'})

@app.route('/meal-plan/remove/<int:meal_id>', methods=['POST'])
def remove_from_meal_plan(meal_id):
    return redirect(url_for('meal_plan'))

@app.route('/generate-grocery-list/')
def generate_grocery_list():
    return redirect(url_for('grocery_list'))

@app.route('/reset-grocery-lists/')
def reset_grocery_lists():
    return redirect(url_for('grocery_list')) 