from utils import validate_tax_data
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_errors_in_tax_data(tax_data):
    """
    Detect errors in tax data using basic validation and anomaly detection
    """
    # Basic validation first
    errors = validate_tax_data(tax_data)
    
    # Advanced anomaly detection
    anomalies = detect_anomalies(tax_data)
    errors.extend(anomalies)
    
    # Check for compliance issues
    compliance_errors = check_compliance(tax_data)
    errors.extend(compliance_errors)
    
    return errors

def detect_anomalies(tax_data):
    """
    Use machine learning to detect anomalies in tax data
    A simple example using Isolation Forest
    """
    anomalies = []
    
    # In a real application, this would use historical data or industry standards
    # For demonstration, we'll create some basic ratio checks
    
    # Income to deductions ratio
    total_deductions = (
        tax_data.mortgage_interest + 
        tax_data.property_tax + 
        tax_data.charitable_contributions + 
        tax_data.medical_expenses
    )
    
    deduction_ratio = total_deductions / max(1, tax_data.income)
    
    if deduction_ratio > 0.7:  # If deductions are more than 70% of income
        anomalies.append({
            'field': 'deductions',
            'message': 'Your total deductions are unusually high compared to your income',
            'severity': 'medium'
        })
    
    # Charitable contributions ratio
    if tax_data.charitable_contributions > 0:
        charity_ratio = tax_data.charitable_contributions / max(1, tax_data.income)
        if charity_ratio > 0.3:  # If charitable contributions are more than 30% of income
            anomalies.append({
                'field': 'charitable_contributions',
                'message': 'Your charitable contributions are unusually high compared to your income',
                'severity': 'medium'
            })
    
    # Business expense ratio for self-employed
    if tax_data.self_employed and tax_data.business_income > 0:
        expense_ratio = tax_data.business_expenses / max(1, tax_data.business_income)
        if expense_ratio > 0.9:  # If expenses are more than 90% of business income
            anomalies.append({
                'field': 'business_expenses',
                'message': 'Your business expenses are unusually high compared to your business income',
                'severity': 'medium'
            })
    
    # In a real application with sufficient data, we could use Isolation Forest like this:
    # features = np.array([
    #     [tax_data.income, total_deductions, tax_data.charitable_contributions, 
    #      tax_data.business_income, tax_data.business_expenses]
    # ])
    # model = IsolationForest(contamination=0.1)
    # outliers = model.fit_predict(features)
    # if outliers[0] == -1:  # -1 indicates an outlier
    #     anomalies.append({
    #         'field': 'general',
    #         'message': 'Your tax data contains unusual patterns that may require review',
    #         'severity': 'low'
    #     })
    
    return anomalies

def check_compliance(tax_data):
    """
    Check for compliance issues with tax regulations
    """
    compliance_errors = []
    
    # Example compliance checks
    current_year = 2023  # For demonstration
    
    # Check for excess retirement contributions
    max_401k = 22500  # 2023 limit
    if tax_data.retirement_contributions > max_401k:
        compliance_errors.append({
            'field': 'retirement_contributions',
            'message': f'Your retirement contributions exceed the {current_year} limit of ${max_401k}',
            'severity': 'high'
        })
    
    # Mortgage interest deduction check
    # 2023 limit is interest on up to $750,000 of qualified residence loans
    if tax_data.mortgage_interest > 30000:  # Approximate limit for demonstration
        compliance_errors.append({
            'field': 'mortgage_interest',
            'message': 'Your mortgage interest deduction may exceed IRS limits',
            'severity': 'medium'
        })
    
    # State and local tax (SALT) deduction check
    # 2023 limit is $10,000
    if tax_data.property_tax > 10000:
        compliance_errors.append({
            'field': 'property_tax',
            'message': 'Your state and local tax deduction may exceed the $10,000 limit',
            'severity': 'medium'
        })
    
    # Medical expense deduction threshold check
    # Can only deduct medical expenses that exceed 7.5% of AGI
    medical_threshold = tax_data.income * 0.075
    if tax_data.medical_expenses < medical_threshold and tax_data.medical_expenses > 0:
        compliance_errors.append({
            'field': 'medical_expenses',
            'message': f'Your medical expenses must exceed 7.5% of your income (${medical_threshold:.2f}) to qualify for a deduction',
            'severity': 'low'
        })
    
    return compliance_errors
