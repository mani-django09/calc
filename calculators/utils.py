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

# Add these functions to your utils.py file

def calculate_401k(current_age, retirement_age, current_balance, annual_salary, 
                   contribution_rate, employer_match, return_rate):
    """
    Calculate 401k retirement savings with year-by-year breakdown.
    
    Args:
        current_age: Current age (18-100)
        retirement_age: Age planning to retire (50-80)
        current_balance: Current 401k balance (can be 0)
        annual_salary: Annual salary before taxes
        contribution_rate: Percentage of salary contributed (0-100)
        employer_match: Percentage employer matches (0-100)
        return_rate: Expected annual return rate (0-20)
    
    Returns:
        Dictionary with retirement projections and yearly breakdown
    """
    try:
        # Convert inputs
        current_age = int(current_age)
        retirement_age = int(retirement_age)
        current_balance = float(current_balance) if current_balance else 0
        annual_salary = float(annual_salary)
        contribution_rate = float(contribution_rate) / 100
        employer_match = float(employer_match) / 100
        return_rate = float(return_rate) / 100
        
        # Validation
        if current_age >= retirement_age:
            raise ValueError("Retirement age must be greater than current age")
        
        if current_age < 18 or current_age > 100:
            raise ValueError("Current age must be between 18 and 100")
        
        if retirement_age < 50 or retirement_age > 80:
            raise ValueError("Retirement age must be between 50 and 80")
        
        if annual_salary < 1000 or annual_salary > 10000000:
            raise ValueError("Annual salary must be between $1,000 and $10,000,000")
        
        # Calculate annual contributions
        annual_contribution = annual_salary * contribution_rate
        annual_employer_match = annual_salary * employer_match
        annual_total_contribution = annual_contribution + annual_employer_match
        
        # Calculate year by year
        years_to_retirement = retirement_age - current_age
        balance = current_balance
        
        total_personal_contributions = 0
        total_employer_contributions = 0
        total_investment_growth = 0
        
        yearly_breakdown = []
        
        for year in range(years_to_retirement):
            age = current_age + year + 1
            
            # Add contributions
            personal_contrib = annual_contribution
            employer_contrib = annual_employer_match
            
            # Calculate interest on current balance plus contributions
            # Assumes contributions happen throughout the year (average)
            interest_earned = (balance + (personal_contrib + employer_contrib) / 2) * return_rate
            
            # Update balance
            balance += personal_contrib + employer_contrib + interest_earned
            
            # Track totals
            total_personal_contributions += personal_contrib
            total_employer_contributions += employer_contrib
            total_investment_growth += interest_earned
            
            # Store first 10 years for display
            if year < 10:
                yearly_breakdown.append({
                    'age': age,
                    'contribution': personal_contrib,
                    'employer': employer_contrib,
                    'interest': interest_earned,
                    'balance': balance
                })
        
        # Calculate total investment growth
        # (subtracting initial balance that wasn't from contributions)
        total_investment_growth = balance - current_balance - total_personal_contributions - total_employer_contributions
        
        return {
            'total_at_retirement': round(balance, 2),
            'total_contributions': round(total_personal_contributions, 2),
            'employer_contributions': round(total_employer_contributions, 2),
            'investment_growth': round(total_investment_growth, 2),
            'current_balance': round(current_balance, 2),
            'years_to_retirement': years_to_retirement,
            'annual_contribution': round(annual_contribution, 2),
            'annual_employer_match': round(annual_employer_match, 2),
            'yearly_breakdown': yearly_breakdown,
            'contribution_percentage': round(contribution_rate * 100, 1),
            'employer_match_percentage': round(employer_match * 100, 1),
            'return_rate_percentage': round(return_rate * 100, 1)
        }
        
    except (ValueError, ZeroDivisionError, TypeError) as e:
        raise ValueError(f"Invalid calculation parameters: {str(e)}")
    

# Add these functions to your utils.py file

