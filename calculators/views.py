from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg
from datetime import date, datetime
import uuid
import json
from .forms import AgeCalculatorForm, BMICalculatorForm, GPAFormSet
from .models import Calculator, HomepageContent, Feature, Testimonial, SEOContent
from .utils import calculate_age_detailed, get_bmi_category_info, calculate_gpa

def home(request):
    # Get dynamic homepage content
    homepage_content = HomepageContent.objects.filter(is_active=True).first()
    if not homepage_content:
        homepage_content = HomepageContent(
            title="Calculator Hub",
            subtitle="Your one-stop destination for free online calculators",
            show_features=True
        )

    # Get active calculators
    calculators = Calculator.objects.filter(is_active=True).order_by('order', 'name')
    featured_calculators = calculators.filter(featured=True)[:3]
    
    # Get features if enabled
    features = []
    if homepage_content.show_features:
        features = Feature.objects.filter(is_active=True).order_by('order')

    # Get testimonials
    testimonials = []
    if homepage_content.show_testimonials:
        testimonials = Testimonial.objects.filter(is_active=True)[:3]

    # Calculate statistics
    total_calculators = calculators.count()
    total_calculations = sum(calc.usage_count for calc in calculators)
    
    # Get SEO content
    seo_content = SEOContent.objects.filter(page_name='homepage', is_active=True).first()

    context = {
        'homepage_content': homepage_content,
        'calculators': calculators,
        'featured_calculators': featured_calculators,
        'features': features,
        'testimonials': testimonials,
        'seo_content': seo_content,
        'statistics': {
            'total_calculators': total_calculators,
            'total_calculations': total_calculations,
            'user_satisfaction': 98,
            'years_active': 1
        },
        'page_title': (seo_content.title if seo_content else homepage_content.meta_title) or homepage_content.title,
        'meta_description': (seo_content.description if seo_content else homepage_content.meta_description) or homepage_content.subtitle,
        'meta_keywords': (seo_content.keywords if seo_content else homepage_content.meta_keywords) or 'calculator, online calculator, free tools'
    }
    
    return render(request, 'calculators/home.html', context)

def calculator_detail(request, slug):
    calculator = get_object_or_404(Calculator, slug=slug, is_active=True)
    
    # Increment usage count
    calculator.increment_usage()
    
    # Route to specific calculator logic
    if slug == 'age-calculator':
        return age_calculator(request, calculator)
    elif slug == 'bmi-calculator':
        return bmi_calculator(request, calculator)
    elif slug == 'gpa-calculator':
        return gpa_calculator(request, calculator)
    else:
        # Generic calculator handler (for future calculators)
        return render(request, 'calculators/generic_calculator.html', {
            'calculator': calculator,
            'page_title': calculator.meta_title or f"{calculator.name} - Calculator Hub",
            'meta_description': calculator.meta_description or calculator.description
        })

def age_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='age-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="Age Calculator",
                description="Calculate your exact age in years, months, and days",
                slug="age-calculator"
            )
    
    # Handle AJAX requests for calculation
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            birth_month = int(request.POST.get('birth_month'))
            birth_day = int(request.POST.get('birth_day'))
            birth_year = int(request.POST.get('birth_year'))
            
            target_month = int(request.POST.get('target_month'))
            target_day = int(request.POST.get('target_day'))
            target_year = int(request.POST.get('target_year'))
            
            birth_date = date(birth_year, birth_month, birth_day)
            target_date = date(target_year, target_month, target_day)
            
            if birth_date > target_date:
                return JsonResponse({'error': 'Birth date cannot be after target date'})
            
            result = calculate_age_between_dates(birth_date, target_date)
            return JsonResponse({'success': True, 'result': result})
            
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': 'Invalid date values'})
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='age-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'related_calculators': related_calculators,
        'page_title': getattr(calculator, 'meta_title', None) or f"{calculator.name} - Calculator Hub",
        'meta_description': getattr(calculator, 'meta_description', None) or calculator.description,
        'meta_keywords': getattr(calculator, 'meta_keywords', None) or 'age calculator, calculate age, birth date'
    }
    
    return render(request, 'calculators/age_calculator.html', context)

