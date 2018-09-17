from django.db import models
from django.urls import reverse
from datetime import datetime
from decimal import Decimal

class Company(models.Model):
    base_salary = models.DecimalField(max_digits=9, decimal_places=2)
    #Standard deduction for employees
    emp_deduct = models.DecimalField(max_digits=6, decimal_places=2)
    #Standard deduction for dependents
    dep_deduct = models.DecimalField(max_digits=6, decimal_places=2)
    company_name = models.CharField(max_length=30)
    #Character code for discount policy
    discount_policy = models.CharField(max_length=1)
    #Discount percentage for qualifying employees/dependents
    discount_percentage = models.DecimalField(default=0,max_digits=6, decimal_places=2)
    #Percentage that company pays for benefits
    contribution_percent = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    salary = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.first_name+" "+self.last_name

    def get_absolute_url(self):
        #Returns the url to access a detail record for this employee.
        return reverse('employee-detail', args=[str(self.id)])

    class Meta:
         unique_together = ('first_name', 'last_name',)


class Dependent(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    birth_date = models.DateField()

    def get_deduction(self, company):
        discount_per = Decimal(0)
        deduction = company.dep_deduct
        #check for discount
        if company.discount_policy.lower() == self.f_name[0].lower():
            discount_per = company.discount_percentage
        discount = ((discount_per/100)*deduction)
        deduction = deduction -discount

        return deduction

    def __str__(self):
        return self.f_name +' '+ self.l_name


