from django.core.management.base import BaseCommand
from valuetrack.models import Category, Service, Solution
import openpyxl
import os

class Command(BaseCommand):
    help = 'Seed Category, Service, and Solution data from Excel file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\debbi\OneDrive\Documents\Category Service Solution.xlsx'  # Update if needed

        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error opening file: {e}'))
            return

        created_categories = {}
        created_services = {}
        count_solutions = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            category_name, service_name, solution_name = row[:3]

            if not category_name or not service_name or not solution_name:
                continue

            # Create or get Category
            category, _ = Category.objects.get_or_create(name=category_name.strip())

            # Create or get Service linked to Category
            service, _ = Service.objects.get_or_create(
                name=service_name.strip(),
                category=category
            )

            # Create Solution linked to Service
            Solution.objects.create(
                name=solution_name.strip(),
                service=service
            )
            count_solutions += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded data: {Category.objects.count()} categories, {Service.objects.count()} services, {count_solutions} solutions.'
        ))