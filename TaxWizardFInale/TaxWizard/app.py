import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, User
from flask_login import LoginManager
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///tax_assistant.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def ask_gpt(question):
    try:
        response = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[
                {"role": "system", "content": "You are a friendly and helpful tax assistant. Provide accurate and helpful information about taxes, tax calculations, and related financial matters."},
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=500,
            timeout=20
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Import all routes
from routes import *

# Routes are now defined in routes.py

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
