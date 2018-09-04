from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.login, name='login'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/', views.EmployeeListView.as_view(), name='employees'),
    path('add_new/', views.add_new, name='add_new'),
    #path('calculate/', views.calculate, name='calculate'),
    path('calculate/', views.calculate, name='calculate'),
    path('results/', views.results, name='results'),
]
