from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Employee
from django.shortcuts import get_object_or_404
from .forms import CalcForm

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

#def calculate(request):
#    return render(request, 'calculate.html')

def calculate(request):
    calc_form = CalcForm()

    return render(request, 'calculate.html', {'calc_form': calc_form})

def results(request):

    salary = float(request.POST['emp_salary'])

    dep = request.POST['dependents']


    deduction = 1000+(500* int(dep))

    after_deduction = float(salary)-deduction



    context = {
        'salary': '${:,.2f}'.format(salary),
        'dep': dep,
        'deduction': '${:,.2f}'.format(deduction),
        'after_deduction': '${:,.2f}'.format(after_deduction),
    }



    return render(request, 'results.html', context)


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


