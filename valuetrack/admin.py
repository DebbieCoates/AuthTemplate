from django.contrib import admin
from .models import Customer, Category, Service, Solution, Problem

# Register Customer
admin.site.register(Customer)
admin.site.register(Problem)
# Inline Services under Category
class ServiceInline(admin.TabularInline):  # Use StackedInline for more detail
    model = Service
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ServiceInline]

admin.site.register(Category, CategoryAdmin)

# Inline Solutions under Service
class SolutionInline(admin.TabularInline):  # Use StackedInline for more detail
    model = Solution
    extra = 1
    show_change_link = True

class ServiceAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']

admin.site.register(Service, ServiceAdmin)

# Register Solution separately (optional)
admin.site.register(Solution)