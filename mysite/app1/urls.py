from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/', views.EmployeeListView.as_view(), name='employees'),
    path('add_new/', views.add_new, name='add_new'),
    path('calculate/', views.calculate, name='calculate'),
    path('results/', views.results, name='results'),
    path('added/', views.added, name='added'),
    path('dependents/', views.add_dependents, name='dependents'),
    path('employee_search/', views.employee_search, name='employee_search'),
    path('delete_dependent/', views.delete_dependent, name='delete_dependent'),
    path('help/', views.help, name='help'),
]
