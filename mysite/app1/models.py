from django.db import models
from django.urls import reverse


class Company(models.Model):
    #might need to be explicit with pk?
    base_salary = models.DecimalField(max_digits=9, decimal_places=2)
    emp_deduct = models.DecimalField(max_digits=6, decimal_places=2)
    dep_deduct = models.DecimalField(max_digits=6, decimal_places=2)
    std_deduct = models.BooleanField(default=True)
    company_name = models.CharField(max_length=30)
    def __str__(self):
        return self.company_name

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    dependents = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name+" "+self.last_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this employee."""
        return reverse('employee-detail', args=[str(self.id)])

class Dependent(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    def __str__(self):
        return self.f_name +' '+ self.l_name


