import os
import shutil
import sys
from pathlib import Path
from flask_frozen import Freezer
from run import app
from app.models import Recipe

def clean_directory(path):
    """Clean a directory and all its contents"""
    try:
        if os.path.exists(path):
            print(f"Removing existing directory: {path}")
            shutil.rmtree(path)
        print(f"Creating fresh directory: {path}")
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"Error handling directory {path}: {e}", file=sys.stderr)
        raise

# Configure Frozen-Flask
build_dir = os.path.abspath('_site')
app.config['FREEZER_DESTINATION'] = build_dir
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_BASE_URL'] = 'https://marty.github.io/forkast/'
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True
app.config['FREEZER_STATIC_IGNORE'] = ['*.db']

# Initialize Freezer
freezer = Freezer(app)

# URL generators for dynamic routes
@freezer.register_generator
def recipe_detail():
    for recipe in Recipe.query.all():
        yield {'recipe_id': recipe.id}

@freezer.register_generator
def recipes():
    yield {}

@freezer.register_generator
def new_recipe():
    yield {}

@freezer.register_generator
def meal_plan():
    yield {}

@freezer.register_generator
def grocery_list():
    yield {}

@freezer.register_generator
def seasonal_ingredients():
    yield {}

if __name__ == '__main__':
    print("Starting static site generation...")
    print(f"Build directory: {build_dir}")
    
    # Clean and recreate the build directory
    clean_directory(build_dir)
    
    # Also clean any potential conflicting directories
    for path in [
        os.path.join(build_dir, 'recipes'),
        os.path.join(build_dir, 'recipe'),
        os.path.join(build_dir, 'meal-plan'),
        os.path.join(build_dir, 'grocery-list'),
        os.path.join(build_dir, 'seasonal-ingredients'),
    ]:
        clean_directory(path)
    
    print("Generating static files...")
    try:
        freezer.freeze()
        print("Static site generation completed successfully!")
    except Exception as e:
        print(f"Error during static site generation: {e}", file=sys.stderr)
        raise