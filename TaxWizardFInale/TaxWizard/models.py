from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with other tables
    tax_data = db.relationship('TaxData', backref='user', lazy=True)
    tax_documents = db.relationship('TaxDocument', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TaxData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    filing_status = db.Column(db.String(50), nullable=False)
    dependents = db.Column(db.Integer, default=0)
    mortgage_interest = db.Column(db.Float, default=0)
    property_tax = db.Column(db.Float, default=0)
    medical_expenses = db.Column(db.Float, default=0)
    charitable_contributions = db.Column(db.Float, default=0)
    retirement_contributions = db.Column(db.Float, default=0)
    life_insurance = db.Column(db.Float, default=0)
    education_loan = db.Column(db.Float, default=0)
    self_employed = db.Column(db.Boolean, default=False)
    business_income = db.Column(db.Float, default=0)
    business_expenses = db.Column(db.Float, default=0)
    capital_gains = db.Column(db.Float, default=0)
    rental_income = db.Column(db.Float, default=0)
    rental_expenses = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaxDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    tax_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

class TaxAdvice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tax_year = db.Column(db.Integer, nullable=False)
    advice_text = db.Column(db.Text, nullable=False)
    potential_savings = db.Column(db.Float)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ErrorDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tax_year = db.Column(db.Integer, nullable=False)
    error_field = db.Column(db.String(100), nullable=False)
    error_message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # e.g., 'high', 'medium', 'low'
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)

class TaxOptimization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tax_year = db.Column(db.Integer, nullable=False)
    strategy = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    potential_savings = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)