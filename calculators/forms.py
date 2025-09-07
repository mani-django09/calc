from django import forms
from django.forms import formset_factory
from datetime import date
from .models import GPAEntry

class AgeCalculatorForm(forms.Form):
    birth_month = forms.ChoiceField(
        choices=[(f'{i:02d}', month) for i, month in enumerate([
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ], 1)],
        widget=forms.Select(attrs={'class': 'form-select date-select'})
    )
    
    birth_day = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 32)],
        widget=forms.Select(attrs={'class': 'form-select date-select'})
    )
    
    birth_year = forms.IntegerField(
        min_value=1900,
        max_value=2030,
        initial=2000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control date-input',
            'placeholder': '2000'
        })
    )
    
    target_month = forms.ChoiceField(
        choices=[(f'{i:02d}', month) for i, month in enumerate([
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ], 1)],
        widget=forms.Select(attrs={'class': 'form-select date-select'})
    )
    
    target_day = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 32)],
        widget=forms.Select(attrs={'class': 'form-select date-select'})
    )
    
    target_year = forms.IntegerField(
        min_value=1900,
        max_value=2100,
        initial=date.today().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control date-input',
            'placeholder': str(date.today().year)
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        try:
            birth_date = date(
                int(cleaned_data.get('birth_year')),
                int(cleaned_data.get('birth_month')),
                int(cleaned_data.get('birth_day'))
            )
            
            target_date = date(
                int(cleaned_data.get('target_year')),
                int(cleaned_data.get('target_month')),
                int(cleaned_data.get('target_day'))
            )
            
            if birth_date > target_date:
                raise forms.ValidationError("Birth date cannot be after the target date.")
                
            cleaned_data['birth_date'] = birth_date
            cleaned_data['target_date'] = target_date
            
        except (ValueError, TypeError):
            raise forms.ValidationError("Please enter valid dates.")
            
        return cleaned_data

class BMICalculatorForm(forms.Form):
    UNIT_CHOICES = [
        ('metric', 'Metric (kg/cm)'),
        ('imperial', 'Imperial (lbs/inches)')
    ]
    
    unit_system = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='metric'
    )
    
    weight = forms.FloatField(
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Weight'
        })
    )
    
    height = forms.FloatField(
        min_value=1,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Height'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        unit_system = cleaned_data.get('unit_system')
        weight = cleaned_data.get('weight')
        height = cleaned_data.get('height')

        if unit_system and weight and height:
            if unit_system == 'metric':
                if weight > 500:
                    raise forms.ValidationError("Weight seems unrealistic for metric system")
                if height > 250:
                    raise forms.ValidationError("Height seems unrealistic for metric system")
            else:  # imperial
                if weight > 1000:
                    raise forms.ValidationError("Weight seems unrealistic for imperial system")
                if height > 120:
                    raise forms.ValidationError("Height seems unrealistic for imperial system")

        return cleaned_data

class GPAEntryForm(forms.Form):
    GRADE_CHOICES = [
        ('', 'Select Grade'),
        ('A+', 'A+ (4.0)'),
        ('A', 'A (4.0)'),
        ('A-', 'A- (3.7)'),
        ('B+', 'B+ (3.3)'),
        ('B', 'B (3.0)'),
        ('B-', 'B- (2.7)'),
        ('C+', 'C+ (2.3)'),
        ('C', 'C (2.0)'),
        ('C-', 'C- (1.7)'),
        ('D+', 'D+ (1.3)'),
        ('D', 'D (1.0)'),
        ('F', 'F (0.0)'),
    ]

    subject_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject Name'
        })
    )
    
    grade = forms.ChoiceField(
        choices=GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    credit_hours = forms.FloatField(
        min_value=0.5,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.5',
            'placeholder': 'Credit Hours'
        })
    )

# Create a formset for multiple GPA entries
GPAFormSet = formset_factory(GPAEntryForm, extra=4, max_num=20)