from datetime import date, timedelta
from typing import Dict, Any

def calculate_pregnancy(calc_method: str, month: int, day: int, year: int, cycle_length: int = 28) -> Dict[str, Any]:
    """
    Calculate pregnancy due date and related information.
    
    Args:
        calc_method: 'lmp', 'conception', or 'due_date'
        month: Month (1-12)
        day: Day (1-31)
        year: Year
        cycle_length: Average cycle length in days (default 28)
    
    Returns:
        Dictionary with pregnancy information
    """
    try:
        input_date = date(int(year), int(month), int(day))
        today = date.today()
        
        # Calculate due date based on method
        if calc_method == 'lmp':
            # Standard pregnancy: 280 days from LMP
            due_date = input_date + timedelta(days=280)
            conception_date = input_date + timedelta(days=14)  # Approximate
            
        elif calc_method == 'conception':
            # 266 days from conception
            due_date = input_date + timedelta(days=266)
            conception_date = input_date
            
        elif calc_method == 'due_date':
            # Working backwards from due date
            due_date = input_date
            conception_date = input_date - timedelta(days=266)
        
        else:
            raise ValueError("Invalid calculation method")
        
        # Calculate current pregnancy stats
        days_pregnant = (today - (due_date - timedelta(days=280))).days
        
        # Ensure we don't show negative days
        if days_pregnant < 0:
            days_pregnant = 0
        
        weeks_pregnant = days_pregnant // 7
        current_week = min(weeks_pregnant, 40)  # Cap at 40 weeks
        
        # Days until due date
        days_until_due = (due_date - today).days
        
        # Determine trimester
        if current_week <= 13:
            trimester = 1
            trimester_name = "First Trimester"
            trimester_info = "Your baby's organs and body systems are forming. You might experience morning sickness, fatigue, and tender breasts. This is a critical time for development."
        elif current_week <= 27:
            trimester = 2
            trimester_name = "Second Trimester"
            trimester_info = "You'll likely feel better now. Your baby is growing fast, and you'll probably start to feel movements. Your bump will become more noticeable."
        else:
            trimester = 3
            trimester_name = "Third Trimester"
            trimester_info = "Your baby is gaining weight and getting ready for birth. You might feel more uncomfortable as your due date approaches. Start preparing for your baby's arrival."
        
        # Key milestones
        milestones = [
            {
                'week': 8,
                'description': 'First ultrasound and heartbeat detection',
                'date': (conception_date + timedelta(weeks=6)).strftime('%b %d, %Y')
            },
            {
                'week': 12,
                'description': 'End of first trimester - morning sickness often improves',
                'date': (conception_date + timedelta(weeks=10)).strftime('%b %d, %Y')
            },
            {
                'week': 20,
                'description': 'Anatomy scan - you can usually find out the sex',
                'date': (conception_date + timedelta(weeks=18)).strftime('%b %d, %Y')
            },
            {
                'week': 24,
                'description': 'Viability milestone - baby could survive with medical help',
                'date': (conception_date + timedelta(weeks=22)).strftime('%b %d, %Y')
            },
            {
                'week': 28,
                'description': 'Third trimester begins',
                'date': (conception_date + timedelta(weeks=26)).strftime('%b %d, %Y')
            },
            {
                'week': 37,
                'description': 'Full term - baby is considered ready for birth',
                'date': (conception_date + timedelta(weeks=35)).strftime('%b %d, %Y')
            }
        ]
        
        # Only show upcoming milestones
        upcoming_milestones = [m for m in milestones if m['week'] > current_week][:4]
        
        return {
            'due_date': due_date,
            'due_date_formatted': due_date.strftime('%B %d, %Y'),
            'conception_date': conception_date.strftime('%B %d, %Y'),
            'days_pregnant': max(0, days_pregnant),
            'current_week': max(0, current_week),
            'days_until_due': max(0, days_until_due),
            'trimester': trimester,
            'trimester_name': trimester_name,
            'trimester_info': trimester_info,
            'milestones': upcoming_milestones,
            'weeks_remaining': max(0, 40 - current_week),
            'percent_complete': min(100, round((current_week / 40) * 100, 1))
        }
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid date or calculation parameters: {str(e)}")
    
