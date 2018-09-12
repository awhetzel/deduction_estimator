from django.contrib import admin
from .models import Company
from .models import Employee, Dependent

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Dependent)
