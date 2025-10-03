from django.core.management.base import BaseCommand
from valuetrack.models import Customer, Category, Service, Solution, Problem, Provider, SolutionProvider
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seed test data for second customer and problem scenario"

    def handle(self, *args, **kwargs):
        # Get or create admin user
        admin_user = User.objects.first()
        if not admin_user:
            admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass')

        # Categories and Services
        infra = Category.objects.create(name="Infrastructure", description="Systems and hardware")
        logistics = Category.objects.create(name="Logistics", description="Fleet and supply chain")

        monitoring = Service.objects.create(name="Network Monitoring", category=infra)
        route_planning = Service.objects.create(name="Route Optimization", category=logistics)

        # Providers
        netwatch = Provider.objects.create(
            name="NetWatch Systems",
            type="Internal",
            contact_name="Priya Desai",
            email="priya@netwatch.local",
            phone="07700 555666",
            address="Tech Campus",
            city="Leeds",
            county="West Yorkshire",
            postcode="LS2 7AB",
            country="United Kingdom",
            created_by=admin_user
        )

        fleetgenix = Provider.objects.create(
            name="FleetGenix Ltd",
            type="External",
            contact_name="Ben Carter",
            email="ben@fleetgenix.co.uk",
            phone="07700 777888",
            address="12 Fleet Street",
            city="Manchester",
            county="Greater Manchester",
            postcode="M1 4AB",
            country="United Kingdom",
            created_by=admin_user
        )

        # New Customer
        translogix = Customer.objects.create(
            name="TransLogix",
            main_contact="Mark Taylor",
            email="mark@translogix.co.uk",
            phone="0161 7654321",
            industry="Transportation & Logistics",
            location="North West"
        )

        # New Problem
        problem = Problem.objects.create(
            customer=translogix,
            title="Fleet tracking interruptions",
            description="Real-time vehicle tracking system goes offline intermittently",
            root_cause="Unstable network and outdated routing logic",
            impact="Delayed deliveries and poor customer visibility",
            urgency="Critical",
            status="Open",
            notes="Needs resolution before winter peak season"
        )

        # Solutions
        solution1 = Solution.objects.create(
            name="Upgrade Network Monitoring",
            description="Deploy advanced monitoring tools to detect outages",
            service=monitoring,
            problem=problem
        )

        solution2 = Solution.objects.create(
            name="Implement Route Optimization Engine",
            description="AI-based routing to reduce delivery delays",
            service=route_planning,
            problem=problem
        )

        # Assign providers via SolutionProvider
        SolutionProvider.objects.create(
            solution=solution1,
            provider=netwatch,
            notes="Installed real-time alerting and diagnostics"
        )

        SolutionProvider.objects.create(
            solution=solution2,
            provider=fleetgenix,
            notes="Integrated with GPS and delivery scheduling system"
        )

        self.stdout.write(self.style.SUCCESS("✅ New customer and problem seeded successfully."))