def calculate_bmr(age, gender, height, height_unit, weight, weight_unit):
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation.
    
    Args:
        age: Age in years
        gender: 'male' or 'female'
        height: Height value
        height_unit: 'cm' or 'inches'
        weight: Weight value
        weight_unit: 'kg' or 'lbs'
    
    Returns:
        Dictionary with BMR and activity level calorie calculations
    """
    try:
        age = int(age)
        height = float(height)
        weight = float(weight)
        
        # Convert to metric
        if height_unit == 'inches':
            height = height * 2.54  # Convert to cm
        
        if weight_unit == 'lbs':
            weight = weight * 0.453592  # Convert to kg
        
        # Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        # Calculate TDEE for different activity levels
        activity_levels = [
            {
                'name': 'Sedentary',
                'description': 'Little to no exercise, desk job',
                'multiplier': 1.2,
                'calories': round(bmr * 1.2, 0)
            },
            {
                'name': 'Lightly Active',
                'description': 'Light exercise 1-3 days/week',
                'multiplier': 1.375,
                'calories': round(bmr * 1.375, 0)
            },
            {
                'name': 'Moderately Active',
                'description': 'Moderate exercise 3-5 days/week',
                'multiplier': 1.55,
                'calories': round(bmr * 1.55, 0)
            },
            {
                'name': 'Very Active',
                'description': 'Hard exercise 6-7 days/week',
                'multiplier': 1.725,
                'calories': round(bmr * 1.725, 0)
            },
            {
                'name': 'Extra Active',
                'description': 'Very hard exercise, physical job',
                'multiplier': 1.9,
                'calories': round(bmr * 1.9, 0)
            }
        ]
        
        return {
            'bmr': round(bmr, 1),
            'weekly_bmr': round(bmr * 7, 0),
            'activity_levels': activity_levels,
            'age': age,
            'gender': gender,
            'height_cm': round(height, 1),
            'weight_kg': round(weight, 1)
        }
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculation parameters: {str(e)}")
    
from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_mortgage(home_price, down_payment, interest_rate, loan_term, 
                       property_tax=0, home_insurance=0, hoa_fees=0):
    """
    Calculate mortgage payments with full breakdown.
    """
    try:
        home_price = float(home_price)
        down_payment = float(down_payment)
        interest_rate = float(interest_rate) / 100
        loan_term = int(loan_term)
        property_tax = float(property_tax) if property_tax else 0
        home_insurance = float(home_insurance) if home_insurance else 0
        hoa_fees = float(hoa_fees) if hoa_fees else 0
        
        # Calculate loan amount
        loan_amount = home_price - down_payment
        down_payment_percent = (down_payment / home_price) * 100
        
        # Calculate monthly payment (P&I)
        monthly_rate = interest_rate / 12
        num_payments = loan_term * 12
        
        if interest_rate == 0:
            principal_interest = loan_amount / num_payments
        else:
            principal_interest = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                                ((1 + monthly_rate)**num_payments - 1)
        
        # Calculate PMI if down payment < 20%
        monthly_pmi = 0
        has_pmi = False
        if down_payment_percent < 20:
            has_pmi = True
            annual_pmi = loan_amount * 0.01  # 1% of loan amount
            monthly_pmi = annual_pmi / 12
        
        # Monthly extras
        monthly_tax = property_tax / 12 if property_tax else 0
        monthly_insurance = home_insurance / 12 if home_insurance else 0
        
        # Total monthly payment
        total_monthly = principal_interest + monthly_tax + monthly_insurance + monthly_pmi + hoa_fees
        
        # Calculate totals
        total_paid = principal_interest * num_payments
        total_interest = total_paid - loan_amount
        
        # Payoff date
        payoff_date = date.today() + relativedelta(years=loan_term)
        
        # Amortization schedule (first 12 months)
        schedule = []
        balance = loan_amount
        
        for month in range(1, min(13, num_payments + 1)):
            interest_payment = balance * monthly_rate
            principal_payment = principal_interest - interest_payment
            balance -= principal_payment
            
            schedule.append({
                'month': month,
                'payment': principal_interest,
                'principal': principal_payment,
                'interest': interest_payment,
                'balance': balance
            })
        
        return {
            'total_monthly': round(total_monthly, 2),
            'principal_interest': round(principal_interest, 2),
            'loan_amount': round(loan_amount, 2),
            'total_interest': round(total_interest, 2),
            'total_paid': round(total_paid, 2),
            'monthly_tax': round(monthly_tax, 2) if monthly_tax else None,
            'monthly_insurance': round(monthly_insurance, 2) if monthly_insurance else None,
            'monthly_pmi': round(monthly_pmi, 2) if monthly_pmi else None,
            'has_pmi': has_pmi,
            'hoa_fees': round(hoa_fees, 2) if hoa_fees else None,
            'payoff_date': payoff_date.strftime('%B %Y'),
            'loan_term': loan_term,
            'down_payment_percent': round(down_payment_percent, 1),
            'amortization_schedule': schedule
        }
        
    except (ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid mortgage calculation parameters: {str(e)}")


# Add these functions to your utils.py file

def calculate_final_grade(assignments: list) -> dict:
    """
    Calculate final grade from weighted assignments.
    
    Args:
        assignments: List of dicts with 'name', 'score', 'max_points', 'weight'
    
    Returns:
        Dictionary with grade calculations
    """
    try:
        total_weight = 0
        weighted_score = 0
        category_breakdown = {}
        
        for assignment in assignments:
            score = float(assignment['score'])
            max_points = float(assignment['max_points'])
            weight = float(assignment['weight'])
            category = assignment.get('category', 'Assignment')
            
            if max_points <= 0:
                raise ValueError("Max points must be greater than 0")
            
            if score < 0 or score > max_points:
                raise ValueError(f"Score must be between 0 and {max_points}")
            
            # Calculate percentage for this assignment
            percentage = (score / max_points) * 100
            
            # Add to weighted score
            weighted_score += percentage * (weight / 100)
            total_weight += weight
            
            # Track by category
            if category not in category_breakdown:
                category_breakdown[category] = {
                    'score': 0,
                    'max': 0,
                    'weight': 0,
                    'count': 0
                }
            
            category_breakdown[category]['score'] += score
            category_breakdown[category]['max'] += max_points
            category_breakdown[category]['weight'] += weight
            category_breakdown[category]['count'] += 1
        
        if total_weight == 0:
            raise ValueError("Total weight cannot be zero")
        
        # Calculate final grade
        final_grade = weighted_score
        
        # Determine letter grade
        if final_grade >= 97:
            letter = 'A+'
        elif final_grade >= 93:
            letter = 'A'
        elif final_grade >= 90:
            letter = 'A-'
        elif final_grade >= 87:
            letter = 'B+'
        elif final_grade >= 83:
            letter = 'B'
        elif final_grade >= 80:
            letter = 'B-'
        elif final_grade >= 77:
            letter = 'C+'
        elif final_grade >= 73:
            letter = 'C'
        elif final_grade >= 70:
            letter = 'C-'
        elif final_grade >= 67:
            letter = 'D+'
        elif final_grade >= 63:
            letter = 'D'
        elif final_grade >= 60:
            letter = 'D-'
        else:
            letter = 'F'
        
        # Calculate category percentages
        for category, data in category_breakdown.items():
            if data['max'] > 0:
                data['percentage'] = round((data['score'] / data['max']) * 100, 2)
        
        return {
            'final_grade': round(final_grade, 2),
            'letter_grade': letter,
            'total_weight': round(total_weight, 1),
            'category_breakdown': category_breakdown,
            'assignments': assignments,
            'passing': final_grade >= 60
        }
        
    except (ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid calculation parameters: {str(e)}")


def calculate_needed_grade(current_grade: float, desired_grade: float, 
                          final_weight: float) -> dict:
    """
    Calculate what grade is needed on final exam to achieve desired grade.
    
    Args:
        current_grade: Current grade percentage
        desired_grade: Desired final grade percentage
        final_weight: Weight of final exam (as percentage)
    
    Returns:
        Dictionary with needed grade calculation
    """
    try:
        current_grade = float(current_grade)
        desired_grade = float(desired_grade)
        final_weight = float(final_weight)
        
        if final_weight <= 0 or final_weight > 100:
            raise ValueError("Final exam weight must be between 0 and 100")
        
        # Calculate current weight
        current_weight = 100 - final_weight
        
        # Calculate needed grade
        # Formula: (desired - (current * current_weight/100)) / (final_weight/100)
        needed = (desired_grade - (current_grade * current_weight / 100)) / (final_weight / 100)
        
        # Determine feasibility
        is_possible = needed <= 100
        is_easy = needed < 70
        is_moderate = 70 <= needed < 85
        is_difficult = 85 <= needed <= 100
        is_impossible = needed > 100
        
        difficulty = 'Easy' if is_easy else 'Moderate' if is_moderate else 'Difficult' if is_difficult else 'Impossible'
        
        return {
            'needed_grade': round(needed, 2),
            'current_grade': round(current_grade, 2),
            'desired_grade': round(desired_grade, 2),
            'final_weight': round(final_weight, 1),
            'current_weight': round(current_weight, 1),
            'is_possible': is_possible,
            'difficulty': difficulty,
            'difference': round(needed - current_grade, 2)
        }
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculation parameters: {str(e)}")


def calculate_semester_grade(course_grades: list) -> dict:
    """
    Calculate semester GPA and average from multiple courses.
    
    Args:
        course_grades: List of dicts with 'course_name', 'grade', 'credits'
    
    Returns:
        Dictionary with semester calculations
    """
    try:
        grade_points_map = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        
        total_points = 0
        total_credits = 0
        total_percentage = 0
        course_count = 0
        
        for course in course_grades:
            credits = float(course['credits'])
            
            # Handle both letter grades and percentages
            if isinstance(course['grade'], str):
                # Letter grade
                grade = course['grade'].upper()
                if grade not in grade_points_map:
                    raise ValueError(f"Invalid letter grade: {grade}")
                points = grade_points_map[grade]
                percentage = points * 25  # Approximate percentage
            else:
                # Percentage grade
                percentage = float(course['grade'])
                if percentage < 0 or percentage > 100:
                    raise ValueError("Grade percentage must be between 0 and 100")
                points = percentage / 25  # Convert to 4.0 scale
            
            total_points += points * credits
            total_credits += credits
            total_percentage += percentage
            course_count += 1
        
        if total_credits == 0:
            raise ValueError("Total credits cannot be zero")
        
        semester_gpa = total_points / total_credits
        average_percentage = total_percentage / course_count
        
        # Determine semester standing
        if semester_gpa >= 3.7:
            standing = 'Dean\'s List'
        elif semester_gpa >= 3.0:
            standing = 'Good Standing'
        elif semester_gpa >= 2.0:
            standing = 'Satisfactory'
        else:
            standing = 'Academic Warning'
        
        return {
            'semester_gpa': round(semester_gpa, 2),
            'average_percentage': round(average_percentage, 1),
            'total_credits': total_credits,
            'course_count': course_count,
            'standing': standing,
            'courses': course_grades
        }
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculation parameters: {str(e)}")
