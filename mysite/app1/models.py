from django.db import models
from django.urls import reverse

#Testing new stuff here!
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
        
    def __str__(self):
        return self.first_name+" "+self.last_name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this employee."""
        return reverse('employee-detail', args=[str(self.id)])
