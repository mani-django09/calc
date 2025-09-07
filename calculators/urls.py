from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    
    path('calculator/<slug:slug>/', views.calculator_detail, name='calculator_detail'),
    # Direct calculator URLs for backward compatibility
    path('age-calculator/', views.age_calculator, name='age_calculator'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('gpa-calculator/', views.gpa_calculator, name='gpa_calculator'),
    # Add this to your urlpatterns
    path('calorie-calculator/', views.calorie_calculator, name='calorie_calculator'),
    # Add this to your urlpatterns
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