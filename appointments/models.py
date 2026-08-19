from django.db import models
from django.contrib.auth.models import User


class Barber(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return f"{self.name} ({self.duration} min)"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        unique_together = ("barber", "date", "time")

    def __str__(self):
        return f"{self.customer.username} - {self.barber.name} - {self.date} {self.time}"
