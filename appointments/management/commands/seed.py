from django.core.management.base import BaseCommand
from appointments.models import Barber, Service
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Seed the database with sample barbers, services, and an admin user."

    def handle(self, *args, **options):
        Barber.objects.get_or_create(name="John Okafor", specialty="Fades & Tapers", phone="08012345678")
        Barber.objects.get_or_create(name="Michael Eze", specialty="Beard Grooming", phone="08023456789")
        Barber.objects.get_or_create(name="David Nwosu", specialty="Classic Cuts", phone="08034567890")

        Service.objects.get_or_create(name="Haircut", defaults={"description": "Standard haircut", "price": 2500, "duration": 30})
        Service.objects.get_or_create(name="Beard Trim", defaults={"description": "Beard shaping and trim", "price": 1500, "duration": 20})
        Service.objects.get_or_create(name="Haircut + Beard", defaults={"description": "Full grooming package", "price": 3500, "duration": 45})

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@barberbook.com", "adminpass123")
            self.stdout.write(self.style.SUCCESS("Created admin user (username: admin, password: adminpass123)"))

        self.stdout.write(self.style.SUCCESS("Seed data created."))
