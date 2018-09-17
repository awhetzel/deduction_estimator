from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views import generic
from .models import Employee, Company, Dependent
from .forms import CalcForm, EmployeeForm, DependentForm, SearchForm, EmployeeMod
from django.db.models import Q
from django.urls import reverse
from decimal import Decimal
import locale
from django.http import HttpResponseRedirect

#set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#Home page
def index(request):
    #Demo basic use of session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


#login function for employers
def login(request):
    return render(request, 'login.html')


#allow employers to add new employees
@login_required
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
            temp.first_name = temp.first_name.lower()
            temp.last_name = temp.last_name.lower()
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
            target = 'add_new'
            return error_page(request, error_msg, target)
    #create blank form
    else:
        employee_form = EmployeeForm()
        return render(request, 'add_new.html', {'employee_form': employee_form})


#Allow users to remove employees
def remove_employee(request):
    if request.method == 'POST':
        emp_id = request.POST.get('delete', "")
        Employee.objects.filter(pk=emp_id).delete()
        return HttpResponseRedirect(reverse('employees'))
    else:
        #This shouldn't happen, I had to try to be funny somewhere
        error_msg = "Error: delete failed, it's your fault"
        return render(request, 'error.html', {'error_msg': error_msg})


#Helper error message function used by multiple views
def error_page(request, error_msg, target):
    context = {
        'error_msg': error_msg,
        'target': target,
    }
    return render(request, 'error.html', context)


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
        #last names in the database ignores any subsequent input
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
@login_required
def added(request):
    return render(request, 'added.html')


#Allows the user to add depdndents after adding an employee
@login_required
def add_dependents(request):
    emp_id = request.session['last_accessed']
    employee = Employee.objects.get(pk=emp_id)

    if request.method == 'POST':
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
        #If form input is invlaid
        else:
            error_msg = "Error: Please enter date in the specified format."
            target = 'dependents'
            return error_page(request, error_msg, target)
    else:
        dependent_form = DependentForm()
        context = {
            'employee': employee,
            'dependent_form': dependent_form,
        }
        return render(request, 'dependents.html', context=context)


#Allows users to delete dependents
@login_required
def delete_dependent(request):
    if request.method == 'POST':
        dependent = request.POST.get('delete', "")
        Dependent.objects.filter(pk=dependent).delete()
        #Get the url
        emp_id = str(request.session['last_accessed'])
        employee = Employee.objects.get(pk=emp_id)
        url = employee.get_absolute_url()

        return redirect( url)
    else:
        #This shouldn't happen, I had to try to be funny somewhere
        error_msg = "Error: delete failed, it's your fault"
        return render(request, 'error.html', {'error_msg': error_msg})


#Deduction calculator form page
def calculate(request):
    calc_form = CalcForm()
    return render(request, 'calculate.html', {'calc_form': calc_form})


#Deduction calculator logic, redirects to results page
def results(request):
    try:
        #this employee's salary
        salary = float(request.POST.get('emp_salary'))
        #base deduction
        base_deduct= float(request.POST.get('base_deduction'))
        #number of dependents
        dep = float(request.POST.get('dependents'))
        #dependent deduction
        dep_deduct = float(request.POST.get('dependent_deduction'))
        #discount percentage
        discount = float(request.POST.get('discount'))/100
        #number of dependents eligible for discount
        num_eligible = float(request.POST.get('num_eligible'))
        #percentage of benefit cost that employer pays
        co_pays = float(request.POST.get('co_pays'))/100
        #True if employee is eligible for discount
        emp_eligible = request.POST.get('emp_eligible')
        #calculate deduction
        deduction =0
    except:
        error_msg = "Invalid input, see help page for more info."
        target = 'calculate'
        return error_page(request, error_msg, target)
    #Calculate deduction
    if emp_eligible == True:
        deduction = base_deduct - (discount*base_deduct)
    else:
        deduction = base_deduct
    if dep > 0 and num_eligible > 0:
        deduction += (dep - num_eligible) * dep_deduct + num_eligible * (dep_deduct - (discount * dep_deduct))
    else:
        deduction += dep*dep_deduct
    company_pays = co_pays*deduction
    deduction -= company_pays
    #salary after deduction
    after_deduction = float(salary)-deduction
    #formatted context values to display on results page
    context = {
        'salary': locale.currency( salary, grouping=True ),
        'dep': int(dep),
        'deduction': locale.currency(deduction, grouping=True ),
        'after_deduction': locale.currency(after_deduction, grouping=True ),
        'company_pays': locale.currency(company_pays, grouping=True ),
    }
    return render(request, 'results.html', context)


#Help page
def help(request):
    return render(request, 'help.html')


#List of employees for the company that the user represents
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

    #Get this employee's url
    def get_success_url(self):
        return reverse('employee-detail', kwargs={'pk': self.object.id})


    #Add a little to the context and session
    def get_context_data(self, **kwargs):
        #Keep track of current employee in session
        self.request.session['last_accessed'] =self.kwargs['pk']
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        #Calculate deduction
        deduction = self.get_deduction()
        #The company this employee works for
        company = self.get_company()
        #Total cost of benefit package
        total_cost = self.get_total_cost(company)
        #Employer cost
        employer_cost = self.get_company_cost(total_cost, company)
        #Set context variables
        context['company_name'] = company.company_name
        context['form'] = EmployeeMod(initial={'post': self.object})
        context['deduction'] = locale.currency(deduction, grouping=True)
        context['check_deduction'] = locale.currency((deduction/26), grouping=True)
        context['total_cost'] = locale.currency(total_cost, grouping=True)
        context['employer_cost'] = locale.currency(employer_cost, grouping=True)
        context['salary'] = locale.currency(self.object.salary, grouping=True)

        return context


    #Add form to detail view
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    #Add some data before saving
    def form_valid(self, form):
        temp = form.save(commit=False)
        temp.company_id = self.object.company_id
        temp.pk = self.object.pk
        temp.first_name = self.object.first_name
        temp.save()
        return super(EmployeeDetailView, self).form_valid(form)


    #Calculate the deduction
    def get_deduction(self):
        company = self.get_company()
        deduction = self.get_total_cost(company)
        #subtract the amount that the company pays
        company_pays = self.get_company_cost(deduction, company)
        deduction -= company_pays
        return deduction


    #Get the company this employee belongs to
    def get_company(self):
        return Company.objects.get(pk=self.object.company.pk)


    #Get the total cost after discounts
    def get_total_cost(self, company):
        discount_per = Decimal(0)
        cost = 0
        cost = company.emp_deduct
        #check for employee discount
        if company.discount_policy.lower() == self.object.first_name[0].lower():
            discount_per = company.dicount_percentage
        discount = ((discount_per/100)*cost)
        #Employee portion of the cost
        cost = cost - discount
        #cost for dependents
        for dependent in self.object.dependent_set.all():
            cost += dependent.get_deduction(company)
        return cost


    #Get the amount the company pays
    def get_company_cost(self, total_cost, company):
        return ((company.contribution_percent/100)*total_cost)
