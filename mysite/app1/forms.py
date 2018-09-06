from django import forms
from .models import Company

class CalcForm(forms.Form):
    emp_salary = forms.DecimalField(label='Salary')
    base_deduction = forms.CharField(label='Base Deduction')
    dependents = forms.IntegerField(label='Dependents')
    per_dependent = forms.DecimalField(label='Deduction/Dependent')
    discount = forms.DecimalField(label='Discount Percentage')


