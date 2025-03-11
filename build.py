import os
import shutil
from flask_frozen import Freezer
from run import app
from app.models import Recipe

# Configure Frozen-Flask
app.config['FREEZER_DESTINATION'] = '_site'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_BASE_URL'] = 'https://marty.github.io/forkast/'

freezer = Freezer(app)

# URL generators for dynamic routes
@freezer.register_generator
def recipe_detail():
    for recipe in Recipe.query.all():
        yield {'recipe_id': recipe.id}

@freezer.register_generator
def toggle_grocery_item():
    return []  # API endpoint, no need to generate static files

@freezer.register_generator
def remove_from_meal_plan():
    return []  # API endpoint, no need to generate static files

@freezer.register_generator
def reset_grocery_lists():
    return []  # API endpoint, no need to generate static files

@freezer.register_generator
def generate_grocery_list():
    return []  # API endpoint, no need to generate static files

if __name__ == '__main__':
    # Clean the build directory if it exists
    if os.path.exists('_site'):
        shutil.rmtree('_site')
    
    # Create a fresh build directory
    os.makedirs('_site', exist_ok=True)
    
    # Generate static files
    freezer.freeze()