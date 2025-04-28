from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
import json
import pandas as pd

from app import app, db, login_manager, ask_gpt
from models import User, TaxData, TaxDocument, TaxAdvice, ErrorDetection, TaxOptimization
from models import User, TaxData, TaxDocument, TaxAdvice, ErrorDetection, TaxOptimization
from utils import allowed_file
from tax_calculator import calculate_tax_liability, get_tax_optimization_strategies
from error_detector import detect_errors_in_tax_data

# Configure file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
            return render_template('register.html')
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get the user's tax data for the current year
    current_year = datetime.now().year
    tax_data = TaxData.query.filter_by(user_id=current_user.id, year=current_year).first()
    
    # Get the user's tax documents
    tax_documents = TaxDocument.query.filter_by(user_id=current_user.id).all()
    
    # Get the user's tax advice
    tax_advice = TaxAdvice.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    # Get the user's error detections
    errors = ErrorDetection.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    # Get the user's tax optimizations
    optimizations = TaxOptimization.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    return render_template('dashboard.html', 
                          tax_data=tax_data, 
                          tax_documents=tax_documents,
                          tax_advice=tax_advice,
                          errors=errors,
                          optimizations=optimizations,
                          current_year=current_year)

@app.route('/tax_refund_prediction')
@login_required
def tax_refund_prediction():
    return render_template('tax_refund_prediction.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
            
        question = data['question']
        answer = ask_gpt(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_refund', methods=['POST'])
@login_required
def predict_refund():
    from tax_predictor import predict_refund
    data = request.get_json()
    predicted_refund = predict_refund(
        float(data['annual_income']),
        float(data['investment_80C']),
        float(data['insurance_premium_80D']),
        float(data['home_loan_interest']),
        float(data['education_loan_interest']),
        float(data['house_rent_paid'])
    )
    return jsonify({'predicted_refund': predicted_refund})

@app.route('/data_collection', methods=['GET', 'POST'])
@login_required
def data_collection():
    current_year = datetime.now().year
    
    # Check if the user already has tax data for the current year
    existing_data = TaxData.query.filter_by(user_id=current_user.id, year=current_year).first()
    
    if request.method == 'POST':
        try:
            # Extract form data
            income = float(request.form.get('income', 0))
            filing_status = request.form.get('filing_status')
            dependents = int(request.form.get('dependents', 0))
            mortgage_interest = float(request.form.get('mortgage_interest', 0))
            property_tax = float(request.form.get('property_tax', 0))
            medical_expenses = float(request.form.get('medical_expenses', 0))
            charitable_contributions = float(request.form.get('charitable_contributions', 0))
            retirement_contributions = float(request.form.get('retirement_contributions', 0))
            life_insurance = float(request.form.get('life_insurance', 0))
            education_loan = float(request.form.get('education_loan', 0))
            self_employed = True if request.form.get('self_employed') == 'yes' else False
            business_income = float(request.form.get('business_income', 0))
            business_expenses = float(request.form.get('business_expenses', 0))
            capital_gains = float(request.form.get('capital_gains', 0))
            rental_income = float(request.form.get('rental_income', 0))
            rental_expenses = float(request.form.get('rental_expenses', 0))
            
            # Create or update tax data
            if existing_data:
                # Update existing record
                existing_data.income = income
                existing_data.filing_status = filing_status
                existing_data.dependents = dependents
                existing_data.mortgage_interest = mortgage_interest
                existing_data.property_tax = property_tax
                existing_data.medical_expenses = medical_expenses
                existing_data.charitable_contributions = charitable_contributions
                existing_data.retirement_contributions = retirement_contributions
                existing_data.life_insurance = life_insurance
                existing_data.education_loan = education_loan
                existing_data.self_employed = self_employed
                existing_data.business_income = business_income
                existing_data.business_expenses = business_expenses
                existing_data.capital_gains = capital_gains
                existing_data.rental_income = rental_income
                existing_data.rental_expenses = rental_expenses
                existing_data.updated_at = datetime.utcnow()
            else:
                # Create new record
                new_tax_data = TaxData(
                    user_id=current_user.id,
                    year=current_year,
                    income=income,
                    filing_status=filing_status,
                    dependents=dependents,
                    mortgage_interest=mortgage_interest,
                    property_tax=property_tax,
                    medical_expenses=medical_expenses,
                    charitable_contributions=charitable_contributions,
                    retirement_contributions=retirement_contributions,
                    life_insurance=life_insurance,
                    education_loan=education_loan,
                    self_employed=self_employed,
                    business_income=business_income,
                    business_expenses=business_expenses,
                    capital_gains=capital_gains,
                    rental_income=rental_income,
                    rental_expenses=rental_expenses
                )
                db.session.add(new_tax_data)
            
            db.session.commit()
            
            # Run error detection
            tax_data = existing_data if existing_data else new_tax_data
            errors = detect_errors_in_tax_data(tax_data)
            
            for error in errors:
                # Check if this error already exists
                existing_error = ErrorDetection.query.filter_by(
                    user_id=current_user.id,
                    tax_year=current_year,
                    error_field=error['field']
                ).first()
                
                if existing_error:
                    existing_error.error_message = error['message']
                    existing_error.severity = error['severity']
                    existing_error.detected_at = datetime.utcnow()
                    existing_error.resolved = False
                else:
                    new_error = ErrorDetection(
                        user_id=current_user.id,
                        tax_year=current_year,
                        error_field=error['field'],
                        error_message=error['message'],
                        severity=error['severity']
                    )
                    db.session.add(new_error)
            
            db.session.commit()
            
            flash('Tax data saved successfully', 'success')
            return redirect(url_for('tax_advice'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving tax data: {str(e)}', 'danger')
            logging.error(f"Error in data_collection: {str(e)}")
    
    return render_template('data_collection.html', tax_data=existing_data)

from datetime import datetime

@app.route('/file_upload', methods=['GET', 'POST'])
@login_required
def file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            document_type = request.form.get('document_type')
            tax_year = request.form.get('tax_year')
            description = request.form.get('description', '')
            
            # Create user's folder if it doesn't exist
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            
            # Save document reference to database
            new_document = TaxDocument(
                user_id=current_user.id,
                document_type=document_type,
                filename=filename,
                tax_year=tax_year,
                description=description
            )
            
            db.session.add(new_document)
            db.session.commit()

            # Basic file upload without OCR processing
            flash('File uploaded successfully', 'success')
            return redirect(url_for('dashboard'))
            
            flash('File uploaded successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('File type not allowed', 'danger')
    
    return render_template('file_upload.html', datetime=datetime)

@app.route('/tax_advice')
@login_required
def tax_advice():
    current_year = datetime.now().year
    tax_data = TaxData.query.filter_by(user_id=current_user.id, year=current_year).first()
    
    if not tax_data:
        flash('Please enter your tax information first', 'warning')
        return redirect(url_for('data_collection'))
    
    # Calculate tax liability
    tax_liability = calculate_tax_liability(tax_data)
    
    # Get existing advice or generate new advice
    advice_list = TaxAdvice.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    if not advice_list:
        # Generate personalized advice based on tax data
        advice_items = [
            {
                'category': 'Deductions',
                'advice_text': 'Consider itemizing your deductions since your mortgage interest and property tax payments are substantial.',
                'potential_savings': 1200.00
            },
            {
                'category': 'Retirement',
                'advice_text': 'Increasing your retirement contributions can lower your taxable income.',
                'potential_savings': 800.00
            },
            {
                'category': 'Education',
                'advice_text': 'You may qualify for education credits if you have dependents in college.',
                'potential_savings': 500.00
            }
        ]
        
        for item in advice_items:
            new_advice = TaxAdvice(
                user_id=current_user.id,
                tax_year=current_year,
                advice_text=item['advice_text'],
                potential_savings=item['potential_savings'],
                category=item['category']
            )
            db.session.add(new_advice)
        
        db.session.commit()
        advice_list = TaxAdvice.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    return render_template('tax_advice.html', tax_data=tax_data, tax_liability=tax_liability, advice_list=advice_list)

@app.route('/tax_optimization')
@login_required
def tax_optimization():
    current_year = datetime.now().year
    tax_data = TaxData.query.filter_by(user_id=current_user.id, year=current_year).first()
    
    if not tax_data:
        flash('Please enter your tax information first', 'warning')
        return redirect(url_for('data_collection'))
    
    # Get existing optimizations or generate new ones
    optimizations = TaxOptimization.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    if not optimizations:
        # Generate tax optimization strategies
        strategies = get_tax_optimization_strategies(tax_data)
        
        for strategy in strategies:
            new_optimization = TaxOptimization(
                user_id=current_user.id,
                tax_year=current_year,
                strategy=strategy['strategy'],
                description=strategy['description'],
                potential_savings=strategy['potential_savings']
            )
            db.session.add(new_optimization)
        
        db.session.commit()
        optimizations = TaxOptimization.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    # Calculate total potential savings
    total_savings = sum(opt.potential_savings for opt in optimizations)
    
    return render_template('tax_optimization.html', 
                           tax_data=tax_data, 
                           optimizations=optimizations, 
                           total_savings=total_savings)

@app.route('/compliance')
@login_required
def compliance():
    current_year = datetime.now().year
    tax_data = TaxData.query.filter_by(user_id=current_user.id, year=current_year).first()
    
    if not tax_data:
        flash('Please enter your tax information first', 'warning')
        return redirect(url_for('data_collection'))
    
    # Get errors detected in the user's tax data
    errors = ErrorDetection.query.filter_by(user_id=current_user.id, tax_year=current_year).all()
    
    # Count errors by severity
    error_counts = {
        'high': len([e for e in errors if e.severity == 'high']),
        'medium': len([e for e in errors if e.severity == 'medium']),
        'low': len([e for e in errors if e.severity == 'low'])
    }
    
    # Create compliance status based on errors
    if error_counts['high'] > 0:
        compliance_status = 'Critical Issues'
        compliance_class = 'danger'
    elif error_counts['medium'] > 0:
        compliance_status = 'Warning Issues'
        compliance_class = 'warning'
    elif error_counts['low'] > 0:
        compliance_status = 'Minor Issues'
        compliance_class = 'info'
    else:
        compliance_status = 'Compliant'
        compliance_class = 'success'
    
    return render_template('compliance.html', 
                          tax_data=tax_data, 
                          errors=errors, 
                          error_counts=error_counts,
                          compliance_status=compliance_status,
                          compliance_class=compliance_class)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'update_profile' in request.form:
            # Update user information
            email = request.form.get('email')
            
            # Check if email is already in use by another user
            existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
            if existing_user:
                flash('Email already in use', 'danger')
                return redirect(url_for('profile'))
            
            current_user.email = email
            db.session.commit()
            flash('Profile updated successfully', 'success')
            
        elif 'change_password' in request.form:
            # Change password
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'danger')
                return redirect(url_for('profile'))
                
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return redirect(url_for('profile'))
                
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully', 'success')
    
    return render_template('profile.html')

@app.route('/resolve_error/<int:error_id>', methods=['POST'])
@login_required
def resolve_error(error_id):
    error = ErrorDetection.query.get_or_404(error_id)
    
    # Check if the error belongs to the current user
    if error.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('compliance'))
    
    error.resolved = True
    error.resolved_at = datetime.utcnow()
    db.session.commit()
    
    flash('Error marked as resolved', 'success')
    return redirect(url_for('compliance'))
