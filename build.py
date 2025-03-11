import os
import shutil
import sys
from pathlib import Path
from flask_frozen import Freezer
from run import app
from app.models import Recipe

# Configure Frozen-Flask
build_dir = os.path.abspath('_site')
app.config['FREEZER_DESTINATION'] = build_dir
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_BASE_URL'] = 'https://marty.github.io/forkast/'
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True
app.config['FREEZER_STATIC_IGNORE'] = ['*.db']

# Configure URL handling
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_REDIRECT_POLICY'] = 'follow'

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
    
    # Clean the build directory if it exists
    if os.path.exists(build_dir):
        print(f"Removing existing directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    print(f"Creating fresh directory: {build_dir}")
    os.makedirs(build_dir)
    
    print("Generating static files...")
    try:
        freezer.freeze()
        print("Static site generation completed successfully!")
    except Exception as e:
        print(f"Error during static site generation: {e}", file=sys.stderr)
        raise