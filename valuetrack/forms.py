from django import forms
from .models import Customer, Problem, Category, Service, Solution
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category']

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['name', 'description', 'service']
        
        
class UpdateProblem(forms.ModelForm):
    customer = forms.ModelChoiceField(label='Customer',queryset=Customer.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),required=True)
    title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'placeholder': 'Problem Title', 'class': 'form-control'}),max_length=200,required=True)
    description = forms.CharField(label='Description',widget=forms.Textarea(attrs={'placeholder': 'Describe the problem', 'class': 'form-control', 'rows': 3}),required=True    )
    root_cause = forms.CharField(label='Root Cause',widget=forms.Textarea(attrs={'placeholder': 'What caused the issue?', 'class': 'form-control', 'rows': 2}),required=False    )
    impact = forms.CharField(label='Impact',widget=forms.Textarea(attrs={'placeholder': 'What was affected?', 'class': 'form-control', 'rows': 2}),required=False)
    urgency = forms.ChoiceField(label='Urgency',choices=Problem.Urgency_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}),required=False)
    status = forms.ChoiceField(label='Status',choices=Problem.status_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}),required=False)
    notes = forms.CharField(label='Notes',widget=forms.Textarea(attrs={'placeholder': 'Additional notes', 'class': 'form-control', 'rows': 2}),required=False)

    class Meta:
        model = Problem
        fields = ['customer','title','description','root_cause','impact','urgency','status','notes']

# Form to Update Customer Details
class UpdateCustomer(forms.ModelForm):
    
	name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Customer Name', 'class': 'form-control'}), max_length=200, required=False)
	main_contact = forms.CharField(label='Main Contact', widget=forms.TextInput(attrs={'placeholder': 'Main Contact Name', 'class': 'form-control'}), max_length=200, required=False)
	address1 = forms.CharField(label='Address Line 1', widget=forms.TextInput(attrs={'placeholder': 'Address Line 1', 'class': 'form-control'}), max_length=200, required=False)
	address2 = forms.CharField(label='Address Line 2', widget=forms.TextInput(attrs={'placeholder': 'Address Line 2', 'class': 'form-control'}), max_length=200, required=False)
	city = forms.CharField(label='City', widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), max_length=100, required=False)
	postcode = forms.CharField(label='Postcode', widget=forms.TextInput(attrs={'placeholder': 'Postcode', 'class': 'form-control'}), max_length=20, required=False)
	county = forms.CharField(label='County', widget=forms.TextInput(attrs={'placeholder': 'County', 'class': 'form-control'}), max_length=100, required=False)
	country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}), max_length=100, required=False, initial='United Kingdom')
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}), max_length=254, required=False)
	phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}), max_length=20, required=False)
	website = forms.URLField(label='Website', widget=forms.URLInput(attrs={'placeholder': 'Website URL', 'class': 'form-control'}), max_length=200, required=False)
	industry = forms.ChoiceField(label='Industry', choices=[('', 'Select Industry'), ('Tech', 'Technology'), ('Finance', 'Finance'), ('Health', 'Healthcare'), ('Edu', 'Education'), ('Retail', 'Retail'), ('Eng', 'Engineering'), ('Auto', 'Automotive'), ('Food', 'Food & Beverage'), ('Media', 'Media & Entertainment'), ('Con', 'Construction'), ('Manu', 'Manufacturing'), ('Other', 'Other')], widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	sector = forms.CharField(label='Sector', widget=forms.TextInput(attrs={'placeholder': 'Sector', 'class': 'form-control'}), max_length=100, required=False)
	location = forms.ChoiceField(label='Location', choices=[('', 'Select Location'), ('East of England', 'East of England'), ('East Midlands', 'East Midlands'), ('London', 'London'), ('North East', 'North East'), ('North West', 'North West'), ('South East', 'South East'), ('South West', 'South West'), ('West Midlands', 'West Midlands'), ('Yorkshire and the Humber', 'Yorkshire and the Humber'), ('Scotland', 'Scotland'), ('Wales', 'Wales'), ('Northern Ireland', 'Northern Ireland'), ('Other', 'Other')], widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	hayley_account_manager = forms.CharField(label='Account Manager', widget=forms.TextInput(attrs={'placeholder': 'Account Manager Name', 'class': 'form-control'}), max_length=100, required=False)
	notes = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'placeholder': 'Additional Notes', 'class': 'form-control', 'rows': 4}), required=False)	
	archived = forms.BooleanField(label='Archived', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))	

	class Meta:
		model = Customer
		fields = ['name', 'main_contact', 'address1', 'address2', 'city', 'postcode', 'county', 'country', 'email', 'phone', 'website', 'industry', 'sector', 'location', 'hayley_account_manager', 'notes', 'archived']	
  
  
# Update User Details
class UpdateUserForm(UserChangeForm):
	# Hide Password Stuff
	password = None
	# Get the other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
    
# Update User Password
class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

# Register New User
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=False)
	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
  
