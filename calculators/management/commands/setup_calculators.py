from django.core.management.base import BaseCommand
from calculators.models import Calculator, HomepageContent, Feature

class Command(BaseCommand):
    help = 'Set up initial calculator data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up calculators...')
        
        # Create calculators
        calculators_data = [
            {
                'slug': 'age-calculator',
                'name': 'Age Calculator',
                'description': 'Calculate your exact age in years, months, and days',
                'detailed_description': 'Our age calculator helps you find your exact age down to the day. Simply enter your birth date and get detailed information about your age including years, months, days, and total days lived.',
                'icon': '🎂',
                'is_active': True,
                'featured': True,
                'order': 1,
                'meta_title': 'Age Calculator - Calculate Your Exact Age Online',
                'meta_description': 'Free online age calculator to find your exact age in years, months, days, and more. Fast and accurate results.',
                'meta_keywords': 'age calculator, calculate age, birth date, exact age'
            },
            {
                'slug': 'bmi-calculator',
                'name': 'BMI Calculator',
                'description': 'Calculate your Body Mass Index and health category',
                'detailed_description': 'Calculate your Body Mass Index (BMI) to determine if you are underweight, normal weight, overweight, or obese. Supports both metric and imperial units.',
                'icon': '⚖️',
                'is_active': True,
                'featured': True,
                'order': 2,
                'meta_title': 'BMI Calculator - Body Mass Index Calculator Online',
                'meta_description': 'Calculate your BMI (Body Mass Index) with our free online calculator. Supports metric and imperial units.',
                'meta_keywords': 'BMI calculator, body mass index, health calculator, weight calculator'
            },
            {
                'slug': 'gpa-calculator',
                'name': 'GPA Calculator',
                'description': 'Calculate your Grade Point Average from your grades and credit hours',
                'detailed_description': 'Calculate your cumulative Grade Point Average (GPA) by entering your course grades and credit hours. Supports standard 4.0 grading scale.',
                'icon': '🎓',
                'is_active': True,
                'featured': True,
                'order': 3,
                'meta_title': 'GPA Calculator - Calculate Your Grade Point Average',
                'meta_description': 'Free online GPA calculator to calculate your Grade Point Average. Enter grades and credit hours for accurate results.',
                'meta_keywords': 'GPA calculator, grade point average, academic calculator, college GPA'
            }
        ]

        for calc_data in calculators_data:
            calculator, created = Calculator.objects.get_or_create(
                slug=calc_data['slug'],
                defaults=calc_data
            )
            if created:
                self.stdout.write(f'✅ Created calculator: {calculator.name}')
            else:
                self.stdout.write(f'⏭️  Calculator already exists: {calculator.name}')

        # Create homepage content
        homepage_data = {
            'title': 'Calculator Hub',
            'subtitle': 'Your one-stop destination for free online calculators',
            'hero_text': 'Fast, accurate, and easy-to-use calculators for all your daily needs. No registration required, completely free to use.',
            'about_section': 'Calculator Hub provides a comprehensive collection of free online calculators designed to help you with everyday calculations. Our tools are fast, accurate, and work perfectly on all devices.',
            'features_title': 'Why Choose Our Calculators?',
            'show_features': True,
            'show_statistics': True,
            'show_testimonials': False,
            'meta_title': 'Calculator Hub - Free Online Calculators',
            'meta_description': 'Free online calculators including Age Calculator, BMI Calculator, GPA Calculator and more. Fast, accurate, mobile-friendly tools.',
            'meta_keywords': 'calculator, online calculator, free tools, age calculator, BMI calculator, GPA calculator',
            'is_active': True
        }

        homepage_content, created = HomepageContent.objects.get_or_create(
            defaults=homepage_data
        )
        if created:
            self.stdout.write('✅ Created homepage content')
        else:
            self.stdout.write('⏭️  Homepage content already exists')

        # Create features
        features_data = [
            {
                'title': 'Free to Use',
                'description': 'All calculators are completely free with no hidden costs or registration required.',
                'detailed_description': 'We believe in providing free access to essential calculation tools for everyone.',
                'icon': '✅',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Mobile Friendly',
                'description': 'Works perfectly on all devices - desktop, tablet, and mobile phones.',
                'detailed_description': 'Our responsive design ensures optimal experience across all screen sizes.',
                'icon': '📱',
                'order': 2,
                'is_active': True
            },
            {
                'title': 'Secure & Private',
                'description': 'Your data is processed securely and never stored on our servers.',
                'detailed_description': 'We prioritize your privacy and security with client-side calculations.',
                'icon': '🔒',
                'order': 3,
                'is_active': True
            },
            {
                'title': 'Instant Results',
                'description': 'Get accurate calculations instantly without any delays.',
                'detailed_description': 'Our optimized algorithms provide lightning-fast results.',
                'icon': '⚡',
                'order': 4,
                'is_active': True
            },
            {
                'title': 'No Registration',
                'description': 'Start calculating immediately without creating an account.',
                'detailed_description': 'Jump right in and use any calculator without signup hassles.',
                'icon': '🚀',
                'order': 5,
                'is_active': True
            },
            {
                'title': 'Always Available',
                'description': 'Access our calculators 24/7 from anywhere in the world.',
                'detailed_description': 'Round-the-clock availability for all your calculation needs.',
                'icon': '🌍',
                'order': 6,
                'is_active': True
            }
        ]

        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(
                title=feature_data['title'],
                defaults=feature_data
            )
            if created:
                self.stdout.write(f'✅ Created feature: {feature.title}')
            else:
                self.stdout.write(f'⏭️  Feature already exists: {feature.title}')

        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully set up calculator data!')
        )
        

