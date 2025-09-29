from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from valuetrack.models import Customer
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with fake customer data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = User.objects.first()

        location_choices = [choice[0] for choice in Customer._meta.get_field('location').choices]
        industry_choices = [choice[0] for choice in Customer._meta.get_field('industry').choices]

        for _ in range(20):
            customer = Customer.objects.create(
                name=fake.company(),
                main_contact=fake.name(),
                address1=fake.street_address(),
                address2=fake.secondary_address(),
                city=fake.city(),
                postcode=fake.postcode(),
                county=fake.state(),
                country="United Kingdom",
                email=fake.company_email(),
                phone=fake.phone_number(),
                website=fake.url(),
                industry=random.choice(industry_choices),
                sector=fake.bs().title(),
                location=random.choice(location_choices),
                hayley_account_manager=fake.name(),
                notes=fake.paragraph(nb_sentences=3),
                archived=False,

            )
            self.stdout.write(self.style.SUCCESS(f"Created: {customer.name}"))
