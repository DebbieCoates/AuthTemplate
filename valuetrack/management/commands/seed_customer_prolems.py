from django.core.management.base import BaseCommand
from valuetrack.models import Customer, Problem
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed Customer and Problem data for stock control, training, and PPE issues'

    def handle(self, *args, **kwargs):
        customers = [
            {
                'name': 'Alpha Manufacturing Ltd',
                'main_contact': 'Jane Holloway',
                'industry': 'Manufacturing',
                'location': 'East Midlands',
                'hayley_account_manager': 'Debbie',
            },
            {
                'name': 'Beacon Construction Group',
                'main_contact': 'Tom Reilly',
                'industry': 'Construction',
                'location': 'North West',
                'hayley_account_manager': 'Debbie',
            },
            {
                'name': 'CareWell Healthcare',
                'main_contact': 'Dr. Priya Singh',
                'industry': 'Healthcare',
                'location': 'South East',
                'hayley_account_manager': 'Debbie',
            },
        ]

        problems = [
            {
                'title': 'Inconsistent Stock Control Procedures',
                'description': 'Frequent discrepancies between physical inventory and system records.',
                'root_cause': 'Lack of standardized stock reconciliation process.',
                'impact': 'Delays in order fulfillment and increased operational costs.',
                'urgency': 'High',
                'status': 'Open',
                'customer_name': 'Alpha Manufacturing Ltd',
            },
            {
                'title': 'Insufficient Staff Training on Equipment',
                'description': 'New hires are struggling to operate machinery safely and efficiently.',
                'root_cause': 'No formal onboarding or training program in place.',
                'impact': 'Increased risk of accidents and reduced productivity.',
                'urgency': 'Critical',
                'status': 'In Progress',
                'customer_name': 'Beacon Construction Group',
            },
            {
                'title': 'PPE Compliance Issues in Clinical Settings',
                'description': 'Staff frequently fail to wear appropriate PPE during patient interactions.',
                'root_cause': 'Lack of awareness and inconsistent enforcement of PPE policies.',
                'impact': 'Elevated risk of infection and regulatory non-compliance.',
                'urgency': 'Critical',
                'status': 'Open',
                'customer_name': 'CareWell Healthcare',
            },
        ]

        for data in customers:
            customer, _ = Customer.objects.get_or_create(
                name=data['name'],
                defaults={
                    'main_contact': data['main_contact'],
                    'industry': data['industry'],
                    'location': data['location'],
                    'hayley_account_manager': data['hayley_account_manager'],
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
            )

        for issue in problems:
            customer = Customer.objects.get(name=issue['customer_name'])
            Problem.objects.create(
                customer=customer,
                title=issue['title'],
                description=issue['description'],
                root_cause=issue['root_cause'],
                impact=issue['impact'],
                urgency=issue['urgency'],
                status=issue['status'],
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS('Seeded customers and problems successfully.'))