# Add this to your existing setup_calculators.py in the calculators_data list

{
    'slug': 'loan-calculator',
    'name': 'Loan Calculator',
    'description': 'Calculate monthly payments, total interest, and amortization schedule for any loan',
    'detailed_description': 'Our comprehensive loan calculator helps you calculate monthly payments, total interest costs, and detailed amortization schedules for mortgages, auto loans, personal loans, student loans, and business loans. Compare different loan terms and payment frequencies to find the best option for your financial needs.',
    'icon': '🏦',
    'is_active': True,
    'featured': True,
    'order': 4,
    'meta_title': 'Loan Calculator - Calculate Monthly Payments & Interest | Free Online Tool',
    'meta_description': 'Free loan calculator to calculate monthly payments, total interest, and amortization schedule. Compare loan terms, rates, and payment frequencies. Get instant results for personal loans, mortgages, auto loans, and more.',
    'meta_keywords': 'loan calculator, monthly payment calculator, mortgage calculator, auto loan calculator, personal loan calculator, loan payment, interest calculator, amortization schedule, loan comparison, debt calculator, loan payment formula, calculate loan interest, loan repayment calculator, business loan calculator, student loan calculator'
}

# Add this to your calculators_data list in setup_calculators.py
{
    'slug': 'percentage-calculator',
    'name': 'Percentage Calculator',
    'description': 'Calculate percentages, percentage changes, discounts, tips, and more with our comprehensive percentage calculator',
    'detailed_description': 'Our advanced percentage calculator handles all types of percentage calculations including basic percentages, percentage changes, discounts, markups, tips, and bill splitting. Perfect for students, professionals, shoppers, and anyone needing quick and accurate percentage calculations.',
    'icon': '📊',
    'is_active': True,
    'featured': True,
    'order': 5,
    'meta_title': 'Percentage Calculator - Calculate Percentages, Discounts, Tips & More | Free Online Tool',
    'meta_description': 'Free percentage calculator to calculate percentages, percentage changes, discounts, markups, tips, and more. Instant results with detailed breakdowns. Works on all devices.',
    'meta_keywords': 'percentage calculator, calculate percentage, percentage change calculator, discount calculator, tip calculator, markup calculator, percentage of a number, how to calculate percentage, percentage increase calculator, percentage decrease calculator, online percentage calculator, free percentage calculator, percentage math, percentage formula, percentage problems, percentage solutions'
}



# Add this to your calculators_data list in setup_calculators.py
{
    'slug': 'calorie-calculator',
    'name': 'Calorie Calculator',
    'description': 'Calculate your daily calorie needs based on age, gender, height, weight, and activity level for healthy weight management',
    'detailed_description': 'Our evidence-based calorie calculator helps you determine your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the scientifically validated Mifflin-St Jeor equation. Get personalized calorie recommendations for weight loss, weight gain, or weight maintenance with a focus on healthy, sustainable approaches.',
    'icon': '🔥',
    'is_active': True,
    'featured': True,
    'order': 6,
    'meta_title': 'Calorie Calculator - Calculate Daily Calorie Needs for Weight Management | Free Tool',
    'meta_description': 'Free calorie calculator to determine your daily calorie requirements based on age, gender, height, weight, and activity level. Get personalized recommendations for healthy weight management, weight loss, and weight gain goals.',
    'meta_keywords': 'calorie calculator, daily calorie needs, BMR calculator, TDEE calculator, weight loss calculator, weight management, calories per day, metabolic rate calculator, calorie requirements, healthy weight loss, calorie deficit calculator, maintenance calories, nutrition calculator, fitness calculator'
}