def bmi_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='bmi-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="BMI Calculator",
                description="Calculate your Body Mass Index and health category",
                slug="bmi-calculator"
            )
    
    form = BMICalculatorForm()
    result = None
    
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            unit_system = form.cleaned_data['unit_system']
            
            # Convert to metric if needed
            if unit_system == 'imperial':
                weight = weight * 0.453592  # lbs to kg
                height = height * 2.54  # inches to cm
            
            # Convert height from cm to meters
            height_m = height / 100
            
            # Calculate BMI
            bmi = weight / (height_m ** 2)
            category_info = get_bmi_category_info(bmi)
            
            result = {
                'bmi': round(bmi, 1),
                'weight': form.cleaned_data['weight'],
                'height': form.cleaned_data['height'],
                'unit_system': unit_system,
                **category_info
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'result': result})
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='bmi-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'form': form,
        'result': result,
        'related_calculators': related_calculators,
        'page_title': getattr(calculator, 'meta_title', None) or f"{calculator.name} - Calculator Hub",
        'meta_description': getattr(calculator, 'meta_description', None) or calculator.description,
        'meta_keywords': getattr(calculator, 'meta_keywords', None) or 'BMI calculator, body mass index, health calculator'
    }
    
    return render(request, 'calculators/bmi_calculator.html', context)

def gpa_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='gpa-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="GPA Calculator",
                description="Calculate your Grade Point Average from your grades and credit hours",
                slug="gpa-calculator"
            )
    
    session_id = request.session.get('gpa_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['gpa_session_id'] = session_id
    
    formset = GPAFormSet()
    result = None
    
    if request.method == 'POST':
        formset = GPAFormSet(request.POST)
        if formset.is_valid():
            entries = []
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    entries.append({
                        'subject_name': form.cleaned_data['subject_name'],
                        'grade': form.cleaned_data['grade'],
                        'credit_hours': form.cleaned_data['credit_hours']
                    })
            
            if entries:
                result = calculate_gpa(entries)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'result': result})
            else:
                messages.error(request, 'Please add at least one subject.')
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='gpa-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'formset': formset,
        'result': result,
        'related_calculators': related_calculators,
        'page_title': getattr(calculator, 'meta_title', None) or f"{calculator.name} - Calculator Hub",
        'meta_description': getattr(calculator, 'meta_description', None) or calculator.description,
        'meta_keywords': getattr(calculator, 'meta_keywords', None) or 'GPA calculator, grade point average, academic calculator'
    }
    
    return render(request, 'calculators/gpa_calculator.html', context)

@require_http_methods(["POST"])
def add_gpa_row(request):
    """AJAX endpoint to add new GPA row"""
    form_count = int(request.POST.get('form_count', 0))
    new_form = GPAFormSet().empty_form
    new_form.prefix = f'form-{form_count}'
    
    context = {'form': new_form, 'form_index': form_count}
    html = render(request, 'calculators/gpa_row.html', context).content.decode('utf-8')
    
    return JsonResponse({'success': True, 'html': html})

# Add this to your existing views.py

from .utils import calculate_loan_payment, get_loan_recommendations

