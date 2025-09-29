from django.contrib import admin
from .models import Customer
from django.contrib.auth.models import User
from django.db import models


# Register your models here.
admin.site.register(Customer)
