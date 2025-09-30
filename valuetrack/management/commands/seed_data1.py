from django.core.management.base import BaseCommand
from valuetrack.models import Category, Service
import os
import openpyxl

class Command(BaseCommand):
    help = 'Seed Category and Service data from Excel file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\debbi\OneDrive\Documents\Category Service .xlsx'


        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        created_categories = {}
        count_services = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            category_name, service_name = row[:2]



            if not category_name or not service_name:
                continue

            category, created = Category.objects.get_or_create(name=category_name.strip())
            if created:
                created_categories[category_name] = category

            Service.objects.create(
                name=service_name.strip(),
                category=category
            )
            count_services += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {len(created_categories)} categories and {count_services} services.'
        ))