from django.contrib import admin
from .models import Customer, Category, Service, Solution, Problem

# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_contact', 'email', 'phone']
    search_fields = ['name', 'main_contact', 'email', 'phone']

admin.site.register(Customer, CustomerAdmin)

# Problem Admin
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'status', 'urgency']
    search_fields = ['title', 'description', 'customer__name']

admin.site.register(Problem, ProblemAdmin)

# Inline Services under Category
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ServiceInline]
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

# Inline Solutions under Service
class SolutionInline(admin.TabularInline):
    model = Solution
    extra = 1
    show_change_link = True

class ServiceAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']

admin.site.register(Service, ServiceAdmin)

# Solution Admin
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'service']
    search_fields = ['name', 'service__name']

admin.site.register(Solution, SolutionAdmin)