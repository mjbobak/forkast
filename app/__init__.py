from flask import Flask, url_for
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

# GitHub Pages configuration
if os.getenv('GITHUB_ACTIONS'):
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'mjbobak.github.io'

# Initialize database
db = SQLAlchemy(app)

# Template filters and functions
@app.template_filter('month_name')
def month_name(month_number):
    return calendar.month_name[month_number]

@app.context_processor
def utility_processor():
    def full_url_for(endpoint, **kwargs):
        with app.test_request_context():
            if os.getenv('GITHUB_ACTIONS'):
                return f"/forkast{url_for(endpoint, **kwargs)}"
            return url_for(endpoint, **kwargs)
    
    return {
        'now': datetime.now,
        'full_url_for': full_url_for
    }

from app import routes, models 