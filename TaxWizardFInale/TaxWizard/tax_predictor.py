
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_tax_refund_model():
    np.random.seed(42)
    n_samples = 1000
    data = {
        'annual_income': np.random.normal(800000, 200000, n_samples).clip(300000, 2000000),
        'investment_80C': np.random.uniform(0, 150000, n_samples),
        'insurance_premium_80D': np.random.uniform(0, 50000, n_samples),
        'home_loan_interest': np.random.uniform(0, 200000, n_samples),
        'education_loan_interest': np.random.uniform(0, 100000, n_samples),
        'house_rent_paid': np.random.uniform(0, 250000, n_samples)
    }
    
    df = pd.DataFrame(data)
    df['expected_tax_refund'] = df.apply(calculate_tax_refund, axis=1)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(df.drop('expected_tax_refund', axis=1), df['expected_tax_refund'])
    return model

def calculate_tax_refund(row):
    total_deductions = (
        row['investment_80C'] + 
        row['insurance_premium_80D'] + 
        row['home_loan_interest'] + 
        row['education_loan_interest'] + 
        (0.4 * row['house_rent_paid'])
    )
    taxable_income = max(row['annual_income'] - total_deductions, 250000)
    
    if taxable_income <= 500000:
        tax_payable = 0
    elif taxable_income <= 1000000:
        tax_payable = 0.1 * (taxable_income - 500000)
    else:
        tax_payable = 0.2 * (taxable_income - 1000000) + 50000

    max_tax = 0.2 * (row['annual_income'] - 1000000) + 50000 if row['annual_income'] > 1000000 else 0.1 * (row['annual_income'] - 500000)
    max_tax = max(max_tax, 0)
    return max(0, max_tax - tax_payable)

def predict_refund(annual_income, investment_80C, insurance_premium_80D, 
                  home_loan_interest, education_loan_interest, house_rent_paid):
    model = train_tax_refund_model()
    user_input = pd.DataFrame([{
        'annual_income': annual_income,
        'investment_80C': investment_80C,
        'insurance_premium_80D': insurance_premium_80D,
        'home_loan_interest': home_loan_interest,
        'education_loan_interest': education_loan_interest,
        'house_rent_paid': house_rent_paid
    }])
    return round(float(model.predict(user_input)[0]), 2)
