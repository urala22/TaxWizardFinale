import numpy as np
from datetime import datetime

def calculate_tax_liability(tax_data):
    """
    Calculate the estimated tax liability based on Indian tax regulations
    """
    # Define Indian tax slabs for FY 2023-24 (New Tax Regime)
    slabs = [
        (0, 300000, 0),
        (300001, 600000, 0.05),
        (600001, 900000, 0.10),
        (900001, 1200000, 0.15),
        (1200001, 1500000, 0.20),
        (1500001, float('inf'), 0.30)
    ]

    # Calculate gross total income
    income = tax_data.income

    # Add business income if self-employed
    if tax_data.self_employed:
        business_profit = max(0, tax_data.business_income - tax_data.business_expenses)
        income += business_profit

    # Add rental income
    rental_profit = max(0, tax_data.rental_income - tax_data.rental_expenses)
    income += rental_profit

    # Add capital gains (simplified)
    income += tax_data.capital_gains

    # Calculate deductions under Section 80C (limit of ₹1.5 lakh)
    sec_80c_deductions = min(150000, (
        tax_data.retirement_contributions +  # PPF, EPF, NPS, etc.
        tax_data.life_insurance             # Life insurance premiums
    ))

    # Health Insurance Premium deduction under Section 80D (limit of ₹25,000)
    health_insurance_deduction = min(25000, tax_data.medical_expenses)

    # Home loan interest deduction under Section 24 (limit of ₹2 lakh for self-occupied property)
    home_loan_deduction = min(200000, tax_data.mortgage_interest)
    
    # Education loan interest deduction under Section 80E (no maximum limit)
    education_loan_deduction = tax_data.education_loan
    
    # Charitable donations deduction under Section 80G (assuming 50% deduction for simplicity)
    charitable_deduction = tax_data.charitable_contributions * 0.5

    # Total deductions
    total_deductions = (
        sec_80c_deductions +
        health_insurance_deduction +
        home_loan_deduction +
        education_loan_deduction +
        charitable_deduction
    )

    # Calculate taxable income
    taxable_income = max(0, income - total_deductions)

    # Calculate tax based on slabs
    tax = 0
    for lower, upper, rate in slabs:
        if taxable_income > lower:
            tax += min(upper - lower, taxable_income - lower) * rate

    # Add health and education cess (4%)
    tax = tax + (tax * 0.04)

    return {
        'gross_income': income,
        'taxable_income': taxable_income,
        'tax_liability': tax,
        'sec_80c_deductions': sec_80c_deductions,
        'health_insurance_deduction': health_insurance_deduction,
        'home_loan_deduction': home_loan_deduction,
        'education_loan_deduction': education_loan_deduction,
        'charitable_deduction': charitable_deduction,
        'total_deductions': total_deductions,
        # Keep these fields for template compatibility but with Indian values
        'agi': income,  # Total income before deductions
        'deduction_used': 'Itemized',  # In Indian tax system there's no standard deduction concept like US
        'standard_deduction': 50000,  # For salaried employees, there is a standard deduction of ₹50,000
        'itemized_deductions': total_deductions,
        'dependent_credit': tax_data.dependents * 4000  # ₹4000 per dependent (example value)
    }

def get_tax_optimization_strategies(tax_data):
    """
    Generate tax optimization strategies based on Indian tax regulations
    """
    strategies = []
    tax_calc = calculate_tax_liability(tax_data)

    # Section 80C optimization
    max_80c = 150000
    current_80c = tax_calc['sec_80c_deductions']
    if current_80c < max_80c:
        potential_saving = min(max_80c - current_80c, tax_data.income * 0.1)
        if potential_saving > 10000:
            strategies.append({
                'strategy': 'Maximize Section 80C Investments',
                'description': f'Consider investing up to ₹{int(potential_saving):,} more in PPF, ELSS funds, or EPF to maximize your Section 80C deductions (up to ₹1.5 lakh limit).',
                'potential_savings': potential_saving * 0.30  # Maximum tax rate
            })
    
    # Life Insurance Premium (part of 80C)
    if tax_data.life_insurance < 25000 and current_80c < max_80c:
        strategies.append({
            'strategy': 'Life Insurance Premium',
            'description': 'Consider getting a life insurance policy to protect your family and claim tax benefits under Section 80C.',
            'potential_savings': min(25000, max_80c - current_80c) * 0.30
        })

    # Health Insurance Premium (Section 80D)
    if tax_data.medical_expenses < 25000:
        strategies.append({
            'strategy': 'Health Insurance Benefits',
            'description': 'Consider getting a health insurance policy for yourself and family to claim deductions under Section 80D up to ₹25,000.',
            'potential_savings': (25000 - tax_data.medical_expenses) * 0.30
        })

    # Home Loan Interest
    if tax_data.mortgage_interest > 0 and tax_data.mortgage_interest < 200000:
        strategies.append({
            'strategy': 'Home Loan Interest Benefits',
            'description': 'You can claim up to ₹2,00,000 as deduction on home loan interest under Section 24.',
            'potential_savings': (200000 - tax_data.mortgage_interest) * 0.30
        })

    # NPS Investment
    strategies.append({
        'strategy': 'National Pension System (NPS)',
        'description': 'Consider investing in NPS to get additional deduction of up to ₹50,000 under Section 80CCD(1B).',
        'potential_savings': 50000 * 0.30
    })

    # Electric Vehicle Loan Interest
    strategies.append({
        'strategy': 'Electric Vehicle Loan',
        'description': 'If planning to buy an electric vehicle, loan interest up to ₹1,50,000 is deductible under Section 80EEB.',
        'potential_savings': 150000 * 0.30
    })

    return strategies