from datetime import date, datetime
from typing import Dict, Any, List
from calendar import monthrange

def calculate_age_detailed(birth_date: date) -> Dict[str, Any]:
    """Calculate detailed age information including next birthday."""
    today = date.today()
    return calculate_age_between_dates(birth_date, today)

def calculate_age_between_dates(birth_date: date, target_date: date) -> Dict[str, Any]:
    """Calculate age between two specific dates."""
    
    if birth_date > target_date:
        raise ValueError("Birth date cannot be after the target date")
    
    # Calculate age
    years = target_date.year - birth_date.year
    months = target_date.month - birth_date.month
    days = target_date.day - birth_date.day
    
    # Adjust for negative days
    if days < 0:
        months -= 1
        if target_date.month == 1:
            prev_month = 12
            prev_year = target_date.year - 1
        else:
            prev_month = target_date.month - 1
            prev_year = target_date.year
        days_in_prev_month = monthrange(prev_year, prev_month)[1]
        days = days_in_prev_month + days
    
    # Adjust for negative months
    if months < 0:
        years -= 1
        months = 12 + months
    
    # Calculate totals
    total_days = (target_date - birth_date).days
    total_weeks = total_days // 7
    total_months = years * 12 + months
    total_hours = total_days * 24
    total_minutes = total_hours * 60
    total_seconds = total_minutes * 60
    
    # Calculate next birthday (only if target_date is today)
    days_to_birthday = None
    next_birthday = None
    if target_date == date.today():
        next_birthday = birth_date.replace(year=target_date.year)
        if next_birthday < target_date:
            next_birthday = birth_date.replace(year=target_date.year + 1)
        days_to_birthday = (next_birthday - target_date).days
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'total_days': total_days,
        'total_months': total_months,
        'total_weeks': total_weeks,
        'total_hours': total_hours,
        'total_minutes': total_minutes,
        'total_seconds': total_seconds,
        'days_to_birthday': days_to_birthday,
        'next_birthday': next_birthday,
        'birth_date_formatted': birth_date.strftime('%B %d, %Y'),
        'target_date_formatted': target_date.strftime('%B %d, %Y')
    }

def get_bmi_category_info(bmi: float) -> Dict[str, str]:
    """Get BMI category information with health recommendations."""
    if bmi < 18.5:
        return {
            'category': 'Underweight',
            'color': 'info',
            'description': 'Below normal weight range',
            'recommendation': 'Consider consulting a healthcare provider about healthy weight gain.',
            'range': 'Below 18.5'
        }
    elif 18.5 <= bmi < 25:
        return {
            'category': 'Normal weight',
            'color': 'success',
            'description': 'Within healthy weight range',
            'recommendation': 'Maintain your current lifestyle with balanced diet and regular exercise.',
            'range': '18.5 - 24.9'
        }
    elif 25 <= bmi < 30:
        return {
            'category': 'Overweight',
            'color': 'warning',
            'description': 'Above normal weight range',
            'recommendation': 'Consider a balanced diet and increased physical activity.',
            'range': '25.0 - 29.9'
        }
    else:
        return {
            'category': 'Obese',
            'color': 'danger',
            'description': 'Significantly above normal weight range',
            'recommendation': 'Consult a healthcare provider for personalized weight management advice.',
            'range': '30.0 and above'
        }