def loan_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='loan-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="Loan Calculator",
                description="Calculate monthly payments, total interest, and amortization schedule for any loan",
                slug="loan-calculator"
            )
    
    result = None
    form_data = None
    
    if request.method == 'POST':
        try:
            loan_amount = request.POST.get('loan_amount')
            interest_rate = request.POST.get('interest_rate')
            loan_term = request.POST.get('loan_term')
            payment_frequency = request.POST.get('payment_frequency', '12')
            
            if loan_amount and interest_rate and loan_term:
                result = calculate_loan_payment(
                    principal=loan_amount,
                    annual_rate=interest_rate,
                    years=loan_term,
                    payment_frequency=payment_frequency
                )
                
                # Add loan recommendations
                result['recommendations'] = get_loan_recommendations(float(loan_amount))
                
                # Store form data
                form_data = {
                    'loan_amount': loan_amount,
                    'interest_rate': interest_rate,
                    'loan_term': loan_term,
                    'payment_frequency': payment_frequency
                }
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'result': result})
                    
        except (ValueError, TypeError) as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid input values. Please check your entries.'})
            messages.error(request, 'Invalid input values. Please check your entries.')
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='loan-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'result': result,
        'form_data': form_data,
        'related_calculators': related_calculators,
        'page_title': 'Loan Calculator - Calculate Monthly Payments & Interest | Free Online Tool',
        'meta_description': 'Free loan calculator to calculate monthly payments, total interest, and amortization schedule. Compare loan terms, rates, and payment frequencies. Get instant results for personal loans, mortgages, auto loans, and more.',
        'meta_keywords': 'loan calculator, monthly payment calculator, mortgage calculator, auto loan calculator, personal loan calculator, loan payment, interest calculator, amortization schedule, loan comparison, debt calculator'
    }
    
    return render(request, 'calculators/loan_calculator.html', context)


def percentage_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='percentage-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="Percentage Calculator",
                description="Calculate percentages, percentage changes, discounts, tips, and more",
                slug="percentage-calculator"
            )
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='percentage-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'related_calculators': related_calculators,
        'page_title': 'Percentage Calculator - Calculate Percentages, Discounts, Tips & More | Free Online Tool',
        'meta_description': 'Free percentage calculator to calculate percentages, percentage changes, discounts, markups, tips, and more. Instant results with detailed breakdowns. Works on all devices.',
        'meta_keywords': 'percentage calculator, calculate percentage, percentage change calculator, discount calculator, tip calculator, markup calculator, percentage of a number, how to calculate percentage, percentage increase calculator, percentage decrease calculator, online percentage calculator, free percentage calculator'
    }
    
    return render(request, 'calculators/percentage_calculator.html', context)


def calorie_calculator(request, calculator=None):
    if not calculator:
        try:
            calculator = Calculator.objects.get(slug='calorie-calculator')
        except Calculator.DoesNotExist:
            calculator = Calculator(
                name="Calorie Calculator",
                description="Calculate your daily calorie needs for healthy weight management",
                slug="calorie-calculator"
            )
    
    # Get related calculators
    related_calculators = Calculator.objects.filter(
        is_active=True
    ).exclude(slug='calorie-calculator')[:3]
    
    context = {
        'calculator': calculator,
        'related_calculators': related_calculators,
        'page_title': 'Calorie Calculator - Calculate Daily Calorie Needs for Weight Management | Free Tool',
        'meta_description': 'Free calorie calculator to determine your daily calorie requirements based on age, gender, height, weight, and activity level. Get personalized recommendations for healthy weight management, weight loss, and weight gain goals.',
        'meta_keywords': 'calorie calculator, daily calorie needs, BMR calculator, TDEE calculator, weight loss calculator, weight management, calories per day, metabolic rate calculator, calorie requirements, healthy weight loss, calorie deficit calculator, maintenance calories'
    }
    
    return render(request, 'calculators/calorie_calculator.html', context)


# Add these imports at the top
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Add these view functions to your existing views.py

def about_us(request):
    context = {
        'page_title': 'About Us - Calculator.net | Free Online Calculators',
        'meta_description': 'Learn about Calculator.net - your trusted source for free, accurate online calculators. Discover our mission to provide professional-grade calculation tools for everyone.',
        'meta_keywords': 'about calculator.net, online calculator company, free calculation tools, calculator website'
    }
    return render(request, 'calculators/about_us.html', context)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # Send email (configure your email settings in Django settings)
                send_mail(
                    f'Contact Form: {subject}',
                    f'From: {name} ({email})\n\nMessage:\n{message}',
                    email,
                    ['support@calculator.net'],  # Replace with your email
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
                return redirect('calculators:contact_us')
            except:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'page_title': 'Contact Us - Calculator.net | Get in Touch',
        'meta_description': 'Contact Calculator.net for support, feedback, or questions about our free online calculators. We\'re here to help with all your calculation needs.',
        'meta_keywords': 'contact calculator.net, calculator support, feedback, help, customer service'
    }
    return render(request, 'calculators/contact_us.html', context)

