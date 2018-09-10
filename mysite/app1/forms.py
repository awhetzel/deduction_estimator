from django import forms
from .models import Company, Employee, Dependent
from django.forms.models import modelformset_factory

class CalcForm(forms.Form):
    emp_salary = forms.CharField(label='Salary')
    base_deduction = forms.CharField(label='Base Deduction')
    dependents = forms.CharField(label='Dependents')
    per_dependent = forms.CharField(label='Deduction/Dependent')
    discount = forms.CharField(label='Discount Percentage')




#DependentFormSet = modelformset_factory(Dependent, exclude=(), extra=1)



