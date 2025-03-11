from flask import render_template, request, jsonify, redirect, url_for, flash
from app import app, db
from app.models import Recipe, Ingredient, RecipeIngredient, MealPlan, GroceryList, GroceryItem
from datetime import datetime, timedelta
import calendar

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    if request.method == 'POST':
        recipe = Recipe(
            name=request.form['name'],
            description=request.form['description'],
            instructions=request.form['instructions'],
            prep_time=int(request.form['prep_time']),
            cook_time=int(request.form['cook_time']),
            servings=int(request.form['servings'])
        )
        db.session.add(recipe)
        db.session.flush()

        # Handle ingredients
        ingredient_ids = request.form.getlist('ingredient_id[]')
        quantities = request.form.getlist('quantity[]')
        
        for i in range(len(ingredient_ids)):
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=int(ingredient_ids[i]),
                quantity=float(quantities[i])
            )
            db.session.add(recipe_ingredient)

        db.session.commit()
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('recipes'))

    ingredients = Ingredient.query.order_by(Ingredient.category, Ingredient.name).all()
    return render_template('new_recipe.html', ingredients=ingredients)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/meal-plan', methods=['GET', 'POST'])
def meal_plan():
    if request.method == 'POST':
        recipe_id = request.form.get('recipe_id')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        meal_type = request.form.get('meal_type')
        
        meal_plan = MealPlan(recipe_id=recipe_id, date=date, meal_type=meal_type)
        db.session.add(meal_plan)
        db.session.commit()
        
        return redirect(url_for('meal_plan'))
    
    # Get current week's meal plan
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    meal_plans = MealPlan.query.filter(
        MealPlan.date.between(week_start, week_end)
    ).order_by(MealPlan.date, MealPlan.meal_type).all()
    
    # Organize meals by date and meal type
    organized_meals = {}
    for meal in meal_plans:
        if meal.date not in organized_meals:
            organized_meals[meal.date] = {
                'breakfast': [],
                'lunch': [],
                'dinner': [],
                'snack': []
            }
        organized_meals[meal.date][meal.meal_type].append(meal)
    
    recipes = Recipe.query.order_by(Recipe.name).all()
    return render_template('meal_plan.html', 
                         meal_plan=organized_meals,
                         recipes=recipes,
                         week_start=week_start,
                         week_end=week_end)

@app.route('/grocery-list')
def grocery_list():
    # Get current week's dates
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Try to get existing grocery list for the week
    grocery_list = GroceryList.query.filter_by(
        week_start=week_start,
        week_end=week_end
    ).first()
    
    # Only create a new list if one doesn't exist
    if not grocery_list:
        grocery_list = GroceryList(week_start=week_start, week_end=week_end)
        db.session.add(grocery_list)
        db.session.commit()
        
        # Generate grocery list items from meal plan
        meal_plans = MealPlan.query.filter(
            MealPlan.date.between(week_start, week_end)
        ).all()
        
        ingredients_needed = {}
        for meal_plan in meal_plans:
            for recipe_ingredient in meal_plan.recipe.ingredients:
                ingredient = recipe_ingredient.ingredient
                if ingredient.id in ingredients_needed:
                    ingredients_needed[ingredient.id] += recipe_ingredient.quantity
                else:
                    ingredients_needed[ingredient.id] = recipe_ingredient.quantity
        
        for ingredient_id, quantity in ingredients_needed.items():
            item = GroceryItem(
                grocery_list_id=grocery_list.id,
                ingredient_id=ingredient_id,
                quantity=quantity
            )
            db.session.add(item)
        
        db.session.commit()
        
        # Reload the grocery list to get all relationships
        grocery_list = GroceryList.query.get(grocery_list.id)
    
    return render_template('grocery_list.html', 
                         grocery_list=grocery_list,
                         week_start=week_start,
                         week_end=week_end)

@app.route('/seasonal-ingredients')
def seasonal_ingredients():
    current_month = datetime.now().month
    seasonal_ingredients = Ingredient.query.filter(
        Ingredient.season_start <= current_month,
        Ingredient.season_end >= current_month
    ).all()
    return render_template('seasonal_ingredients.html', ingredients=seasonal_ingredients)

@app.route('/api/toggle-grocery-item/<int:item_id>', methods=['POST'])
def toggle_grocery_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    item.purchased = not item.purchased
    db.session.commit()
    return jsonify({'status': 'success', 'purchased': item.purchased})

@app.route('/reset-grocery-lists')
def reset_grocery_lists():
    # Delete all grocery items first (due to foreign key constraints)
    GroceryItem.query.delete()
    # Delete all grocery lists
    GroceryList.query.delete()
    db.session.commit()
    flash('All grocery lists have been reset.', 'success')
    return redirect(url_for('grocery_list'))

@app.route('/meal-plan/remove/<int:meal_id>', methods=['POST'])
def remove_from_meal_plan(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for('meal_plan'))

@app.route('/generate-grocery-list')
def generate_grocery_list():
    # Delete existing grocery list for the week
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    GroceryList.query.filter_by(
        week_start=week_start,
        week_end=week_end
    ).delete()
    
    # Create new grocery list
    grocery_list = GroceryList(week_start=week_start, week_end=week_end)
    db.session.add(grocery_list)
    db.session.commit()
    
    # Generate grocery list items from meal plan
    meal_plans = MealPlan.query.filter(
        MealPlan.date.between(week_start, week_end)
    ).all()
    
    ingredients_needed = {}
    for meal_plan in meal_plans:
        for recipe_ingredient in meal_plan.recipe.ingredients:
            ingredient = recipe_ingredient.ingredient
            if ingredient.id in ingredients_needed:
                ingredients_needed[ingredient.id] += recipe_ingredient.quantity
            else:
                ingredients_needed[ingredient.id] = recipe_ingredient.quantity
    
    for ingredient_id, quantity in ingredients_needed.items():
        item = GroceryItem(
            grocery_list_id=grocery_list.id,
            ingredient_id=ingredient_id,
            quantity=quantity
        )
        db.session.add(item)
    
    db.session.commit()
    
    return redirect(url_for('grocery_list')) 