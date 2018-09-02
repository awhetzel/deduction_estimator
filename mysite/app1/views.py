from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Employee
from django.shortcuts import get_object_or_404


def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


def login(request):
    return render(request, 'login.html')

#new stuff
def add_new(request):
    return render(request, 'add_new.html')


#new stuff

class EmployeeListView(LoginRequiredMixin, generic.ListView):
    #Keeps people from accessing this page with the url
    #redirects to login page if they try
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Employee
    #this forces pagination, 10 employees per page
    paginate_by = 10

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Employee
    

