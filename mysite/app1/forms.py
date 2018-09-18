from django import forms
from .models import Company, Employee, Dependent
from django.forms import ModelForm

#Form for quick calculation
class CalcForm(forms.Form):
    emp_salary = forms.CharField(label='Salary')
    base_deduction = forms.CharField(label='Employee Cost')
    dependents = forms.CharField(label='Number of Dependents')
    dependent_deduction = forms.CharField(label= 'Dependent Cost')
    discount = forms.CharField(label='Discount Percentage')
    num_eligible = forms.CharField(label ='Discount eligible dependents')
    co_pays = forms.CharField(label ='Percentage Paid by Employer')
    emp_eligible = forms.BooleanField(label= 'Employee eligible for discount?', required=False)


#Form for adding new employees
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        labels ={
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'salary': 'Annual Salary',
        }
        fields = ['first_name', 'last_name', 'salary']


#Form for modifying employee info
class EmployeeMod(ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name', 'salary']


#Add dependents
class DependentForm(ModelForm):
    class Meta:
        model = Dependent
        labels = {
            'f_name': 'First Name',
            'l_name': 'Last Name',
            'birth_date': 'Birth Date (mm/dd/yyyy)',
        }
        fields = ['f_name', 'l_name', 'birth_date']


#Search database for employee
class SearchForm(forms.Form):
    full_name = forms.CharField(label ='Full Name')

