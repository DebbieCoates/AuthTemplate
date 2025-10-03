from django.core.management.base import BaseCommand
from valuetrack.models import Customer, Problem, Category, Service, Solution, Provider, SolutionProvider
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seed complete test data with customer, problem, solutions, and providers"

    def handle(self, *args, **kwargs):
        # Get or create admin user
        admin_user = User.objects.first()
        if not admin_user:
            admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass')

        # Categories
        ops = Category.objects.create(name="Operations", description="Workflow and logistics")
        support = Category.objects.create(name="Customer Support", description="Fulfilment and helpdesk")

        # Services
        vending = Service.objects.create(name="Automated Vending", category=ops)
        call_centre = Service.objects.create(name="24-Hour Call Centre", category=support)

        # Providers
        abc_vending = Provider.objects.create(
            name="ABC Vending Limited",
            type="External",
            contact_name="Sarah Green",
            email="sarah@abcvending.co.uk",
            phone="07700 111222",
            address="1 Vending Way",
            city="Sheffield",
            county="South Yorkshire",
            postcode="S1 2AB",
            country="United Kingdom",
            created_by=admin_user
        )

        doncaster_support = Provider.objects.create(
            name="Doncaster Support Hub",
            type="Partner",
            contact_name="James White",
            email="james@supporthub.org",
            phone="07700 333444",
            address="99 Help Street",
            city="Doncaster",
            county="South Yorkshire",
            postcode="DN1 3XY",
            country="United Kingdom",
            created_by=admin_user
        )

        # Customer
        retailco = Customer.objects.create(
            name="RetailCo Ltd",
            main_contact="Tom Spencer",
            email="tom@retailco.com",
            phone="0113 1234567",
            industry="Retail",
            location="Yorkshire and the Humber"
        )

        # Problem
        problem = Problem.objects.create(
            customer=retailco,
            title="Stock control inefficiencies",
            description="Staff unable to access supplies when needed",
            root_cause="Manual stock tracking and limited access",
            impact="Delays in operations and staff frustration",
            urgency="High",
            status="In Progress",
            notes="Needs urgent resolution before Q4 rollout"
        )

        # Solutions
        solution1 = Solution.objects.create(
            name="Vending Machine Install",
            description="Automated dispensing units installed across key locations",
            service=vending,
            problem=problem
        )

        solution2 = Solution.objects.create(
            name="24-Hour Call Centre Setup",
            description="Support hub to manage after-hours supply requests",
            service=call_centre,
            problem=problem
        )

        # Link providers to solutions
        SolutionProvider.objects.create(
            solution=solution1,
            provider=abc_vending,
            notes="Installed and configured vending units"
        )

        SolutionProvider.objects.create(
            solution=solution2,
            provider=doncaster_support,
            notes="Handles all off-hours support calls"
        )

        self.stdout.write(self.style.SUCCESS("✅ Seed data created successfully."))