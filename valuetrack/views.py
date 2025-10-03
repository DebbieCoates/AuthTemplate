from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Problem, Service, Solution, Category
from django.contrib import messages
from .forms import  CategoryForm, SignUpForm,  UpdateUserForm, ChangePasswordForm, UpdateCustomer, UpdateProblem, CategoryForm, ServiceForm, SolutionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Customer
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, 'home.html')

################################################# Category Hierarchy


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_hierarchy')  # or use JsonResponse for AJAX
    else:
        form = CategoryForm()
    return render(request, 'partials/add_category_form.html', {'form': form})

# Repeat for add_service and add_solution
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_hierarchy')  # or use JsonResponse for AJAX
    else:
        form = ServiceForm()
    return render(request, 'partials/add_service_form.html', {'form': form})


def add_solution(request):
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_hierarchy')  # or use JsonResponse for AJAX
    else:
        form = SolutionForm()
    return render(request, 'partials/add_solution_form.html', {'form': form})

@login_required
def category_hierarchy(request):
    selected_category = request.GET.get('category')
    selected_service = request.GET.get('service')
    selected_solution = request.GET.get('solution')

    categories = Category.objects.prefetch_related('services__solutions')

    # Optional: filter logic
    if selected_category:
        categories = categories.filter(name=selected_category)

    return render(request, 'category_hierarchy.html', {
        'categories': categories,
        'selected_category': selected_category,
        'selected_service': selected_service,
        'selected_solution': selected_solution,
    })

################################################# Problems

# View All Problems
@login_required
def problems(request):
    problems = Problem.objects.all()
    add_form = UpdateProblem()

    wrapped_problems = []
    for problem in problems:
        wrapped_problems.append({
            'problem': problem,
            'form': UpdateProblem(instance=problem)
        })

    return render(request, 'problems.html', {
        'problems': wrapped_problems,
        'form': add_form
    })

# View Single Problem
@login_required
def problem(request, pk):
    problem = Problem.objects.all()
    customer = Customer.objects.all()
    problem = get_object_or_404(problem, pk=pk)
    return render(request, 'problem.html', {'problem': problem, 'customer': customer})

# Add Problem
@login_required
def problem_add(request):
    if request.method == 'POST':
        form = UpdateProblem(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New problem added successfully.')

            called_from = request.POST.get('called_from')
            customer_id = request.POST.get('customer_id')

            if called_from == 'customer' and customer_id:
                return redirect('customer', pk=customer_id)
            return redirect('problems')
    else:
        customer_id = request.GET.get('customer_id')
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            form = UpdateProblem(initial={'customer': customer})
        else:
            form = UpdateProblem()

    return render(request, 'problems.html', {'form': form})

# Edit Problem
@login_required
def problem_edit(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if request.method == 'POST':
        form = UpdateProblem(request.POST, instance=problem)
        called_from = request.POST.get('called_from', '').strip()

        if form.is_valid():
            form.save()
            messages.success(request, 'Problem updated successfully.')

            if called_from == 'customer':
                return redirect('customer', pk=problem.customer.pk)
            else:
                return redirect('problems')
    else:
        form = UpdateProblem(instance=problem)

    return render(request, 'problems.html', {
        'form': form,
        'problem': problem,
        'edit_mode': True
    })

# Delete Problem
@login_required
def problem_delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    problem.delete()
    messages.success(request, 'Problem deleted successfully.')

    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    return redirect('problems')  # fallback

################################################# Customers

class CustomerFormWrapper:
    def __init__(self, customer, form):
        self.customer = customer
        self.form = form

# View All Customers
@login_required
def customers(request):
    customers = Customer.objects.all()
    customer_count = customers.count()
    add_form = UpdateCustomer()

    wrapped_customers = [
        CustomerFormWrapper(c, UpdateCustomer(instance=c)) for c in customers
    ]

    context = {
        'customers': wrapped_customers,  # now contains both customer and form
        'customer_count': customer_count,
        'form': add_form,  # for Add modal
    }
    return render(request, 'customers.html', context)

# View Single Customer
@login_required
def customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    problems = customer.problem_statements.all()

    wrapped_problems = []
    for problem in problems:
        form = UpdateProblem(instance=problem)
        wrapped_problems.append({'problem': problem, 'form': form})

    return render(request, 'customer.html', {
        'customer': customer,
        'problems': wrapped_problems,
        'form': UpdateProblem(initial={'customer': customer}),  # for Add Problem modal
    })
# Add Customer
@login_required
def customer_add(request):
    if request.method == 'POST':
        form = UpdateCustomer(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'New customer added successfully.')
            return redirect('customers')
    else:
        form = UpdateCustomer()
    return render(request, 'customers.html.html', {'form': form})

# Delete Customer
@login_required
def customer_delete(request, pk):
    # get the contact to be deleted
    customer = Customer.objects.get(id=pk)
    # delete the contact
    customer.delete()
    # display a success message
    messages.success(request, f'{customer.name} deleted successfully.')
    # redirect to the customer list page
    return redirect('customers')

# Edit Customer
@login_required
def customer_edit(request, pk):
    # Get the customer to be edited
    customer = Customer.objects.get(id=pk)
    # Pre-fill the form with the existing customer data
    form = UpdateCustomer(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomer(request.POST, request.FILES or None, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.name} updated successfully.')
            return redirect('customers')
    return render(request, 'customers.html', {'customer': customer, 'form': form})
    

################################################# Authoristion 

# Update User Info
def update_user(request):
	if request.user.is_authenticated:
		# Get current user
		current_user = User.objects.get(id=request.user.id)
		# Create our form
		user_form = UpdateUserForm(request.POST or None, instance=current_user)
	
		if user_form.is_valid():
			# Update and Save user info
			user_form.save()
			# Log user back in
			login(request, current_user)
			messages.success(request, "Your User Info Has Been Updated!")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form':user_form})
	else:
		messages.success(request, "Must Be Logged In To View That Page...")
		return redirect('login')

# Update User Password
def update_password(request):
	if request.user.is_authenticated:
		#get the current user
		current_user = request.user
		
		# Did they post? Or are they viewing the page
		if request.method == "POST":
			# Define our form
			form = ChangePasswordForm(current_user, request.POST)
			# is form valid
			if form.is_valid():
				#save the form info
				form.save()
				# re-login the user
				login(request,current_user)
				# Success message
				messages.success(request, "Your Password Has Been Updated!")
				return redirect('update_user')
			else:
				# loop thru error messages
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			# Define our form
			form = ChangePasswordForm(current_user)
			return render(request, 'update_password.html', {"form":form})

	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home') 

#login
def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('home')
            else:
                messages.error(request, "There was an error logging in. Please try again...")
                return redirect('login')    
        else:
            return render(request, 'login.html', {})

#logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

# Register
def register_user(request):
	# Grab the register form
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Log them in
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# Authenticate
			user = authenticate(username=username, password=password)
			# Log them in
			login(request, user)
			messages.success(request, "Login Succesful! Welcome!")
			return redirect('home')
		else:
			messages.success(request, "Whoops!  Looks Like There Was A Problem... Try Again!")
			return redirect('register')

	else:
		return render(request, 'register.html', {'form':form})
