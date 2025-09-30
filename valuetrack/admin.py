from django.contrib import admin
from .models import Customer, Category, Service
from django.contrib.auth.models import User
from django.db import models


# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Service)