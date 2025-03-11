from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime
import calendar

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Static file configuration
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.config['STATIC_URL_PATH'] = '/static'

# Initialize database
db = SQLAlchemy(app)

# Template filters and functions
@app.template_filter('month_name')
def month_name(month_number):
    return calendar.month_name[month_number]

@app.context_processor
def utility_processor():
    return {
        'now': datetime.now,
        'base_url': '/forkast' if os.getenv('GITHUB_ACTIONS') else ''
    }

from app import routes, models 