from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.views import generic
from .models import Employee, Company, Dependent
from django.shortcuts import get_object_or_404
from .forms import CalcForm, EmployeeForm, DependentForm, SearchForm, EmployeeMod
from django.forms.models import modelformset_factory
from django.http import HttpRequest
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect
#TODO combine imports

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
        #get user company to populate employee company
        groups = request.user.groups.all()
        company = groups.last()
        company_obj = Company.objects.get(company_name=company)
        company_id = company_obj.pk
        #get form input
        employee_form = EmployeeForm(request.POST)
        #validate form input
        if employee_form.is_valid():
            temp = employee_form.save(commit=False)
            temp.company_id = company_id
            temp.save()
            emp_id = temp.pk
            request.session['last_accessed'] = emp_id;
            #specify employee string so we can reuse added.html
            type_added = 'Employee'
            context = {
                'type_added': type_added,
            }
            return render(request, 'added.html', context=context)
        #If user attempts to add duplicate first and last name
        else:
            error_msg = "Error: employee is already in the database"
            context = {
                'error_msg': error_msg,
            }
            return render(request, 'error.html', context)
    #create blank form
    else:
        employee_form = EmployeeForm()
        return render(request, 'add_new.html', {'employee_form': employee_form})


#Allows the user to search for a specific employee
def employee_search(request):
    #Get first and last name
    full_name = request.POST.get('full_name').split()
    employee_set = None
    failed  = False
    #If two or more strings were entered
    if len(full_name) > 1:
        f_name = full_name[0]
        l_name = full_name[1]
        #Checks the first two keywords against first and
        #last names in the database ignores any subsequent keywords
        employee_set = Employee.objects.filter(Q(first_name__icontains = f_name) | Q(last_name__icontains = l_name)
        |Q(first_name__icontains = l_name) | Q(last_name__icontains = f_name))
    #If only first or last name was entered, we will list any matches to either
    elif len(full_name) >0:
        f_name = full_name[0]
        employee_set = Employee.objects.filter( Q(first_name__icontains = f_name) | Q(last_name__icontains = f_name))
    #If filter failed
    if employee_set is None or len(employee_set) ==0:
            failed = True
    context = {
            'failed': failed,
            'employee_set': employee_set,
        }
    return render(request, 'search_results.html', context)


#Let user know adding employee was successful
def added(request):
    return render(request, 'added.html')


#Allows the user to add depdndents after adding an employee
#I orginally had some JavaScript and formsets in this function
#that I thought was really cool, but my wife didn't like it and
#I decided she was right because users would get frustrated with
#long formsets, particularly when they make mistakes with entries
def add_dependents(request):
    if request.method == 'POST':
        emp_id = request.session['last_accessed']
        dependent_form = DependentForm(request.POST)
        if dependent_form.is_valid():
            temp = dependent_form.save(commit=False)
            temp.employee_id = emp_id
            temp.save()

            type_added = 'Dependent'
            context = {
                'type_added': type_added
            }
            return render(request, 'added.html', context=context)
        #TODO else display error message
    else:
        dependent_form = DependentForm()
        return render(request, 'dependents.html', {'dependent_form': dependent_form})


def delete_dependent(request):
    if request.method == 'POST':
        dependent = request.POST.get('delete', "")
        Dependent.objects.filter(pk=dependent).delete()
        #Build redirect string
        emp_id = str(request.session['last_accessed'])
        direct = 'employee/'+emp_id

        return redirect(direct)
    else:
        error_msg = "Error: delete failed, it's your fault"
        return render(request, 'error.html', {'error_msg': error_msg})


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
    #basic calculation TODO try catch this stuff
    deduction = base_deduct+(dep_deduct*dep)
    deduction -= ((discount/100)*deduction)
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
            #get the company name, this will be the last (2nd)
            #element in the queryset because every user is a
            #member of 'employer' and their own company groups
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
class EmployeeDetailView(FormMixin, LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Employee
    form_class = EmployeeMod

    def get_success_url(self):
        return reverse('employee-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        self.request.session['last_accessed'] =self.kwargs['pk']



        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        context['form'] = EmployeeMod(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        temp = form.save(commit=False)
        temp.company_id = self.object.company_id
        temp.pk = self.object.pk
        temp.first_name = self.object.first_name
        temp.save()
        return super(EmployeeDetailView, self).form_valid(form)
