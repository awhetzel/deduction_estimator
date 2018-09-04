from django import forms

class CalcForm(forms.Form):
    emp_salary = forms.DecimalField(label='Salary')
    dependents = forms.IntegerField(label='Dependents')

