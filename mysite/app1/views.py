from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Employee, Company, EmployeeForm, Dependent
from django.shortcuts import get_object_or_404
from .forms import CalcForm #, DependentFormSet
from django.forms.models import modelformset_factory


#main page: demonstrates basic use of session variables
def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)

#login function for employers
def login(request):
    return render(request, 'login.html')

#allow employers to add new employees
def add_new(request):
    #if POST request, process input
    if request.method == 'POST':
        print('METHOD WAS POST IN ADD_NEW VIEW')
        employee_form = EmployeeForm(request.POST)
        #validate form input
        if employee_form.is_valid():
            #TODO put stuff in DB here
            new_employee = employee_form.save()
            return render(request, 'added.html')
    #create blank form
    else:
        employee_form = EmployeeForm()
        return render(request, 'add_new.html', {'employee_form': employee_form})


def add_dependents(request):
    DependentFormSet = modelformset_factory(Dependent, exclude=(), extra=1)

    if request.method == 'POST':

        formset = DependentFormSet(data=request.POST)


        if formset.is_valid():
            #TODO save dependent data
            return render(request, 'dependents.html', {'formset': formset})
    else:
        formset = DependentFormSet()
        return render(request, 'dependents.html', {'formset': formset})



#Deduction calculator form page
def calculate(request):
    calc_form = CalcForm()
    return render(request, 'calculate.html', {'calc_form': calc_form})




#Deduction calculator logic, redirects to results page
def results(request):
    #this employee's salary
    salary = float(request.POST['emp_salary'])
    #number of dependents
    dep = int(request.POST['dependents'])
    #base deduction
    base_deduct= float(request.POST['base_deduction'])
    #dependent deduction
    dep_deduct = float(request.POST['per_dependent'])
    #discount
    discount = float(request.POST['discount'])
    #basic calculation
    deduction = base_deduct+(dep_deduct*dep)
    deduction -= (discount*deduction)
    #salary after deduction
    after_deduction = float(salary)-deduction
    #context to display on results page
    context = {
        'salary': '${:,.2f}'.format(salary),
        'dep': dep,
        'deduction': '${:,.2f}'.format(deduction),
        'after_deduction': '${:,.2f}'.format(after_deduction),
    }
    return render(request, 'results.html', context)










#view for the list of employees
class EmployeeListView(LoginRequiredMixin, generic.ListView):
    #Keeps people from accessing this page with the url
    #redirects to login page if they try
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Employee
    #this forces pagination, 10 employees per page
    paginate_by = 10
    def get_queryset(self):

        #filter employees that belong to same company as user
        groups = self.request.user.groups.all()

        if groups:
            #get the company name
            co_name = groups.last()
            #get the company object in a queryset
            company_set = Company.objects.filter(company_name__icontains =co_name)
            #only one object in queryset
            co = company_set[0]
            #get the primary key
            co_id = co.pk
            #return employees that belong to this company
            return Employee.objects.filter(company=co_id)
        else:
            return Employee.objects.all()


#employee details
class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Employee


