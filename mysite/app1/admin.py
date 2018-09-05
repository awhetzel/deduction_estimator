from django.contrib import admin
from .models import Company
from .models import Employee

admin.site.register(Company)
admin.site.register(Employee)
