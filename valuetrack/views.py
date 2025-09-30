from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer 
from django.contrib import messages
from .forms import  SignUpForm,  UpdateUserForm, ChangePasswordForm, UpdateCustomer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

################################################# Customers
# View Customers
@login_required
def Customers(request):
    customers = Customer.objects.all()
    customer_count = customers.count()
    return render(request, 'customers.html', {
        'customers': customers,
        'customer_count': customer_count
    })



# View Single Customer
@login_required
def customer(request, pk):
	customer = get_object_or_404(Customer, pk=pk)
	return render(request, 'customer.html', {'customer': customer})

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
    return render(request, 'customer_add.html', {'form': form})

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
    return render(request, 'customer_edit.html', {'customer': customer, 'form': form})
    

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
