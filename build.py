import os
import shutil
from flask_frozen import Freezer
from run import app
from app.models import Recipe

# Configure Frozen-Flask
app.config['FREEZER_DESTINATION'] = os.path.abspath('_site')
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_BASE_URL'] = 'https://marty.github.io/forkast/'
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True
app.config['FREEZER_STATIC_IGNORE'] = ['*.db']

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
    # Clean the build directory if it exists
    build_dir = os.path.abspath('_site')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    # Create a fresh build directory
    os.makedirs(build_dir, exist_ok=True)
    
    # Generate static files
    freezer.freeze()