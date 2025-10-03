from django.core.management.base import BaseCommand
from valuetrack.models import Customer, Problem, Category, Service, Solution, Provider, SolutionProvider
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seed test data for development"

    def handle(self, *args, **kwargs):
        admin_user = User.objects.first()
        if not admin_user:
            admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass')

        nova = Customer.objects.create(
            name="Nova Systems",
            main_contact="Clara Reynolds",
            email="clara@novasystems.co.uk",
            phone="020 7946 1234",
            industry="Engineering",
            location="South East"
        )

        orbit = Customer.objects.create(
            name="Orbit Analytics",
            main_contact="Raj Patel",
            email="raj@orbitanalytics.com",
            phone="0161 555 9876",
            industry="Finance",
            location="North West"
        )

        data_cat = Category.objects.create(name="Data Infrastructure", description="Systems for storing and processing data")
        iot_cat = Category.objects.create(name="IoT Solutions", description="Connected device services")

        data_service = Service.objects.create(name="Warehouse Optimization", category=data_cat)
        iot_service = Service.objects.create(name="Sensor Network Management", category=iot_cat)

        solution1 = Solution.objects.create(name="Redshift Tuning", service=data_service)
        solution2 = Solution.objects.create(name="Edge Device Sync", service=iot_service)

        provider1 = Provider.objects.create(
            name="DataForge Ltd",
            type="External",
            contact_name="Emily Chen",
            email="emily@dataforge.io",
            phone="07800 123456",
            address="123 Tech Street",
            city="Leeds",
            county="West Yorkshire",
            postcode="LS1 4AB",
            country="United Kingdom",
            created_by=admin_user
        )

        provider2 = Provider.objects.create(
            name="IoTrix",
            type="Partner",
            contact_name="Tomas Alvarez",
            email="tomas@iotrix.com",
            phone="07900 654321",
            address="456 Innovation Way",
            city="Cambridge",
            county="Cambridgeshire",
            postcode="CB2 3PQ",
            country="United Kingdom",
            created_by=admin_user
        )

        SolutionProvider.objects.create(solution=solution1, provider=provider1, notes="Performance tuning specialist")
        SolutionProvider.objects.create(solution=solution2, provider=provider2, notes="Edge sync protocol developer")

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
