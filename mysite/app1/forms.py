from django import forms
from .models import Company, Employee, Dependent
from django.forms.models import modelformset_factory
from django.forms import ModelForm

#Form for quick calculation
class CalcForm(forms.Form):
    emp_salary = forms.CharField(label='Salary')
    base_deduction = forms.CharField(label='Base Deduction')
    dependents = forms.CharField(label='Dependents')
    per_dependent = forms.CharField(label='Deduction/Dependent')
    discount = forms.CharField(label='Discount Percentage')

#Form for adding new employees
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'salary']


class DependentForm(ModelForm):
    class Meta:
        model = Dependent
        fields = ['f_name', 'l_name', 'age']

class SearchForm(forms.Form):
    full_name = forms.CharField(label ='Full Name')




