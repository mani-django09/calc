from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    
    path('calculator/<slug:slug>/', views.calculator_detail, name='calculator_detail'),
    path('citation-generator/', views.citation_generator, name='citation_generator'),
    path('age-calculator/', views.age_calculator, name='age_calculator'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('bmr-calculator/', views.bmr_calculator, name='bmr_calculator'),
    path('mortgage-calculator/', views.mortgage_calculator, name='mortgage_calculator'),
    path('date-of-birth-calculator/', views.date_of_birth_calculator, name='date_of_birth_calculator'),
    path('calculator/date-of-birth-calculator/', views.calculator_detail, {'slug': 'date-of-birth-calculator'}, name='date_of_birth_calculator_detail'),
    path('grade-calculator/', views.grade_calculator, name='grade_calculator'),
    path('calculator/grade-calculator/', views.calculator_detail, {'slug': 'grade-calculator'}, name='grade_calculator_detail'),
    path('gpa-calculator/', views.gpa_calculator, name='gpa_calculator'),
    path('pregnancy-calculator/', views.pregnancy_calculator, name='pregnancy_calculator'),
    path('calculator/pregnancy-calculator/', views.calculator_detail, {'slug': 'pregnancy-calculator'}, name='pregnancy_calculator_detail'),    path('calorie-calculator/', views.calorie_calculator, name='calorie_calculator'),
    path('401k-calculator/', views.k401_calculator, name='401k_calculator'),
    path('calculator/401k-calculator/', views.calculator_detail, {'slug': '401k-calculator'}, name='401k_calculator_detail'),
    path('percentage-calculator/', views.percentage_calculator, name='percentage_calculator'),
    path('loan-calculator/', views.loan_calculator, name='loan_calculator'),
    path('calculator/loan-calculator/', views.calculator_detail, {'slug': 'loan-calculator'}, name='loan_calculator_detail'),
    # AJAX endpoints
    path('ajax/add-gpa-row/', views.add_gpa_row, name='add_gpa_row'),
    
        # Static pages
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('sitemap/', views.sitemap_page, name='sitemap_page'),
    
    
]