def privacy_policy(request):
    context = {
        'page_title': 'Privacy Policy - Calculator.net | Your Privacy Matters',
        'meta_description': 'Read Calculator.net\'s privacy policy to understand how we protect your personal information and ensure your privacy while using our free online calculators.',
        'meta_keywords': 'privacy policy, data protection, personal information, calculator privacy'
    }
    return render(request, 'calculators/privacy_policy.html', context)

def terms_conditions(request):
    context = {
        'page_title': 'Terms and Conditions - Calculator.net | Terms of Use',
        'meta_description': 'Read the terms and conditions for using Calculator.net\'s free online calculators. Understand your rights and responsibilities as a user.',
        'meta_keywords': 'terms and conditions, terms of use, calculator terms, legal information'
    }
    return render(request, 'calculators/terms_conditions.html', context)

def sitemap_page(request):
    # Get all active calculators for sitemap
    calculators = Calculator.objects.filter(is_active=True).order_by('name')
    
    context = {
        'calculators': calculators,
        'page_title': 'Sitemap - Calculator.net | Find All Our Tools',
        'meta_description': 'Navigate Calculator.net easily with our sitemap. Find all our free online calculators, tools, and pages in one convenient location.',
        'meta_keywords': 'sitemap, calculator list, navigation, website map, all calculators'
    }
    return render(request, 'calculators/sitemap.html', context)

from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from datetime import datetime

def sitemap_xml(request):
    """Generate dynamic XML sitemap"""
    
    # Static pages with their priorities and change frequencies
    static_pages = [
        {
            'loc': request.build_absolute_uri(reverse('calculators:home')),
            'changefreq': 'daily',
            'priority': '1.0',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:about_us')),
            'changefreq': 'monthly',
            'priority': '0.8',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:contact_us')),
            'changefreq': 'monthly',
            'priority': '0.7',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:privacy_policy')),
            'changefreq': 'yearly',
            'priority': '0.5',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:terms_conditions')),
            'changefreq': 'yearly',
            'priority': '0.5',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:sitemap_page')),
            'changefreq': 'monthly',
            'priority': '0.6',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        }
    ]
    
    # Calculator pages with high priority
    calculator_pages = [
        {
            'loc': request.build_absolute_uri(reverse('calculators:age_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:bmi_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:gpa_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:loan_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:percentage_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'loc': request.build_absolute_uri(reverse('calculators:calorie_calculator')),
            'changefreq': 'weekly',
            'priority': '0.9',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        }
    ]
    
    # Combine all pages
    all_pages = static_pages + calculator_pages
    
    # Load template and render XML
    template = loader.get_template('calculators/sitemap.xml')
    context = {
        'pages': all_pages,
        'domain': request.get_host()
    }
    
    xml_content = template.render(context)
    return HttpResponse(xml_content, content_type='application/xml')

def robots_txt(request):
    """Generate robots.txt file"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemap location",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
        "# Crawl-delay for politeness",
        "Crawl-delay: 1",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /ajax/",
        "Disallow: /api/",
        "",
        "# Allow all calculator pages",
        "Allow: /age-calculator/",
        "Allow: /bmi-calculator/",
        "Allow: /gpa-calculator/",
        "Allow: /loan-calculator/",
        "Allow: /percentage-calculator/",
        "Allow: /calorie-calculator/",
    ]
    
    return HttpResponse("\n".join(lines), content_type="text/plain")