def calculate_gpa(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate GPA from list of grade entries."""
    if not entries:
        raise ValueError("No entries provided")
    
    grade_points = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }
    
    total_quality_points = 0
    total_credit_hours = 0
    grade_distribution = {}
    
    for entry in entries:
        grade = entry['grade']
        credit_hours = float(entry['credit_hours'])
        points = grade_points.get(grade, 0.0)
        
        total_quality_points += points * credit_hours
        total_credit_hours += credit_hours
        
        # Track grade distribution
        if grade in grade_distribution:
            grade_distribution[grade] += credit_hours
        else:
            grade_distribution[grade] = credit_hours
    
    if total_credit_hours == 0:
        raise ValueError("Total credit hours cannot be zero")
    
    gpa = total_quality_points / total_credit_hours
    
    # Determine GPA category
    if gpa >= 3.7:
        category = 'Excellent'
        color = 'success'
    elif gpa >= 3.0:
        category = 'Good'
        color = 'info'
    elif gpa >= 2.0:
        category = 'Satisfactory'
        color = 'warning'
    else:
        category = 'Needs Improvement'
        color = 'danger'
    
    return {
        'gpa': round(gpa, 2),
        'total_credit_hours': total_credit_hours,
        'total_quality_points': round(total_quality_points, 1),
        'category': category,
        'color': color,
        'grade_distribution': grade_distribution,
        'entries': entries,
        'percentage': round(gpa * 25, 1) if gpa <= 4.0 else 100  # Convert to percentage
    }
    
    
# Add to your existing utils.py file

def calculate_loan_payment(principal, annual_rate, years, payment_frequency=12):
    """Calculate loan payment with comprehensive details."""
    try:
        principal = float(principal)
        annual_rate = float(annual_rate) / 100  # Convert percentage to decimal
        years = float(years)
        payment_frequency = int(payment_frequency)
        
        if principal <= 0 or annual_rate < 0 or years <= 0:
            raise ValueError("Invalid input values")
        
        # Calculate payment details
        total_payments = years * payment_frequency
        periodic_rate = annual_rate / payment_frequency if annual_rate > 0 else 0
        
        if annual_rate == 0:
            # No interest loan
            payment = principal / total_payments
            total_amount = principal
            total_interest = 0
        else:
            # Standard loan calculation
            payment = (principal * periodic_rate * (1 + periodic_rate)**total_payments) / \
                     ((1 + periodic_rate)**total_payments - 1)
            total_amount = payment * total_payments
            total_interest = total_amount - principal
        
        # Create amortization schedule (first 12 payments for display)
        schedule = []
        remaining_balance = principal
        
        for i in range(min(12, int(total_payments))):
            interest_payment = remaining_balance * periodic_rate
            principal_payment = payment - interest_payment
            remaining_balance -= principal_payment
            
            schedule.append({
                'payment_number': i + 1,
                'payment_amount': round(payment, 2),
                'principal_payment': round(principal_payment, 2),
                'interest_payment': round(interest_payment, 2),
                'remaining_balance': round(max(0, remaining_balance), 2)
            })
        
        # Calculate summary statistics
        monthly_payment = payment if payment_frequency == 12 else payment * payment_frequency / 12
        debt_to_income_ratio = (monthly_payment * 12) / (principal * 0.1) * 100  # Assuming 10% income ratio
        
        return {
            'payment_amount': round(payment, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2),
            'total_payments': int(total_payments),
            'monthly_payment': round(monthly_payment, 2),
            'principal': round(principal, 2),
            'annual_rate': round(annual_rate * 100, 2),
            'years': years,
            'payment_frequency': payment_frequency,
            'amortization_schedule': schedule,
            'interest_percentage': round((total_interest / principal) * 100, 1) if principal > 0 else 0,
            'payment_frequency_text': {
                12: 'Monthly',
                26: 'Bi-weekly',
                52: 'Weekly',
                4: 'Quarterly',
                1: 'Annual'
            }.get(payment_frequency, 'Custom')
        }
        
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError("Invalid calculation parameters")

def get_loan_recommendations(loan_amount, credit_score=None):
    """Get loan recommendations based on amount and credit score."""
    recommendations = []
    
    if loan_amount <= 50000:
        recommendations.append({
            'type': 'Personal Loan',
            'description': 'Best for debt consolidation, home improvements, or major purchases',
            'typical_rate': '6-36%',
            'term': '2-7 years'
        })
    
    if loan_amount >= 100000:
        recommendations.append({
            'type': 'Home Equity Loan',
            'description': 'Use your home equity for large expenses with potentially lower rates',
            'typical_rate': '3-12%',
            'term': '5-30 years'
        })
    
    if loan_amount >= 200000:
        recommendations.append({
            'type': 'Mortgage Loan',
            'description': 'Perfect for home purchases with long-term repayment options',
            'typical_rate': '3-8%',
            'term': '15-30 years'
        })
    
    recommendations.append({
        'type': 'Credit Card',
        'description': 'For smaller amounts or short-term financing needs',
        'typical_rate': '15-25%',
        'term': 'Revolving credit'
    })
    
    return recommendations