from django.db import models
from django.contrib.auth.models import User


location_CHOICES = [
        ('East of England', 'East of England'), 
        ('East Midlands', 'East Midlands'), 
        ('London', 'London'), 
        ('North East', 'North East'), 
        ('North West', 'North West'),
        ('South East', 'South East'),
        ('South West', 'South West'),  
        ('West Midlands', 'West Midlands'),
        ('Yorkshire and the Humber', 'Yorkshire and the Humber'),
        ('Scotland', 'Scotland'),
        ('Wales', 'Wales'),
        ('Northern Ireland', 'Northern Ireland'),
        ('Other', 'Other')
    ]

Industry_CHOICES = [
        ('Technology', 'Technology'), 
        ('Finance', 'Finance'), 
        ('Healthcare', 'Healthcare'), 
        ('Education', 'Education'), 
        ('Retail', 'Retail'),
        ('Engineering', 'Engineering'),
        ('Automotive', 'Automotive'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Media & Entertainment', 'Media & Entertainment'),
        ('Construction', 'Construction'),
        ('Manufacturing', 'Manufacturing'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Telecommunications', 'Telecommunications'),
        ('Education', 'Education'),
        ('Hospitality', 'Hospitality'),
        ('Real Estate', 'Real Estate'),
        ('Transportation & Logistics', 'Transportation & Logistics'),
        ('Energy & Utilities', 'Energy & Utilities'),
        ('Non-Profit', 'Non-Profit'),
        ('Other', 'Other')
    ]

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    main_contact = models.CharField(max_length=100)
    # Address fields
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='United Kingdom')
    # Contact details
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    # Industry and location
    industry = models.CharField(max_length=100, choices=Industry_CHOICES, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    # Location
    location = models.CharField(max_length=100, choices=location_CHOICES, blank=True, null=True)
    # Account Manager
    hayley_account_manager = models.CharField(max_length=100, blank=True, null=True)  
    # Additional notes 
    notes = models.TextField(blank=True, null=True) 
    archived = models.BooleanField(default=False)
    # ✅ Audit Trail   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='services')
    def __str__(self):
        return self.name


